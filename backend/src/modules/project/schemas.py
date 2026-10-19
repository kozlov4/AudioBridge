from datetime import datetime

from pydantic import BaseModel


class ProjectResponse(BaseModel):
    id: int
    user_id: int
    file_name: str
    file_path: str
    file_size_mb: float | None = None
    duration_seconds: float | None = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
