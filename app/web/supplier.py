from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.supplier import SupplierCreate, SupplierUpdate
from app.services.supplier_service import SupplierService

router = APIRouter(tags=["Supplier Pages"])

templates = Jinja2Templates(directory="app/templates")


@router.get("/suppliers")
async def supplier_page(
    request: Request,
    db: Session = Depends(get_db),
):
    service = SupplierService(db)

    return templates.TemplateResponse(
        request=request,
        name="suppliers/index.html",
        context={
            "title": "Suppliers",
            "suppliers": service.get_all(),
        },
    )


@router.post("/suppliers")
async def create_supplier(
    supplier_code: str = Form(...),
    company_name: str = Form(...),
    contact_person: str = Form(""),
    phone: str = Form(...),
    email: str = Form(""),
    gstin: str = Form(""),
    address: str = Form(""),
    city: str = Form(""),
    state: str = Form(""),
    pincode: str = Form(""),
    is_active: bool = Form(True),
    db: Session = Depends(get_db),
):
    service = SupplierService(db)

    try:
        service.create(
            SupplierCreate(
                supplier_code=supplier_code,
                company_name=company_name,
                contact_person=contact_person,
                phone=phone,
                email=email or None,
                gstin=gstin or None,
                address=address or None,
                city=city or None,
                state=state or None,
                pincode=pincode or None,
                is_active=is_active,
            )
        )
    except ValueError:
        pass

    return RedirectResponse("/suppliers", status_code=303)


@router.post("/suppliers/{supplier_id}/delete")
async def delete_supplier(
    supplier_id: int,
    db: Session = Depends(get_db),
):
    service = SupplierService(db)

    try:
        service.delete(supplier_id)
    except ValueError:
        pass

    return RedirectResponse("/suppliers", status_code=303)


@router.post("/suppliers/{supplier_id}/edit")
async def edit_supplier(
    supplier_id: int,
    supplier_code: str = Form(...),
    company_name: str = Form(...),
    contact_person: str = Form(""),
    phone: str = Form(...),
    email: str = Form(""),
    gstin: str = Form(""),
    address: str = Form(""),
    city: str = Form(""),
    state: str = Form(""),
    pincode: str = Form(""),
    is_active: bool = Form(False),
    db: Session = Depends(get_db),
):
    service = SupplierService(db)

    try:
        service.update(
            supplier_id,
            SupplierUpdate(
                supplier_code=supplier_code,
                company_name=company_name,
                contact_person=contact_person,
                phone=phone,
                email=email or None,
                gstin=gstin or None,
                address=address or None,
                city=city or None,
                state=state or None,
                pincode=pincode or None,
                is_active=is_active,
            ),
        )
    except ValueError:
        pass

    return RedirectResponse("/suppliers", status_code=303)