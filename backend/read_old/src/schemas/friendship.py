from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class FriendshipStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

class FriendshipBase(BaseModel):
    friend_id: int

class FriendshipCreate(FriendshipBase):
    pass

class FriendshipResponse(BaseModel):
    id: int
    user_id: int
    friend_id: int
    status: FriendshipStatus
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class FriendshipUpdate(BaseModel):
    status: FriendshipStatus

class UserFriendResponse(BaseModel):
    id: int
    username: str
    full_name: Optional[str] = None
    profile_picture: Optional[str] = None
    is_online: bool = False  # This would be calculated based on last activity
    
    class Config:
        from_attributes = True

class FriendshipWithUserResponse(BaseModel):
    id: int
    status: FriendshipStatus
    created_at: datetime
    updated_at: datetime
    friend: UserFriendResponse
    
    class Config:
        from_attributes = True

class FriendRequestResponse(BaseModel):
    id: int
    status: FriendshipStatus
    created_at: datetime
    user: UserFriendResponse
    
    class Config:
        from_attributes = True 