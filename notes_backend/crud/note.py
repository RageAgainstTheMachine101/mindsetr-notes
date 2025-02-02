"""CRUD operations for notes."""
from sqlalchemy.orm import Session

from notes_backend.models.notes import Note
from notes_backend.schemas.note import NoteCreate, NoteUpdate
from notes_backend.models.enums import NoteType, InsightState


class CRUDNote:
    def create_note(self, db: Session, note: NoteCreate) -> Note:
        """Create a new note."""
        is_insight = note.type == NoteType.AI_INSIGHT
        db_note = Note(
            text=note.text,
            type=note.type,
            tags=note.tags,
            file_path=note.file_path,
            editable=not is_insight,
            insight_state=InsightState.DEFAULT if is_insight else None
        )
        db.add(db_note)
        db.commit()
        db.refresh(db_note)
        return db_note

    def get_note(self, db: Session, note_id: int) -> Note | None:
        """Get a note by ID."""
        return db.query(Note).filter(Note.id == note_id).first()

    def get_notes(self, db: Session, skip: int = 0, limit: int = 100) -> list[Note]:
        """Get all notes with pagination."""
        return db.query(Note).offset(skip).limit(limit).all()

    def update_note(self, db: Session, note_id: int, note: NoteUpdate) -> Note | None:
        """Update a note."""
        db_note = self.get_note(db, note_id)
        if not db_note:
            return None
        if not db_note.editable:
            raise ValueError("Cannot update a non-editable note")
        
        update_data = note.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_note, key, value)
        
        db.commit()
        db.refresh(db_note)
        return db_note

    def delete_note(self, db: Session, note_id: int) -> Note | None:
        """Delete a note."""
        db_note = self.get_note(db, note_id)
        if not db_note:
            return None
        db.delete(db_note)
        db.commit()
        return db_note

    def resolve_insight(self, db: Session, note_id: int) -> Note | None:
        """Resolve an AI insight note."""
        db_note = self.get_note(db, note_id)
        if not db_note or db_note.type != NoteType.AI_INSIGHT:
            return None
        db_note.insight_state = InsightState.RESOLVED
        db.commit()
        db.refresh(db_note)
        return db_note


note = CRUDNote()
