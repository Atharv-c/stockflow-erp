from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    """
    Base Product Schema
    """

    sku: str = Field(
        min_length=1,
        max_length=50,
    )

    name: str = Field(
        min_length=2,
        max_length=150,
    )

    description: str | None = Field(
        default=None,
        max_length=500,
    )

    category_id: int

    purchase_price: Decimal = Field(
        ge=0,
    )

    selling_price: Decimal = Field(
        ge=0,
    )

    stock_quantity: int = Field(
        ge=0,
    )

    minimum_stock: int = Field(
        ge=0,
    )


class ProductCreate(ProductBase):
    """
    Schema for creating a product.
    """
    pass


class ProductUpdate(ProductBase):
    """
    Schema for updating a product.
    """
    pass


class ProductResponse(ProductBase):
    """
    Schema returned to client.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime