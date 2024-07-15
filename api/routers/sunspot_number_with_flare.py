import json
from pathlib import Path

import polars as pl
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from api.libs import sunspot_number_with_flare
from api.routers.config.sunspot_number_with_flare import (
    router as router_config,
)
from api.routers.draw.sunspot_number_with_flare import router as router_draw


class SunspotNumberWithFlareAgg(BaseModel):
    seiryo_path: str
    flare_files_north: list[str]
    flare_files_south: list[str]
    flare_files_total: list[str]
    output_name: str
    overwrite: bool = False


class SunspotNumberWithFlareAggRes(BaseModel):
    output_with_flare: str
    output_factors: str


router = APIRouter(
    prefix="/sunspot_number/with_flare", tags=["sunspot_number", "with_flare"]
)
router.include_router(router_config)
router.include_router(router_draw)


@router.post("/agg", response_model=SunspotNumberWithFlareAggRes)
def with_flare_agg(
    body: SunspotNumberWithFlareAgg,
) -> SunspotNumberWithFlareAggRes:
    seiryo_path = Path(body.seiryo_path)
    if not seiryo_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {seiryo_path} not found"
        )
    files_north = [Path(file) for file in body.flare_files_north]
    files_south = [Path(file) for file in body.flare_files_south]
    files_total = [Path(file) for file in body.flare_files_total]
    for file in files_north + files_south + files_total:
        if not file.exists():
            raise HTTPException(
                status_code=404, detail=f"file {file} not found"
            )
    output_dir = Path("out/sunspot_with_flare") / body.output_name
    output_dir.mkdir(exist_ok=True, parents=True)
    output_paths = {
        "with_flare": output_dir / "with_flare.parquet",
        "factors": output_dir / "flare_factors.json",
    }
    for path in output_paths.values():
        if not body.overwrite and path.exists():
            raise HTTPException(
                status_code=400, detail=f"file {path} already exists"
            )
    df_seiryo = pl.read_parquet(seiryo_path)
    df_flare = sunspot_number_with_flare.load_flare_files(
        files_north, files_south, files_total
    )
    df_with_flare = sunspot_number_with_flare.join_data(df_seiryo, df_flare)
    df_with_flare.write_parquet(output_paths["with_flare"])
    factors = sunspot_number_with_flare.calc_factors(df_with_flare)
    with output_paths["factors"].open("w") as f:
        json.dump(factors, f)
    return SunspotNumberWithFlareAggRes(
        output_with_flare=str(output_paths["with_flare"]),
        output_factors=str(output_paths["factors"]),
    )
