from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FeedbackCreate(BaseModel):
    type: Optional[str] = None
    rating: int
    comment: Optional[str] = None
    route_id: int

class FeedbackRead(BaseModel):
    id: int
    type: Optional[str] = None
    rating: int
    comment: Optional[str] = None
    route_id: int
    timestamp: datetime

    class Config:
        from_attributes = True 