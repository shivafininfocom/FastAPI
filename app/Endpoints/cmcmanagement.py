import base64
from datetime import datetime
import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import ContentManagement
from app.Endpoints.token_handler import get_current_user
from app.schemas import ContentManagementCreate, ContentManagementResponse, ContentManagementResponseUpdated, ContentManagementUpdate



router_content = APIRouter()


@router_content.post("/content/create")
async def create_content(content: ContentManagementCreate, db:Session = Depends(get_db),  current_user: str = Depends(get_current_user)):

    try:
        image_name = content.image["name"]
        base64_image = content.image["content"]
        
        image_data = base64.b64decode(base64_image)

        folder_path = "D:/shivat/FastAPI/app/banner_images"

        image_path = os.path.join(folder_path, image_name)
        
        with open(image_path, "wb") as file:
            file.write(image_data)

        image_url = f"http://localhost:8000/banner_images/{image_name}"

        content.image = image_url

        content_banner = ContentManagement(**content.model_dump())
        
        db.add(content_banner)
        db.commit()
        db.refresh(content_banner)
        return content_banner
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Something went wrong {str(e)}")
    

@router_content.get("/contents",  response_model=list[ContentManagementResponse])
async def get_all_content(db:Session = Depends(get_db),  current_user: str = Depends(get_current_user)):
    try:
        content_list = db.query(ContentManagement).all()

        if not content_list:
            raise HTTPException(status_code=404, detail="Bad request, Content does not found")

        return content_list

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {str(e)}")


@router_content.put("/contentUpdate/{contentid}", response_model=ContentManagementResponseUpdated)
def update_content(contentid:int, content_update: ContentManagementUpdate, db:Session = Depends(get_db),  current_user: str = Depends(get_current_user)):
    try:
        
        content = db.query(ContentManagement).filter(ContentManagement.id == contentid).first()

        if not content:
            raise HTTPException(status_code=404, detail="Bad request, Content not found")

        image_name = content_update.image["name"]
        base64_image = content_update.image["content"]
        
        image_data = base64.b64decode(base64_image)

        folder_path = "D:/shivat/FastAPI/app/banner_images"

        image_path = os.path.join(folder_path, image_name)
        
        with open(image_path, "wb") as file:
            file.write(image_data)

        image_url = f"http://localhost:8000/banner_images/{image_name}"

        content.image = image_url

        content.content_title = content_update.content_title
        content.content_description = content_update.content_description
        content.userid = content_update.userid
        
        db.commit()
        db.refresh(content)

        return content
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error {str(e)}")


@router_content.get("/content/{contentid}", response_model=ContentManagementResponse)
async def get_content_id(contentid:int, db: Session = Depends(get_db),  current_user: str = Depends(get_current_user)):
    try:
        content = db.query(ContentManagement).filter(ContentManagement.id == contentid).first()

        if not content:
            raise HTTPException(status_code=400, detail="Bad request, content does not found")
    
        return content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {str(e)}")


@router_content.patch("/contentRemove/{contentid}")
async def remove_content(contentid: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    try:
        content = db.query(ContentManagement).filter(ContentManagement.id == contentid).first()

        if not content:
            raise HTTPException(status_code=404, detail="Bad Request, Content does not found")

        content.status = "inactive"
        content.deleted_by_user = contentid
        content.deleted_at = datetime.now()

        db.commit()
        db.refresh(content)

        return {"message": "Content has deleted successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error {str(e)}")


