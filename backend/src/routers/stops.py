from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from src.schemas.stop import StopCreate, StopRead, StopUpdate
from src.models import models
from config.database import SessionLocal
from src.routers.auth import get_current_user
from src.services.cache_service import cache_get, cache_set, redis_client
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/stops", tags=["Stops"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=StopRead)
def create_stop(stop: StopCreate, db: Session = Depends(get_db)):
    # تحقق من عدم تكرار الاسم
    existing = db.query(models.Stop).filter(models.Stop.name == stop.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="اسم المحطة مستخدم مسبقًا")
    db_stop = models.Stop(**stop.dict())
    db.add(db_stop)
    try:
        db.commit()
        db.refresh(db_stop)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="خطأ في حفظ المحطة: تأكد من صحة البيانات المدخلة وعدم تكرار اسم المحطة")
    redis_client.delete("stops:all")
    redis_client.delete(f"stops:{db_stop.id}")
    return db_stop

@router.post("/bulk", response_model=List[StopRead])
def create_stops_bulk(stops: List[StopCreate], db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """إنشاء عدة محطات دفعة واحدة"""
    created_stops = []
    for stop_data in stops:
        if db.query(models.Stop).filter(models.Stop.name == stop_data.name).first():
            continue  # Skip if stop already exists
        db_stop = models.Stop(
            name=stop_data.name,
            lat=stop_data.lat,
            lng=stop_data.lng,
            geom=f'POINT({stop_data.lng} {stop_data.lat})'
        )
        db.add(db_stop)
        created_stops.append(db_stop)
    
    db.commit()
    for stop in created_stops:
        db.refresh(stop)
    
    redis_client.delete("stops:all")
    return created_stops

@router.get("/nearby", response_model=List[StopRead])
def get_nearby_stops(
    lat: float = Query(..., description="خط العرض"),
    lng: float = Query(..., description="خط الطول"),
    radius: float = Query(1.0, description="نصف القطر بالكيلومترات"),
    db: Session = Depends(get_db)
):
    """البحث عن المحطات القريبة من نقطة معينة"""
    # Simple distance calculation using Haversine formula
    # In a real application, you'd use PostGIS ST_DWithin for better performance
    stops = db.query(models.Stop).all()
    nearby_stops = []
    
    for stop in stops:
        # Calculate distance using Haversine formula
        import math
        R = 6371  # Earth's radius in kilometers
        
        lat1, lon1 = math.radians(lat), math.radians(lng)
        lat2, lon2 = math.radians(stop.lat), math.radians(stop.lng)
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        distance = R * c
        
        if distance <= radius:
            nearby_stops.append(stop)
    
    return nearby_stops

@router.get("/", response_model=list[StopRead])
def read_stops(db: Session = Depends(get_db)):
    cache_key = "stops:all"
    cached = cache_get(cache_key)
    if cached:
        return cached
    stops = db.query(models.Stop).all()
    stops_data = [StopRead.model_validate(stop, from_attributes=True).model_dump() for stop in stops]
    cache_set(cache_key, stops_data, ttl=300)
    return stops_data

@router.get("/{stop_id}", response_model=StopRead)
def read_stop(stop_id: int, db: Session = Depends(get_db)):
    cache_key = f"stops:{stop_id}"
    cached = cache_get(cache_key)
    if cached:
        return StopRead(**cached)
    stop = db.query(models.Stop).filter(models.Stop.id == stop_id).first()
    if not stop:
        raise HTTPException(status_code=404, detail="Stop not found")
    stop_data = StopRead.model_validate(stop, from_attributes=True).model_dump()
    cache_set(cache_key, stop_data, ttl=300)
    return StopRead(**stop_data)

@router.put("/{stop_id}", response_model=StopRead)
def update_stop(stop_id: int, stop: StopUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_stop = db.query(models.Stop).filter(models.Stop.id == stop_id).first()
    if not db_stop:
        raise HTTPException(status_code=404, detail="Stop not found")
    for var, value in vars(stop).items():
        if value is not None:
            setattr(db_stop, var, value)
    db.commit()
    db.refresh(db_stop)
    redis_client.delete("stops:all")
    redis_client.delete(f"stops:{stop_id}")
    return db_stop

@router.delete("/{stop_id}")
def delete_stop(stop_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_stop = db.query(models.Stop).filter(models.Stop.id == stop_id).first()
    if not db_stop:
        raise HTTPException(status_code=404, detail="Stop not found")
    db.delete(db_stop)
    db.commit()
    redis_client.delete("stops:all")
    redis_client.delete(f"stops:{stop_id}")
    return {"ok": True} 