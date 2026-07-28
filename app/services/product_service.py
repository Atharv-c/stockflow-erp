from sqlalchemy.orm import Session

from app.models.product import Product
from app.repositories.category_repository import CategoryRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate, ProductUpdate


class ProductService:
    """
    Business logic for Product management.
    """

    def __init__(self, db: Session):
        self.product_repository = ProductRepository(db)
        self.category_repository = CategoryRepository(db)

    def create(self, data: ProductCreate) -> Product:
        """
        Create a new product.
        """

        if self.product_repository.get_by_sku(data.sku):
            raise ValueError("SKU already exists.")

        category = self.category_repository.get_by_id(data.category_id)

        if not category:
            raise ValueError("Category not found.")

        product = Product(
            sku=data.sku,
            name=data.name,
            description=data.description,
            category_id=data.category_id,
            purchase_price=data.purchase_price,
            selling_price=data.selling_price,
            stock_quantity=data.stock_quantity,
            minimum_stock=data.minimum_stock,
        )

        return self.product_repository.create(product)

    def get_all(self) -> list[Product]:
        """
        Return all products.
        """
        return self.product_repository.get_all()

    def update(
        self,
        product_id: int,
        data: ProductUpdate,
    ) -> Product:
        """
        Update an existing product.
        """

        product = self.product_repository.get_by_id(product_id)

        if not product:
            raise ValueError("Product not found.")

        duplicate = self.product_repository.get_by_sku(data.sku)

        if duplicate and duplicate.id != product.id:
            raise ValueError("SKU already exists.")

        category = self.category_repository.get_by_id(data.category_id)

        if not category:
            raise ValueError("Category not found.")

        product.sku = data.sku
        product.name = data.name
        product.description = data.description
        product.category_id = data.category_id
        product.purchase_price = data.purchase_price
        product.selling_price = data.selling_price
        product.stock_quantity = data.stock_quantity
        product.minimum_stock = data.minimum_stock

        return self.product_repository.update(product)

    def delete(self, product_id: int) -> None:
        """
        Delete a product.
        """

        product = self.product_repository.get_by_id(product_id)

        if not product:
            raise ValueError("Product not found.")

        self.product_repository.delete(product)