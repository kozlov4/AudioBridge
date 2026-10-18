from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Float, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.base import Base

if TYPE_CHECKING:
    from src.modules.subtitle.models import SubtitleTrack
    from src.modules.user.models import User


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    file_name: Mapped[str] = mapped_column(String(255))
    file_path: Mapped[str] = mapped_column(String)
    file_size_mb: Mapped[float] = mapped_column(Float, nullable=True)
    duration_seconds: Mapped[float] = mapped_column(Float, nullable=True)

    status: Mapped[str] = mapped_column(String(50), default="uploaded")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    owner: Mapped[User] = relationship(back_populates="projects")
    subtitle_tracks: Mapped[list[SubtitleTrack]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
