from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ComplaintCreate(BaseModel):
    user_id: Optional[int] = None
    route_id: Optional[int] = None
    makro_id: Optional[str] = None
    complaint_text: str

class ComplaintRead(BaseModel):
    id: int
    user_id: Optional[int] = None
    route_id: Optional[int] = None
    makro_id: Optional[str] = None
    complaint_text: str
    status: str
    timestamp: datetime

    class Config:
        from_attributes = True

class ComplaintUpdate(BaseModel):
    status: Optional[str] = None
    complaint_text: Optional[str] = None 