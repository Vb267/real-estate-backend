from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, database
from app.utils.jwt_handler import get_current_user

router = APIRouter(prefix="/listings", tags=["Listings"])


@router.post("/")
def create_listing(
    title: str,
    description: str,
    price: float,
    location: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db),
):
    new_listing = models.Listing(
        title=title,
        description=description,
        price=price,
        location=location,
        owner_id=current_user.id,
    )
    db.add(new_listing)
    db.commit()
    db.refresh(new_listing)
    return new_listing


@router.get("/")
def get_listings(
    skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)
):
    listings = db.query(models.Listing).offset(skip).limit(limit).all()
    return listings


@router.get("/{listing_id}")
def get_listing(listing_id: int, db: Session = Depends(database.get_db)):
    listing = db.query(models.Listing).filter(models.Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing
