import json
from pathlib import Path

import polars as pl
from fastapi import APIRouter, Depends, HTTPException

from api.libs import sunspot_number, utils
from api.libs.sunspot_number_config import (
    SunspotNumberHemispheric,
    SunspotNumberWholeDisk,
)
from api.models.draw import PreviewQuery, PreviewRes, SaveBody, SaveRes

router = APIRouter(prefix="/draw")


@router.get("/whole_disk", response_model=PreviewRes)
def sunspot_number_draw_whole_disk(
    query: PreviewQuery = Depends(),
) -> PreviewRes:
    input_path = Path(query.filename)
    if not input_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {input_path} not found"
        )
    config_path = Path(query.config_name)
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
    return PreviewRes(img=img)


@router.post("/whole_disk", response_model=SaveRes)
def sunspot_number_save_whole_disk(body: SaveBody) -> SaveRes:
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
    return SaveRes(output=str(output_path))


@router.get("/hemispheric", response_model=PreviewRes)
def sunspot_number_draw_hemispheric(
    query: PreviewQuery = Depends(),
) -> PreviewRes:
    input_path = Path(query.filename)
    if not input_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {input_path} not found"
        )
    config_path = Path(query.config_name)
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
    return PreviewRes(img=img)


@router.post("/hemispheric", response_model=SaveRes)
def sunspot_number_save_hemispheric(body: SaveBody) -> SaveRes:
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
    return SaveRes(output=str(output_path))
