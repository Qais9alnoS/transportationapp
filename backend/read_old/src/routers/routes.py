from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.schemas.route import RouteCreate, RouteRead, RouteUpdate
from src.schemas.stop import StopCreate, StopRead
from src.schemas.route_path import RoutePathCreate, RoutePathRead
from src.models import models
from config.database import SessionLocal
from geoalchemy2.shape import from_shape
from shapely.geometry import Point
from src.routers.auth import get_current_user
from src.services.cache_service import cache_get, cache_set
from src.services.cache_service import redis_client

router = APIRouter(prefix="/routes", tags=["Routes"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=RouteRead)
def create_route(route: RouteCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    # تحقق من عدم تكرار الاسم
    if db.query(models.Route).filter(models.Route.name == route.name).first():
        raise HTTPException(status_code=400, detail="Route name already exists")
    db_route = models.Route(
        name=route.name,
        description=route.description,
        price=route.price,
        operating_hours=route.operating_hours
    )
    db.add(db_route)
    db.commit()
    db.refresh(db_route)

    # إضافة المحطات
    stop_objs = []
    if route.stops:
        for stop in route.stops:
            stop_obj = models.Stop(
                name=stop.name,
                lat=stop.lat,
                lng=stop.lng,
                geom=from_shape(Point(stop.lng, stop.lat), srid=4326)
            )
            db.add(stop_obj)
            db.commit()
            db.refresh(stop_obj)
            # ربط المحطة بالخط عبر RouteStop
            route_stop = models.RouteStop(route_id=db_route.id, stop_id=stop_obj.id)
            db.add(route_stop)
            stop_objs.append(stop_obj)
        db.commit()

    # إضافة المسارات
    path_objs = []
    if route.paths:
        for path in route.paths:
            path_obj = models.RoutePath(
                route_id=db_route.id,
                lat=path.lat,
                lng=path.lng,
                point_order=path.point_order,
                geom=from_shape(Point(path.lng, path.lat), srid=4326)
            )
            db.add(path_obj)
            path_objs.append(path_obj)
        db.commit()

    # إعادة تحميل الخط مع العلاقات
    db.refresh(db_route)
    stops = db.query(models.Stop).join(models.RouteStop).filter(models.RouteStop.route_id == db_route.id).all()
    paths = db.query(models.RoutePath).filter(models.RoutePath.route_id == db_route.id).all()
    stops_data = [StopRead.model_validate(stop, from_attributes=True).model_dump() for stop in stops]
    paths_data = [RoutePathRead.model_validate(path, from_attributes=True).model_dump() for path in paths]
    route_data = RouteRead(
        id=db_route.id,
        name=db_route.name,
        description=db_route.description,
        price=db_route.price,
        operating_hours=db_route.operating_hours,
        stops=stops_data,
        paths=paths_data
    )
    cache_set(f"routes:{db_route.id}", route_data.model_dump(), ttl=300)
    redis_client.delete("routes:all")
    return route_data

@router.get("/", response_model=list[RouteRead])
def read_routes(db: Session = Depends(get_db)):
    cache_key = "routes:all"
    cached = cache_get(cache_key)
    if cached:
        return cached
    routes = db.query(models.Route).all()
    result = []
    for route in routes:
        stops = db.query(models.Stop).join(models.RouteStop).filter(models.RouteStop.route_id == route.id).all()
        paths = db.query(models.RoutePath).filter(models.RoutePath.route_id == route.id).all()
        stops_data = [StopRead.model_validate(stop, from_attributes=True).model_dump() for stop in stops]
        paths_data = [RoutePathRead.model_validate(path, from_attributes=True).model_dump() for path in paths]
        result.append(RouteRead(
            id=route.id,
            name=route.name,
            description=route.description,
            price=route.price,
            operating_hours=route.operating_hours,
            stops=stops_data,
            paths=paths_data
        ))
    cache_set(cache_key, [r.model_dump() for r in result], ttl=300)
    redis_client.delete("routes:all")
    return result

@router.get("/{route_id}", response_model=RouteRead)
def read_route(route_id: int, db: Session = Depends(get_db)):
    cache_key = f"routes:{route_id}"
    cached = cache_get(cache_key)
    if cached:
        return RouteRead(**cached)
    route = db.query(models.Route).filter(models.Route.id == route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    stops = db.query(models.Stop).join(models.RouteStop).filter(models.RouteStop.route_id == route.id).all()
    paths = db.query(models.RoutePath).filter(models.RoutePath.route_id == route.id).all()
    stops_data = [StopRead.model_validate(stop, from_attributes=True).model_dump() for stop in stops]
    paths_data = [RoutePathRead.model_validate(path, from_attributes=True).model_dump() for path in paths]
    route_data = RouteRead(
        id=route.id,
        name=route.name,
        description=route.description,
        price=route.price,
        operating_hours=route.operating_hours,
        stops=stops_data,
        paths=paths_data
    )
    cache_set(cache_key, route_data.model_dump(), ttl=300)
    redis_client.delete(f"routes:{route_id}")
    return route_data

@router.put("/{route_id}", response_model=RouteRead)
def update_route(route_id: int, route: RouteUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_route = db.query(models.Route).filter(models.Route.id == route_id).first()
    if not db_route:
        raise HTTPException(status_code=404, detail="Route not found")
    for var, value in vars(route).items():
        if value is not None:
            setattr(db_route, var, value)
    db.commit()
    db.refresh(db_route)
    stops = db.query(models.Stop).join(models.RouteStop).filter(models.RouteStop.route_id == db_route.id).all()
    paths = db.query(models.RoutePath).filter(models.RoutePath.route_id == db_route.id).all()
    stops_data = [StopRead.model_validate(stop, from_attributes=True).model_dump() for stop in stops]
    paths_data = [RoutePathRead.model_validate(path, from_attributes=True).model_dump() for path in paths]
    route_data = RouteRead(
        id=db_route.id,
        name=db_route.name,
        description=db_route.description,
        price=db_route.price,
        operating_hours=db_route.operating_hours,
        stops=stops_data,
        paths=paths_data
    )
    cache_set(f"routes:{db_route.id}", route_data.model_dump(), ttl=300)
    redis_client.delete("routes:all")
    return route_data

@router.delete("/{route_id}")
def delete_route(route_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_route = db.query(models.Route).filter(models.Route.id == route_id).first()
    if not db_route:
        raise HTTPException(status_code=404, detail="Route not found")
    # حذف العلاقات والمسارات والمحطات المرتبطة
    db.query(models.RouteStop).filter(models.RouteStop.route_id == db_route.id).delete()
    db.query(models.RoutePath).filter(models.RoutePath.route_id == db_route.id).delete()
    db.delete(db_route)
    db.commit()
    redis_client.delete(f"routes:{route_id}")
    redis_client.delete("routes:all")
    return {"ok": True} 