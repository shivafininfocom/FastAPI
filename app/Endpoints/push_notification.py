from fastapi import APIRouter, Depends, HTTPException, status
import firebase_admin
from firebase_admin import messaging, credentials
from sqlalchemy.orm import Session
from app.Endpoints.auth_user import send_otp_email
from app.Endpoints.token_handler import get_current_user
from app.database import get_db
from app.schemas import NotificationData, OTPRequestNotification
import random
from app.models import Notification

# Initialize Firebase Admin SDK
cred = credentials.Certificate("D:/shivat/FastAPI/flutter_notifications.json")
firebase_admin.initialize_app(cred)

push_notification_router = APIRouter()


@push_notification_router.patch("/sendotp/")
async def get_otp(otp_request: OTPRequestNotification,  db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):

    try:

        otp = str(random.randint(100000, 999999))
        notification_user = db.query(Notification).filter(Notification.userid == otp_request.userid).first()

        if not notification_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        send_otp_email(otp_request.email_id, otp)

        notification_user.otp_push_notification = otp
        db.commit()

        return {"message":"success"}
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")




@push_notification_router.post("/sendnotification/")
async def send_notification(notification_data: NotificationData, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):

    try:

        notification_user = db.query(Notification).filter(Notification.userid == notification_data.userid).first()

        if notification_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        if(notification_user.otp_push_notification == notification_data.request_otp):
            try:
                # Create the notification message
                message = messaging.Message(
                    notification=messaging.Notification(
                        title=notification_data.notification_title,
                        body=notification_data.notification_description
                    ),
                    topic="all"
                )
                # Send the notification
                response = messaging.send(message)

                return {"message": "success"}

            except Exception as e:
                return {"error": str(e)}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error processing data: {str(e)}")

