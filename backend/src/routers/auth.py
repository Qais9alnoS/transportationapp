from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional

from ..database import get_db
from ..services.auth_service import AuthService
from ..schemas.auth import (
    UserCreate, UserLogin, UserResponse, Token, TokenRefresh, 
    GoogleAuthRequest, PasswordResetRequest, PasswordReset, ChangePassword, UserWithToken
)
from ..config.auth import verify_token, create_tokens
import os
import shutil

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[UserResponse]:
    """Get current authenticated user"""
    try:
        token_data = verify_token(credentials.credentials)
        auth_service = AuthService(db)
        user = auth_service.get_user_by_id(token_data.user_id)
        
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )
        
        return UserResponse.from_orm(user)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

def get_current_admin(
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> UserResponse:
    """Get current authenticated admin user"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user

@router.post("/register", response_model=UserWithToken)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user with email and password"""
    try:
        auth_service = AuthService(db)
        user = auth_service.create_user(user_data)
        tokens = create_tokens(user.username, user.id)
        return UserWithToken(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            is_verified=user.is_verified,
            is_admin=user.is_admin,
            profile_picture=user.profile_picture,
            created_at=user.created_at,
            updated_at=user.updated_at,
            access_token=tokens.access_token,
            refresh_token=tokens.refresh_token,
            token_type=tokens.token_type,
            expires_in=tokens.expires_in
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"فشل في التسجيل: {str(e)}")

@router.post("/login", response_model=Token)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """Login with email and password"""
    try:
        auth_service = AuthService(db)
        user = auth_service.authenticate_user(user_data.email, user_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Account is deactivated"
            )
        tokens = create_tokens(user.username, user.id)
        return tokens
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"فشل في تسجيل الدخول: {str(e)}")

@router.post("/google", response_model=Token)
async def google_auth(google_data: GoogleAuthRequest, db: Session = Depends(get_db)):
    """Authenticate with Google OAuth"""
    try:
        auth_service = AuthService(db)
        user = auth_service.authenticate_google_user(google_data)
        tokens = create_tokens(user.username, user.id)
        return tokens
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"فشل في المصادقة عبر Google: {str(e)}")

@router.post("/refresh", response_model=Token)
async def refresh_token(token_data: TokenRefresh, db: Session = Depends(get_db)):
    """Refresh access token using refresh token"""
    try:
        token_data_decoded = verify_token(token_data.refresh_token, "refresh")
        auth_service = AuthService(db)
        user = auth_service.get_user_by_id(token_data_decoded.user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )
        tokens = create_tokens(user.username, user.id)
        return tokens
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Refresh token failed: {str(e)}")

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: UserResponse = Depends(get_current_user)):
    """Get current user information"""
    return current_user

@router.post("/forgot-password")
async def forgot_password(request: PasswordResetRequest, db: Session = Depends(get_db)):
    """Request password reset"""
    try:
        auth_service = AuthService(db)
        # لا تكشف إذا كان البريد موجودًا أم لا
        _ = auth_service.get_user_by_email(request.email)
        # في تطبيق حقيقي: أرسل إيميل إعادة تعيين
        return {"message": "If the email exists, a password reset link has been sent"}
    except Exception as e:
        return {"message": "If the email exists, a password reset link has been sent"}

@router.post("/reset-password")
async def reset_password(reset_data: PasswordReset, db: Session = Depends(get_db)):
    """Reset password using token"""
    try:
        # في تطبيق حقيقي: تحقق من التوكن وغيّر كلمة المرور
        return {"message": "Password reset successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Password reset failed: {str(e)}")

@router.post("/change-password")
async def change_password(
    password_data: ChangePassword,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change password for authenticated user"""
    try:
        auth_service = AuthService(db)
        user = auth_service.get_user_by_id(current_user.id)
        if not auth_service.verify_password(password_data.current_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
        # Update password
        from ..config.auth import get_password_hash
        user.hashed_password = get_password_hash(password_data.new_password)
        db.commit()
        return {"message": "Password changed successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Change password failed: {str(e)}")

@router.get("/google/url")
async def get_google_auth_url():
    """Get Google OAuth URL"""
    from ..config.auth import GOOGLE_CLIENT_ID, GOOGLE_REDIRECT_URI
    
    google_auth_url = f"https://accounts.google.com/o/oauth2/v2/auth"
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline"
    }
    
    # Build URL with parameters
    import urllib.parse
    query_string = urllib.parse.urlencode(params)
    full_url = f"{google_auth_url}?{query_string}"
    
    return {"auth_url": full_url}

@router.get("/profile", response_model=UserResponse)
async def get_user_profile(current_user: UserResponse = Depends(get_current_user)):
    """Get user profile information"""
    return current_user

@router.put("/profile", response_model=UserResponse)
async def update_user_profile(
    profile_data: dict,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user profile information"""
    auth_service = AuthService(db)
    user = auth_service.get_user_by_id(current_user.id)
    
    # Update allowed fields
    allowed_fields = ["full_name", "profile_picture"]
    for field, value in profile_data.items():
        if field in allowed_fields and value is not None:
            setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    
    return UserResponse.from_orm(user) 

@router.post("/upload-profile-picture")
async def upload_profile_picture(
    file: UploadFile = File(...),
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    رفع صورة الملف الشخصي للمستخدم الحالي
    """
    # تحقق من نوع الملف
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=415, detail="الملف المرفوع ليس صورة")

    # تحديد مسار الحفظ
    upload_dir = os.path.join("uploads", "profile_pictures")
    os.makedirs(upload_dir, exist_ok=True)
    filename = f"user_{current_user.id}_{file.filename}"
    file_path = os.path.join(upload_dir, filename)

    # حفظ الملف
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # تحديث قاعدة البيانات
    auth_service = AuthService(db)
    user = auth_service.get_user_by_id(current_user.id)
    user.profile_picture = file_path.replace("\\", "/")  # مسار متوافق مع URL
    db.commit()

    # إرجاع رابط الصورة (يمكنك تعديله حسب إعدادات السيرفر)
    url = f"/static/profile_pictures/{filename}"
    return {"url": url} 