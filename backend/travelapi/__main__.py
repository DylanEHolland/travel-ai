from typing import List
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .models import SessionLocal, Destinations
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,  # Allow cookies or authentication
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers (Authorization, Content-Type, etc.)
)

@app.get("/")
def read_root() -> dict[object, object]:
    return {}

@app.get("/destinations")
def read_destinations(db: Session = Depends(get_db)) -> dict[object, object]:
    destinations: List[Destinations] = db.query(Destinations).all()     
    return {"destinations": [destination.to_dict() for destination in destinations]}

@app.post("/destinations")
def create_destination(destination: dict[object, object], db: Session = Depends(get_db)) -> dict[object, object]:
    new_destination: Destinations = Destinations(name=destination["name"])

    db.add(new_destination)
    db.commit()
    db.refresh(new_destination) 

    return {
        "id": new_destination.id,
        "name": new_destination.name,
        "created_at": new_destination.created_at,
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

