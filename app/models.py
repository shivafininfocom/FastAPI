from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Date, JSON, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from datetime import datetime
import random


#----------------------------------------------
#Department
#----------------------------------------------


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    userid = Column(Integer, default=7)
    department_name = Column(String(100))
    created_date = Column(DateTime(timezone=True), server_default=func.now())

    status = Column(String(10), default="active")
    deleted_by_user = Column(Integer, default=None, nullable=True)  # Can reference another user ID
    deleted_at = Column(DateTime, default=None, nullable=True)




#---------------------------------------------
#UserManagement
#----------------------------------------------


class UserManagement(Base):
    __tablename__ = "user_management"

    userid = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)
    emailid = Column(String(100), unique=True, nullable=False)
    departmentname = Column(String(100), nullable=True)
    password = Column(String(255), nullable=False)  # Store hashed passwords
    mobilenumber = Column(String(15), nullable=True)
    created_date = Column(DateTime, default=datetime.now(), nullable=True)

    status = Column(String(10), default="active")
    deleted_by_user = Column(Integer, default=None, nullable=True)  # Can reference another user ID
    deleted_at = Column(DateTime, default=None, nullable=True)

    # Relationship with Permission model
    permissions = relationship("Permission", back_populates="user")



# Permission model
class Permission(Base):
    __tablename__ = "permission"

    id = Column(Integer, primary_key=True, index=True)
    userid = Column(Integer, ForeignKey("user_management.userid"), nullable=False)
    username = Column(String(100), nullable=False)

    dashboard_view = Column(Boolean, default=False)
    dashboard_create = Column(Boolean, default=False)
    dashboard_update = Column(Boolean, default=False)
    dashboard_delete = Column(Boolean, default=False)
    dashboard_download = Column(Boolean, default=False)

    notification_view = Column(Boolean, default=False)
    notification_create = Column(Boolean, default=False)
    notification_update = Column(Boolean, default=False)
    notification_delete = Column(Boolean, default=False)
    notification_download = Column(Boolean, default=False)

    banner_view = Column(Boolean, default=False)
    banner_create = Column(Boolean, default=False)
    banner_update = Column(Boolean, default=False)
    banner_delete = Column(Boolean, default=False)
    banner_download = Column(Boolean, default=False)

    reports_view = Column(Boolean, default=False)
    reports_create = Column(Boolean, default=False)
    reports_update = Column(Boolean, default=False)
    reports_delete = Column(Boolean, default=False)
    reports_download = Column(Boolean, default=False)

    logs_view = Column(Boolean, default=False)
    logs_create = Column(Boolean, default=False)
    logs_update = Column(Boolean, default=False)
    logs_delete = Column(Boolean, default=False)
    logs_download = Column(Boolean, default=False)

    usermanagement_view = Column(Boolean, default=False)
    usermanagement_create = Column(Boolean, default=False)
    usermanagement_update = Column(Boolean, default=False)
    usermanagement_delete = Column(Boolean, default=False)
    usermanagement_download = Column(Boolean, default=False)

    # Relationship back to UserManagement
    user = relationship("UserManagement", back_populates="permissions")

    
    
#---------------------------------------
#Banner
#---------------------------------------

class Banner(Base):
    __tablename__ = "banners"

    id = Column(Integer, primary_key=True, index=True)
    userid = Column(Integer)
    banner_name = Column(String(255), nullable=False)
    banner_type = Column(String(50), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    created_date = Column(DateTime, default=datetime.now())
    banner_meta_title = Column(JSON, default=list)
    images = Column(JSON, nullable=True, default=None)
    youtube_link = Column(JSON, default=list, nullable=True)


    status = Column(String(10), default="active")
    deleted_by_user = Column(Integer, default=None, nullable=True)  # Can reference another user ID
    deleted_at = Column(DateTime, default=None, nullable=True)


#--------------------------------------------------------------------
#Report
#--------------------------------------------------------------------


def get_random_val():
    letters_and_nums = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 
                        1, 2, 3, 4, 5, 6, 7, 8, 9, 'A', 'B', 'C', 
                        'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']
    return ''.join(str(random.choice(letters_and_nums)) for _ in range(18))

def getrandomreference():
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N']
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    lettersRes = ''.join(random.choice(letters) for _ in range(3))
    nums = ''.join(str(random.choice(numbers)) for _ in range(5))
    return lettersRes + nums

def get_random_num():
    nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    return ''.join(str(random.choice(nums)) for _ in range(6))

class Report(Base):
    __tablename__ = 'reports'  # Table name in the database

    TRANSACTION_STATUS_CHOICES = {
        'success': 'Success',
        'failed': 'Failed'
    }

    id = Column(Integer, primary_key=True, index=True)
    userid = Column(Integer, default=7)
    name = Column(String(100))
    phone_number = Column(String(12))
    order_id = Column(String(100), default=get_random_val)
    billdesk_reference_id = Column(String(100), default=getrandomreference)
    billdesk_transaction_id = Column(String(100), default=get_random_num)
    transaction_amount = Column(String(1000))
    transaction_date = Column(DateTime, default=datetime.now())
    transaction_status = Column(String(100), default='success', nullable=False)


#--------------------------------------------------------------------
#Notification
#--------------------------------------------------------------------

class Notification(Base):
    __tablename__ = "notification"

    id = Column(Integer, primary_key=True, index=True)
    userid = Column(Integer)
    created_date = Column(DateTime, default=datetime.now())
    notification_title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)

    status = Column(String(10), default="active")
    deleted_by_user = Column(Integer, default=None, nullable=True)  # Can reference another user ID
    deleted_at = Column(DateTime, default=None, nullable=True)



class OTPValidation(Base):
    __tablename__ = "otp_validation"

    id = Column(Integer, primary_key=True, index=True)
    mobile_number = Column(String(15), unique=True, nullable=False)
    otp = Column(String(6), nullable=False)
    generated_at = Column(DateTime, default=datetime.now())

    def __repr__(self):
        return f"<OTPValidation(mobile_number={self.mobile_number}, otp={self.otp}, timestamp={self.timestamp})>"
 

#------------------------------------------
#Content Management
#------------------------------------------
    
class ContentManagement(Base):
    __tablename__ = "content_management"

    id = Column(Integer, primary_key=True, index=True)
    userid = Column(Integer, nullable=False)
    content_title = Column(String(255), nullable=False)
    content_description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    image = Column(String(200), nullable=False)

    status = Column(String(10), default="active")
    deleted_by_user = Column(Integer, default=None, nullable=True)  # Can reference another user ID
    deleted_at = Column(DateTime, default=None, nullable=True)


