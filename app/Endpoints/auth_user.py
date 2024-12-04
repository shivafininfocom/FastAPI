from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.Endpoints.token_handler import create_access_token, create_reset_token, verify_password, verify_reset_token
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_db
from app.models import UserManagement
from app.schemas import PasswordReset, PasswordResetRequest
from app.Endpoints.token_handler import pwd_context


router_login = APIRouter()



@router_login.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        user = db.query(UserManagement).filter(UserManagement.emailid == form_data.username).first()

        if not user or not verify_password(form_data.password, user.password):
            return JSONResponse(content={"message":"username and password does not match"})

        token = create_access_token({"userid": user.userid})
        return {"access_token": token, "token_type": "bearer", "userid": user.userid}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {str(e)}")


@router_login.post("/request-password-reset/")
def request_password_reset(request: PasswordResetRequest, db: Session = Depends(get_db)):
    user = db.query(UserManagement).filter(UserManagement.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    reset_token = create_reset_token(
        data={"sub": user.email}
    )
    return {"email": user.email, "token": reset_token}


@router_login.post("/reset-password/")
def reset_password(data: PasswordReset, db: Session = Depends(get_db)):
    email = verify_reset_token(data.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
    user = db.query(UserManagement).filter(UserManagement.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    hashed_password = pwd_context.hash(data.new_password)
    user.password = hashed_password
    db.commit()
    return {"message": "Password has been reset successfully"}