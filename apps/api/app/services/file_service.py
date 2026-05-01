from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import settings

RAW_DATA_DIR = Path("/app/data/raw")
ALLOWED_EXTENSIONS = {".pdf", ".txt", ".docx"}


def validate_uploaded_file(uploaded_file: UploadFile) -> None:
    filename = uploaded_file.filename or ""
    suffix = Path(filename).suffix.lower()

    if suffix not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {suffix or 'unknown'}. Allowed types are: .pdf, .txt, .docx")

    uploaded_file.file.seek(0, 2)
    file_size_bytes = uploaded_file.file.tell()
    uploaded_file.file.seek(0)

    max_size_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024

    if file_size_bytes > max_size_bytes:
        raise ValueError(
            f"File is too large: {file_size_bytes} bytes. Maximum allowed size is {settings.MAX_UPLOAD_SIZE_MB} MB."
        )


def save_uploaded_file(uploaded_file: UploadFile) -> tuple[str, str]:
    """
    Save the uploaded file into /app/data/raw with a unique filename.

    Returns:
        tuple[str, str]: (stored_filename, stored_file_path)
    """
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    unique_filename = f"{uuid4()}_{uploaded_file.filename}"
    file_path = RAW_DATA_DIR / unique_filename

    with open(file_path, "wb") as output_file:
        output_file.write(uploaded_file.file.read())

    return unique_filename, str(file_path)
