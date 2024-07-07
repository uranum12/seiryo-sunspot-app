import csv
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel


class FilesRes(BaseModel):
    files: list[str]


class FileCsvQuery(BaseModel):
    input: str


class FileCsvRes(BaseModel):
    data: list[list[str | None]]


router = APIRouter(prefix="/utils", tags=["utils"])


@router.get("/files", response_model=FilesRes)
def files(path: str, glob: str) -> FilesRes:
    return FilesRes(
        files=[str(file) for file in Path(path).glob(glob) if file.is_file()]
    )


@router.get("/file/csv", response_model=FileCsvRes)
def file_csv(query: FileCsvQuery = Depends()) -> FileCsvRes:
    input_path = Path(query.input)
    if not input_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {input_path} not found"
        )
    with input_path.open("r") as f:
        reader = csv.reader(f)
        data = list(reader)
    max_len = max(len(row) for row in data)
    return FileCsvRes(
        data=[(row + [None] * max_len)[:max_len] for row in data]
    )
