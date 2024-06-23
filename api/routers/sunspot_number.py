import json
from pathlib import Path

import polars as pl
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from api.libs import sunspot_number, utils
from api.libs.sunspot_number_config import (
    SunspotNumberHemispheric,
    SunspotNumberWholeDisk,
)


class SunspotNumberAgg(BaseModel):
    filename: str
    overwrite: bool = False


class SunspotNumberAggRes(BaseModel):
    output_raw: str
    output_daily: str
    output_monthly: str


class SunspotNumberDrawPreviewRes(BaseModel):
    img: str


class SunspotNumberDrawSave(BaseModel):
    input: str
    config: str
    format: str
    dpi: int = 300
    overwrite: bool = False


class SunspotNumberDrawSaveRes(BaseModel):
    output: str


router = APIRouter(prefix="/sunspot_number", tags=["sunspot_number"])


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


@router.get("/draw/whole_disk", response_model=SunspotNumberDrawPreviewRes)
def sunspot_number_draw_whole_disk(
    filename: str, config_name: str
) -> SunspotNumberDrawPreviewRes:
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
            config = SunspotNumberWholeDisk(**json.load(f))
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"config {config_path} is broken"
        ) from e
    df = pl.read_parquet(input_path)
    fig = sunspot_number.draw_sunspot_number_whole_disk(df, config)
    img = utils.fig_to_base64(fig)
    return SunspotNumberDrawPreviewRes(img=img)


@router.post("/draw/whole_disk", response_model=SunspotNumberDrawSaveRes)
def sunspot_number_save_whole_disk(
    body: SunspotNumberDrawSave,
) -> SunspotNumberDrawSaveRes:
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
    output_path = input_path.with_name(f"whole_disk.{body.format}")
    if not body.overwrite and output_path.exists():
        raise HTTPException(
            status_code=400, detail=f"file {output_path} already exists"
        )
    try:
        with config_path.open("r") as f:
            config = SunspotNumberWholeDisk(**json.load(f))
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"config {config_path} is broken"
        ) from e
    df = pl.read_parquet(input_path)
    fig = sunspot_number.draw_sunspot_number_whole_disk(df, config)
    fig.savefig(
        output_path,
        format=body.format,
        dpi=body.dpi,
        bbox_inches="tight",
        pad_inches=0.1,
    )
    return SunspotNumberDrawSaveRes(output=str(output_path))


@router.get("/draw/hemispheric", response_model=SunspotNumberDrawPreviewRes)
def sunspot_number_draw_hemispheric(
    filename: str, config_name: str
) -> SunspotNumberDrawPreviewRes:
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
            config = SunspotNumberHemispheric(**json.load(f))
    except ValueError as e:
        print(e)
        raise HTTPException(
            status_code=400, detail=f"config {config_path} is broken"
        ) from e
    df = pl.read_parquet(input_path)
    fig = sunspot_number.draw_sunspot_number_hemispheric(df, config)
    img = utils.fig_to_base64(fig)
    return SunspotNumberDrawPreviewRes(img=img)


@router.post("/draw/hemispheric", response_model=SunspotNumberDrawSaveRes)
def sunspot_number_save_hemispheric(
    body: SunspotNumberDrawSave,
) -> SunspotNumberDrawSaveRes:
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
    output_path = input_path.with_name(f"hemispheric.{body.format}")
    if not body.overwrite and output_path.exists():
        raise HTTPException(
            status_code=400, detail=f"file {output_path} already exists"
        )
    try:
        with config_path.open("r") as f:
            config = SunspotNumberHemispheric(**json.load(f))
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"config {config_path} is broken"
        ) from e
    df = pl.read_parquet(input_path)
    fig = sunspot_number.draw_sunspot_number_hemispheric(df, config)
    fig.savefig(
        output_path,
        format=body.format,
        dpi=body.dpi,
        bbox_inches="tight",
        pad_inches=0.1,
    )
    return SunspotNumberDrawSaveRes(output=str(output_path))
