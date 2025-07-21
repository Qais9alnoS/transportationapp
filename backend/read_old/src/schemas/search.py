from pydantic import BaseModel
from typing import List, Optional

class SearchRouteRequest(BaseModel):
    start_lat: float
    start_lng: float
    end_lat: float
    end_lng: float
    filter_type: Optional[str] = "fastest"  # fastest, cheapest, least_transfers

class RouteSegment(BaseModel):
    type: str  # walk or makro
    distance_meters: Optional[float] = None
    duration_seconds: Optional[int] = None
    instructions: Optional[str] = None
    makro_id: Optional[str] = None
    start_stop_id: Optional[str] = None
    end_stop_id: Optional[str] = None
    estimated_cost: Optional[int] = None

class SuggestedRoute(BaseModel):
    route_id: str
    description: str
    segments: List[RouteSegment]
    total_estimated_time_seconds: int
    total_estimated_cost: int

class SearchRouteResponse(BaseModel):
    routes: List[SuggestedRoute] 