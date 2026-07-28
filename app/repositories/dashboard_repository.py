from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.invoice import Invoice
from app.models.product import Product
from app.models.supplier import Supplier


class DashboardRepository:

    def __init__(self, db: Session):
        self.db = db

    def total_products(self):
        return self.db.scalar(
            select(func.count(Product.id))
        ) or 0

    def total_customers(self):
        return self.db.scalar(
            select(func.count(Customer.id))
        ) or 0

    def total_suppliers(self):
        return self.db.scalar(
            select(func.count(Supplier.id))
        ) or 0

    def total_invoices(self):
        return self.db.scalar(
            select(func.count(Invoice.id))
        ) or 0

    def total_sales(self):
        total = self.db.scalar(
            select(func.sum(Invoice.grand_total))
        )
        return total or 0

    def low_stock_products(self):
        return self.db.scalar(
            select(func.count(Product.id))
            .where(Product.stock_quantity <= Product.minimum_stock)
        ) or 0

    def recent_invoices(self):
        return (
            self.db.query(Invoice)
            .order_by(Invoice.id.desc())
            .limit(5)
            .all()
        )