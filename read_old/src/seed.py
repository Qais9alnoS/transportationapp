import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sqlalchemy.orm import Session
from config.database import SessionLocal
from src.models import models
from geoalchemy2.shape import from_shape
from shapely.geometry import Point

# بيانات تجريبية
routes_data = [
    {
        "name": "خط المزة - العباسيين",
        "description": "من المزة إلى ساحة العباسيين عبر وسط المدينة",
        "price": 500,
        "operating_hours": "06:00-23:00",
        "stops": [
            {"name": "موقف المزة", "lat": 33.500, "lng": 36.300},
            {"name": "موقف ساحة العباسيين", "lat": 33.501, "lng": 36.301},
            {"name": "موقف البرامكة", "lat": 33.502, "lng": 36.302}
        ],
        "paths": [
            {"lat": 33.500, "lng": 36.300, "point_order": 1},
            {"lat": 33.501, "lng": 36.301, "point_order": 2},
            {"lat": 33.502, "lng": 36.302, "point_order": 3}
        ]
    },
    {
        "name": "خط ركن الدين - باب توما",
        "description": "من ركن الدين إلى باب توما مروراً بساحة المرجة",
        "price": 400,
        "operating_hours": "05:30-22:30",
        "stops": [
            {"name": "موقف ركن الدين", "lat": 33.520, "lng": 36.280},
            {"name": "موقف ساحة المرجة", "lat": 33.510, "lng": 36.290},
            {"name": "موقف باب توما", "lat": 33.515, "lng": 36.305}
        ],
        "paths": [
            {"lat": 33.520, "lng": 36.280, "point_order": 1},
            {"lat": 33.510, "lng": 36.290, "point_order": 2},
            {"lat": 33.515, "lng": 36.305, "point_order": 3}
        ]
    }
]

def seed():
    db: Session = SessionLocal()
    for route_data in routes_data:
        route = models.Route(
            name=route_data["name"],
            description=route_data["description"],
            price=route_data["price"],
            operating_hours=route_data["operating_hours"]
        )
        db.add(route)
        db.commit()
        db.refresh(route)
        # إضافة المحطات
        stop_objs = []
        for stop in route_data["stops"]:
            stop_obj = models.Stop(
                name=stop["name"],
                lat=stop["lat"],
                lng=stop["lng"],
                geom=from_shape(Point(stop["lng"], stop["lat"]), srid=4326)
            )
            db.add(stop_obj)
            db.commit()
            db.refresh(stop_obj)
            route_stop = models.RouteStop(route_id=route.id, stop_id=stop_obj.id)
            db.add(route_stop)
            stop_objs.append(stop_obj)
        db.commit()
        # إضافة المسارات
        for path in route_data["paths"]:
            path_obj = models.RoutePath(
                route_id=route.id,
                lat=path["lat"],
                lng=path["lng"],
                point_order=path["point_order"],
                geom=from_shape(Point(path["lng"], path["lat"]), srid=4326)
            )
            db.add(path_obj)
        db.commit()
    db.close()
    print("تمت تعبئة قاعدة البيانات ببيانات تجريبية بنجاح.")

if __name__ == "__main__":
    seed() 