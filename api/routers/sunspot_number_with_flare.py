import json
from pathlib import Path

import polars as pl
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from api.libs import sunspot_number_with_flare, utils
from api.libs.sunspot_number_with_flare_config import (
    SunspotNumberWithFlare,
    SunspotNumberWithFlareHemispheric,
)
from api.models import draw


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


@router.get("/draw/with_flare", response_model=draw.PreviewRes)
def draw_with_flare(query: draw.PreviewQuery = Depends()) -> draw.PreviewRes:
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
    return draw.PreviewRes(img=img)


@router.post("/draw/with_flare", response_model=draw.SaveRes)
def save_with_flare(body: draw.SaveBody) -> draw.SaveRes:
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
    return draw.SaveRes(output=str(output_path))


@router.get("/draw/with_flare_with_factor", response_model=draw.PreviewRes)
def draw_with_flare_with_factor(
    query: draw.PreviewQuery = Depends(),
) -> draw.PreviewRes:
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
    return draw.PreviewRes(img=img)


@router.post("/draw/with_flare_with_factor", response_model=draw.SaveRes)
def save_with_flare_with_factor(body: draw.SaveBody) -> draw.SaveRes:
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
    return draw.SaveRes(output=str(output_path))


@router.get("/draw/hemispheric", response_model=draw.PreviewRes)
def draw_hemispheric(query: draw.PreviewQuery = Depends()) -> draw.PreviewRes:
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
    return draw.PreviewRes(img=img)


@router.post("/draw/hemispheric", response_model=draw.SaveRes)
def save_hemispheric(body: draw.SaveBody) -> draw.SaveRes:
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
    return draw.SaveRes(output=str(output_path))


@router.get("/draw/hemispheric_with_factors", response_model=draw.PreviewRes)
def draw_hemispheric_with_factors(
    query: draw.PreviewQuery = Depends(),
) -> draw.PreviewRes:
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
    return draw.PreviewRes(img=img)


@router.post("/draw/hemispheric_with_factors", response_model=draw.SaveRes)
def save_hemispheric_with_factors(body: draw.SaveBody) -> draw.SaveRes:
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
    return draw.SaveRes(output=str(output_path))
