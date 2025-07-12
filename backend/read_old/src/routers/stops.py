from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.schemas.stop import StopCreate, StopRead, StopUpdate
from src.models import models
from config.database import SessionLocal
from src.routers.auth import get_current_user
from src.services.cache_service import cache_get, cache_set, redis_client

router = APIRouter(prefix="/stops", tags=["Stops"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=StopRead)
def create_stop(stop: StopCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if db.query(models.Stop).filter(models.Stop.name == stop.name).first():
        raise HTTPException(status_code=400, detail="Stop name already exists")
    db_stop = models.Stop(
        name=stop.name,
        lat=stop.lat,
        lng=stop.lng,
        geom=f'POINT({stop.lng} {stop.lat})'
    )
    db.add(db_stop)
    db.commit()
    db.refresh(db_stop)
    redis_client.delete("stops:all")
    redis_client.delete(f"stops:{db_stop.id}")
    return db_stop

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