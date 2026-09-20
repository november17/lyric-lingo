from uuid import UUID
from typing import List, Optional
from pydantic import BaseModel, ConfigDict

class GlossaryTermResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    term: str
    dialect_code: str
    region: Optional[str]
    literal_translation: str
    contextual_notes: Optional[str]

class AnnotationSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    term_id: UUID
    term: str
    start_char: int
    end_char: int
    literal_translation: str
    contextual_notes: Optional[str]

class LyricLineAnnotatedSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    line_number: int
    raw_text: str
    standard_translation: str
    annotations: List[AnnotationSchema]

class TrackAnnotatedResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    artist: str
    primary_language: str
    lines: List[LyricLineAnnotatedSchema]
