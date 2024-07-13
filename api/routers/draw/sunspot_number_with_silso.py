import json
from pathlib import Path

import polars as pl
from fastapi import APIRouter, Depends, HTTPException

from api.libs import sunspot_number_with_silso, utils
from api.libs.sunspot_number_with_silso_config import (
    SunspotNumberDiff,
    SunspotNumberRatio,
    SunspotNumberRatioDiff1,
    SunspotNumberRatioDiff2,
    SunspotNumberScatter,
    SunspotNumberWithSilso,
)
from api.models.draw import PreviewQuery, PreviewRes, SaveBody, SaveRes

router = APIRouter(prefix="/draw")


@router.get("/with_silso", response_model=PreviewRes)
def draw_with_silso(query: PreviewQuery = Depends()) -> PreviewRes:
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
            config = SunspotNumberWithSilso(**json.load(f))
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"config {config_path} is broken"
        ) from e
    df = pl.read_parquet(input_path)
    fig = sunspot_number_with_silso.draw_sunspot_number_with_silso(df, config)
    img = utils.fig_to_base64(fig)
    return PreviewRes(img=img)


@router.post("/with_silso", response_model=SaveRes)
def save_with_silso(body: SaveBody) -> SaveRes:
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
    output_path = input_path.with_name(f"with_silso.{body.format}")
    if not body.overwrite and output_path.exists():
        raise HTTPException(
            status_code=400, detail=f"file {output_path} already exists"
        )
    try:
        with config_path.open("r") as f:
            config = SunspotNumberWithSilso(**json.load(f))
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"config {config_path} is broken"
        ) from e
    df = pl.read_parquet(input_path)
    fig = sunspot_number_with_silso.draw_sunspot_number_with_silso(df, config)
    fig.savefig(
        output_path,
        format=body.format,
        dpi=body.dpi,
        bbox_inches="tight",
        pad_inches=0.1,
    )
    return SaveRes(output=str(output_path))


@router.get("/scatter", response_model=PreviewRes)
def draw_scatter(query: PreviewQuery = Depends()) -> PreviewRes:
    with_silso_path = Path(query.filename).with_name("with_silso.parquet")
    if not with_silso_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {with_silso_path} not found"
        )
    factor_r2_path = Path(query.filename).with_name("factor_r2.json")
    if not factor_r2_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {factor_r2_path} not found"
        )
    config_path = Path(query.config_name)
    if not config_path.exists():
        raise HTTPException(
            status_code=404, detail=f"config {config_path} not found"
        )
    try:
        with config_path.open("r") as f_config:
            config = SunspotNumberScatter(**json.load(f_config))
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"config {config_path} is broken"
        ) from e
    df = pl.read_parquet(with_silso_path)
    with factor_r2_path.open("r") as f_factor_r2:
        json_data = json.load(f_factor_r2)
        factor = json_data["factor"]
        r2 = json_data["r2"]
    fig = sunspot_number_with_silso.draw_scatter(df, factor, r2, config)
    img = utils.fig_to_base64(fig)
    return PreviewRes(img=img)


@router.post("/scatter", response_model=SaveRes)
def save_scatter(body: SaveBody) -> SaveRes:
    with_silso_path = Path(body.input).with_name("with_silso.parquet")
    if not with_silso_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {with_silso_path} not found"
        )
    factor_r2_path = Path(body.input).with_name("factor_r2.json")
    if not factor_r2_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {factor_r2_path} not found"
        )
    config_path = Path(body.config)
    if not config_path.exists():
        raise HTTPException(
            status_code=404, detail=f"config {config_path} not found"
        )
    output_path = with_silso_path.with_name(f"scatter.{body.format}")
    if not body.overwrite and output_path.exists():
        raise HTTPException(
            status_code=400, detail=f"file {output_path} already exists"
        )
    try:
        with config_path.open("r") as f_config:
            config = SunspotNumberScatter(**json.load(f_config))
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"config {config_path} is broken"
        ) from e
    df = pl.read_parquet(with_silso_path)
    with factor_r2_path.open("r") as f_factor_r2:
        json_data = json.load(f_factor_r2)
        factor = json_data["factor"]
        r2 = json_data["r2"]
    fig = sunspot_number_with_silso.draw_scatter(df, factor, r2, config)
    fig.savefig(
        output_path,
        format=body.format,
        dpi=body.dpi,
        bbox_inches="tight",
        pad_inches=0.1,
    )
    return SaveRes(output=str(output_path))


@router.get("/ratio", response_model=PreviewRes)
def draw_ratio(query: PreviewQuery = Depends()) -> PreviewRes:
    ratio_diff_path = Path(query.filename).with_name("ratio_diff.parquet")
    if not ratio_diff_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {ratio_diff_path} not found"
        )
    factor_r2_path = Path(query.filename).with_name("factor_r2.json")
    if not factor_r2_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {factor_r2_path} not found"
        )
    config_path = Path(query.config_name)
    if not config_path.exists():
        raise HTTPException(
            status_code=404, detail=f"config {config_path} not found"
        )
    try:
        with config_path.open("r") as f_config:
            config = SunspotNumberRatio(**json.load(f_config))
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"config {config_path} is broken"
        ) from e
    df = pl.read_parquet(ratio_diff_path)
    with factor_r2_path.open("r") as f_factor_r2:
        json_data = json.load(f_factor_r2)
        factor = json_data["factor"]
    fig = sunspot_number_with_silso.draw_ratio(df, factor, config)
    img = utils.fig_to_base64(fig)
    return PreviewRes(img=img)


@router.post("/ratio", response_model=SaveRes)
def save_ratio(body: SaveBody) -> SaveRes:
    ratio_diff_path = Path(body.input).with_name("ratio_diff.parquet")
    if not ratio_diff_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {ratio_diff_path} not found"
        )
    factor_r2_path = Path(body.input).with_name("factor_r2.json")
    if not factor_r2_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {factor_r2_path} not found"
        )
    config_path = Path(body.config)
    if not config_path.exists():
        raise HTTPException(
            status_code=404, detail=f"config {config_path} not found"
        )
    output_path = ratio_diff_path.with_name(f"ratio.{body.format}")
    if not body.overwrite and output_path.exists():
        raise HTTPException(
            status_code=400, detail=f"file {output_path} already exists"
        )
    try:
        with config_path.open("r") as f_config:
            config = SunspotNumberRatio(**json.load(f_config))
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"config {config_path} is broken"
        ) from e
    df = pl.read_parquet(ratio_diff_path)
    with factor_r2_path.open("r") as f_factor_r2:
        json_data = json.load(f_factor_r2)
        factor = json_data["factor"]
    fig = sunspot_number_with_silso.draw_ratio(df, factor, config)
    fig.savefig(
        output_path,
        format=body.format,
        dpi=body.dpi,
        bbox_inches="tight",
        pad_inches=0.1,
    )
    return SaveRes(output=str(output_path))


@router.get("/diff", response_model=PreviewRes)
def draw_diff(query: PreviewQuery = Depends()) -> PreviewRes:
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
        with config_path.open("r") as f_config:
            config = SunspotNumberDiff(**json.load(f_config))
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"config {config_path} is broken"
        ) from e
    df = pl.read_parquet(input_path)
    fig = sunspot_number_with_silso.draw_diff(df, config)
    img = utils.fig_to_base64(fig)
    return PreviewRes(img=img)


@router.post("/diff", response_model=SaveRes)
def save_diff(body: SaveBody) -> SaveRes:
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
    output_path = input_path.with_name(f"diff.{body.format}")
    if not body.overwrite and output_path.exists():
        raise HTTPException(
            status_code=400, detail=f"file {output_path} already exists"
        )
    try:
        with config_path.open("r") as f:
            config = SunspotNumberDiff(**json.load(f))
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"config {config_path} is broken"
        ) from e
    df = pl.read_parquet(input_path)
    fig = sunspot_number_with_silso.draw_diff(df, config)
    fig.savefig(
        output_path,
        format=body.format,
        dpi=body.dpi,
        bbox_inches="tight",
        pad_inches=0.1,
    )
    return SaveRes(output=str(output_path))


@router.get("/ratio_diff_1", response_model=PreviewRes)
def draw_ratio_diff_1(query: PreviewQuery = Depends()) -> PreviewRes:
    ratio_diff_path = Path(query.filename).with_name("ratio_diff.parquet")
    if not ratio_diff_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {ratio_diff_path} not found"
        )
    factor_r2_path = Path(query.filename).with_name("factor_r2.json")
    if not factor_r2_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {factor_r2_path} not found"
        )
    config_path = Path(query.config_name)
    if not config_path.exists():
        raise HTTPException(
            status_code=404, detail=f"config {config_path} not found"
        )
    try:
        with config_path.open("r") as f_config:
            config = SunspotNumberRatioDiff1(**json.load(f_config))
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"config {config_path} is broken"
        ) from e
    df = pl.read_parquet(ratio_diff_path)
    with factor_r2_path.open("r") as f_factor_r2:
        json_data = json.load(f_factor_r2)
        factor = json_data["factor"]
    fig = sunspot_number_with_silso.draw_ratio_diff_1(df, factor, config)
    img = utils.fig_to_base64(fig)
    return PreviewRes(img=img)


@router.post("/ratio_diff_1", response_model=SaveRes)
def save_ratio_diff_1(body: SaveBody) -> SaveRes:
    ratio_diff_path = Path(body.input).with_name("ratio_diff.parquet")
    if not ratio_diff_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {ratio_diff_path} not found"
        )
    factor_r2_path = Path(body.input).with_name("factor_r2.json")
    if not factor_r2_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {factor_r2_path} not found"
        )
    config_path = Path(body.config)
    if not config_path.exists():
        raise HTTPException(
            status_code=404, detail=f"config {config_path} not found"
        )
    output_path = ratio_diff_path.with_name(f"ratio_diff_1.{body.format}")
    if not body.overwrite and output_path.exists():
        raise HTTPException(
            status_code=400, detail=f"file {output_path} already exists"
        )
    try:
        with config_path.open("r") as f_config:
            config = SunspotNumberRatioDiff1(**json.load(f_config))
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"config {config_path} is broken"
        ) from e
    df = pl.read_parquet(ratio_diff_path)
    with factor_r2_path.open("r") as f_factor_r2:
        json_data = json.load(f_factor_r2)
        factor = json_data["factor"]
    fig = sunspot_number_with_silso.draw_ratio_diff_1(df, factor, config)
    fig.savefig(
        output_path,
        format=body.format,
        dpi=body.dpi,
        bbox_inches="tight",
        pad_inches=0.1,
    )
    return SaveRes(output=str(output_path))


@router.get("/ratio_diff_2", response_model=PreviewRes)
def draw_ratio_diff_2(query: PreviewQuery = Depends()) -> PreviewRes:
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
        with config_path.open("r") as f_config:
            config = SunspotNumberRatioDiff2(**json.load(f_config))
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"config {config_path} is broken"
        ) from e
    df = pl.read_parquet(input_path)
    fig = sunspot_number_with_silso.draw_ratio_diff_2(df, config)
    img = utils.fig_to_base64(fig)
    return PreviewRes(img=img)


@router.post("/ratio_diff_2", response_model=SaveRes)
def save_ratio_diff_2(body: SaveBody) -> SaveRes:
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
    output_path = input_path.with_name(f"ratio_diff_2.{body.format}")
    if not body.overwrite and output_path.exists():
        raise HTTPException(
            status_code=400, detail=f"file {output_path} already exists"
        )
    try:
        with config_path.open("r") as f:
            config = SunspotNumberRatioDiff2(**json.load(f))
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"config {config_path} is broken"
        ) from e
    df = pl.read_parquet(input_path)
    fig = sunspot_number_with_silso.draw_ratio_diff_2(df, config)
    fig.savefig(
        output_path,
        format=body.format,
        dpi=body.dpi,
        bbox_inches="tight",
        pad_inches=0.1,
    )
    return SaveRes(output=str(output_path))
