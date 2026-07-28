from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.purchase import PurchaseCreate
from app.services.purchase_service import PurchaseService

router = APIRouter(
    prefix="/api/purchases",
    tags=["Purchases"],
)


# -------------------------
# Create Purchase
# -------------------------

@router.post("")
def create_purchase(
    purchase: PurchaseCreate,
    db: Session = Depends(get_db),
):
    service = PurchaseService(db)

    return service.create(purchase)


# -------------------------
# Get All Purchases
# -------------------------

@router.get("")
def get_all_purchases(
    db: Session = Depends(get_db),
):
    service = PurchaseService(db)

    return service.get_all()


# -------------------------
# Get Purchase By ID
# -------------------------

@router.get("/{purchase_id}")
def get_purchase(
    purchase_id: int,
    db: Session = Depends(get_db),
):
    service = PurchaseService(db)

    return service.get_by_id(
        purchase_id
    )