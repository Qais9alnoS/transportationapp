from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MakroLocationCreate(BaseModel):
    makro_id: str
    lat: float
    lng: float
    timestamp: Optional[datetime] = None

class MakroLocationRead(BaseModel):
    id: int
    makro_id: str
    lat: float
    lng: float
    timestamp: datetime 