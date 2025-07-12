from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from src.services.traffic_data import get_mock_traffic_data, get_directions_with_traffic

router = APIRouter(prefix="/traffic-data", tags=["Traffic"])

class PathPoint(BaseModel):
    lat: float
    lng: float

class TrafficRequest(BaseModel):
    path: List[PathPoint]

class DirectionsRequest(BaseModel):
    origin: PathPoint
    destination: PathPoint
    departure_time: str = "now"  # يمكن تركها "now" أو تحديد وقت Unix timestamp

@router.post("/", summary="جلب بيانات الازدحام لمسار معين (محاكاة)")
def get_traffic_data(req: TrafficRequest):
    """
    يستقبل مسار (قائمة نقاط) ويعيد بيانات ازدحام وهمية لكل نقطة.
    """
    path = [point.dict() for point in req.path]
    return get_mock_traffic_data(path)

@router.post("/google", summary="جلب بيانات المسار والزمن الفعلي من Google Directions API")
def get_google_directions(req: DirectionsRequest):
    """
    يستقبل نقطتي بداية ونهاية (origin, destination) ويعيد بيانات المسار والزمن الفعلي مع مراعاة الازدحام من Google Directions API.
    يجب وضع مفتاح Google API في src/services/traffic_data.py.
    """
    return get_directions_with_traffic(
        req.origin.lat, req.origin.lng,
        req.destination.lat, req.destination.lng,
        req.departure_time
    ) 