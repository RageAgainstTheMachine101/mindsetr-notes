from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from notes_backend.models.enums import NoteType, InsightState

class NoteBase(BaseModel):
    text: str = Field(..., min_length=1)
    tags: Optional[List[str]] = None
    file_path: Optional[str] = None  # Path to voice recording

class NoteCreate(NoteBase):
    type: NoteType = NoteType.USER_NOTE

class NoteUpdate(NoteBase):
    text: Optional[str] = None
    tags: Optional[List[str]] = None

class NoteResponse(NoteBase):
    id: int
    type: NoteType
    created_at: datetime
    updated_at: Optional[datetime] = None
    editable: bool
    insight_state: Optional[InsightState] = None
    from_thread_id: Optional[int] = None

    @field_validator('editable', mode='before')
    def set_editable(cls, v, info):
        if 'type' in info.data and info.data['type'] == NoteType.AI_INSIGHT:
            return False
        return v
