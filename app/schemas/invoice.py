from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class InvoiceItemCreate(BaseModel):
    """
    Invoice Item Schema
    """

    product_id: int

    quantity: int = Field(gt=0)

    unit_price: Decimal = Field(ge=0)

    gst_percent: Decimal = Field(ge=0)

    line_total: Decimal = Field(ge=0)


class InvoiceCreate(BaseModel):
    """
    Invoice Create Schema
    """

    customer_id: int

    invoice_date: date

    payment_status: str

    discount_amount: Decimal = Decimal("0.00")

    notes: Optional[str] = None

    items: list[InvoiceItemCreate]


class InvoiceUpdate(BaseModel):
    """
    Invoice Update Schema
    """

    customer_id: int

    invoice_date: date

    payment_status: str

    discount_amount: Decimal

    notes: Optional[str] = None


class InvoiceResponse(BaseModel):
    """
    Invoice Response
    """

    model_config = ConfigDict(from_attributes=True)

    id: int

    invoice_number: str

    customer_id: int

    subtotal: Decimal

    gst_amount: Decimal

    discount_amount: Decimal

    grand_total: Decimal

    payment_status: str