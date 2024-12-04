from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import List, Optional


#Schema for verifying username and password 
class LoginRequest(BaseModel):
    email: str
    password: str


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

class UserManagementBase(BaseModel):
    username: str
    emailid: str
    departmentname: Optional[str] = None
    password: str
    mobilenumber: Optional[str] = None 


class UserManagementResponse(BaseModel):
    username: str
    emailid: EmailStr
    departmentname: str
    mobilenumber: str  

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
    dashboard_view: bool = Field(default=False)
    dashboard_create: bool = Field(default=False)
    dashboard_update: bool = Field(default=False)
    dashboard_delete: bool = Field(default=False)
    dashboard_download: bool = Field(default=False)

    notification_view: bool = Field(default=False)
    notification_create: bool = Field(default=False)
    notification_update: bool = Field(default=False)
    notification_delete: bool = Field(default=False)
    notification_download: bool = Field(default=False)

    banner_view: bool = Field(default=False)
    banner_create: bool = Field(default=False)
    banner_update: bool = Field(default=False)
    banner_delete: bool = Field(default=False)
    banner_download: bool = Field(default=False)

    reports_view: bool = Field(default=False)
    reports_create: bool = Field(default=False)
    reports_update: bool = Field(default=False)
    reports_delete: bool = Field(default=False)
    reports_download: bool = Field(default=False)

    logs_view: bool = Field(default=False)
    logs_create: bool = Field(default=False)
    logs_update: bool = Field(default=False)
    logs_delete: bool = Field(default=False)
    logs_download: bool = Field(default=False)

    usermanagement_view: bool = Field(default=False)
    usermanagement_create: bool = Field(default=False)
    usermanagement_update: bool = Field(default=False)
    usermanagement_delete: bool = Field(default=False)
    usermanagement_download: bool = Field(default=False)

class UserPermissions(BaseModel):
    data: UserManagementBase
    permissions : dict

class UserManagementPermissionsResponse(BaseModel):
    user: UserManagementResponse
    permissions: PermissionBaseResponse


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
    files: list

class BannerCreate(BannerBase):
    userid: int
