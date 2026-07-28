from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class InvoiceItemBase(BaseModel):
    """
    Base Invoice Item Schema
    """

    product_id: int = Field(
        gt=0,
    )

    quantity: int = Field(
        gt=0,
    )

    unit_price: Decimal = Field(
        ge=0,
        decimal_places=2,
    )

    gst_percent: Decimal = Field(
        default=Decimal("18.00"),
        ge=0,
        le=100,
        decimal_places=2,
    )


class InvoiceItemCreate(InvoiceItemBase):
    """
    Create Invoice Item
    """
    pass


class InvoiceItemUpdate(InvoiceItemBase):
    """
    Update Invoice Item
    """
    pass


class InvoiceItemResponse(InvoiceItemBase):
    """
    Invoice Item Response
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int

    product_name: str

    gst_amount: Decimal

    line_total: Decimal