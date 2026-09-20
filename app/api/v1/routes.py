from uuid import UUID
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.corpus import Track, GlossaryTerm, Dialect, LyricLine, LineTermMapping
from app.schemas.corpus import GlossaryTermResponse, TrackAnnotatedResponse, AnnotationSchema, LyricLineAnnotatedSchema
from app.core.db import get_async_session

router = APIRouter(prefix="/api/v1", tags=["Corpus"])

@router.get("/glossary/search", response_model=List[GlossaryTermResponse])
async def search_glossary(
    query: str = Query(..., min_length=2, description="Term to search for"),
    dialect: Optional[str] = Query(None, description="Dialect code like es-GT, quc, or kek"),
    db: AsyncSession = Depends(get_async_session)
):
    stmt = select(GlossaryTerm).join(GlossaryTerm.dialect_rel)
    
    if dialect:
        stmt = stmt.where(Dialect.code == dialect)
        
    stmt = stmt.where(GlossaryTerm.term.ilike(f"%{query}%"))
    result = await db.execute(stmt)
    terms = result.scalars().all()

    return [
        GlossaryTermResponse(
            id=t.id,
            term=t.term,
            dialect_code=t.dialect_rel.code,
            region=t.dialect_rel.region,
            literal_translation=t.literal_translation,
            contextual_notes=t.contextual_notes
        )
        for t in terms
    ]

@router.get("/tracks/{track_id}/annotated", response_model=TrackAnnotatedResponse)
async def get_annotated_track(
    track_id: UUID,
    db: AsyncSession = Depends(get_async_session)
):
    stmt = (
        select(Track)
        .where(Track.id == track_id)
        .options(
            selectinload(Track.lines)
            .selectinload(LyricLine.annotations)
            .selectinload(LineTermMapping.term)
        )
    )
    
    result = await db.execute(stmt)
    track = result.scalar_one_or_none()

    if not track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Track not found")

    annotated_lines = []
    for line in track.lines:
        annotations = [
            AnnotationSchema(
                term_id=m.term.id,
                term=m.term.term,
                start_char=m.start_char,
                end_char=m.end_char,
                literal_translation=m.term.literal_translation,
                contextual_notes=m.term.contextual_notes,
            )
            for m in line.annotations
        ]
        
        annotated_lines.append(
            LyricLineAnnotatedSchema(
                line_number=line.line_number,
                raw_text=line.raw_text,
                standard_translation=line.standard_translation,
                annotations=annotations,
            )
        )

    return TrackAnnotatedResponse(
        id=track.id,
        title=track.title,
        artist=track.artist,
        primary_language=track.primary_language,
        lines=annotated_lines,
    )
