from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import List, Optional
from datetime import datetime

from ..models.models import User, Friendship, FriendshipStatus
from ..schemas.friendship import FriendshipCreate, FriendshipUpdate, FriendshipStatus as FriendshipStatusEnum

class FriendshipService:
    def __init__(self, db: Session):
        self.db = db

    def send_friend_request(self, user_id: int, friend_id: int) -> Friendship:
        """Send a friend request"""
        # Check if users exist
        user = self.db.query(User).filter(User.id == user_id).first()
        friend = self.db.query(User).filter(User.id == friend_id).first()
        
        if not user or not friend:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        if user_id == friend_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot send friend request to yourself"
            )
        
        # Check if friendship already exists
        existing_friendship = self.db.query(Friendship).filter(
            ((Friendship.user_id == user_id) & (Friendship.friend_id == friend_id)) |
            ((Friendship.user_id == friend_id) & (Friendship.friend_id == user_id))
        ).first()
        
        if existing_friendship:
            if existing_friendship.status == FriendshipStatus.ACCEPTED:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Already friends"
                )
            elif existing_friendship.status == FriendshipStatus.PENDING:
                if existing_friendship.user_id == user_id:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Friend request already sent"
                    )
                else:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Friend request already received from this user"
                    )
        
        # Create new friendship request
        friendship = Friendship(
            user_id=user_id,
            friend_id=friend_id,
            status=FriendshipStatus.PENDING
        )
        
        self.db.add(friendship)
        self.db.commit()
        self.db.refresh(friendship)
        
        return friendship

    def respond_to_friend_request(self, user_id: int, friendship_id: int, status: FriendshipStatusEnum) -> Friendship:
        """Accept or reject a friend request"""
        friendship = self.db.query(Friendship).filter(
            Friendship.id == friendship_id,
            Friendship.friend_id == user_id,
            Friendship.status == FriendshipStatus.PENDING
        ).first()
        
        if not friendship:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Friend request not found"
            )
        
        friendship.status = FriendshipStatus(status)
        friendship.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(friendship)
        
        return friendship

    def get_friends(self, user_id: int) -> List[User]:
        """Get all friends of a user"""
        friendships = self.db.query(Friendship).filter(
            ((Friendship.user_id == user_id) | (Friendship.friend_id == user_id)) &
            (Friendship.status == FriendshipStatus.ACCEPTED)
        ).all()
        
        friends = []
        for friendship in friendships:
            if friendship.user_id == user_id:
                friends.append(friendship.friend)
            else:
                friends.append(friendship.user)
        
        return friends

    def get_friend_requests(self, user_id: int) -> List[Friendship]:
        """Get pending friend requests received by user"""
        return self.db.query(Friendship).filter(
            Friendship.friend_id == user_id,
            Friendship.status == FriendshipStatus.PENDING
        ).all()

    def get_sent_friend_requests(self, user_id: int) -> List[Friendship]:
        """Get pending friend requests sent by user"""
        return self.db.query(Friendship).filter(
            Friendship.user_id == user_id,
            Friendship.status == FriendshipStatus.PENDING
        ).all()

    def remove_friend(self, user_id: int, friend_id: int) -> bool:
        """Remove a friend (delete friendship)"""
        friendship = self.db.query(Friendship).filter(
            ((Friendship.user_id == user_id) & (Friendship.friend_id == friend_id)) |
            ((Friendship.user_id == friend_id) & (Friendship.friend_id == user_id)),
            Friendship.status == FriendshipStatus.ACCEPTED
        ).first()
        
        if not friendship:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Friendship not found"
            )
        
        self.db.delete(friendship)
        self.db.commit()
        
        return True

    def cancel_friend_request(self, user_id: int, friendship_id: int) -> bool:
        """Cancel a sent friend request"""
        friendship = self.db.query(Friendship).filter(
            Friendship.id == friendship_id,
            Friendship.user_id == user_id,
            Friendship.status == FriendshipStatus.PENDING
        ).first()
        
        if not friendship:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Friend request not found"
            )
        
        self.db.delete(friendship)
        self.db.commit()
        
        return True

    def search_users(self, user_id: int, query: str, limit: int = 10) -> List[User]:
        """Search for users by username or full name"""
        # Get current user's friends and pending requests to exclude them
        existing_relationships = self.db.query(Friendship).filter(
            (Friendship.user_id == user_id) | (Friendship.friend_id == user_id)
        ).all()
        
        excluded_ids = {user_id}
        for rel in existing_relationships:
            if rel.user_id == user_id:
                excluded_ids.add(rel.friend_id)
            else:
                excluded_ids.add(rel.user_id)
        
        # Search for users
        users = self.db.query(User).filter(
            User.id.notin_(excluded_ids),
            User.is_active == True,
            (User.username.ilike(f"%{query}%")) | (User.full_name.ilike(f"%{query}%"))
        ).limit(limit).all()
        
        return users

    def get_friendship_status(self, user_id: int, other_user_id: int) -> Optional[FriendshipStatus]:
        """Get friendship status between two users"""
        friendship = self.db.query(Friendship).filter(
            ((Friendship.user_id == user_id) & (Friendship.friend_id == other_user_id)) |
            ((Friendship.user_id == other_user_id) & (Friendship.friend_id == user_id))
        ).first()
        
        return friendship.status if friendship else None 