from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.schemas.makro_location import MakroLocationCreate, MakroLocationRead
from src.models import models
from config.database import SessionLocal
from geoalchemy2.shape import from_shape
from shapely.geometry import Point
from datetime import datetime

router = APIRouter(prefix="/makro-locations", tags=["MakroLocations"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=MakroLocationRead)
def create_makro_location(loc: MakroLocationCreate, db: Session = Depends(get_db)):
    """
    يستقبل هذا المسار بيانات موقع مكرو (GPS) ويحفظها في قاعدة البيانات.
    أرسل طلب POST مع البيانات التالية:
    {
      "makro_id": "makro_123",
      "lat": 33.500,
      "lng": 36.300,
      "timestamp": "2024-06-01T12:00:00Z" // اختياري
    }
    """
    db_loc = models.MakroLocation(
        makro_id=loc.makro_id,
        lat=loc.lat,
        lng=loc.lng,
        geom=from_shape(Point(loc.lng, loc.lat), srid=4326),
        timestamp=loc.timestamp or datetime.utcnow()
    )
    db.add(db_loc)
    db.commit()
    db.refresh(db_loc)
    return db_loc

@router.put("/{makro_location_id}", response_model=MakroLocationRead)
def update_makro_location(makro_location_id: int, loc: MakroLocationCreate, db: Session = Depends(get_db)):
    db_loc = db.query(models.MakroLocation).filter(models.MakroLocation.id == makro_location_id).first()
    if not db_loc:
        raise HTTPException(status_code=404, detail="Not Found")
    db_loc.lat = loc.lat
    db_loc.lng = loc.lng
    db_loc.makro_id = loc.makro_id
    db_loc.timestamp = loc.timestamp or datetime.utcnow()
    db_loc.geom = from_shape(Point(loc.lng, loc.lat), srid=4326)
    db.commit()
    db.refresh(db_loc)
    return db_loc

@router.get("/", response_model=list[MakroLocationRead])
def get_makro_locations(db: Session = Depends(get_db)):
    return db.query(models.MakroLocation).all()

"""
راوتر تتبع مواقع المكاري (MakroLocations)

هذا الراوتر يسمح لأي جهاز (مثل جهاز GPS في المكرو) بإرسال موقعه الحالي إلى السيرفر عبر طلب POST.

مثال على البيانات المطلوبة (يجب إرسالها كـ JSON):

POST /api/v1/makro-locations/
Content-Type: application/json

{
  "makro_id": "makro_123",
  "lat": 33.500,
  "lng": 36.300,
  "timestamp": "2024-06-01T12:00:00Z"  // يمكن تركه فارغًا وسيتم تعبئته تلقائيًا
}

يمكن لأي جهاز أو برنامج إرسال هذه البيانات عبر الإنترنت وسيتم حفظ الموقع مباشرة في قاعدة البيانات.
""" 