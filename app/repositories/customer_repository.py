from typing import Optional

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.customer import Customer


class CustomerRepository:
    """
    Repository for Customer database operations.
    """

    def __init__(self, db: Session):
        self.db = db

    # -------------------------
    # Create
    # -------------------------

    def create(self, customer: Customer) -> Customer:
        self.db.add(customer)
        self.db.commit()
        self.db.refresh(customer)
        return customer

    # -------------------------
    # Get All Customers
    # -------------------------

    def get_all(self) -> list[Customer]:
        stmt = (
            select(Customer)
            .order_by(Customer.customer_name)
        )

        return list(self.db.scalars(stmt).all())

    # -------------------------
    # Search Customers
    # -------------------------

    def search(
        self,
        keyword: str,
    ) -> list[Customer]:

        stmt = (
            select(Customer)
            .where(
                or_(
                    Customer.customer_code.ilike(f"%{keyword}%"),
                    Customer.customer_name.ilike(f"%{keyword}%"),
                    Customer.phone.ilike(f"%{keyword}%"),
                    Customer.email.ilike(f"%{keyword}%"),
                    Customer.gstin.ilike(f"%{keyword}%"),
                    Customer.city.ilike(f"%{keyword}%"),
                    Customer.state.ilike(f"%{keyword}%"),
                )
            )
            .order_by(Customer.customer_name)
        )

        return list(self.db.scalars(stmt).all())

    # -------------------------
    # Customer Statistics
    # -------------------------

    def get_statistics(self) -> dict:
        """
        Return customer statistics.
        """

        total = self.db.query(Customer).count()

        active = (
            self.db.query(Customer)
            .filter(Customer.is_active == True)
            .count()
        )

        inactive = total - active

        return {
            "total": total,
            "active": active,
            "inactive": inactive,
        }

    # -------------------------
    # Get By ID
    # -------------------------

    def get_by_id(
        self,
        customer_id: int,
    ) -> Optional[Customer]:

        stmt = (
            select(Customer)
            .where(Customer.id == customer_id)
        )

        return self.db.scalar(stmt)

    # -------------------------
    # Get By Code
    # -------------------------

    def get_by_code(
        self,
        customer_code: str,
    ) -> Optional[Customer]:

        stmt = (
            select(Customer)
            .where(Customer.customer_code == customer_code)
        )

        return self.db.scalar(stmt)

    # -------------------------
    # Update
    # -------------------------

    def update(
        self,
        customer: Customer,
    ) -> Customer:

        self.db.commit()
        self.db.refresh(customer)

        return customer

    # -------------------------
    # Delete
    # -------------------------

    def delete(
        self,
        customer: Customer,
    ) -> None:
        """
        Delete a customer.
        """

        self.db.delete(customer)
        self.db.commit()