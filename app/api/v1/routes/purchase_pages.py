from datetime import date
import json

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.purchase import PurchaseCreate, PurchaseItemCreate
from app.services.purchase_service import PurchaseService
from app.services.product_service import ProductService
from app.services.supplier_service import SupplierService

router = APIRouter(tags=["Purchase Pages"])

templates = Jinja2Templates(directory="app/templates")


@router.get("/purchases")
async def purchase_page(
    request: Request,
    db: Session = Depends(get_db),
):
    purchase_service = PurchaseService(db)
    supplier_service = SupplierService(db)
    product_service = ProductService(db)

    return templates.TemplateResponse(
        request=request,
        name="purchases/index.html",
        context={
            "title": "Purchases",
            "suppliers": supplier_service.get_all(),
            "products": product_service.get_all(),
            "purchases": purchase_service.get_all(),
        },
    )


@router.post("/purchases")
async def create_purchase(
    supplier_id: int = Form(...),
    purchase_date: date = Form(...),
    payment_status: str = Form(...),
    discount_amount: float = Form(0),
    notes: str = Form(""),
    items: str = Form(...),
    db: Session = Depends(get_db),
):
    service = PurchaseService(db)

    raw_items = json.loads(items)

    purchase_items = []

    for item in raw_items:

        purchase_items.append(
            PurchaseItemCreate(
                product_id=item["product_id"],
                quantity=item["quantity"],
                unit_price=item["unit_price"],
                gst_percent=item["gst_percent"],
                line_total=item["line_total"],
            )
        )

    purchase = PurchaseCreate(
        supplier_id=supplier_id,
        purchase_date=purchase_date,
        payment_status=payment_status,
        discount_amount=discount_amount,
        notes=notes,
        items=purchase_items,
    )

    service.create(purchase)

    return RedirectResponse(
        "/purchases",
        status_code=303,
    )