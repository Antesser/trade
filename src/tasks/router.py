from auth.base_config import current_user
from fastapi import APIRouter, Depends

from tasks.tasks import send_email_report_dashboard


router = APIRouter(prefix="/reports", tags=["report"])


@router.get("/dashboard")
def get_dashboard_report(recipient_name: str, user=Depends(current_user)):
    # background_tasks.add_task(send_email_report_dashboard, recipient_name, user.username)
    send_email_report_dashboard.delay(recipient_name, user.username)
    return {"status": 200, "data": "Letter has been sent", "details": None}
