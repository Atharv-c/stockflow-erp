from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.v1.routes.auth import router as auth_router
from app.api.v1.routes.category import router as category_router
from app.core.config import settings
from app.web.category import router as category_page_router
from app.api.v1.routes.product import router as product_router
from app.web.product import router as product_page_router
from app.api.v1.routes.supplier import router as supplier_router
from app.web.supplier import router as supplier_page_router
from app.api.v1.routes.customer import router as customer_router
from app.web.customer import router as customer_page_router
from starlette.middleware.sessions import SessionMiddleware
from app.api.v1.routes.invoice import router as invoice_router
from app.web.invoice import router as invoice_page_router
from app.web.dashboard import router as dashboard_router
from app.api.v1.routes.purchase import router as purchase_api_router
from app.api.v1.routes.purchase_pages import router as purchase_page_router


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    debug=settings.DEBUG,
)
app.add_middleware(
    SessionMiddleware,
    secret_key="stockflow-pro-secret-key-change-in-production",
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

app.include_router(auth_router)
app.include_router(category_router)
app.include_router(category_page_router)
app.include_router(product_router)
app.include_router(product_page_router)
app.include_router(supplier_router)
app.include_router(supplier_page_router)
app.include_router(customer_router)
app.include_router(customer_page_router)
app.include_router(invoice_router)
app.include_router(invoice_page_router)
app.include_router(dashboard_router)
app.include_router(purchase_api_router)
app.include_router(purchase_page_router)


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "title": "Dashboard",
        },
    )