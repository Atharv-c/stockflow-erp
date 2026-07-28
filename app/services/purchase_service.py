from decimal import Decimal
from uuid import uuid4

from sqlalchemy.orm import Session

from app.models.product import Product
from app.models.purchase import Purchase
from app.models.purchase_item import PurchaseItem
from app.repositories.product_repository import ProductRepository
from app.repositories.purchase_repository import PurchaseRepository
from app.schemas.purchase import PurchaseCreate


class PurchaseService:
    """
    Business logic for Purchase Management.
    """

    def __init__(self, db: Session):
        self.db = db
        self.repository = PurchaseRepository(db)
        self.product_repository = ProductRepository(db)

    # ---------------------------------
    # Create Purchase
    # ---------------------------------

    def create(
        self,
        data: PurchaseCreate,
    ) -> Purchase:

        subtotal = Decimal("0")
        gst_total = Decimal("0")

        for item in data.items:

            line_subtotal = (
                item.quantity *
                item.unit_price
            )

            gst_amount = (
                line_subtotal *
                item.gst_percent
            ) / Decimal("100")

            subtotal += line_subtotal
            gst_total += gst_amount

        grand_total = (
            subtotal +
            gst_total -
            data.discount_amount
        )

        purchase = Purchase(

            purchase_number=f"PUR-{uuid4().hex[:8].upper()}",

            supplier_id=data.supplier_id,

            purchase_date=data.purchase_date,

            subtotal=subtotal,

            gst_amount=gst_total,

            discount_amount=data.discount_amount,

            grand_total=grand_total,

            payment_status=data.payment_status,

            notes=data.notes,

        )

        try:

            self.repository.create(purchase)

            for item in data.items:

                purchase_item = PurchaseItem(

                    purchase_id=purchase.id,

                    product_id=item.product_id,

                    quantity=item.quantity,

                    unit_price=item.unit_price,

                    gst_percent=item.gst_percent,

                    line_total=item.line_total,

                )

                self.repository.add_item(
                    purchase_item
                )

                # Update Stock

                product = self.product_repository.get_by_id(
                    item.product_id
                )

                if product:

                    product.quantity += item.quantity

            self.repository.commit()

            self.repository.refresh(
                purchase
            )

            return purchase

        except Exception:

            self.repository.rollback()

            raise

    # ---------------------------------
    # Get All Purchases
    # ---------------------------------

    def get_all(self):

        return self.repository.get_all()

    # ---------------------------------
    # Get Purchase
    # ---------------------------------

    def get_by_id(
        self,
        purchase_id: int,
    ):

        return self.repository.get_with_items(
            purchase_id
        )