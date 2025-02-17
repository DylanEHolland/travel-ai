from typing import List
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .helpers import create_embeddings, runAugmentedChat, save_to_knowledge_base
from .models import KnowledgeBase, SessionLocal, Destinations, get_db
app = FastAPI()

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

@app.get("/destinations/{destination_id}")
def read_destination(destination_id: str, db: Session = Depends(get_db)) -> dict[object, object]:
    destination: Destinations = db.query(Destinations).filter(Destinations.id == destination_id).first()
    return {"destination": destination.to_dict()}

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

@app.get("/knowledgebase/{destination_id}")
def read_knowledgebase(destination_id: str, db: Session = Depends(get_db)) -> dict[object, object]:
    knowledgebase: List[KnowledgeBase] = db.query(KnowledgeBase).filter(KnowledgeBase.destination_id == destination_id).all()
    return {"knowledgebase": [knowledgebase.to_dict() for knowledgebase in knowledgebase]}

@app.post("/knowledgebase")
def create_knowledgebase_item(knowledgebase_item: dict[object, object], db: Session = Depends(get_db)) -> dict[object, object]:
    new_knowledgebase_item = save_to_knowledge_base(db, knowledgebase_item["destinationId"], knowledgebase_item["content"])
    return {
        "id": new_knowledgebase_item.id,
    }

@app.post("/chat")
def chat(chat_message: dict[object, object], db: Session = Depends(get_db)) -> dict[object, object]:
    print("got here")
    response = runAugmentedChat(chat_message['message'], chat_message['destinationId'])
    return {
        "response": response["response"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

