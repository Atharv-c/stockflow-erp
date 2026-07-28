from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.invoice import Invoice
from app.models.invoice_item import InvoiceItem


class InvoiceRepository:
    """
    Repository for Invoice database operations.
    """

    def __init__(self, db: Session):
        self.db = db

    # ----------------------------------
    # Create Invoice
    # ----------------------------------

    def create(self, invoice: Invoice) -> Invoice:
        self.db.add(invoice)
        self.db.flush()
        return invoice

    # ----------------------------------
    # Add Invoice Item
    # ----------------------------------

    def add_item(
        self,
        item: InvoiceItem,
    ) -> InvoiceItem:

        self.db.add(item)
        return item

    # ----------------------------------
    # Commit Transaction
    # ----------------------------------

    def commit(self):
        self.db.commit()

    # ----------------------------------
    # Rollback Transaction
    # ----------------------------------

    def rollback(self):
        self.db.rollback()

    # ----------------------------------
    # Refresh
    # ----------------------------------

    def refresh(
        self,
        invoice: Invoice,
    ):
        self.db.refresh(invoice)

    # ----------------------------------
    # Get All
    # ----------------------------------

    def get_all(self) -> list[Invoice]:

        stmt = (
            select(Invoice)
            .order_by(Invoice.id.desc())
        )

        return list(self.db.scalars(stmt).all())

    # ----------------------------------
    # Get By ID
    # ----------------------------------

    def get_by_id(
        self,
        invoice_id: int,
    ) -> Invoice | None:

        stmt = (
            select(Invoice)
            .where(Invoice.id == invoice_id)
        )

        return self.db.scalar(stmt)

    # ----------------------------------
    # Get Invoice with Customer & Items
    # ----------------------------------

    def get_with_items(
        self,
        invoice_id: int,
    ) -> Invoice | None:
        """
        Return invoice with customer and line items.
        """

        stmt = (
            select(Invoice)
            .options(
                joinedload(Invoice.customer),
                joinedload(Invoice.items),
            )
            .where(Invoice.id == invoice_id)
        )

        return self.db.scalar(stmt)