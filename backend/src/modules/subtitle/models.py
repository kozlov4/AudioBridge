from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.base import Base

if TYPE_CHECKING:
    from src.modules.project.models import Project


class SubtitleTrack(Base):
    __tablename__ = "subtitle_tracks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE")
    )

    language: Mapped[str] = mapped_column(String(50))

    track_type: Mapped[str] = mapped_column(String(50), default="original")

    project: Mapped[Project] = relationship(back_populates="subtitle_tracks")
    segments: Mapped[list[SubtitleSegment]] = relationship(
        back_populates="track", cascade="all, delete-orphan"
    )


class SubtitleSegment(Base):
    __tablename__ = "subtitle_segments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    track_id: Mapped[int] = mapped_column(
        ForeignKey("subtitle_tracks.id", ondelete="CASCADE")
    )

    start_time: Mapped[float] = mapped_column(Float)
    end_time: Mapped[float] = mapped_column(Float)

    text: Mapped[str] = mapped_column(Text)

    track: Mapped[SubtitleTrack] = relationship(back_populates="segments")
