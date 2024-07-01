import json
from datetime import date
from pathlib import Path

import polars as pl
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from api.libs import observations, observations_calendar, utils
from api.libs.observations_config import ObservationsMonthly


class ObservationsAgg(BaseModel):
    filename: str
    overwrite: bool = False


class ObservationsAggRes(BaseModel):
    output_daily: str
    output_monthly: str


class ObservationsDrawPreviewRes(BaseModel):
    img: str


class ObservationsDrawSave(BaseModel):
    input: str
    config: str
    format: str
    dpi: int = 300
    overwrite: bool = False


class ObservationsDrawSaveRes(BaseModel):
    output: str


class ObsDay(BaseModel):
    date: date
    obs: bool


class ObservationsCalendarRes(BaseModel):
    calendar: list[list[ObsDay]]


router = APIRouter(prefix="/observations", tags=["observations"])


@router.post("/agg", response_model=ObservationsAggRes)
def observations_agg(body: ObservationsAgg) -> ObservationsAggRes:
    input_path = Path(body.filename)
    if not input_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {input_path} not found"
        )
    output_dir = Path("out/observations") / input_path.stem
    output_dir.mkdir(exist_ok=True, parents=True)
    output_paths = {
        "daily": output_dir / "daily.parquet",
        "monthly": output_dir / "monthly.parquet",
    }
    for path in output_paths.values():
        if not body.overwrite and path.exists():
            raise HTTPException(
                status_code=400, detail=f"file {path} already exists"
            )
    df = pl.scan_parquet(input_path)
    start, end = observations.adjust_dates(*observations.calc_date_range(df))
    df_daily = observations.calc_dayly_obs(df, start, end).collect()
    df_daily.write_parquet(output_paths["daily"])
    df_monthly = observations.calc_monthly_obs(df_daily.lazy()).collect()
    df_monthly.write_parquet(output_paths["monthly"])
    return ObservationsAggRes(
        output_daily=str(output_paths["daily"]),
        output_monthly=str(output_paths["monthly"]),
    )


@router.get("/draw/monthly", response_model=ObservationsDrawPreviewRes)
def observations_draw_monthly_preview(
    filename: str, config_name: str
) -> ObservationsDrawPreviewRes:
    input_path = Path(filename)
    if not input_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {input_path} not found"
        )
    config_path = Path(config_name)
    if not config_path.exists():
        raise HTTPException(
            status_code=404, detail=f"config {config_path} not found"
        )
    try:
        with config_path.open("r") as f:
            config = ObservationsMonthly(**json.load(f))
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"config {config_path} is broken"
        ) from e
    df = pl.read_parquet(input_path)
    fig = observations.draw_monthly_obs_days(df, config)
    img = utils.fig_to_base64(fig)
    return ObservationsDrawPreviewRes(img=img)


@router.post("/draw/monthly", response_model=ObservationsDrawSaveRes)
def observations_draw_monthly_save(
    body: ObservationsDrawSave,
) -> ObservationsDrawSaveRes:
    input_path = Path(body.input)
    if not input_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {input_path} not found"
        )
    config_path = Path(body.config)
    if not config_path.exists():
        raise HTTPException(
            status_code=404, detail=f"config {config_path} not found"
        )
    output_path = input_path.with_name(f"monthly.{body.format}")
    if not body.overwrite and output_path.exists():
        raise HTTPException(
            status_code=400, detail=f"file {output_path} already exists"
        )
    try:
        with config_path.open("r") as f:
            config = ObservationsMonthly(**json.load(f))
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"config {config_path} is broken"
        ) from e
    df = pl.read_parquet(input_path)
    fig = observations.draw_monthly_obs_days(df, config)
    fig.savefig(
        output_path,
        format=body.format,
        dpi=body.dpi,
        bbox_inches="tight",
        pad_inches=0.1,
    )
    return ObservationsDrawSaveRes(output=str(output_path))


@router.get("/calendar", response_model=ObservationsCalendarRes)
def observations_get_calendar(
    filename: str, year: int, month: int, first: int = 0
) -> ObservationsCalendarRes:
    input_path = Path(filename)
    df = pl.read_parquet(input_path)
    cal = observations_calendar.create_calendar(df, year, month, first)
    return ObservationsCalendarRes(
        calendar=[
            [ObsDay(date=day.date, obs=day.obs == 1) for day in week]
            for week in cal["calendar"]
        ]
    )
