from enum import Enum
from datetime import datetime
from datetime import timezone as tz
from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, ForeignKey
from notes_backend.database import Base
from notes_backend.models.enums import NoteType, InsightState

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(tz.utc))
    type = Column(String, nullable=False)
    text = Column(String, nullable=False)
    tags = Column(JSON)
    updated_at = Column(DateTime, onupdate=lambda: datetime.now(tz.utc))
    editable = Column(Boolean, default=True)
    file_path = Column(String)  # For voice recordings
    
    # Insight-specific fields
    from_thread_id = Column(Integer, ForeignKey('notes.id'))
    insight_state = Column(String)

    def __repr__(self):
        return f"<Note(id={self.id}, type={self.type})>"
