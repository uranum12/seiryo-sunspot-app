from pathlib import Path

import polars as pl
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from libs import agg


class AggMain(BaseModel):
    files: list[str]
    filename: str


class AggMainRes(BaseModel):
    output: str


router = APIRouter(prefix="/agg")


@router.post("", response_model=AggMainRes)
def agg_main(body: AggMain) -> AggMainRes:
    output_dir = Path("out")
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / f"{body.filename}.parquet"
    if output_path.exists():
        raise HTTPException(
            status_code=400, detail=f"file {output_path} already exists"
        )
    df = (
        pl.scan_csv(body.files, infer_schema_length=0)
        .pipe(agg.fill_date)
        .pipe(agg.convert_number)
        .pipe(agg.convert_date)
        .pipe(agg.convert_coord, col="lat", dtype=pl.Int8)
        .pipe(agg.convert_coord, col="lon", dtype=pl.Int16)
        .pipe(agg.sort)
        .collect()
    )
    df.write_parquet(output_path)
    return AggMainRes(output=str(output_path))
