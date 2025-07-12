from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..services.location_share_service import LocationShareService
from ..schemas.location_share import (
    LocationShareCreate, LocationShareResponse, LocationShareUpdate,
    LocationShareWithUserResponse, LocationShareCancel
)
from ..routers.auth import get_current_user
from ..schemas.auth import UserResponse

router = APIRouter(prefix="/location-share", tags=["Location Sharing"])

@router.post("/share", response_model=List[LocationShareResponse])
async def share_location(
    share_data: LocationShareCreate,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Share current location with friends"""
    location_service = LocationShareService(db)
    location_shares = location_service.share_location(
        user_id=current_user.id,
        share_data=share_data
    )
    return [LocationShareResponse.from_orm(share) for share in location_shares]

@router.put("/{share_id}/update", response_model=LocationShareResponse)
async def update_location_share(
    share_id: int,
    update_data: LocationShareUpdate,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update an active location share"""
    location_service = LocationShareService(db)
    location_share = location_service.update_location_share(
        user_id=current_user.id,
        share_id=share_id,
        update_data=update_data
    )
    return LocationShareResponse.from_orm(location_share)

@router.delete("/{share_id}/cancel")
async def cancel_location_share(
    share_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cancel an active location share"""
    location_service = LocationShareService(db)
    success = location_service.cancel_location_share(
        user_id=current_user.id,
        share_id=share_id
    )
    return {"message": "Location share cancelled successfully"}

@router.get("/active", response_model=List[LocationShareWithUserResponse])
async def get_active_location_shares(
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all active location shares for the current user"""
    location_service = LocationShareService(db)
    location_shares = location_service.get_active_location_shares(current_user.id)
    
    result = []
    for share in location_shares:
        # Get basic user info
        user_info = {
            "id": share.user.id,
            "username": share.user.username,
            "full_name": share.user.full_name,
            "profile_picture": share.user.profile_picture
        }
        shared_with_info = {
            "id": share.shared_with.id,
            "username": share.shared_with.username,
            "full_name": share.shared_with.full_name,
            "profile_picture": share.shared_with.profile_picture
        }
        
        result.append(LocationShareWithUserResponse(
            **LocationShareResponse.from_orm(share).dict(),
            user=user_info,
            shared_with=shared_with_info
        ))
    
    return result

@router.get("/received", response_model=List[LocationShareWithUserResponse])
async def get_received_location_shares(
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get location shares received by the current user"""
    location_service = LocationShareService(db)
    location_shares = location_service.get_received_location_shares(current_user.id)
    
    result = []
    for share in location_shares:
        user_info = {
            "id": share.user.id,
            "username": share.user.username,
            "full_name": share.user.full_name,
            "profile_picture": share.user.profile_picture
        }
        shared_with_info = {
            "id": share.shared_with.id,
            "username": share.shared_with.username,
            "full_name": share.shared_with.full_name,
            "profile_picture": share.shared_with.profile_picture
        }
        
        result.append(LocationShareWithUserResponse(
            **LocationShareResponse.from_orm(share).dict(),
            user=user_info,
            shared_with=shared_with_info
        ))
    
    return result

@router.get("/sent", response_model=List[LocationShareWithUserResponse])
async def get_sent_location_shares(
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get location shares sent by the current user"""
    location_service = LocationShareService(db)
    location_shares = location_service.get_sent_location_shares(current_user.id)
    
    result = []
    for share in location_shares:
        user_info = {
            "id": share.user.id,
            "username": share.user.username,
            "full_name": share.user.full_name,
            "profile_picture": share.user.profile_picture
        }
        shared_with_info = {
            "id": share.shared_with.id,
            "username": share.shared_with.username,
            "full_name": share.shared_with.full_name,
            "profile_picture": share.shared_with.profile_picture
        }
        
        result.append(LocationShareWithUserResponse(
            **LocationShareResponse.from_orm(share).dict(),
            user=user_info,
            shared_with=shared_with_info
        ))
    
    return result

@router.get("/history", response_model=List[LocationShareWithUserResponse])
async def get_location_share_history(
    limit: int = Query(50, ge=1, le=100, description="Maximum number of history items"),
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get location share history for the current user"""
    location_service = LocationShareService(db)
    location_shares = location_service.get_location_share_history(
        user_id=current_user.id,
        limit=limit
    )
    
    result = []
    for share in location_shares:
        user_info = {
            "id": share.user.id,
            "username": share.user.username,
            "full_name": share.user.full_name,
            "profile_picture": share.user.profile_picture
        }
        shared_with_info = {
            "id": share.shared_with.id,
            "username": share.shared_with.username,
            "full_name": share.shared_with.full_name,
            "profile_picture": share.shared_with.profile_picture
        }
        
        result.append(LocationShareWithUserResponse(
            **LocationShareResponse.from_orm(share).dict(),
            user=user_info,
            shared_with=shared_with_info
        ))
    
    return result

@router.get("/friends/locations", response_model=List[LocationShareWithUserResponse])
async def get_friend_locations(
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current locations of friends who are sharing with the user"""
    location_service = LocationShareService(db)
    location_shares = location_service.get_friend_locations(current_user.id)
    
    result = []
    for share in location_shares:
        user_info = {
            "id": share.user.id,
            "username": share.user.username,
            "full_name": share.user.full_name,
            "profile_picture": share.user.profile_picture
        }
        shared_with_info = {
            "id": share.shared_with.id,
            "username": share.shared_with.username,
            "full_name": share.shared_with.full_name,
            "profile_picture": share.shared_with.profile_picture
        }
        
        result.append(LocationShareWithUserResponse(
            **LocationShareResponse.from_orm(share).dict(),
            user=user_info,
            shared_with=shared_with_info
        ))
    
    return result

@router.post("/cleanup")
async def cleanup_expired_shares(
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Clean up expired location shares (admin function)"""
    location_service = LocationShareService(db)
    cleaned_count = location_service.cleanup_expired_shares()
    return {"message": f"Cleaned up {cleaned_count} expired location shares"} 