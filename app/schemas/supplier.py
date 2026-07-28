from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class SupplierBase(BaseModel):
    """
    Base Supplier Schema
    """

    supplier_code: str = Field(
        min_length=2,
        max_length=30,
    )

    company_name: str = Field(
        min_length=2,
        max_length=150,
    )

    contact_person: str | None = Field(
        default=None,
        max_length=100,
    )

    phone: str = Field(
        min_length=10,
        max_length=20,
    )

    email: EmailStr | None = None

    gstin: str | None = Field(
        default=None,
        max_length=15,
    )

    address: str | None = Field(
        default=None,
        max_length=500,
    )

    city: str | None = Field(
        default=None,
        max_length=100,
    )

    state: str | None = Field(
        default=None,
        max_length=100,
    )

    pincode: str | None = Field(
        default=None,
        max_length=10,
    )

    is_active: bool = True


class SupplierCreate(SupplierBase):
    """
    Schema for creating a supplier.
    """
    pass


class SupplierUpdate(SupplierBase):
    """
    Schema for updating a supplier.
    """
    pass


class SupplierResponse(SupplierBase):
    """
    Schema returned to client.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime