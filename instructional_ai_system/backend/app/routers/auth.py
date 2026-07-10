from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
import os
from .. import schemas, models, database, auth
from ..dependencies import get_db, get_current_user

router = APIRouter()

@router.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    normalized_email = user.email.strip().lower()
    db_user = db.query(models.User).filter(models.User.email == normalized_email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(name=user.name.strip(), email=normalized_email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    normalized_email = form_data.username.strip().lower()
    user = db.query(models.User).filter(models.User.email == normalized_email).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email, "user_id": user.id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user

from ..services.email import send_password_reset_email

@router.post("/forgot-password")
async def forgot_password(request: Request, payload: schemas.ForgotPasswordRequest, db: Session = Depends(get_db)):
    normalized_email = payload.email.strip().lower()
    user = db.query(models.User).filter(models.User.email == normalized_email).first()
    if not user:
        # We return success even if user not found for security reasons
        return {"message": "If this email is registered, a reset link has been sent."}
    
    # Create a short-lived reset token (15 mins)
    reset_token = auth.create_access_token(
        data={"sub": user.email, "purpose": "password_reset"}, 
        expires_delta=timedelta(minutes=15)
    )
    
    frontend_url = os.getenv("FRONTEND_URL", "").strip().rstrip("/")
    if not frontend_url:
        origin = request.headers.get("origin", "").strip().rstrip("/")
        frontend_url = origin or "http://localhost:5173"
    reset_link = f"{frontend_url}/reset-password?token={reset_token}"
    
    # Send actual email (background task or await)
    try:
        await send_password_reset_email(user.email, reset_link)
        return {"message": "Password reset link has been sent to your email."}
    except Exception as e:
        # Fallback to local log if mail fails during setup
        print(f"\n[EMAIL FAILED] Reset link for {user.email}: {reset_link}\nError: {e}")
        return {"message": "If this email is registered, a reset link has been sent."}

@router.post("/reset-password")
def reset_password(request: schemas.ResetPasswordRequest, db: Session = Depends(get_db)):
    try:
        from jose import jwt
        payload = jwt.decode(request.token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        email: str = payload.get("sub")
        purpose: str = payload.get("purpose")
        
        if email is None or purpose != "password_reset":
            raise HTTPException(status_code=400, detail="Invalid reset token")
            
        user = db.query(models.User).filter(models.User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        user.hashed_password = auth.get_password_hash(request.new_password)
        db.commit()
        return {"message": "Password reset successful"}
        
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")

