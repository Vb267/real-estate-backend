from fastapi import FastAPI
from app.routers import listings, auth

app = FastAPI()

# Register routers for endpoints
app.include_router(listings.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Welcome to the Real Estate Listings API"}
