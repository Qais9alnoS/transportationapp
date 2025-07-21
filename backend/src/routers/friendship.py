from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..services.friendship_service import FriendshipService
from ..services.auth_service import AuthService
from ..schemas.friendship import (
    FriendshipCreate, FriendshipResponse, FriendshipUpdate, 
    UserFriendResponse, FriendshipWithUserResponse, FriendRequestResponse
)
from ..routers.auth import get_current_user
from ..schemas.auth import UserResponse

router = APIRouter(prefix="/friends", tags=["Friendship"])

@router.post("/request", response_model=FriendshipResponse)
async def send_friend_request(
    friend_data: FriendshipCreate,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send a friend request to another user"""
    friendship_service = FriendshipService(db)
    friendship = friendship_service.send_friend_request(
        user_id=current_user.id,
        friend_id=friend_data.friend_id
    )
    return FriendshipResponse.from_orm(friendship)

@router.put("/request/{friendship_id}/respond", response_model=FriendshipResponse)
async def respond_to_friend_request(
    friendship_id: int,
    response_data: FriendshipUpdate,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Accept or reject a friend request"""
    friendship_service = FriendshipService(db)
    friendship = friendship_service.respond_to_friend_request(
        user_id=current_user.id,
        friendship_id=friendship_id,
        status=response_data.status
    )
    return FriendshipResponse.from_orm(friendship)

@router.get("/", response_model=List[UserFriendResponse])
async def get_friends(
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all friends of the current user"""
    friendship_service = FriendshipService(db)
    friends = friendship_service.get_friends(current_user.id)
    return [UserFriendResponse.from_orm(friend) for friend in friends]

@router.get("/requests/received", response_model=List[FriendRequestResponse])
async def get_received_friend_requests(
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get pending friend requests received by the current user"""
    friendship_service = FriendshipService(db)
    requests = friendship_service.get_friend_requests(current_user.id)
    
    result = []
    for req in requests:
        user_info = UserFriendResponse.from_orm(req.user)
        result.append(FriendRequestResponse(
            id=req.id,
            status=req.status,
            created_at=req.created_at,
            user=user_info
        ))
    
    return result

@router.get("/requests/sent", response_model=List[FriendRequestResponse])
async def get_sent_friend_requests(
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get pending friend requests sent by the current user"""
    friendship_service = FriendshipService(db)
    requests = friendship_service.get_sent_friend_requests(current_user.id)
    
    result = []
    for req in requests:
        user_info = UserFriendResponse.from_orm(req.friend)
        result.append(FriendRequestResponse(
            id=req.id,
            status=req.status,
            created_at=req.created_at,
            user=user_info
        ))
    
    return result

@router.delete("/{friend_id}")
async def remove_friend(
    friend_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove a friend"""
    friendship_service = FriendshipService(db)
    success = friendship_service.remove_friend(
        user_id=current_user.id,
        friend_id=friend_id
    )
    return {"message": "Friend removed successfully"}

@router.delete("/request/{friendship_id}/cancel")
async def cancel_friend_request(
    friendship_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cancel a sent friend request"""
    friendship_service = FriendshipService(db)
    success = friendship_service.cancel_friend_request(
        user_id=current_user.id,
        friendship_id=friendship_id
    )
    return {"message": "Friend request cancelled successfully"}

@router.get("/search", response_model=List[UserFriendResponse])
async def search_users(
    query: str = Query(..., min_length=2, description="Search query for username or full name"),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of results"),
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Search for users to add as friends"""
    friendship_service = FriendshipService(db)
    users = friendship_service.search_users(
        user_id=current_user.id,
        query=query,
        limit=limit
    )
    return [UserFriendResponse.from_orm(user) for user in users]

@router.get("/status/{user_id}")
async def get_friendship_status(
    user_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get friendship status with another user"""
    friendship_service = FriendshipService(db)
    status = friendship_service.get_friendship_status(
        user_id=current_user.id,
        other_user_id=user_id
    )
    return {"status": status.value if status else None} 