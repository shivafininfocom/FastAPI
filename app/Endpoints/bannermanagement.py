import base64, os
from fastapi import APIRouter
from datetime import datetime
from fastapi import Depends, APIRouter, HTTPException, Request, status, FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Banner
from app.schemas import BannerCreate, DeleteBannerRequest
from app.Endpoints.token_handler import get_current_user


router_banner = APIRouter()

app = FastAPI()



@router_banner.post("/banner/banners/")
async def upload_banner_data(request: Request, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    try:
        form_data = await request.json()
        banner_name = form_data.get("banner_name")
        banner_type = form_data.get("banner_type")
        start_date = form_data.get("start_date")
        end_date = form_data.get("end_date")
        userid = form_data.get("userid")
        banner_meta_title = form_data.get("banner_meta_title", [])
        youtube_link = form_data.get("youtube_links", [])
        files = form_data.get("files", [])

        image_urls = []

        def save_base64_image(base64_content: str, filename: str) -> str:
        
            unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}_{filename}"
            image_path = os.path.join("D:/shivat/FastAPI/app/images/", unique_filename)

            with open(image_path, "wb") as f:
                f.write(base64.b64decode(base64_content))

            return f"http://localhost:8000/images/{unique_filename}"

        for file in files:
            filename = file["name"]
            base64_content = file["content"]
            image_url = save_base64_image(base64_content, filename)
            image_urls.append(image_url)

        banner = Banner(
            userid=userid,
            banner_name=banner_name,
            banner_type=banner_type,
            start_date=start_date,
            end_date=end_date,
            banner_meta_title=banner_meta_title,
            youtube_link=youtube_link,
            images=image_urls
        )

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




@router_banner.get("/banner/banners/", status_code=status.HTTP_200_OK)
async def get_all_banners(request:Request, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    try:
        banners = db.query(Banner).all()
        if not banners:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No banners found.")
        
        base_url = "http://localhost:8000/images"  # Base URL for serving images
        banners_data = []

        for banner in banners:
            banner_info = {
                "id": banner.id,
                "userid": banner.userid,
                # Generate URLs for images stored in the IMAGES_FOLDER
                "images": [f"{base_url}/{os.path.basename(image)}" for image in banner.images],
                "banner_name": banner.banner_name,
                "banner_type": banner.banner_type,
                "start_date": banner.start_date.isoformat() if banner.start_date else None,
                "end_date": banner.end_date.isoformat() if banner.end_date else None,
                "banner_meta_title": banner.banner_meta_title,
                "youtube_link": banner.youtube_link
            }
            banners_data.append(banner_info)

        return JSONResponse(content=banners_data, status_code=status.HTTP_200_OK)

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error {str(e)}")



@router_banner.get("/banner/{banner_id}", status_code=status.HTTP_200_OK)
async def get_banner_by_id(banner_id: int, request: Request, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):

    banner = db.query(Banner).filter(Banner.id == banner_id).first()
    if not banner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Banner not found.")

    image_urls = [str(request.url_for('images', path=img)) for img in banner.images]

    banner_data = {
        'id': banner.id,
        'banner_name': banner.banner_name,
        'banner_type': banner.banner_type,
        'start_date': banner.start_date.isoformat() if banner.start_date else None,
        'end_date': banner.end_date.isoformat() if banner.end_date else None,
        'banner_meta_title': banner.banner_meta_title,
        'youtube_link':banner.youtube_link,
        'images': image_urls
    }

    return JSONResponse(content=banner_data)



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

        #print(banner.banner_meta_title, banner.banner_name, banner.created_date)

        form_data = await request.json()
        banner_name = form_data.get("banner_name")
        banner_type = form_data.get("banner_type")
        start_date = form_data.get("start_date")
        end_date = form_data.get("end_date")
        userid = form_data.get("userid")
        banner_meta_titles = form_data.get("banner_meta_title", [])
        youtube_links = form_data.get("youtube_links", [])
        files = form_data.get("files", [])

        image_urls = []
        

        def save_base64_image(base64_content: str, filename: str) -> str:

            unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}_{filename}"
            image_path = os.path.join("D:/shivat/FastAPI/app/images/", unique_filename)

            with open(image_path, "wb") as f:
                f.write(base64.b64decode(base64_content))

            return f"http://localhost:8000/images/{unique_filename}"

        for file in files:
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

        return {
            "id": banner.id,
            "banner_name": banner.banner_name,
            "banner_type": banner.banner_type,
            "start_date": banner.start_date.isoformat() if banner.start_date else None,
            "end_date": banner.end_date.isoformat() if banner.end_date else None,
            "banner_meta_title": banner.banner_meta_title,
            "youtube_link": banner.youtube_link,
            "images": banner.images
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error {str(e)}")


@router_banner.patch("/bannerdelete/{banner_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_banner(banner_id: int, request: DeleteBannerRequest, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    try:
        banner = db.query(Banner).filter(Banner.id == banner_id).first()
        if not banner:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Banner not found.")

        banner.status = "inactive"
        banner.deleted_by_user = int(request.userid)
        banner.deleted_at = datetime.now()

        #db.delete(banner)
        db.commit()

        return {"detail": "Banner deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {str(e)}")

