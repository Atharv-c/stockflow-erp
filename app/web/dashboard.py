from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.dashboard_service import DashboardService

router = APIRouter(tags=["Dashboard"])

templates = Jinja2Templates(directory="app/templates")


@router.get("/")
@router.get("/dashboard")
async def dashboard(
    request: Request,
    db: Session = Depends(get_db),
):
    service = DashboardService(db)

    data = service.get_dashboard_data()

    return templates.TemplateResponse(
        request=request,
        name="dashboard/index.html",
        context={
            "title": "Dashboard",
            **data,
        },
    )