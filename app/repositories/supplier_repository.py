from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.supplier import Supplier


class SupplierRepository:
    """
    Repository for Supplier database operations.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, supplier: Supplier) -> Supplier:
        self.db.add(supplier)
        self.db.commit()
        self.db.refresh(supplier)
        return supplier

    def get_all(self) -> list[Supplier]:
        stmt = select(Supplier).order_by(Supplier.company_name)
        return list(self.db.scalars(stmt).all())

    def get_by_id(self, supplier_id: int) -> Optional[Supplier]:
        stmt = select(Supplier).where(Supplier.id == supplier_id)
        return self.db.scalar(stmt)

    def get_by_code(self, supplier_code: str) -> Optional[Supplier]:
        stmt = select(Supplier).where(
            Supplier.supplier_code == supplier_code
        )
        return self.db.scalar(stmt)

    def update(self, supplier: Supplier) -> Supplier:
        self.db.commit()
        self.db.refresh(supplier)
        return supplier

    def delete(self, supplier: Supplier) -> None:
        self.db.delete(supplier)
        self.db.commit()