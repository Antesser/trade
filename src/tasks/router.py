from auth.base_config import current_user
from fastapi import APIRouter, BackgroundTasks, Depends

from tasks.tasks import send_email_report_dashboard


router = APIRouter(prefix="/reports", tags=["report"])


@router.get("/dashboard")
def get_dashboard_report(user=Depends(current_user)):
    # background_tasks.add_task(send_email_report_dashboard, username)
    send_email_report_dashboard.delay(user.username)
    return {"status": 200, "data": "Letter has been sent", "details": None}
