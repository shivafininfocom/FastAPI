from datetime import datetime
from fastapi import Body, Depends, APIRouter, HTTPException, Request, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Permission, UserManagement
from app.schemas import UserPermissions
from app.Endpoints.token_handler import hash_password
from app.Endpoints.token_handler import get_current_user


router_userpermissions = APIRouter()


@router_userpermissions.post("/createuserspermissions/")
async def create_user_with_permissions( user_permissions: UserPermissions, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    try:
        user_data = user_permissions.data
        permission_data = user_permissions.permissions

        user_data.password = hash_password(user_permissions.data.password)
        new_user = UserManagement(**user_data.model_dump())

        db.add(new_user)
        db.commit()
        db.refresh(new_user)  

        new_permission = Permission(userid=new_user.userid, username=new_user.username)

        # Map permissions from `permission_data` to the Permission model dynamically
        for section, actions in permission_data.items():
            for action, value in actions.items():
                field_name = f"{section}_{action}"
                if hasattr(new_permission, field_name):
                    setattr(new_permission, field_name, value)


        db.add(new_permission)
        db.commit()
        db.refresh(new_permission)

        return {"message": "User and permissions created successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router_userpermissions.get("/getalluserspermissions")
async def get_all_users_with_permissions(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):

    users = db.query(UserManagement).all()
    permissions = db.query(Permission).all()

    users_data = []
    for user in users:
        users_data.append({
            "userid": user.userid,
            "username": user.username,
            "emailid": user.emailid,
            "password": user.password,
            "departmentname": user.departmentname,
            "mobilenumber": user.mobilenumber,
            "created_date": user.created_date
        })

    permissions_data = []
    for perm in permissions:
        permissions_data.append({
            "userid": perm.userid,
            "username": perm.username,
            "dashboard_view": perm.dashboard_view,
            "dashboard_create": perm.dashboard_create,
            "dashboard_update": perm.dashboard_update,
            "dashboard_delete": perm.dashboard_delete,
            "dashboard_download": perm.dashboard_download,
            "notification_view": perm.notification_view,
            "notification_create": perm.notification_create,
            "notification_update": perm.notification_update,
            "notification_delete": perm.notification_delete,
            "notification_download": perm.notification_download,
            "banner_view": perm.banner_view,
            "banner_create": perm.banner_create,
            "banner_update": perm.banner_update,
            "banner_delete": perm.banner_delete,
            "banner_download": perm.banner_download,
            "reports_view": perm.reports_view,
            "reports_create": perm.reports_create,
            "reports_update": perm.reports_update,
            "reports_delete": perm.reports_delete,
            "reports_download": perm.reports_download,
            "logs_view": perm.logs_view,
            "logs_create": perm.logs_create,
            "logs_update": perm.logs_update,
            "logs_delete": perm.logs_delete,
            "logs_download": perm.logs_download,
            "usermanagement_view": perm.usermanagement_view,
            "usermanagement_create": perm.usermanagement_create,
            "usermanagement_update": perm.usermanagement_update,
            "usermanagement_delete": perm.usermanagement_delete,
            "usermanagement_download": perm.usermanagement_download
        })

    return {
        "users": users_data,
        "permissions": permissions_data
    }


@router_userpermissions.get("/userspermissions/{userid}")
async def get_user(userid: int, request: Request, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    try:

        user = db.query(UserManagement).filter(UserManagement.userid == userid).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        permission = db.query(Permission).filter(Permission.userid == userid).first()
        if not permission:
            raise HTTPException(status_code=404, detail="Permission not found")

        return {
            'user': {
                "userid": user.userid,
                "username": user.username,
                "emailid": user.emailid,
                "departmentname": user.departmentname,
                "mobilenumber": user.mobilenumber,
                "created_date": user.created_date
            },
            'permission': {
                "userid": permission.userid,
                "username": user.username,
                "dashboard_view": permission.dashboard_view,
                "dashboard_create": permission.dashboard_create,
                "dashboard_update": permission.dashboard_update,
                "dashboard_delete": permission.dashboard_delete,
                "dashboard_download": permission.dashboard_download,
                "notification_view": permission.notification_view,
                "notification_create": permission.notification_create,
                "notification_update": permission.notification_update,
                "notification_delete": permission.notification_delete,
                "notification_download": permission.notification_download,
                "banner_view": permission.banner_view,
                "banner_create": permission.banner_create,
                "banner_update": permission.banner_update,
                "banner_delete": permission.banner_delete,
                "banner_download": permission.banner_download,
                "reports_view": permission.reports_view,
                "reports_create": permission.reports_create,
                "reports_update": permission.reports_update,
                "reports_delete": permission.reports_delete,
                "reports_download": permission.reports_download,
                "logs_view": permission.logs_view,
                "logs_create": permission.logs_create,
                "logs_update": permission.logs_update,
                "logs_delete": permission.logs_delete,
                "logs_download": permission.logs_download,
                "usermanagement_view": permission.usermanagement_view,
                "usermanagement_create": permission.usermanagement_create,
                "usermanagement_update": permission.usermanagement_update,
                "usermanagement_delete": permission.usermanagement_delete,
                "usermanagement_download": permission.usermanagement_download
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {str(e)}")


@router_userpermissions.patch("/updateuserpermission/{userid}")
async def update_user_permissions(userid: int, request: Request, db: Session = Depends(get_db), data: dict = Body(...), current_user: str = Depends(get_current_user)):

    try:
        user = db.query(UserManagement).filter(UserManagement.userid == userid).first()

        if not user:
                raise HTTPException(status_code=404, detail="User not found")
        
        permission = db.query(Permission).filter(Permission.userid == userid).first()

        if not permission:
                raise HTTPException(status_code=404, detail="Permission not found")
        

        user_data = data.get("user")
        user.username = user_data.get("username")
        user.emailid = user_data.get("emailid")
        user.departmentname = user_data.get("departmentname")
        user.mobilenumber = user_data.get("mobilenumber")

        permission_data = data.get("permission")
        permission.dashboard_view = permission_data.get("dashboard_view")
        permission.dashboard_create = permission_data.get("dashboard_create")
        permission.dashboard_update = permission_data.get("dashboard_update")
        permission.dashboard_delete = permission_data.get("dashboard_delete")
        permission.dashboard_download = permission_data.get("dashboard_download")
        permission.notification_view = permission_data.get("notification_view")
        permission.notification_create = permission_data.get("notification_create")
        permission.notification_update = permission_data.get("notification_update")
        permission.notification_delete = permission_data.get("notification_delete")
        permission.notification_download = permission_data.get("notification_download")
        permission.banner_view = permission_data.get("banner_view")
        permission.banner_create = permission_data.get("banner_create")
        permission.banner_update = permission_data.get("banner_update")
        permission.banner_delete = permission_data.get("banner_delete")
        permission.banner_download = permission_data.get("banner_download")
        permission.reports_view = permission_data.get("reports_view")
        permission.reports_create = permission_data.get("reports_create")
        permission.reports_update = permission_data.get("reports_update")
        permission.reports_delete = permission_data.get("reports_delete")
        permission.reports_download = permission_data.get("reports_download")
        permission.logs_view = permission_data.get("logs_view")
        permission.logs_create = permission_data.get("logs_create")
        permission.logs_update = permission_data.get("logs_update")
        permission.logs_delete = permission_data.get("logs_delete")
        permission.logs_download = permission_data.get("logs_download")
        permission.usermanagement_view = permission_data.get("usermanagement_view")
        permission.usermanagement_create = permission_data.get("usermanagement_create")
        permission.usermanagement_update = permission_data.get("usermanagement_update")
        permission.usermanagement_delete = permission_data.get("usermanagement_delete")
        permission.usermanagement_download = permission_data.get("usermanagement_download")

        db.commit()

        return {
                "user": {
                    "userid": user.userid,
                    "username": user.username,
                    "emailid": user.emailid,
                    "departmentname": user.departmentname,
                    "mobilenumber": user.mobilenumber,
                    "created_date": user.created_date
                },
                "permission": {
                    "userid": permission.userid,
                    "username": permission.username,
                    "dashboard_view": permission.dashboard_view,
                    "dashboard_create": permission.dashboard_create,
                    "dashboard_update": permission.dashboard_update,
                    "dashboard_delete": permission.dashboard_delete,
                    "dashboard_download": permission.dashboard_download,
                    "notification_view": permission.notification_view,
                    "notification_create": permission.notification_create,
                    "notification_update": permission.notification_update,
                    "notification_delete": permission.notification_delete,
                    "notification_download": permission.notification_download,
                    "banner_view": permission.banner_view,
                    "banner_create": permission.banner_create,
                    "banner_update": permission.banner_update,
                    "banner_delete": permission.banner_delete,
                    "banner_download": permission.banner_download,
                    "reports_view": permission.reports_view,
                    "reports_create": permission.reports_create,
                    "reports_update": permission.reports_update,
                    "reports_delete": permission.reports_delete,
                    "reports_download": permission.reports_download,
                    "logs_view": permission.logs_view,
                    "logs_create": permission.logs_create,
                    "logs_update": permission.logs_update,
                    "logs_delete": permission.logs_delete,
                    "logs_download": permission.logs_download,
                    "usermanagement_view": permission.usermanagement_view,
                    "usermanagement_create": permission.usermanagement_create,
                    "usermanagement_update": permission.usermanagement_update,
                    "usermanagement_delete": permission.usermanagement_delete,
                    "usermanagement_download": permission.usermanagement_download
                }
            }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error {str(e)}")


@router_userpermissions.patch("/deleteuserpermission/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db),  current_user: str = Depends(get_current_user)):
    try:
        user = db.query(UserManagement).filter(UserManagement.userid == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        permission = db.query(Permission).filter(Permission.userid == user_id).first()
        if permission is None:
            raise HTTPException(status_code=404, detail="Permission not found for this user")

        user.status = "inactive"
        user.deleted_by_user = 4
        user.deleted_at = datetime.now()
        # db.delete(user)
        # db.delete(permission)
        db.commit()

        return {"message": "User and related permissions deleted successfully."}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

