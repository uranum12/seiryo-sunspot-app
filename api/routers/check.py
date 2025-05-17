from pathlib import Path
from typing import Literal, TypeAlias

import nkf
import polars as pl
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from seiryo_sunspot_lib import check_data, check_file, finder


class CheckFileErrorHeader(BaseModel):
    type: Literal["header"]
    header: list[str] | None


class CheckFileErrorRow(BaseModel):
    type: Literal["row"]
    line: int
    over: list[str]


class CheckFileErrorField(BaseModel):
    type: Literal["field"]
    line: int
    fields: list[str]


CheckFileError: TypeAlias = (
    CheckFileErrorHeader | CheckFileErrorRow | CheckFileErrorField
)


class CheckFileQuery(BaseModel):
    input: str


class CheckFileRes(BaseModel):
    errors: list[CheckFileError]


class CheckDataGroupNumberQuery(BaseModel):
    input: str


class CheckDataGroupNumberRes(BaseModel):
    date: list[str]
    original: list[list[int]]
    expected: list[list[int]]


class CheckDataLatRangeQuery(BaseModel):
    input: str
    threshold: int


class CheckDataLatRangeRes(BaseModel):
    date: list[str]
    no: list[int]
    lat_min: list[int]
    lat_max: list[int]


class CheckDataLonRangeQuery(BaseModel):
    input: str
    min_threshold: int
    max_threshold: int


class CheckDataLonRangeRes(BaseModel):
    date: list[str]
    no: list[int]
    lon_min: list[int]
    lon_max: list[int]


class CheckDataLatIntervalQuery(BaseModel):
    input: str
    interval: int


class CheckDataLatIntervalRes(BaseModel):
    date: list[str]
    no: list[int]
    lat_min: list[int]
    lat_max: list[int]
    interval: list[int]


class CheckDataLonIntervalQuery(BaseModel):
    input: str
    interval: int


class CheckDataLonIntervalRes(BaseModel):
    date: list[str]
    no: list[int]
    lon_min: list[int]
    lon_max: list[int]
    interval: list[int]


class FinderQuery(BaseModel):
    year: int
    month: int
    day: int


class FinderRes(BaseModel):
    result: list[finder.FinderResult]


router = APIRouter(prefix="/check", tags=["check"])


@router.get("/file", response_model=CheckFileRes)
def validate_file(query: CheckFileQuery = Depends()) -> CheckFileRes:
    input_path = Path(query.input)
    if not input_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {input_path} not found"
        )
    with input_path.open("rb") as fb:
        encoding = nkf.guess(fb.read()).lower()
    with input_path.open("r", encoding=encoding) as f:
        ret = check_file.validate_file(f)
    errors: list[CheckFileError] = []
    for err in ret:
        match err["type"]:
            case "header":
                errors.append(CheckFileErrorHeader(**err))
            case "row":
                errors.append(CheckFileErrorRow(**err))
            case "field":
                errors.append(CheckFileErrorField(**err))
    return CheckFileRes(errors=errors)


@router.get("/data/group_number", response_model=CheckDataGroupNumberRes)
def invalid_group_number(
    query: CheckDataGroupNumberQuery = Depends(),
) -> CheckDataGroupNumberRes:
    input_path = Path(query.input)
    if not input_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {input_path} not found"
        )
    file = pl.read_parquet(input_path)
    df = check_data.find_invalid_group_number(file)
    df = df.sort("date").with_columns(pl.col("date").dt.to_string("%Y-%m-%d"))
    data = df.to_dict(as_series=False)
    return CheckDataGroupNumberRes(
        date=data["date"], original=data["original"], expected=data["expected"]
    )


@router.get("/data/lat_range", response_model=CheckDataLatRangeRes)
def invalid_lat_range(
    query: CheckDataLatRangeQuery = Depends(),
) -> CheckDataLatRangeRes:
    input_path = Path(query.input)
    if not input_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {input_path} not found"
        )
    file = pl.read_parquet(input_path)
    df = check_data.find_invalid_lat_range(file, query.threshold)
    df = (
        df.select("date", "no", "lat_min", "lat_max")
        .sort("date", "no")
        .with_columns(pl.col("date").dt.to_string("%Y-%m-%d"))
    )
    data = df.to_dict(as_series=False)
    return CheckDataLatRangeRes(
        date=data["date"],
        no=data["no"],
        lat_min=data["lat_min"],
        lat_max=data["lat_max"],
    )


@router.get("/data/lon_range", response_model=CheckDataLonRangeRes)
def invalid_lon_range(
    query: CheckDataLonRangeQuery = Depends(),
) -> CheckDataLonRangeRes:
    input_path = Path(query.input)
    if not input_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {input_path} not found"
        )
    file = pl.read_parquet(input_path)
    df = check_data.find_invalid_lon_range(
        file, query.min_threshold, query.max_threshold
    )
    df = (
        df.select("date", "no", "lon_min", "lon_max")
        .sort("date", "no")
        .with_columns(pl.col("date").dt.to_string("%Y-%m-%d"))
    )
    data = df.to_dict(as_series=False)
    return CheckDataLonRangeRes(
        date=data["date"],
        no=data["no"],
        lon_min=data["lon_min"],
        lon_max=data["lon_max"],
    )


@router.get("/data/lat_interval", response_model=CheckDataLatIntervalRes)
def invalid_lat_interval(
    query: CheckDataLatIntervalQuery = Depends(),
) -> CheckDataLatIntervalRes:
    input_path = Path(query.input)
    if not input_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {input_path} not found"
        )
    file = pl.read_parquet(input_path)
    df = check_data.find_invalid_lat_interval(file, query.interval)
    df = (
        df.select("date", "no", "lat_min", "lat_max", "interval")
        .sort("date", "no")
        .with_columns(pl.col("date").dt.to_string("%Y-%m-%d"))
    )
    data = df.to_dict(as_series=False)
    return CheckDataLatIntervalRes(
        date=data["date"],
        no=data["no"],
        lat_min=data["lat_min"],
        lat_max=data["lat_max"],
        interval=data["interval"],
    )


@router.get("/data/lon_interval", response_model=CheckDataLonIntervalRes)
def invalid_lon_interval(
    query: CheckDataLonIntervalQuery = Depends(),
) -> CheckDataLonIntervalRes:
    input_path = Path(query.input)
    if not input_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {input_path} not found"
        )
    file = pl.read_parquet(input_path)
    df = check_data.find_invalid_lon_interval(file, query.interval)
    df = (
        df.select("date", "no", "lon_min", "lon_max", "interval")
        .sort("date", "no")
        .with_columns(pl.col("date").dt.to_string("%Y-%m-%d"))
    )
    data = df.to_dict(as_series=False)
    return CheckDataLonIntervalRes(
        date=data["date"],
        no=data["no"],
        lon_min=data["lon_min"],
        lon_max=data["lon_max"],
        interval=data["interval"],
    )


@router.get("/finder", response_model=FinderRes)
def check_finder(query: FinderQuery = Depends()) -> FinderRes:
    search_path = Path("data")
    result = finder.finder(search_path, query.year, query.month, query.day)
    return FinderRes(result=result)
