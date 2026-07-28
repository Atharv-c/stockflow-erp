from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.services.category_service import CategoryService

router = APIRouter(tags=["Category Pages"])

templates = Jinja2Templates(directory="app/templates")


@router.get("/categories")
async def category_page(
    request: Request,
    db: Session =Depends(get_db),
):
    service = CategoryService(db)

    return templates.TemplateResponse(
        request=request,
        name="categories/index.html",
        context={
            "title": "Categories",
            "categories": service.get_all(),
        },
    )


@router.post("/categories")
async def create_category(
    name: str = Form(...),
    description: str = Form(""),
    db: Session = Depends(get_db),
):
    service = CategoryService(db)

    try:
        service.create(
            CategoryCreate(
                name=name,
                description=description,
            )
        )
    except ValueError:
        pass

    return RedirectResponse(
        "/categories",
        status_code=303,
    )


@router.post("/categories/{category_id}/edit")
async def edit_category(
    category_id: int,
    name: str = Form(...),
    description: str = Form(""),
    db: Session = Depends(get_db),
):
    service = CategoryService(db)

    try:
        service.update(
            category_id,
            CategoryUpdate(
                name=name,
                description=description,
            ),
        )
    except ValueError:
        pass

    return RedirectResponse(
        "/categories",
        status_code=303,
    )


@router.post("/categories/{category_id}/delete")
async def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    service = CategoryService(db)

    try:
        service.delete(category_id)
    except ValueError:
        pass

    return RedirectResponse(
        "/categories",
        status_code=303,
    )