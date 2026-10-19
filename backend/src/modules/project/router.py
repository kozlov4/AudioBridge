import os
from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.db_helper import db_helper
from src.modules.project.models import Project
from src.modules.project.schemas import ProjectResponse
from src.modules.project.service import process_file_upload
from src.modules.user.dependencies import get_current_user

router = APIRouter(prefix="/projects", tags=["Project"])
SessionDep = Annotated[AsyncSession, Depends(db_helper.session_dependency)]


@router.post("/upload", response_model=ProjectResponse)
async def upload_project_file(
    session: SessionDep,
    file: UploadFile = File(...),
    current_user_id: int = Depends(get_current_user),
):
    file_path, file_size_mb = await process_file_upload(file)

    new_project = Project(
        user_id=current_user_id,
        file_name=file.filename,
        file_path=file_path,
        file_size_mb=file_size_mb,
        status="uploaded",
    )
    session.add(new_project)
    await session.commit()
    await session.refresh(new_project)

    return new_project


@router.get("", response_model=list[ProjectResponse])
async def get_my_projects(
    session: SessionDep,
    current_user_id: int = Depends(get_current_user),
):
    stmt = select(Project).where(Project.user_id == current_user_id)
    result = await session.execute(stmt)
    return result.scalars().all()


@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
    session: SessionDep,
    current_user_id: int = Depends(get_current_user),
):
    stmt = select(Project).where(
        Project.id == project_id, Project.user_id == current_user_id
    )
    result = await session.execute(stmt)
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(
            status_code=404, detail="Проєкт не знайдено або доступ заборонено"
        )

    if os.path.exists(project.file_path):
        os.remove(project.file_path)

    await session.delete(project)
    await session.commit()

    return {"message": "Проект успішно видалено"}
