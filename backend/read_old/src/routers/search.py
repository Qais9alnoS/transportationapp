from fastapi import APIRouter
from src.schemas.search import SearchRouteRequest, SearchRouteResponse
from src.services.route_search import search_routes

router = APIRouter(prefix="/search-route", tags=["SearchRoute"])
 
@router.post("/", response_model=SearchRouteResponse)
def search_route(request: SearchRouteRequest):
    return search_routes(request) 