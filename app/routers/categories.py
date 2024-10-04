from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=schemas.Category)
def create_category(
    category: schemas.CategoryCreate, db: Session = Depends(database.get_db)
):
    db_category = (
        db.query(models.Category).filter(models.Category.name == category.name).first()
    )
    if db_category:
        raise HTTPException(status_code=400, detail="Category already exists")

    new_category = models.Category(name=category.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@router.get("/", response_model=List[schemas.Category])
def get_categories(db: Session = Depends(database.get_db)):
    return db.query(models.Category).all()
