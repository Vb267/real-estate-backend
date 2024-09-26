from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from models import Property
from database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/properties/")
def read_properties(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    properties = db.query(Property).offset(skip).limit(limit).all()
    return properties
