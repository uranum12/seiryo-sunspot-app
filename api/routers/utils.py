import csv
from pathlib import Path

import matplotlib.font_manager as fm
import nkf
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel


class FilesRes(BaseModel):
    files: list[str]


class FileCsvQuery(BaseModel):
    input: str


class FileCsvRes(BaseModel):
    data: list[list[str | None]]


class FontsRes(BaseModel):
    names: list[str]


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
    with input_path.open("rb") as fb:
        encoding = nkf.guess(fb.read()).lower()
    with input_path.open("r", encoding=encoding) as f:
        reader = csv.reader(f)
        data = list(reader)
    max_len = max(len(row) for row in data)
    return FileCsvRes(
        data=[(row + [None] * max_len)[:max_len] for row in data]
    )


@router.get("/fonts", response_model=FontsRes)
def fonts() -> FontsRes:
    font_paths = fm.findSystemFonts(fontpaths=None, fontext="ttf")
    fonts_set = {
        fm.FontProperties(fname=path).get_name() for path in font_paths
    }
    return FontsRes(names=list(fonts_set))
