from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Request, status
from app.database import get_db
from app.models import Report
from app.Endpoints.token_handler import get_current_user




router_report = APIRouter()

@router_report.post("/reports/")
async def create_report(request: Request, db=Depends(get_db), current_user: str = Depends(get_current_user)):
    try:
        data = await request.json()
        new_report = Report(
            userid=data.get("userid"),
            name=data["name"],
            phone_number=data["phone_number"],
            transaction_amount=data["transaction_amount"],
            transaction_date=datetime.now(),
            transaction_status=data.get("transaction_status", 'success'),
        )
        db.add(new_report)
        db.commit()
        db.refresh(new_report)
        return {"message": "Report created", "report": new_report}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error {str(e)}")


@router_report.get("/reports/", status_code=status.HTTP_200_OK)
async def read_reports(request: Request, db=Depends(get_db), current_user: str = Depends(get_current_user)):

    try:
        reports = db.query(Report).all()
        
        report_list = []
        for report in reports:
            report_list.append({
                "id": report.id,
                "userid": report.userid,
                "name": report.name,
                "phone_number": report.phone_number,
                "order_id": report.order_id,
                "billdesk_reference_id": report.billdesk_reference_id,
                "billdesk_transaction_id": report.billdesk_transaction_id,
                "transaction_amount": report.transaction_amount,
                "transaction_date": report.transaction_date.strftime('%Y-%m-%d %H:%M:%S'),
                "transaction_status": report.transaction_status,
            })
        
        return report_list

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {str(e)}")


