from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Department
from app.schemas import DepartmentCreate, DepartmentResponse, DepartmentUpdate, DepartmentUserId



router_department = APIRouter()



@router_department.post("/departments/", response_model=DepartmentResponse)
def create_department_endpoint(department: DepartmentCreate, db: Session = Depends(get_db)):
    try:
        db_department = Department(**department.model_dump())

        db.add(db_department)
        db.commit()
        db.refresh(db_department)
        return db_department
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {str(e)}")


@router_department.get("/departments/{department_id}", response_model=DepartmentResponse)
def read_department(department_id: int, db: Session = Depends(get_db)):
    try:
        db_department = db.query(Department).filter(Department.id == department_id).first()

        if db_department is None:
            raise HTTPException(status_code=404, detail="Department not found")
        return db_department
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {str(e)}")


@router_department.get("/departments", response_model=List[DepartmentResponse])
def read_departments(db: Session = Depends(get_db)):
    try:
        departments = db.query(Department).all()
        if departments is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No departments are found")
        
        return departments
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {str(e)}")



@router_department.put("/departments/{department_id}", response_model=DepartmentResponse)
def update_department_endpoint(department_id: int, department: DepartmentUpdate, db: Session = Depends(get_db)):
    try:
        department = db.query(Department).filter(Department.id == department_id).first()
        if department:
            department.department_name = department.department_name
            department.userid = department.userid
            db.commit()
            db.refresh(department)
        
        if department is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No departments are found")

        return department

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {str(e)}")


@router_department.patch("/departments/{department_id}")
def delete_department_endpoint(request: DepartmentUserId, department_id: int, db: Session = Depends(get_db)):
    
    try:
        department = db.query(Department).filter(Department.id == department_id).first()
        print(department)
        if department:
            department.status = "InActive"
            department.deleted_by_user = request.userid
            department.deleted_at = datetime.now()
            db.commit()
        
        if department is None:
            raise HTTPException(status_code=404, detail="Department not found")
        
        return {"message": "Department deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {str(e)}")


