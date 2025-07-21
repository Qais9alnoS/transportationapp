from pydantic import BaseModel, field_validator
from typing import Optional, List
from src.schemas.stop import StopCreate, StopRead
from src.schemas.route_path import RoutePathCreate, RoutePathRead
import re

class RouteBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: Optional[int] = None
    operating_hours: Optional[str] = None

    @field_validator('price')
    def validate_price(cls, v):
        if v is not None and v < 0:
            raise ValueError('Price must be >= 0')
        return v

    @field_validator('operating_hours')
    def validate_operating_hours(cls, v):
        if v is not None:
            pattern = r"^([01]\d|2[0-3]):[0-5]\d-([01]\d|2[0-3]):[0-5]\d$"
            if not re.match(pattern, v):
                raise ValueError('operating_hours must be in format HH:MM-HH:MM')
        return v

class RouteCreate(RouteBase):
    stops: Optional[List[StopCreate]] = None
    paths: Optional[List[RoutePathCreate]] = None

class RouteUpdate(RouteBase):
    name: Optional[str] = None

class RouteRead(RouteBase):
    id: int
    stops: Optional[List[StopRead]] = None
    paths: Optional[List[RoutePathRead]] = None
    class Config:
        from_attributes = True 