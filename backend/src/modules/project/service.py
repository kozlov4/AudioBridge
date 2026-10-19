import os
import shutil

from fastapi import HTTPException, UploadFile

UPLOAD_DIR = "media"
os.makedirs(UPLOAD_DIR, exist_ok=True)

MAX_FILE_SIZE_MB = 200
ALLOWED_CONTENT_TYPES = ["video/mp4", "audio/mpeg", "audio/wav"]


async def process_file_upload(file: UploadFile) -> tuple[str, float]:
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Формат не підтримується. Дозволені формати: MP4, MP3, WAV",
        )

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    if file_size_mb > MAX_FILE_SIZE_MB:
        os.remove(file_path)
        raise HTTPException(
            status_code=400,
            detail="Файл перевищує максимальний розмір (200 МБ)",
        )

    return file_path, file_size_mb
