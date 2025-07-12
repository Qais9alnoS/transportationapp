from pydantic import BaseModel, field_validator
from typing import Optional

class StopBase(BaseModel):
    name: str
    lat: float
    lng: float

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

    @field_validator('name')
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Name must not be empty')
        return v

class StopCreate(StopBase):
    pass

class StopUpdate(StopBase):
    name: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None

class StopRead(StopBase):
    id: int
    class Config:
        from_attributes = True 