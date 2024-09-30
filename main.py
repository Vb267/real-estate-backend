from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import SessionLocal, engine
from utils import hash_password, verify_password
from auth import create_access_token
from fastapi.security import OAuth2PasswordRequestForm


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create a new property
@app.post("/properties/", response_model=schemas.Property)
def create_property(property: schemas.PropertyCreate, db: Session = Depends(get_db)):
    db_property = models.Property(**property.dict())
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property


# Get all properties
@app.get("/properties/", response_model=List[schemas.Property])
def get_properties(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.Property).offset(skip).limit(limit).all()


# Get a specific property by ID
@app.get("/properties/{property_id}", response_model=schemas.Property)
def get_property(property_id: int, db: Session = Depends(get_db)):
    db_property = (
        db.query(models.Property).filter(models.Property.id == property_id).first()
    )
    if not db_property:
        raise HTTPException(status_code=404, detail="Property not found")
    return db_property


# Update a property by ID
@app.put("/properties/{property_id}", response_model=schemas.Property)
def update_property(
    property_id: int, property: schemas.PropertyCreate, db: Session = Depends(get_db)
):
    db_property = (
        db.query(models.Property).filter(models.Property.id == property_id).first()
    )
    if not db_property:
        raise HTTPException(status_code=404, detail="Property not found")
    for key, value in property.dict().items():
        setattr(db_property, key, value)
    db.commit()
    return db_property


# Delete a property by ID
@app.delete("/properties/{property_id}")
def delete_property(property_id: int, db: Session = Depends(get_db)):
    db_property = (
        db.query(models.Property).filter(models.Property.id == property_id).first()
    )
    if not db_property:
        raise HTTPException(status_code=404, detail="Property not found")
    db.delete(db_property)
    db.commit()
    return {"detail": "Property deleted successfully"}


@app.post("/register/")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    db_user = models.User(
        username=user.username, email=user.email, hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User registered successfully"}


@app.post("/login/", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = (
        db.query(models.User).filter(models.User.username == form_data.username).first()
    )
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
