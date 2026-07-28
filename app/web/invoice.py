from datetime import date
import json
from fastapi.responses import Response
from app.utils.pdf_generator import generate_invoice_pdf
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.invoice import InvoiceCreate, InvoiceItemCreate
from app.services.customer_service import CustomerService
from app.services.invoice_service import InvoiceService
from app.services.product_service import ProductService

router = APIRouter(tags=["Invoice Pages"])

templates = Jinja2Templates(directory="app/templates")


@router.get("/invoices")
async def invoice_page(
    request: Request,
    db: Session = Depends(get_db),
):
    invoice_service = InvoiceService(db)
    customer_service = CustomerService(db)
    product_service = ProductService(db)

    return templates.TemplateResponse(
        request=request,
        name="invoices/index.html",
        context={
            "title": "Invoices",
            "customers": customer_service.get_all(),
            "products": product_service.get_all(),
            "invoices": invoice_service.get_all(),
        },
    )


@router.post("/invoices")
async def create_invoice(
    customer_id: int = Form(...),
    invoice_date: date = Form(...),
    payment_status: str = Form(...),
    discount_amount: float = Form(0),
    notes: str = Form(""),
    items: str = Form(...),
    db: Session = Depends(get_db),
):
    service = InvoiceService(db)

    raw_items = json.loads(items)

    invoice_items = []

    for item in raw_items:
        invoice_items.append(
            InvoiceItemCreate(
                product_id=item["product_id"],
                quantity=item["quantity"],
                unit_price=item["unit_price"],
                gst_percent=item["gst_percent"],
                line_total=item["line_total"],
            )
        )

    invoice = InvoiceCreate(
        customer_id=customer_id,
        invoice_date=invoice_date,
        payment_status=payment_status,
        discount_amount=discount_amount,
        notes=notes,
        items=invoice_items,
    )

    service.create(invoice)

    return RedirectResponse(
        "/invoices",
        status_code=303,
    )


# -------------------------------------------------
# Invoice Details
# -------------------------------------------------

@router.get("/invoices/{invoice_id}")
async def invoice_details(
    invoice_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    service = InvoiceService(db)

    invoice = service.get_by_id(invoice_id)

    return templates.TemplateResponse(
        request=request,
        name="invoices/details.html",
        context={
            "title": f"Invoice {invoice.invoice_number}",
            "invoice": invoice,
        },
    )
@router.get("/invoices/{invoice_id}/pdf")
async def download_invoice_pdf(
    invoice_id: int,
    db: Session = Depends(get_db),
):
    service = InvoiceService(db)

    invoice = service.get_by_id(invoice_id)

    pdf = generate_invoice_pdf(invoice)

    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": (
                f'attachment; filename="{invoice.invoice_number}.pdf"'
            )
        },
    )