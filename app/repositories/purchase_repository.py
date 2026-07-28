from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.purchase import Purchase
from app.models.purchase_item import PurchaseItem


class PurchaseRepository:
    """
    Repository for Purchase database operations.
    """

    def __init__(self, db: Session):
        self.db = db

    # -------------------------
    # Create Purchase
    # -------------------------

    def create(
        self,
        purchase: Purchase,
    ) -> Purchase:

        self.db.add(purchase)
        self.db.flush()

        return purchase

    # -------------------------
    # Add Purchase Item
    # -------------------------

    def add_item(
        self,
        item: PurchaseItem,
    ) -> PurchaseItem:

        self.db.add(item)

        return item

    # -------------------------
    # Commit
    # -------------------------

    def commit(self):

        self.db.commit()

    # -------------------------
    # Rollback
    # -------------------------

    def rollback(self):

        self.db.rollback()

    # -------------------------
    # Refresh
    # -------------------------

    def refresh(
        self,
        purchase: Purchase,
    ):

        self.db.refresh(purchase)

    # -------------------------
    # Get All
    # -------------------------

    def get_all(self) -> list[Purchase]:

        stmt = (
            select(Purchase)
            .options(
                joinedload(Purchase.supplier)
            )
            .order_by(
                Purchase.id.desc()
            )
        )

        return list(
            self.db.scalars(stmt).all()
        )

    # -------------------------
    # Get By ID
    # -------------------------

    def get_by_id(
        self,
        purchase_id: int,
    ) -> Purchase | None:

        stmt = (
            select(Purchase)
            .where(
                Purchase.id == purchase_id
            )
        )

        return self.db.scalar(stmt)

    # -------------------------
    # Get With Items
    # -------------------------

    def get_with_items(
        self,
        purchase_id: int,
    ) -> Purchase | None:

        stmt = (
            select(Purchase)
            .options(
                joinedload(Purchase.supplier),
                joinedload(Purchase.items),
            )
            .where(
                Purchase.id == purchase_id
            )
        )

        return self.db.scalar(stmt)