from enum import Enum

class NoteType(str, Enum):
    USER_NOTE = "user_note"
    AI_INSIGHT = "ai_insight"

class InsightState(str, Enum):
    DEFAULT = "default"
    RESOLVED = "resolved"
