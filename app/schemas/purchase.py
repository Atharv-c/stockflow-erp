from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field


class PurchaseItemCreate(BaseModel):
    product_id: int

    quantity: int = Field(
        gt=0,
    )

    unit_price: Decimal = Field(
        gt=0,
    )

    gst_percent: Decimal = Field(
        ge=0,
    )

    line_total: Decimal = Field(
        ge=0,
    )


class PurchaseCreate(BaseModel):
    supplier_id: int

    purchase_date: date

    payment_status: str

    discount_amount: Decimal = 0

    notes: str | None = None

    items: list[PurchaseItemCreate]