from sqlalchemy.orm import Session

from app.models.category import Category
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import (
    CategoryCreate,
    CategoryUpdate,
)


class CategoryService:
    """
    Business logic for Category management.
    """

    def __init__(self, db: Session):
        self.repository = CategoryRepository(db)

    def create(self, data: CategoryCreate) -> Category:
        """
        Create a new category.
        """

        existing = self.repository.get_by_name(data.name)

        if existing:
            raise ValueError("Category already exists.")

        category = Category(
            name=data.name,
            description=data.description,
        )

        return self.repository.create(category)

    def get_all(self) -> list[Category]:
        """
        Return all categories.
        """
        return self.repository.get_all()

    def update(
        self,
        category_id: int,
        data: CategoryUpdate,
    ) -> Category:
        """
        Update a category.
        """

        category = self.repository.get_by_id(category_id)

        if not category:
            raise ValueError("Category not found.")

        duplicate = self.repository.get_by_name(data.name)

        if duplicate and duplicate.id != category.id:
            raise ValueError("Category name already exists.")

        category.name = data.name
        category.description = data.description

        return self.repository.update(category)

    def delete(self, category_id: int) -> None:
        """
        Delete a category.
        """

        category = self.repository.get_by_id(category_id)

        if not category:
            raise ValueError("Category not found.")

        self.repository.delete(category)