import uuid
from typing import List, Optional
from sqlalchemy import String, Text, Integer, ForeignKey, Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

class Base(DeclarativeBase):
    pass

class Dialect(Base):
    __tablename__ = "dialects"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String(10), unique=True, index=True)  # e.g., 'es-GT', 'quc', 'kek'
    name: Mapped[str] = mapped_column(String(100))                          # e.g., 'Guatemalan Spanish', 'K'iche''
    region: Mapped[Optional[str]] = mapped_column(String(100))               # e.g., 'Guatemala'

    terms: Mapped[List["GlossaryTerm"]] = relationship(back_populates="dialect_rel")


class GlossaryTerm(Base):
    __tablename__ = "glossary_terms"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    term: Mapped[str] = mapped_column(String(150), index=True)
    dialect_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("dialects.id"), index=True)
    literal_translation: Mapped[str] = mapped_column(Text)
    contextual_notes: Mapped[Optional[str]] = mapped_column(Text)

    dialect_rel: Mapped["Dialect"] = relationship(back_populates="terms")
    line_mappings: Mapped[List["LineTermMapping"]] = relationship(back_populates="term")

    __table_args__ = (
        Index("idx_term_dialect", "term", "dialect_id"),
    )


class Track(Base):
    __tablename__ = "tracks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(200), index=True)
    artist: Mapped[str] = mapped_column(String(200))
    primary_language: Mapped[str] = mapped_column(String(10), default="es")

    lines: Mapped[List["LyricLine"]] = relationship(
        back_populates="track", cascade="all, delete-orphan", order_by="LyricLine.line_number"
    )


class LyricLine(Base):
    __tablename__ = "lyric_lines"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    track_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tracks.id", ondelete="CASCADE"), index=True)
    line_number: Mapped[int] = mapped_column(Integer)
    raw_text: Mapped[str] = mapped_column(Text)
    standard_translation: Mapped[str] = mapped_column(Text)

    track: Mapped["Track"] = relationship(back_populates="lines")
    annotations: Mapped[List["LineTermMapping"]] = relationship(
        back_populates="line", cascade="all, delete-orphan"
    )


class LineTermMapping(Base):
    __tablename__ = "line_term_mappings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    line_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("lyric_lines.id", ondelete="CASCADE"), index=True)
    glossary_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("glossary_terms.id"), index=True)
    start_char: Mapped[int] = mapped_column(Integer)
    end_char: Mapped[int] = mapped_column(Integer)

    line: Mapped["LyricLine"] = relationship(back_populates="annotations")
    term: Mapped["GlossaryTerm"] = relationship(back_populates="line_mappings")
