import pytest
from datetime import datetime
from fastapi import status
from notes_backend import crud, models
from notes_backend.schemas.note import NoteCreate, NoteUpdate

# Test CRUD operations
def test_create_note(db):
    note_data = NoteCreate(
        text="Test note",
        type="user_note",
        tags=["test"],
        file_path=None
    )
    note = crud.note.create_note(db, note_data)
    assert note.id is not None
    assert note.editable is True
    assert note.type == "user_note"

def test_create_insight(db):
    insight_data = NoteCreate(
        text="AI Insight",
        type="ai_insight",
        tags=["analysis"],
        file_path=None
    )
    insight = crud.note.create_note(db, insight_data)
    assert insight.editable is False
    assert insight.insight_state == "default"

def test_update_note(db):
    note = crud.note.create_note(db, NoteCreate(text="Original", type="user_note"))
    updated = crud.note.update_note(db, note.id, NoteUpdate(text="Updated"))
    assert updated.text == "Updated"

def test_cannot_update_insight(db):
    insight = crud.note.create_note(db, NoteCreate(text="Insight", type="ai_insight"))
    with pytest.raises(ValueError):
        crud.note.update_note(db, insight.id, NoteUpdate(text="Modified"))

# Test API endpoints
def test_create_note_via_api(client):
    response = client.post("/notes/", json={
        "text": "API Test",
        "type": "user_note"
    })
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["editable"] is True

def test_resolve_insight(client, db):
    insight = crud.note.create_note(db, NoteCreate(text="Insight", type="ai_insight"))
    response = client.post(f"/notes/{insight.id}/resolve")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["insight_state"] == "resolved"

def test_delete_note(client, db):
    note = crud.note.create_note(db, NoteCreate(text="To delete", type="user_note"))
    response = client.delete(f"/notes/{note.id}")
    assert response.status_code == status.HTTP_200_OK
    assert db.get(models.Note, note.id) is None
