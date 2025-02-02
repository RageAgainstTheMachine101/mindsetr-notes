from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from notes_backend import schemas, crud
from notes_backend.database import get_db

router = APIRouter(prefix="/notes", tags=["notes"])

@router.post("/", response_model=schemas.NoteResponse)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    return crud.note.create_note(db, note=note)

@router.put("/{note_id}", response_model=schemas.NoteResponse)
def update_note(note_id: int, note: schemas.NoteUpdate, db: Session = Depends(get_db)):
    db_note = crud.note.update_note(db, note_id=note_id, note=note)
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    return db_note

@router.delete("/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    db_note = crud.note.delete_note(db, note_id=note_id)
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"ok": True}

@router.post("/{note_id}/resolve", response_model=schemas.NoteResponse)
def resolve_insight(note_id: int, db: Session = Depends(get_db)):
    db_note = crud.note.resolve_insight(db, note_id=note_id)
    if not db_note:
        raise HTTPException(status_code=400, detail="Cannot resolve this note")
    return db_note
