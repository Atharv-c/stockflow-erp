from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product import Product


class ProductRepository:
    """
    Repository for Product database operations.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, product: Product) -> Product:
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def get_by_id(self, product_id: int) -> Optional[Product]:
        stmt = select(Product).where(Product.id == product_id)
        return self.db.scalar(stmt)

    def get_by_sku(self, sku: str) -> Optional[Product]:
        stmt = select(Product).where(Product.sku == sku)
        return self.db.scalar(stmt)

    def get_all(self) -> list[Product]:
        stmt = select(Product).order_by(Product.name)
        return list(self.db.scalars(stmt).all())

    def update(self, product: Product) -> Product:
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete(self, product: Product) -> None:
        self.db.delete(product)
        self.db.commit()