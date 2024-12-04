from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.models import OTPValidation
from datetime import datetime
import random
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.database import get_db, Base, engine
from app.schemas import OTPRequest
from app.Endpoints.usermanagement import router_userpermissions
from app.Endpoints.bannermanagement import router_banner
from app.Endpoints.reports import router_report
from app.Endpoints.notifications import router_notification
from app.Endpoints.cmcmanagement import router_content
from app.Endpoints.department import router_department
from app.Endpoints.auth_user import router_login

app = FastAPI(title="Metro users management", description="API for users management")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)


# Create tables in the database
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)


BANNER_IMAGES = "D:/shivat/FastAPI/app/banner_images"

IMAGES_FOLDER = "D:/shivat/FastAPI/app/images/"

app.mount("/banner_images", StaticFiles(directory=BANNER_IMAGES), name="banner_images")

app.mount("/images", StaticFiles(directory=IMAGES_FOLDER), name="images")


app.include_router(router_userpermissions, tags=["Users and Permissions"])
app.include_router(router_banner, tags=["Banner management"])
app.include_router(router_report, tags=["Reports"]) 
app.include_router(router_notification, tags=["Notifications"])   
app.include_router(router_content, tags=["Content Management"])
app.include_router(router_department, tags=["Department"])
app.include_router(router_login, tags=["User authentication"])





#----------------------------------------
#App icons
#----------------------------------------


ICON_DIR = Path("D:/shivat/FastAPI/app/icons")
app.mount("/icons", StaticFiles(directory=ICON_DIR), name="icons")

@app.get("/appicons/")
async def get_all_icons():
    
    try:
        if not ICON_DIR.exists() or not ICON_DIR.is_dir():
            raise HTTPException(status_code=400, detail="Invalid directory path")

        svg_files = list(ICON_DIR.glob("*.svg"))

        if not svg_files:
            raise HTTPException(status_code=404, detail="No icons found")

        icon_urls = [f"/icons/{svg_file.name}" for svg_file in svg_files]

        return JSONResponse(content={"icons": icon_urls})
    
    except HTTPException as http_error:
        raise http_error
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {str(e)}")



def generate_otp():
    return str(random.randint(100000, 999999))


@app.post("/generate-otp/")
async def otp_mobile(request: OTPRequest, db: Session = Depends(get_db)):
    mobile_number = request.mobile_number
    otp = generate_otp()
    generated_at = datetime.now()

    try:
        existing_number = db.query(OTPValidation).filter(OTPValidation.mobile_number == mobile_number).first()
        if(existing_number):
            existing_number.otp = otp
            existing_number.generated_at = generated_at
        else:
            new_number = OTPValidation(mobile_number=mobile_number, otp=otp, generated_at = generated_at)
            db.add(new_number)

        db.commit()
        return {"message": "OTP generated successfully", "otp": otp,}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to generate OTP")



