from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


#-----------------------------------------
#Login schema
#-----------------------------------------
class LoginRequest(BaseModel):
    email: str
    password: str


#-----------------------------------------
#Reset password schema
#-----------------------------------------

class PasswordResetRequest(BaseModel):
    email: str

class PasswordReset(BaseModel):
    token: str
    new_password: str



# Schema for creating a new department
class DepartmentCreate(BaseModel):
    userid: int
    department_name: str

# Schema for updating an existing department
class DepartmentUpdate(BaseModel):
    userid: int
    department_name: str

# Schema for the department response
class DepartmentResponse(BaseModel):
    id: int
    userid: int
    department_name: str
    created_date: datetime

    class Config:
        from_attributes = True


class DepartmentUserId(BaseModel):
    userid: int


#--------------------------------------------
#UserManagement schema
#--------------------------------------------

class UserManagementBase(BaseModel):
    username: str
    emailid: str
    departmentname: Optional[str] = None
    password: str
    mobilenumber: Optional[str] = None 


class UserManagementResponse(BaseModel):
    username: str
    emailid: str
    departmentname: str
    mobilenumber: str
    userid: int

class PermissionActions(BaseModel):
    view: bool
    create: bool
    update: bool
    delete: bool
    download: bool


class Permissions(BaseModel):
    userid: int
    username: str
    dashboard: PermissionActions
    notification: PermissionActions
    banner: PermissionActions
    reports: PermissionActions
    logs: PermissionActions
    usermanagement: PermissionActions

class PermissionBaseResponse(BaseModel):

    userid: int
    username: str
    dashboard_view: bool
    dashboard_create: bool 
    dashboard_update: bool 
    dashboard_delete: bool 
    dashboard_download: bool 

    notification_view: bool 
    notification_create: bool 
    notification_update: bool 
    notification_delete: bool 
    notification_download: bool

    banner_view: bool 
    banner_create: bool 
    banner_update: bool 
    banner_delete: bool
    banner_download: bool

    reports_view: bool
    reports_create: bool
    reports_update: bool
    reports_delete: bool
    reports_download: bool

    logs_view: bool
    logs_create: bool
    logs_update: bool
    logs_delete: bool
    logs_download: bool

    usermanagement_view: bool 
    usermanagement_create: bool
    usermanagement_update: bool
    usermanagement_delete: bool
    usermanagement_download: bool

class UserPermissions(BaseModel):
    data: UserManagementBase
    permissions : dict

class UserManagementPermissionsResponse(BaseModel):
    users: List[UserManagementResponse]
    permissions: List[PermissionBaseResponse]


class UserPermissionsItemResponse(BaseModel):
    user: UserManagementResponse
    permissions: PermissionBaseResponse

class UserPermissionsUserId(BaseModel):
    userid: int


#---------------------------------------
class OTPRequest(BaseModel):
    mobile_number: str



class DeleteBannerRequest(BaseModel):
    userid: int

#--------------------------------------
#CMS
#--------------------------------------

class ContentManagementBase(BaseModel):
    userid: int
    content_title: str
    content_description: str
    image: dict

class ContentManagementCreate(ContentManagementBase):
    pass

class ContentManagementResponse(ContentManagementBase):
    created_at: datetime
    id: int
    image: str
    status: str

    class Config:
        form_attributes = True

class ContentManagementUpdate(ContentManagementBase):
    pass

class ContentManagementResponseUpdated(ContentManagementBase):
    created_at: datetime
    id: int

    class Config:
        form_attributes = True


#--------------------------------------
#Notification schemas
#--------------------------------------

class NotificationBase(BaseModel):
    notification_title: str
    description: str


class NotificationCreate(NotificationBase):
    userid: int

class NotificationResponse(NotificationCreate):
    created_date: datetime
    id: int

class NotificationItem(BaseModel):
    notification_title: str
    description: str
    userid: int
    created_date: datetime

class NotificationUserId(BaseModel):
    userid: int


#--------------------------------------
#Banner schemas
#--------------------------------------

class BannerBase(BaseModel):
    banner_name: str
    banner_type: str
    start_date: datetime
    end_date: datetime
    banner_meta_title: list 
    youtube_link: list
    images: list

class BannerCreate(BannerBase):
    userid: int


class BannerResponse(BaseModel):
    banner_name: str
    banner_type: str
    start_date: datetime
    end_date: datetime
    banner_meta_title: list 
    youtube_link: list
    images: list
    userid: int
    id:int

class BannerItemResponse(BannerResponse):
    pass