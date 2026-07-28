from app.api.v1.routes.auth import router as auth_router
from app.api.v1.routes.category import router as category_router
from app.api.v1.routes.customer import router as customer_router
from app.api.v1.routes.product import router as product_router
from app.api.v1.routes.supplier import router as supplier_router

__all__ = [
    "auth_router",
    "category_router",
    "customer_router",
    "product_router",
    "supplier_router",
]