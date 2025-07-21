from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from src.schemas.search import SearchRouteRequest, SearchRouteResponse
from src.services.route_search import search_routes
from src.models.models import SearchLog
from config.database import SessionLocal
from src.routers.auth import get_current_admin

router = APIRouter(prefix="/search-route", tags=["SearchRoute"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=SearchRouteResponse)
def search_route(request: SearchRouteRequest):
    return search_routes(request)

@router.get("/logs", response_model=List[dict])
def get_search_logs(
    limit: int = Query(100, ge=1, le=1000, description="عدد النتائج"),
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin)
):
    """جلب سجلات البحث (للمديرين فقط)"""
    logs = db.query(SearchLog).order_by(SearchLog.timestamp.desc()).limit(limit).all()
    return [
        {
            "id": log.id,
            "start_lat": log.start_lat,
            "start_lng": log.start_lng,
            "end_lat": log.end_lat,
            "end_lng": log.end_lng,
            "route_id": log.route_id,
            "filter_type": log.filter_type,
            "timestamp": log.timestamp
        }
        for log in logs
    ] 