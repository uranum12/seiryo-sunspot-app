from pathlib import Path

from fastapi import APIRouter, Depends
from pydantic import BaseModel


class FilesQuery(BaseModel):
    path: str
    glob: str


class FilesRes(BaseModel):
    files: list[str]


router = APIRouter(prefix="/utils", tags=["utils"])


@router.get("/files", response_model=FilesRes)
def files(query: FilesQuery = Depends()) -> FilesRes:  # noqa: B008
    return FilesRes(
        files=[
            str(file)
            for file in Path(query.path).glob(query.glob)
            if file.is_file()
        ]
    )
