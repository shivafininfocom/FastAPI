from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Notification
from sqlalchemy.exc import NoResultFound
from app.Endpoints.token_handler import get_current_user
from app.schemas import NotificationCreate, NotificationItem, NotificationResponse, NotificationUserId



router_notification = APIRouter()


@router_notification.post("/notifications/")
async def create_notification(notification_data: NotificationCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    try:
        if(notification_data.userid):

            notification = Notification(**notification_data.model_dump())

            db.add(notification)
            db.commit()
            db.refresh(notification)

            return {"message": "Notification created successfully"}
        else:
            db.rollback()
            raise HTTPException(status_code=400, detail={"message": "Bad request"})
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail={"message": str(e)})


@router_notification.get("/notifications/", response_model=list[NotificationResponse])
async def read_notifications(db=Depends(get_db), current_user: str = Depends(get_current_user)):
    try:
        notifications = db.query(Notification).all()

        if notifications is None:
            return {"message": "There are no notifications"}

        return notifications
    
    except HTTPException:
        raise HTTPException(status_code=500, detail="somethong went wrong")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {str(e)}")




@router_notification.get("/notification/{notification_id}", response_model=NotificationItem)
async def get_notification_by_id(notification_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    try:
        notification = db.query(Notification).filter(Notification.id == notification_id).first()

        if not notification:
            raise HTTPException(status_code=404, detail="Bad request, notification not found")

        return notification
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router_notification.put("/notifications/{notification_id}/")
async def update_notification(notification_id: int, notification_data: NotificationCreate, db: Session = Depends(get_db),  current_user: str = Depends(get_current_user)):
    try:
        notification = db.query(Notification).filter(Notification.id == notification_id).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Notification not found")

    try:
        notification.userid = notification_data.userid
        notification.notification_title = notification_data.notification_title
        notification.description = notification_data.description

        db.commit()
        db.refresh(notification_data)

        return {"message": "Notification updated successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error f{str(e)}")


@router_notification.patch("/notifications/{notification_id}/")
async def delete_notification(notification_id: int, notification_userid: NotificationUserId, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    try:
        notification = db.query(Notification).filter(Notification.id == notification_id).first()
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")

        notification.status = "inactive"
        notification.deleted_by_user = notification_userid.userid
        notification.deleted_at = datetime.now()

        #db.delete(notification)
        db.commit()
        return {"message": f"Notification with ID {notification_id} deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error {str(e)}")

