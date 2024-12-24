import random
import smtplib
from email.mime.text import MIMEText
from jinja2 import Template
from app.Endpoints.token_handler import hash_password
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.Endpoints.token_handler import create_access_token, verify_password
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_db
from app.models import UserManagement
from app.schemas import LogoutUser, OTPRequest, PasswordRequest
from app.Endpoints.token_handler import pwd_context


router_login = APIRouter()


@router_login.patch("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        user = db.query(UserManagement).filter(UserManagement.emailid == form_data.username).first()

        if not user or not verify_password(form_data.password, user.password):
            return JSONResponse(content={"message":"username and password does not match"})

        token = create_access_token({"userid": user.userid})
        user.access_token = token

        db.commit()

        return {"access_token": token, "token_type": "bearer", "userid": user.userid}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error {str(e)}")


@router_login.patch("/userlogout/")
async def user_logout(logout_data: LogoutUser, db: Session = Depends(get_db)):

    try:

        logout_user = db.query(UserManagement).filter(UserManagement.userid == logout_data.userid, UserManagement.access_token == logout_data.access_token).first()

        if not logout_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token and user")
        
        logout_user.access_token = None
        db.commit()

        return {"message": "success"}
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


def generate_otp():
    return str(random.randint(100000, 999999))

@router_login.patch("/requestotp/")
def request_password_reset(request: OTPRequest, db: Session = Depends(get_db)):

    user = db.query(UserManagement).filter(UserManagement.emailid == request.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    gen_otp = generate_otp()
    send_otp_email(user.emailid, gen_otp)

    user.otp = gen_otp
    db.commit()

    return {"message": "success"}


@router_login.patch("/changepassword/")
async def change_user_password(request_data: PasswordRequest ,db: Session = Depends(get_db)):
    try:
        user_data = db.query(UserManagement).filter(UserManagement.emailid == request_data.email).first()

        if(user_data.otp == request_data.otp):
            user_data.password = hash_password(request_data.reset_password)
            db.commit()
        else:
            return {"message":"Invalid otp"}

        return {"message": "success"}
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


def send_otp_email(to_email_address, otp):

    template = """
    <html>
    <body style="display:flex; align-items:center; justify-content:center;">
        <div style="border: 1px solid black; padding: 12px; text-align:center">
            <h1 style="text-align: center">OTP</h1>
            <h2>{{ otp }}</h2>
            <h3>Please never share this OTP with anyone</h3>
            <p>Use this OTP to reset your password</p>
        </div>
    </body>
    </html>
    """

    html_content = Template(template).render(otp=otp)

    message = MIMEText(html_content, "html")
    message["From"] = "shiva@fininfocom.com"
    message["To"] = to_email_address
    message["Subject"] = "Your OTP Code"

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login("shiva@fininfocom.com", "wutb zjtz bfct ethg")  # app password
            server.sendmail("shiva@fininfocom.com", to_email_address, message.as_string())
            print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# send_otp_email("shivashivam17@gmail.com", "123456")
