"""
This module contains business logic for note operations.
As the application grows, complex business logic should be moved here from the crud layer.
"""
from typing import List

from ..models.notes import Note
from ..crud.notes import CRUDNote


class NoteService:
    def __init__(self, crud: CRUDNote):
        self.crud = crud

    # Example of a business logic method that could be added in the future:
    # async def get_notes_by_tag(self, tag: str) -> List[Note]:
    #     """Get all notes that have a specific tag."""
    #     pass

    # async def share_note(self, note_id: str, user_id: str) -> Note:
    #     """Share a note with another user."""
    #     pass
