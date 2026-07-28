from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.category import Category


class CategoryRepository:
    """
    Repository for Category database operations.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, category: Category) -> Category:
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def get_by_id(self, category_id: int) -> Optional[Category]:
        stmt = select(Category).where(Category.id == category_id)
        return self.db.scalar(stmt)

    def get_by_name(self, name: str) -> Optional[Category]:
        stmt = select(Category).where(Category.name == name)
        return self.db.scalar(stmt)

    def get_all(self) -> list[Category]:
        stmt = select(Category).order_by(Category.name)
        return list(self.db.scalars(stmt).all())

    def update(self, category: Category) -> Category:
        self.db.commit()
        self.db.refresh(category)
        return category

    def delete(self, category: Category) -> None:
        self.db.delete(category)
        self.db.commit()