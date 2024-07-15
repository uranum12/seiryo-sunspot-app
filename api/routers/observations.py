from datetime import date
from pathlib import Path

import polars as pl
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from api.libs import observations, observations_calendar
from api.routers.config.observations import router as router_config
from api.routers.draw.observations import router as router_draw


class ObservationsAgg(BaseModel):
    filename: str
    overwrite: bool = False


class ObservationsAggRes(BaseModel):
    output_daily: str
    output_monthly: str


class ObsDay(BaseModel):
    date: date
    obs: bool


class ObservationsCalendarRes(BaseModel):
    calendar: list[list[ObsDay]]


router = APIRouter(prefix="/observations", tags=["observations"])
router.include_router(router_config)
router.include_router(router_draw)


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
