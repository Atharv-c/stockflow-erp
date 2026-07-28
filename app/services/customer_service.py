from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.repositories.customer_repository import CustomerRepository
from app.schemas.customer import CustomerCreate, CustomerUpdate


class CustomerService:
    """
    Business logic for Customer management.
    """

    def __init__(self, db: Session):
        self.repository = CustomerRepository(db)

    # -------------------------
    # Create Customer
    # -------------------------

    def create(self, data: CustomerCreate) -> Customer:
        """
        Create a new customer.
        """

        if self.repository.get_by_code(data.customer_code):
            raise ValueError("Customer code already exists.")

        customer = Customer(
            customer_code=data.customer_code,
            customer_name=data.customer_name,
            phone=data.phone,
            email=data.email,
            gstin=data.gstin,
            address=data.address,
            city=data.city,
            state=data.state,
            pincode=data.pincode,
            is_active=data.is_active,
        )

        return self.repository.create(customer)

    # -------------------------
    # Get All Customers
    # -------------------------

    def get_all(self) -> list[Customer]:
        """
        Return all customers.
        """
        return self.repository.get_all()

    # -------------------------
    # Search Customers
    # -------------------------

    def search(self, keyword: str) -> list[Customer]:
        """
        Search customers.
        """

        keyword = keyword.strip()

        if not keyword:
            return self.repository.get_all()

        return self.repository.search(keyword)

    # -------------------------
    # Customer Statistics
    # -------------------------

    def statistics(self) -> dict:
        """
        Return customer statistics.
        """
        return self.repository.get_statistics()

    # -------------------------
    # Update Customer
    # -------------------------

    def update(
        self,
        customer_id: int,
        data: CustomerUpdate,
    ) -> Customer:
        """
        Update an existing customer.
        """

        customer = self.repository.get_by_id(customer_id)

        if not customer:
            raise ValueError("Customer not found.")

        duplicate = self.repository.get_by_code(data.customer_code)

        if duplicate and duplicate.id != customer.id:
            raise ValueError("Customer code already exists.")

        customer.customer_code = data.customer_code
        customer.customer_name = data.customer_name
        customer.phone = data.phone
        customer.email = data.email
        customer.gstin = data.gstin
        customer.address = data.address
        customer.city = data.city
        customer.state = data.state
        customer.pincode = data.pincode
        customer.is_active = data.is_active

        return self.repository.update(customer)

    # -------------------------
    # Delete Customer
    # -------------------------

        # -------------------------
    # Delete Customer
    # -------------------------

    def delete(self, customer_id: int) -> None:
        """
        Delete a customer.
        """

        customer = self.repository.get_by_id(customer_id)

        if not customer:
            raise ValueError("Customer not found.")

        # Do not allow deleting customers that have invoices
        if customer.invoices:
            raise ValueError(
                "Cannot delete customer because invoices exist."
            )

        self.repository.delete(customer)