import json
from pathlib import Path

import polars as pl
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from api.libs import sunspot_number_with_silso, utils
from api.libs.sunspot_number_with_silso_config import SunspotNumberWithSilso
from api.models import draw


class SunspotNumberWithSilsoAgg(BaseModel):
    seiryo_path: str
    silso_path: str
    output_name: str
    overwrite: bool = False


class SunspotNumberWithSilsoAggRes(BaseModel):
    output_with_silso: str
    output_factor_r2: str
    output_ratio_diff: str


router = APIRouter(
    prefix="/sunspot_number/with_silso", tags=["sunspot_number", "with_silso"]
)


@router.post("/agg", response_model=SunspotNumberWithSilsoAggRes)
def with_silso_agg(
    body: SunspotNumberWithSilsoAgg,
) -> SunspotNumberWithSilsoAggRes:
    seiryo_path = Path(body.seiryo_path)
    if not seiryo_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {seiryo_path} not found"
        )
    silso_path = Path(body.silso_path)
    if not silso_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {silso_path} not found"
        )
    output_dir = Path("out/sunspot_with_silso") / body.output_name
    output_dir.mkdir(exist_ok=True, parents=True)
    output_paths = {
        "with_silso": output_dir / "with_silso.parquet",
        "factor_r2": output_dir / "factor_r2.json",
        "ratio_diff": output_dir / "ratio_diff.parquet",
    }
    for path in output_paths.values():
        if not body.overwrite and path.exists():
            raise HTTPException(
                status_code=400, detail=f"file {path} already exists"
            )
    df_seiryo = pl.read_parquet(seiryo_path)
    df_silso = sunspot_number_with_silso.load_silso_data(silso_path)
    df_seiryo_with_silso = sunspot_number_with_silso.join_data(
        df_seiryo, df_silso
    )
    df_seiryo_with_silso.write_parquet(output_paths["with_silso"])
    df_seiryo_with_silso_truncated = sunspot_number_with_silso.truncate_data(
        df_seiryo_with_silso
    )
    factor = sunspot_number_with_silso.calc_factor(
        df_seiryo_with_silso_truncated
    )
    r2 = sunspot_number_with_silso.calc_r2(
        df_seiryo_with_silso_truncated, factor
    )
    with output_paths["factor_r2"].open("w") as json_file:
        json.dump({"factor": factor, "r2": r2}, json_file)
    df_ratio_and_diff = sunspot_number_with_silso.calc_ratio_and_diff(
        df_seiryo_with_silso_truncated, factor
    )
    df_ratio_and_diff.write_parquet(output_paths["ratio_diff"])
    return SunspotNumberWithSilsoAggRes(
        output_with_silso=str(output_paths["with_silso"]),
        output_factor_r2=str(output_paths["factor_r2"]),
        output_ratio_diff=str(output_paths["ratio_diff"]),
    )


@router.get("/draw/with_silso", response_model=draw.PreviewRes)
def draw_with_silso(query: draw.PreviewQuery = Depends()) -> draw.PreviewRes:
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
    return draw.PreviewRes(img=img)


@router.post("/draw/with_silso", response_model=draw.SaveRes)
def save_with_silso(body: draw.SaveBody) -> draw.SaveRes:
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
    return draw.SaveRes(output=str(output_path))
