from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CategoryBase(BaseModel):
    """
    Base Category Schema
    """

    name: str = Field(
        min_length=2,
        max_length=100,
    )

    description: str | None = Field(
        default=None,
        max_length=500,
    )


class CategoryCreate(CategoryBase):
    """
    Schema for creating a category.
    """
    pass


class CategoryUpdate(CategoryBase):
    """
    Schema for updating a category.
    """
    pass


class CategoryResponse(CategoryBase):
    """
    Schema returned to client.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime