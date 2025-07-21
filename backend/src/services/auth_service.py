from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import Optional
import requests
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from google.auth.exceptions import GoogleAuthError

from ..models.models import User
from ..schemas.auth import UserCreate, UserLogin, GoogleAuthRequest
from ..config.auth import verify_password, get_password_hash, create_tokens, GOOGLE_CLIENT_ID

class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_data: UserCreate) -> User:
        """Create a new user with email/password authentication"""
        try:
            # Check if user already exists
            existing_user = self.db.query(User).filter(
                (User.email == user_data.email) | (User.username == user_data.username)
            ).first()
            if existing_user:
                if existing_user.email == user_data.email:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="البريد الإلكتروني مستخدم مسبقًا"
                    )
                else:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="اسم المستخدم مستخدم مسبقًا"
                    )
            # Create new user
            hashed_password = get_password_hash(user_data.password)
            db_user = User(
                username=user_data.username,
                email=user_data.email,
                full_name=user_data.full_name,
                hashed_password=hashed_password,
                is_verified=True,  # For now, we'll assume email verification is done
                is_admin=getattr(user_data, 'is_admin', False)
            )
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            return db_user
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail="خطأ في سلامة البيانات: تحقق من صحة البيانات المدخلة وعدم التكرار")

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        return self.db.query(User).filter(User.username == username).first()

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self.db.query(User).filter(User.id == user_id).first()

    def authenticate_google_user(self, google_data: GoogleAuthRequest) -> User:
        """Authenticate user with Google OAuth"""
        try:
            # Verify the Google ID token
            idinfo = id_token.verify_oauth2_token(
                google_data.code, 
                google_requests.Request(), 
                GOOGLE_CLIENT_ID
            )
            
            google_id = idinfo['sub']
            google_email = idinfo['email']
            full_name = idinfo.get('name', '')
            
            # Check if user exists with this Google ID
            user = self.db.query(User).filter(User.google_id == google_id).first()
            
            if user:
                # Update user info if needed
                if not user.full_name and full_name:
                    user.full_name = full_name
                    self.db.commit()
                return user
            
            # Check if user exists with this email
            user = self.db.query(User).filter(User.email == google_email).first()
            
            if user:
                # Link existing account to Google
                user.google_id = google_id
                user.google_email = google_email
                if not user.full_name and full_name:
                    user.full_name = full_name
                self.db.commit()
                return user
            
            # Create new user with Google info
            username = self._generate_username_from_email(google_email)
            db_user = User(
                username=username,
                email=google_email,
                google_id=google_id,
                google_email=google_email,
                full_name=full_name,
                is_verified=True,
                profile_picture=idinfo.get('picture', '')
            )
            
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            
            return db_user
            
        except GoogleAuthError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Google token"
            )
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User creation failed"
            )

    def _generate_username_from_email(self, email: str) -> str:
        """Generate a unique username from email"""
        base_username = email.split('@')[0]
        username = base_username
        counter = 1
        
        while self.get_user_by_username(username):
            username = f"{base_username}{counter}"
            counter += 1
        
        return username

    def update_user_profile(self, user_id: int, **kwargs) -> User:
        """Update user profile information"""
        user = self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        for key, value in kwargs.items():
            if hasattr(user, key) and value is not None:
                setattr(user, key, value)
        
        self.db.commit()
        self.db.refresh(user)
        return user 