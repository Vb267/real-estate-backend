from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, database
from app.utils.jwt_handler import get_current_user

router = APIRouter(prefix="/listings", tags=["Listings"])

from app.schemas import ListingCreate, Listing


@router.post("/", response_model=Listing)
def create_listing(
    listing: ListingCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(database.get_db),
):
    new_listing = models.Listing(
        title=listing.title,
        description=listing.description,
        price=listing.price,
        location=listing.location,
        owner_id=current_user["user"].id,
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


@router.put("/{listing_id}")
def update_listing(
    listing_id: int,
    title: str = None,
    description: str = None,
    price: float = None,
    location: str = None,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(database.get_db),
):
    listing = db.query(models.Listing).filter(models.Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")

    if current_user["role"] != "admin" and listing.owner_id != current_user["user"].id:
        raise HTTPException(status_code=403, detail="Not authorized")

    if title:
        listing.title = title
    if description:
        listing.description = description
    if price:
        listing.price = price
    if location:
        listing.location = location

    db.commit()
    db.refresh(listing)
    return listing


@router.delete("/{listing_id}")
def delete_listing(
    listing_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db),
):
    listing = (
        db.query(models.Listing)
        .filter(
            models.Listing.id == listing_id, models.Listing.owner_id == current_user.id
        )
        .first()
    )
    if not listing:
        raise HTTPException(
            status_code=404, detail="Listing not found or not authorized"
        )

    db.delete(listing)
    db.commit()
    return {"message": "Listing deleted successfully"}
