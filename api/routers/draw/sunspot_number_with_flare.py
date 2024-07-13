import json
from pathlib import Path

import polars as pl
from fastapi import APIRouter, Depends, HTTPException

from api.libs import sunspot_number_with_flare, utils
from api.libs.sunspot_number_with_flare_config import (
    SunspotNumberWithFlare,
    SunspotNumberWithFlareHemispheric,
)
from api.models.draw import PreviewQuery, PreviewRes, SaveBody, SaveRes

router = APIRouter(prefix="/draw")


@router.get("/with_flare", response_model=PreviewRes)
def draw_with_flare(query: PreviewQuery = Depends()) -> PreviewRes:
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
            config = SunspotNumberWithFlare(**json.load(f))
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"config {config_path} is broken"
        ) from e
    df = pl.read_parquet(input_path)
    fig = sunspot_number_with_flare.draw_sunspot_number_with_flare(df, config)
    img = utils.fig_to_base64(fig)
    return PreviewRes(img=img)


@router.post("/with_flare", response_model=SaveRes)
def save_with_flare(body: SaveBody) -> SaveRes:
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
    output_path = input_path.with_name(f"with_flare.{body.format}")
    if not body.overwrite and output_path.exists():
        raise HTTPException(
            status_code=400, detail=f"file {output_path} already exists"
        )
    try:
        with config_path.open("r") as f:
            config = SunspotNumberWithFlare(**json.load(f))
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"config {config_path} is broken"
        ) from e
    df = pl.read_parquet(input_path)
    fig = sunspot_number_with_flare.draw_sunspot_number_with_flare(df, config)
    fig.savefig(
        output_path,
        format=body.format,
        dpi=body.dpi,
        bbox_inches="tight",
        pad_inches=0.1,
    )
    return SaveRes(output=str(output_path))


@router.get("/with_flare_with_factor", response_model=PreviewRes)
def draw_with_flare_with_factor(query: PreviewQuery = Depends()) -> PreviewRes:
    with_flare_path = Path(query.filename).with_name("with_flare.parquet")
    if not with_flare_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {with_flare_path} not found"
        )
    factors_path = with_flare_path.with_name("flare_factors.json")
    if not factors_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {factors_path} not found"
        )
    config_path = Path(query.config_name)
    if not config_path.exists():
        raise HTTPException(
            status_code=404, detail=f"config {config_path} not found"
        )
    try:
        with config_path.open("r") as f_config:
            config = SunspotNumberWithFlare(**json.load(f_config))
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"config {config_path} is broken"
        ) from e
    df = pl.read_parquet(with_flare_path)
    with factors_path.open("r") as f_factors:
        json_data = json.load(f_factors)
        factor = json_data["total"]
    fig = sunspot_number_with_flare.draw_sunspot_number_with_flare(
        df, config, factor=factor
    )
    img = utils.fig_to_base64(fig)
    return PreviewRes(img=img)


@router.post("/with_flare_with_factor", response_model=SaveRes)
def save_with_flare_with_factor(body: SaveBody) -> SaveRes:
    with_flare_path = Path(body.input).with_name("with_flare.parquet")
    if not with_flare_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {with_flare_path} not found"
        )
    factors_path = with_flare_path.with_name("flare_factors.json")
    if not factors_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {factors_path} not found"
        )
    config_path = Path(body.config)
    if not config_path.exists():
        raise HTTPException(
            status_code=404, detail=f"config {config_path} not found"
        )
    output_path = with_flare_path.with_name(
        f"with_flare_with_factor.{body.format}"
    )
    if not body.overwrite and output_path.exists():
        raise HTTPException(
            status_code=400, detail=f"file {output_path} already exists"
        )
    try:
        with config_path.open("r") as f_config:
            config = SunspotNumberWithFlare(**json.load(f_config))
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"config {config_path} is broken"
        ) from e
    df = pl.read_parquet(with_flare_path)
    with factors_path.open("r") as f_factors:
        json_data = json.load(f_factors)
        factor = json_data["total"]
    fig = sunspot_number_with_flare.draw_sunspot_number_with_flare(
        df, config, factor=factor
    )
    fig.savefig(
        output_path,
        format=body.format,
        dpi=body.dpi,
        bbox_inches="tight",
        pad_inches=0.1,
    )
    return SaveRes(output=str(output_path))


@router.get("/hemispheric", response_model=PreviewRes)
def draw_hemispheric(query: PreviewQuery = Depends()) -> PreviewRes:
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
            config = SunspotNumberWithFlareHemispheric(**json.load(f))
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"config {config_path} is broken"
        ) from e
    df = pl.read_parquet(input_path)
    fig = sunspot_number_with_flare.draw_sunspot_number_with_flare_hemispheric(
        df, config
    )
    img = utils.fig_to_base64(fig)
    return PreviewRes(img=img)


@router.post("/hemispheric", response_model=SaveRes)
def save_hemispheric(body: SaveBody) -> SaveRes:
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
            config = SunspotNumberWithFlareHemispheric(**json.load(f))
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"config {config_path} is broken"
        ) from e
    df = pl.read_parquet(input_path)
    fig = sunspot_number_with_flare.draw_sunspot_number_with_flare_hemispheric(
        df, config
    )
    fig.savefig(
        output_path,
        format=body.format,
        dpi=body.dpi,
        bbox_inches="tight",
        pad_inches=0.1,
    )
    return SaveRes(output=str(output_path))


@router.get("/hemispheric_with_factors", response_model=PreviewRes)
def draw_hemispheric_with_factors(
    query: PreviewQuery = Depends(),
) -> PreviewRes:
    with_flare_path = Path(query.filename).with_name("with_flare.parquet")
    if not with_flare_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {with_flare_path} not found"
        )
    factors_path = with_flare_path.with_name("flare_factors.json")
    if not factors_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {factors_path} not found"
        )
    config_path = Path(query.config_name)
    if not config_path.exists():
        raise HTTPException(
            status_code=404, detail=f"config {config_path} not found"
        )
    try:
        with config_path.open("r") as f_config:
            config = SunspotNumberWithFlareHemispheric(**json.load(f_config))
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"config {config_path} is broken"
        ) from e
    df = pl.read_parquet(with_flare_path)
    with factors_path.open("r") as f_factors:
        json_data = json.load(f_factors)
        factor_north = json_data["north"]
        factor_south = json_data["south"]
    fig = sunspot_number_with_flare.draw_sunspot_number_with_flare_hemispheric(
        df, config, factor_north=factor_north, factor_south=factor_south
    )
    img = utils.fig_to_base64(fig)
    return PreviewRes(img=img)


@router.post("/hemispheric_with_factors", response_model=SaveRes)
def save_hemispheric_with_factors(body: SaveBody) -> SaveRes:
    with_flare_path = Path(body.input).with_name("with_flare.parquet")
    if not with_flare_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {with_flare_path} not found"
        )
    factors_path = with_flare_path.with_name("flare_factors.json")
    if not factors_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {factors_path} not found"
        )
    config_path = Path(body.config)
    if not config_path.exists():
        raise HTTPException(
            status_code=404, detail=f"config {config_path} not found"
        )
    output_path = with_flare_path.with_name(
        f"hemispheric_with_factors.{body.format}"
    )
    if not body.overwrite and output_path.exists():
        raise HTTPException(
            status_code=400, detail=f"file {output_path} already exists"
        )
    try:
        with config_path.open("r") as f_config:
            config = SunspotNumberWithFlareHemispheric(**json.load(f_config))
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"config {config_path} is broken"
        ) from e
    df = pl.read_parquet(with_flare_path)
    with factors_path.open("r") as f_factors:
        json_data = json.load(f_factors)
        factor_north = json_data["north"]
        factor_south = json_data["south"]
    fig = sunspot_number_with_flare.draw_sunspot_number_with_flare_hemispheric(
        df, config, factor_north=factor_north, factor_south=factor_south
    )
    fig.savefig(
        output_path,
        format=body.format,
        dpi=body.dpi,
        bbox_inches="tight",
        pad_inches=0.1,
    )
    return SaveRes(output=str(output_path))
