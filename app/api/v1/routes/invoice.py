from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.invoice import InvoiceCreate, InvoiceResponse
from app.services.invoice_service import InvoiceService

router = APIRouter(
    prefix="/api/invoices",
    tags=["Invoices"],
)


@router.get(
    "/",
    response_model=list[InvoiceResponse],
)
def get_invoices(
    db: Session = Depends(get_db),
):
    service = InvoiceService(db)

    return service.get_all()


@router.get(
    "/{invoice_id}",
    response_model=InvoiceResponse,
)
def get_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
):
    service = InvoiceService(db)

    try:
        return service.get_by_id(invoice_id)

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


@router.post(
    "/",
    response_model=InvoiceResponse,
    status_code=201,
)
def create_invoice(
    invoice: InvoiceCreate,
    db: Session = Depends(get_db),
):
    service = InvoiceService(db)

    try:
        return service.create(invoice)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.delete(
    "/{invoice_id}",
    status_code=204,
)
def delete_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
):
    service = InvoiceService(db)

    try:
        service.delete(invoice_id)

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )