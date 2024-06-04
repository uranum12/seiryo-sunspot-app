from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel


class FilesRes(BaseModel):
    files: list[str]


router = APIRouter(prefix="/utils", tags=["utils"])


@router.get("/files", response_model=FilesRes)
def files(path: str, glob: str) -> FilesRes:
    return FilesRes(
        files=[str(file) for file in Path(path).glob(glob) if file.is_file()]
    )
