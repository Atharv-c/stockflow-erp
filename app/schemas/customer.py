from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CustomerBase(BaseModel):
    """
    Base Customer Schema
    """

    customer_code: str = Field(
        min_length=2,
        max_length=30,
    )

    customer_name: str = Field(
        min_length=2,
        max_length=150,
    )

    phone: str = Field(
        min_length=10,
        max_length=10,
        pattern=r"^[6-9][0-9]{9}$",
    )

    email: EmailStr | None = None

    gstin: str | None = Field(
        default=None,
        pattern=r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9A-Z]$",
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
        pattern=r"^[1-9][0-9]{5}$",
    )

    is_active: bool = True


class CustomerCreate(CustomerBase):
    """
    Create Customer Schema
    """
    pass


class CustomerUpdate(CustomerBase):
    """
    Update Customer Schema
    """
    pass


class CustomerResponse(CustomerBase):
    """
    Response Schema
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime