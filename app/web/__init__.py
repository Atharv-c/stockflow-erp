from app.web.category import router as category_page_router
from app.web.customer import router as customer_page_router
from app.web.product import router as product_page_router
from app.web.supplier import router as supplier_page_router

__all__ = [
    "category_page_router",
    "customer_page_router",
    "product_page_router",
    "supplier_page_router",
]