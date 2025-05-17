from pathlib import Path

import polars as pl
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from seiryo_sunspot_lib import sunspot_number

from api.routers.config.sunspot_number import router as router_config
from api.routers.draw.sunspot_number import router as router_draw


class SunspotNumberAgg(BaseModel):
    filename: str
    overwrite: bool = False


class SunspotNumberAggRes(BaseModel):
    output_raw: str
    output_daily: str
    output_monthly: str


router = APIRouter(prefix="/sunspot_number", tags=["sunspot_number"])
router.include_router(router_config)
router.include_router(router_draw)


@router.post("/agg", response_model=SunspotNumberAggRes)
def sunspot_number_main(body: SunspotNumberAgg) -> SunspotNumberAggRes:
    filename = Path(body.filename)
    if not filename.exists():
        raise HTTPException(
            status_code=404, detail=f"file {filename} not found"
        )
    output_dir = Path("out/sunspot") / filename.stem
    output_dir.mkdir(exist_ok=True, parents=True)
    output_paths = {
        "raw": output_dir / "raw.parquet",
        "daily": output_dir / "daily.parquet",
        "monthly": output_dir / "monthly.parquet",
    }
    for path in output_paths.values():
        if not body.overwrite and path.exists():
            raise HTTPException(
                status_code=400, detail=f"file {path} already exists"
            )
    df_spot, df_nospot = sunspot_number.split(pl.scan_parquet(filename))
    df_spot = df_spot.pipe(sunspot_number.calc_lat).pipe(
        sunspot_number.calc_sn
    )
    df_nospot = df_nospot.select("date").pipe(sunspot_number.fill_sn)
    df_raw = (
        pl.concat([df_spot, df_nospot]).pipe(sunspot_number.sort).collect()
    )
    df_raw.write_parquet(output_paths["raw"])
    df_daily = sunspot_number.agg_daily(df_raw)
    df_daily.write_parquet(output_paths["daily"])
    df_monthly = sunspot_number.agg_monthly(df_raw)
    df_monthly.write_parquet(output_paths["monthly"])
    return SunspotNumberAggRes(
        output_raw=str(output_paths["raw"]),
        output_daily=str(output_paths["daily"]),
        output_monthly=str(output_paths["monthly"]),
    )
