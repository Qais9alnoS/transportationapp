from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class LocationSharingStatus(str, Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    CANCELLED = "cancelled"

class LocationShareBase(BaseModel):
    current_lat: float = Field(..., ge=-90, le=90)
    current_lng: float = Field(..., ge=-180, le=180)
    destination_lat: Optional[float] = Field(None, ge=-90, le=90)
    destination_lng: Optional[float] = Field(None, ge=-180, le=180)
    destination_name: Optional[str] = None
    estimated_arrival: Optional[datetime] = None
    message: Optional[str] = None
    duration_hours: int = Field(default=1, ge=1, le=24)  # How long to share location

class LocationShareCreate(LocationShareBase):
    friend_ids: List[int] = Field(..., min_items=1, max_items=10)

class LocationShareResponse(BaseModel):
    id: int
    user_id: int
    shared_with_id: int
    current_lat: float
    current_lng: float
    destination_lat: Optional[float]
    destination_lng: Optional[float]
    destination_name: Optional[str]
    estimated_arrival: Optional[datetime]
    message: Optional[str]
    status: LocationSharingStatus
    expires_at: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True

class LocationShareWithUserResponse(LocationShareResponse):
    user: dict  # Basic user info
    shared_with: dict  # Basic user info
    
    class Config:
        from_attributes = True

class LocationShareUpdate(BaseModel):
    current_lat: Optional[float] = Field(None, ge=-90, le=90)
    current_lng: Optional[float] = Field(None, ge=-180, le=180)
    destination_lat: Optional[float] = Field(None, ge=-90, le=90)
    destination_lng: Optional[float] = Field(None, ge=-180, le=180)
    destination_name: Optional[str] = None
    estimated_arrival: Optional[datetime] = None
    message: Optional[str] = None

class LocationShareCancel(BaseModel):
    share_id: int 