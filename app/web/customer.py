from fastapi import APIRouter, Depends, Form, Query, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.customer import CustomerCreate, CustomerUpdate
from app.services.customer_service import CustomerService

router = APIRouter(tags=["Customer Pages"])

templates = Jinja2Templates(directory="app/templates")


@router.get("/customers")
async def customer_page(
    request: Request,
    search: str = Query(default=""),
    db: Session = Depends(get_db),
):
    service = CustomerService(db)

    customers = (
        service.search(search)
        if search.strip()
        else service.get_all()
    )

    stats = service.statistics()

    response = templates.TemplateResponse(
        request=request,
        name="customers/index.html",
        context={
            "title": "Customers",
            "customers": customers,
            "search": search,
            "stats": stats,
            "success": request.cookies.get("flash_success"),
            "error": request.cookies.get("flash_error"),
        },
    )

    response.delete_cookie("flash_success")
    response.delete_cookie("flash_error")

    return response

@router.post("/customers")
async def create_customer(
    customer_code: str = Form(...),
    customer_name: str = Form(...),
    phone: str = Form(...),
    email: str = Form(""),
    gstin: str = Form(""),
    address: str = Form(""),
    city: str = Form(""),
    state: str = Form(""),
    pincode: str = Form(""),
    is_active: bool = Form(True),
    db: Session = Depends(get_db),
):
    service = CustomerService(db)

    try:
        customer = CustomerCreate(
            customer_code=customer_code.strip(),
            customer_name=customer_name.strip(),
            phone=phone.strip(),
            email=email.strip() or None,
            gstin=gstin.strip().upper() or None,
            address=address.strip() or None,
            city=city.strip() or None,
            state=state.strip() or None,
            pincode=pincode.strip() or None,
            is_active=is_active,
        )

        service.create(customer)

        response = RedirectResponse(
            "/customers",
            status_code=303,
        )

        response.set_cookie(
            key="flash_success",
            value="Customer added successfully.",
            max_age=5,
        )

        return response

    except (ValueError, ValidationError) as e:

        response = RedirectResponse(
            "/customers",
            status_code=303,
        )

        response.set_cookie(
            key="flash_error",
            value=str(e),
            max_age=5,
        )

        return response


@router.post("/customers/{customer_id}/edit")
async def edit_customer(
    customer_id: int,
    customer_code: str = Form(...),
    customer_name: str = Form(...),
    phone: str = Form(...),
    email: str = Form(""),
    gstin: str = Form(""),
    address: str = Form(""),
    city: str = Form(""),
    state: str = Form(""),
    pincode: str = Form(""),
    is_active: bool = Form(False),
    db: Session = Depends(get_db),
):
    service = CustomerService(db)

    try:
        customer = CustomerUpdate(
            customer_code=customer_code.strip(),
            customer_name=customer_name.strip(),
            phone=phone.strip(),
            email=email.strip() or None,
            gstin=gstin.strip().upper() or None,
            address=address.strip() or None,
            city=city.strip() or None,
            state=state.strip() or None,
            pincode=pincode.strip() or None,
            is_active=is_active,
        )

        service.update(customer_id, customer)

        response = RedirectResponse(
            "/customers",
            status_code=303,
        )

        response.set_cookie(
            key="flash_success",
            value="Customer updated successfully.",
            max_age=5,
        )

        return response

    except (ValueError, ValidationError) as e:

        response = RedirectResponse(
            "/customers",
            status_code=303,
        )

        response.set_cookie(
            key="flash_error",
            value=str(e),
            max_age=5,
        )

        return response


@router.post("/customers/{customer_id}/delete")
async def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db),
):
    service = CustomerService(db)

    try:
        service.delete(customer_id)

        response = RedirectResponse(
            "/customers",
            status_code=303,
        )

        response.set_cookie(
            key="flash_success",
            value="Customer deleted successfully.",
            max_age=5,
        )

        return response

    except ValueError as e:

        response = RedirectResponse(
            "/customers",
            status_code=303,
        )

        response.set_cookie(
            key="flash_error",
            value=str(e),
            max_age=5,
        )

        return response