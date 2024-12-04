from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.Endpoints.token_handler import create_access_token, verify_password
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_db
from app.models import UserManagement


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


