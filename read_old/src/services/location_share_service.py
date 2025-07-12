from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import List, Optional
from datetime import datetime, timedelta

from ..models.models import User, LocationShare, LocationSharingStatus, Friendship, FriendshipStatus
from ..schemas.location_share import LocationShareCreate, LocationShareUpdate

class LocationShareService:
    def __init__(self, db: Session):
        self.db = db

    def share_location(self, user_id: int, share_data: LocationShareCreate) -> List[LocationShare]:
        """Share location with multiple friends"""
        # Verify user exists
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Verify all friends exist and are actually friends
        friends = self.db.query(User).filter(User.id.in_(share_data.friend_ids)).all()
        if len(friends) != len(share_data.friend_ids):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Some friends not found"
            )
        
        # Check if all are actually friends
        for friend_id in share_data.friend_ids:
            friendship = self.db.query(Friendship).filter(
                ((Friendship.user_id == user_id) & (Friendship.friend_id == friend_id)) |
                ((Friendship.user_id == friend_id) & (Friendship.friend_id == user_id)),
                Friendship.status == FriendshipStatus.ACCEPTED
            ).first()
            
            if not friendship:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"User {friend_id} is not your friend"
                )
        
        # Calculate expiration time
        expires_at = datetime.utcnow() + timedelta(hours=share_data.duration_hours)
        
        # Create location shares
        location_shares = []
        for friend_id in share_data.friend_ids:
            location_share = LocationShare(
                user_id=user_id,
                shared_with_id=friend_id,
                current_lat=share_data.current_lat,
                current_lng=share_data.current_lng,
                destination_lat=share_data.destination_lat,
                destination_lng=share_data.destination_lng,
                destination_name=share_data.destination_name,
                estimated_arrival=share_data.estimated_arrival,
                message=share_data.message,
                expires_at=expires_at,
                status=LocationSharingStatus.ACTIVE
            )
            
            self.db.add(location_share)
            location_shares.append(location_share)
        
        self.db.commit()
        
        # Refresh all location shares
        for share in location_shares:
            self.db.refresh(share)
        
        return location_shares

    def update_location_share(self, user_id: int, share_id: int, update_data: LocationShareUpdate) -> LocationShare:
        """Update an active location share"""
        location_share = self.db.query(LocationShare).filter(
            LocationShare.id == share_id,
            LocationShare.user_id == user_id,
            LocationShare.status == LocationSharingStatus.ACTIVE
        ).first()
        
        if not location_share:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Location share not found or not active"
            )
        
        # Update fields
        for field, value in update_data.dict(exclude_unset=True).items():
            if hasattr(location_share, field):
                setattr(location_share, field, value)
        
        self.db.commit()
        self.db.refresh(location_share)
        
        return location_share

    def cancel_location_share(self, user_id: int, share_id: int) -> bool:
        """Cancel an active location share"""
        location_share = self.db.query(LocationShare).filter(
            LocationShare.id == share_id,
            LocationShare.user_id == user_id,
            LocationShare.status == LocationSharingStatus.ACTIVE
        ).first()
        
        if not location_share:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Location share not found or not active"
            )
        
        location_share.status = LocationSharingStatus.CANCELLED
        self.db.commit()
        
        return True

    def get_active_location_shares(self, user_id: int) -> List[LocationShare]:
        """Get all active location shares for a user (both sent and received)"""
        return self.db.query(LocationShare).filter(
            (LocationShare.user_id == user_id) | (LocationShare.shared_with_id == user_id),
            LocationShare.status == LocationSharingStatus.ACTIVE,
            LocationShare.expires_at > datetime.utcnow()
        ).all()

    def get_received_location_shares(self, user_id: int) -> List[LocationShare]:
        """Get location shares received by user"""
        return self.db.query(LocationShare).filter(
            LocationShare.shared_with_id == user_id,
            LocationShare.status == LocationSharingStatus.ACTIVE,
            LocationShare.expires_at > datetime.utcnow()
        ).all()

    def get_sent_location_shares(self, user_id: int) -> List[LocationShare]:
        """Get location shares sent by user"""
        return self.db.query(LocationShare).filter(
            LocationShare.user_id == user_id,
            LocationShare.status == LocationSharingStatus.ACTIVE,
            LocationShare.expires_at > datetime.utcnow()
        ).all()

    def get_location_share_history(self, user_id: int, limit: int = 50) -> List[LocationShare]:
        """Get location share history for a user"""
        return self.db.query(LocationShare).filter(
            (LocationShare.user_id == user_id) | (LocationShare.shared_with_id == user_id)
        ).order_by(LocationShare.created_at.desc()).limit(limit).all()

    def cleanup_expired_shares(self) -> int:
        """Clean up expired location shares (should be run periodically)"""
        expired_shares = self.db.query(LocationShare).filter(
            LocationShare.status == LocationSharingStatus.ACTIVE,
            LocationShare.expires_at <= datetime.utcnow()
        ).all()
        
        for share in expired_shares:
            share.status = LocationSharingStatus.EXPIRED
        
        self.db.commit()
        
        return len(expired_shares)

    def get_friend_locations(self, user_id: int) -> List[LocationShare]:
        """Get current locations of friends who are sharing with the user"""
        return self.db.query(LocationShare).filter(
            LocationShare.shared_with_id == user_id,
            LocationShare.status == LocationSharingStatus.ACTIVE,
            LocationShare.expires_at > datetime.utcnow()
        ).all() 