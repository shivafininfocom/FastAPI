import base64, os
from fastapi import APIRouter
from datetime import datetime
from fastapi import Depends, APIRouter, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Banner
from app.schemas import BannerCreate, DeleteBannerRequest, BannerResponse, BannerItemResponse
from app.Endpoints.token_handler import get_current_user


router_banner = APIRouter()



@router_banner.post("/upload/banner/", status_code=status.HTTP_201_CREATED)
async def upload_banner_data(banner_request: BannerCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    try:

        image_urls = []

        def save_base64_image(base64_content: str, filename: str) -> str:
        
            unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}_{filename}"
            image_path = os.path.join("D:/shivat/FastAPI/app/images/", unique_filename)

            with open(image_path, "wb") as f:
                f.write(base64.b64decode(base64_content))

            return f"http://localhost:8000/images/{unique_filename}"

        for file in banner_request.images:
            filename = file["name"]
            base64_content = file["content"]
            image_url = save_base64_image(base64_content, filename)
            image_urls.append(image_url)

        banner_request.images = image_urls

        banner = Banner(**banner_request.model_dump())

        db.add(banner)
        db.commit()
        db.refresh(banner)

        return JSONResponse(
            content={
                "message": "Banner data saved successfully!"
            }
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error processing banner data: {str(e)}")




@router_banner.get("/banners/", status_code=status.HTTP_200_OK, response_model=list[BannerResponse])
async def get_all_banners(request:Request, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    try:
        banners = db.query(Banner).filter(Banner.status == 'active').all()
        if not banners:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No banners found.")

        return banners

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error {str(e)}")



@router_banner.get("/banner/{banner_id}", status_code=status.HTTP_200_OK, response_model=BannerItemResponse)
async def get_banner_by_id(banner_id: int, request: Request, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):

    try:

        banner = db.query(Banner).filter(Banner.id == banner_id, Banner.status == 'active').first()
        if not banner:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Banner not found.")

        return banner
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{str(e)}")



@router_banner.put("/updatebanner/{banner_id}", status_code=status.HTTP_200_OK)
async def update_banner(
    banner_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    try:
        banner = db.query(Banner).filter(Banner.id == banner_id).first()
        if not banner:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Banner not found.")

        form_data = await request.json()
        banner_name = form_data.get("banner_name")
        banner_type = form_data.get("banner_type")
        start_date = form_data.get("start_date")
        end_date = form_data.get("end_date")
        userid = form_data.get("userid")
        banner_meta_titles = form_data.get("banner_meta_title", [])
        youtube_links = form_data.get("youtube_links", [])
        images = form_data.get("images", [])

        image_urls = []
        

        def save_base64_image(base64_content: str, filename: str) -> str:

            unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}_{filename}"
            image_path = os.path.join("D:/shivat/FastAPI/app/images/", unique_filename)

            with open(image_path, "wb") as f:
                f.write(base64.b64decode(base64_content))

            return f"http://localhost:8000/images/{unique_filename}"

        for file in images:
            filename = file["name"]
            base64_content = file["content"]
            image_url = save_base64_image(base64_content, filename)
            image_urls.append(image_url)

        
        banner.banner_name = banner_name
        banner.banner_type = banner_type
        banner.start_date = start_date
        banner.end_date = end_date
        banner.userid = userid
        banner.banner_meta_title = banner_meta_titles
        banner.youtube_link = youtube_links
        banner.images = image_urls

        db.commit()
        db.refresh(banner)

        return {"message": "Banner data updated successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error {str(e)}")


@router_banner.patch("/bannerdelete/{banner_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_banner(banner_id: int, banner_request: DeleteBannerRequest, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    try:
        banner = db.query(Banner).filter(Banner.id == banner_id).first()
        if not banner:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Banner not found.")

        banner.status = "inactive"
        banner.deleted_by_user = int(banner_request.userid)
        banner.deleted_at = datetime.now()

        db.commit()

        return {"detail": "Banner deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {str(e)}")

