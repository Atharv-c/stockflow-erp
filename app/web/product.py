from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.product import ProductCreate, ProductUpdate
from app.services.category_service import CategoryService
from app.services.product_service import ProductService

router = APIRouter(tags=["Product Pages"])

templates = Jinja2Templates(directory="app/templates")


@router.get("/products")
async def product_page(
    request: Request,
    db: Session = Depends(get_db),
):
    product_service = ProductService(db)
    category_service = CategoryService(db)

    return templates.TemplateResponse(
        request=request,
        name="products/index.html",
        context={
            "title": "Products",
            "products": product_service.get_all(),
            "categories": category_service.get_all(),
        },
    )


@router.post("/products")
async def create_product(
    sku: str = Form(...),
    name: str = Form(...),
    description: str = Form(""),
    category_id: int = Form(...),
    purchase_price: float = Form(...),
    selling_price: float = Form(...),
    stock_quantity: int = Form(...),
    minimum_stock: int = Form(...),
    db: Session = Depends(get_db),
):
    product_service = ProductService(db)

    try:
        product_service.create(
            ProductCreate(
                sku=sku,
                name=name,
                description=description,
                category_id=category_id,
                purchase_price=purchase_price,
                selling_price=selling_price,
                stock_quantity=stock_quantity,
                minimum_stock=minimum_stock,
            )
        )
    except ValueError:
        pass

    return RedirectResponse("/products", status_code=303)


@router.post("/products/{product_id}/edit")
async def edit_product(
    product_id: int,
    sku: str = Form(...),
    name: str = Form(...),
    description: str = Form(""),
    category_id: int = Form(...),
    purchase_price: float = Form(...),
    selling_price: float = Form(...),
    stock_quantity: int = Form(...),
    minimum_stock: int = Form(...),
    db: Session = Depends(get_db),
):
    product_service = ProductService(db)

    try:
        product_service.update(
            product_id,
            ProductUpdate(
                sku=sku,
                name=name,
                description=description,
                category_id=category_id,
                purchase_price=purchase_price,
                selling_price=selling_price,
                stock_quantity=stock_quantity,
                minimum_stock=minimum_stock,
            ),
        )
    except ValueError:
        pass

    return RedirectResponse("/products", status_code=303)


@router.post("/products/{product_id}/delete")
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    product_service = ProductService(db)

    try:
        product_service.delete(product_id)
    except ValueError:
        pass

    return RedirectResponse("/products", status_code=303)