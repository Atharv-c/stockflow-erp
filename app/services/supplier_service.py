from sqlalchemy.orm import Session

from app.models.supplier import Supplier
from app.repositories.supplier_repository import SupplierRepository
from app.schemas.supplier import SupplierCreate, SupplierUpdate


class SupplierService:
    """
    Business logic for Supplier management.
    """

    def __init__(self, db: Session):
        self.repository = SupplierRepository(db)

    def create(self, data: SupplierCreate) -> Supplier:
        """
        Create a new supplier.
        """

        if self.repository.get_by_code(data.supplier_code):
            raise ValueError("Supplier code already exists.")

        supplier = Supplier(
            supplier_code=data.supplier_code,
            company_name=data.company_name,
            contact_person=data.contact_person,
            phone=data.phone,
            email=data.email,
            gstin=data.gstin,
            address=data.address,
            city=data.city,
            state=data.state,
            pincode=data.pincode,
            is_active=data.is_active,
        )

        return self.repository.create(supplier)

    def get_all(self) -> list[Supplier]:
        """
        Return all suppliers.
        """
        return self.repository.get_all()

    def update(
        self,
        supplier_id: int,
        data: SupplierUpdate,
    ) -> Supplier:
        """
        Update an existing supplier.
        """

        supplier = self.repository.get_by_id(supplier_id)

        if not supplier:
            raise ValueError("Supplier not found.")

        duplicate = self.repository.get_by_code(data.supplier_code)

        if duplicate and duplicate.id != supplier.id:
            raise ValueError("Supplier code already exists.")

        supplier.supplier_code = data.supplier_code
        supplier.company_name = data.company_name
        supplier.contact_person = data.contact_person
        supplier.phone = data.phone
        supplier.email = data.email
        supplier.gstin = data.gstin
        supplier.address = data.address
        supplier.city = data.city
        supplier.state = data.state
        supplier.pincode = data.pincode
        supplier.is_active = data.is_active

        return self.repository.update(supplier)

    def delete(self, supplier_id: int) -> None:
        """
        Delete a supplier.
        """

        supplier = self.repository.get_by_id(supplier_id)

        if not supplier:
            raise ValueError("Supplier not found.")

        self.repository.delete(supplier)