from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.invoice import Invoice
from app.models.invoice_item import InvoiceItem
from app.repositories.customer_repository import CustomerRepository
from app.repositories.invoice_repository import InvoiceRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.invoice import InvoiceCreate


class InvoiceService:
    """
    Business logic for Invoice Management.
    """

    def __init__(self, db: Session):
        self.db = db
        self.invoice_repo = InvoiceRepository(db)
        self.product_repo = ProductRepository(db)
        self.customer_repo = CustomerRepository(db)

    # -----------------------------------
    # Generate Invoice Number
    # -----------------------------------

    def generate_invoice_number(self) -> str:

        count = len(self.invoice_repo.get_all()) + 1

        return f"INV-{count:05d}"

    # -----------------------------------
    # Get All Invoices
    # -----------------------------------

    def get_all(self):

        return self.invoice_repo.get_all()
        # -----------------------------------
    # Get Invoice Details
    # -----------------------------------

    def get_by_id(
        self,
        invoice_id: int,
    ) -> Invoice:

        invoice = self.invoice_repo.get_with_items(
            invoice_id
        )

        if not invoice:
            raise ValueError(
                "Invoice not found."
            )

        return invoice

    # -----------------------------------
    # Create Invoice
    # -----------------------------------

    def create(
        self,
        data: InvoiceCreate,
    ) -> Invoice:

        customer = self.customer_repo.get_by_id(
            data.customer_id
        )

        if not customer:
            raise ValueError("Customer not found.")

        subtotal = Decimal("0.00")
        gst_total = Decimal("0.00")

        invoice = Invoice(
            invoice_number=self.generate_invoice_number(),
            customer_id=data.customer_id,
            invoice_date=data.invoice_date,
            payment_status=data.payment_status,
            subtotal=Decimal("0.00"),
            gst_amount=Decimal("0.00"),
            discount_amount=data.discount_amount,
            grand_total=Decimal("0.00"),
            notes=data.notes,
        )

        try:

            self.invoice_repo.create(invoice)

            for item in data.items:

                product = self.product_repo.get_by_id(
                    item.product_id
                )

                if not product:
                    raise ValueError("Product not found.")

                if product.stock_quantity < item.quantity:
                    raise ValueError(
                        f"Insufficient stock for {product.name}"
                    )

                line_subtotal = (
                    item.unit_price * item.quantity
                )

                line_gst = (
                    line_subtotal
                    * item.gst_percent
                    / Decimal("100")
                )

                subtotal += line_subtotal
                gst_total += line_gst

                invoice_item = InvoiceItem(
                    invoice_id=invoice.id,
                    product_id=product.id,
                    product_name=product.name,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    gst_percent=item.gst_percent,
                    gst_amount=line_gst,
                    line_total=line_subtotal + line_gst,
                )

                self.invoice_repo.add_item(invoice_item)

                # Reduce Stock
                product.stock_quantity -= item.quantity

            invoice.subtotal = subtotal
            invoice.gst_amount = gst_total
            invoice.grand_total = (
                subtotal
                + gst_total
                - data.discount_amount
            )

            self.invoice_repo.commit()
            self.invoice_repo.refresh(invoice)

            return invoice

        except Exception:

            self.invoice_repo.rollback()
            raise