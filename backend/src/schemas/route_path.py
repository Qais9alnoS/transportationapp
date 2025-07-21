from pydantic import BaseModel, field_validator
from typing import Optional

class RoutePathBase(BaseModel):
    route_id: Optional[int] = None
    lat: float
    lng: float
    point_order: Optional[int] = None

    @field_validator('lat')
    def validate_lat(cls, v):
        if not (-90 <= v <= 90):
            raise ValueError('Latitude must be between -90 and 90')
        return v

    @field_validator('lng')
    def validate_lng(cls, v):
        if not (-180 <= v <= 180):
            raise ValueError('Longitude must be between -180 and 180')
        return v

class RoutePathCreate(RoutePathBase):
    pass

class RoutePathUpdate(RoutePathBase):
    pass

class RoutePathRead(RoutePathBase):
    id: int
    class Config:
        from_attributes = True 