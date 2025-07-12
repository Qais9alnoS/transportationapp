from src.schemas.search import SearchRouteRequest, SearchRouteResponse, SuggestedRoute, RouteSegment
from src.models import models
from sqlalchemy.orm import Session
from config.database import SessionLocal
from shapely.geometry import Point
from geopy.distance import geodesic
from src.services.traffic import get_traffic_data
from src.services.cache_service import cache_get, cache_set
import hashlib
import json

# منطق بحث مبسط: يبحث عن أقرب خط مكرو يمر بالقرب من نقطة البداية والنهاية

def search_routes(request: SearchRouteRequest) -> SearchRouteResponse:
    # استخدم الكاش إذا كان الطلب مكرر
    cache_key = "route_search:" + hashlib.sha256(json.dumps(request.model_dump(), sort_keys=True).encode()).hexdigest()
    cached = cache_get(cache_key)
    if cached:
        return SearchRouteResponse(**cached)

    db: Session = SessionLocal()
    start = (request.start_lat, request.start_lng)
    end = (request.end_lat, request.end_lng)
    filter_type = request.filter_type or "fastest"

    # جلب جميع الخطوط
    routes = db.query(models.Route).all()
    suggestions = []
    for route in routes:
        # جلب محطات الخط
        stops = db.query(models.Stop).join(models.RouteStop).filter(models.RouteStop.route_id == route.id).all()
        if not stops:
            continue
        # إيجاد أقرب محطة للبداية وأقرب محطة للنهاية
        start_stop = min(stops, key=lambda s: geodesic((s.lat, s.lng), start).meters)
        end_stop = min(stops, key=lambda s: geodesic((s.lat, s.lng), end).meters)
        # حساب المسافة بين البداية وأقرب محطة، وبين النهاية وأقرب محطة
        walk_to_start = geodesic(start, (start_stop.lat, start_stop.lng)).meters
        walk_from_end = geodesic((end_stop.lat, end_stop.lng), end).meters
        # تقدير زمن المشي (سرعة 5 كم/س)
        walk_to_start_time = int(walk_to_start / (5000/3600))
        walk_from_end_time = int(walk_from_end / (5000/3600))
        # تقدير زمن الرحلة داخل المكرو (سرعة 20 كم/س)
        makro_distance = geodesic((start_stop.lat, start_stop.lng), (end_stop.lat, end_stop.lng)).meters
        makro_time = int(makro_distance / (20000/3600))
        # دمج زمن الازدحام إذا كان البحث عن أسرع طريق فقط
        traffic_extra = 0
        if filter_type == "fastest":
            traffic_extra = get_traffic_data(start_stop.lat, start_stop.lng, end_stop.lat, end_stop.lng)
        makro_time_with_traffic = makro_time + traffic_extra
        # بناء المسار المقترح
        segments = []
        if walk_to_start > 30:
            segments.append(RouteSegment(
                type="walk",
                distance_meters=walk_to_start,
                duration_seconds=walk_to_start_time,
                instructions=f"امشِ إلى أقرب موقف: {start_stop.name}",
                start_stop_id=None,
                end_stop_id=str(start_stop.id)
            ))
        segments.append(RouteSegment(
            type="makro",
            distance_meters=makro_distance,
            duration_seconds=makro_time_with_traffic,
            instructions=f"اركب المكرو من {start_stop.name} إلى {end_stop.name}",
            makro_id=str(route.id),
            start_stop_id=str(start_stop.id),
            end_stop_id=str(end_stop.id),
            estimated_cost=route.price
        ))
        if walk_from_end > 30:
            segments.append(RouteSegment(
                type="walk",
                distance_meters=walk_from_end,
                duration_seconds=walk_from_end_time,
                instructions=f"امشِ من موقف {end_stop.name} إلى وجهتك النهائية",
                start_stop_id=str(end_stop.id),
                end_stop_id=None
            ))
        total_time = walk_to_start_time + makro_time_with_traffic + walk_from_end_time
        total_cost = route.price
        suggestions.append(SuggestedRoute(
            route_id=str(route.id),
            description=route.name,
            segments=segments,
            total_estimated_time_seconds=total_time,
            total_estimated_cost=total_cost
        ))
    # التصفية
    if filter_type == "cheapest":
        suggestions.sort(key=lambda r: r.total_estimated_cost)
    elif filter_type == "least_transfers":
        suggestions.sort(key=lambda r: len([s for s in r.segments if s.type == "makro"]))
    else:  # fastest
        suggestions.sort(key=lambda r: r.total_estimated_time_seconds)
    # إعادة فقط أفضل 3 مسارات
    db.close()
    response = SearchRouteResponse(routes=suggestions[:3])
    cache_set(cache_key, response.model_dump(), ttl=120)
    return response 