# notes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from jwt_utils import verify_token
from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base, engine

router = APIRouter()

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    owner_email = Column(String, ForeignKey("users.email"))

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/notes")
def create_note(title: str, content: str, email: str = Depends(verify_token), db: Session = Depends(get_db)):
    note = Note(title=title, content=content, owner_email=email)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

@router.get("/notes")
def get_notes(email: str = Depends(verify_token), db: Session = Depends(get_db)):
    return db.query(Note).filter(Note.owner_email == email).all()

@router.put("/notes/{note_id}")
def update_note(note_id: int, title: str, content: str, email: str = Depends(verify_token), db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id, Note.owner_email == email).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    note.title = title
    note.content = content
    db.commit()
    db.refresh(note)
    return note

@router.delete("/notes/{note_id}")
def delete_note(note_id: int, email: str = Depends(verify_token), db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id, Note.owner_email == email).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
    return {"message": "Note deleted successfully"}
