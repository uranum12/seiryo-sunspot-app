import json
from datetime import date
from pathlib import Path

import numpy as np
import polars as pl
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from api.libs import butterfly, utils
from api.libs.butterfly_config import ButterflyDiagram
from api.models import draw


class ButterflyAgg(BaseModel):
    input_name: str
    output_name: str
    overwrite: bool = False

    lat_min: int = -50
    lat_max: int = 50
    date_start: str | None = None
    date_end: str | None = None
    date_interval: str | None = None


class ButterflyAggRes(BaseModel):
    output_data: str
    output_image: str
    output_info: str


router = APIRouter(prefix="/butterfly", tags=["butterfly"])


@router.post("/agg", response_model=ButterflyAggRes)
def butterfly_agg(body: ButterflyAgg) -> ButterflyAggRes:
    input_path = Path(body.input_name)
    if not input_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {input_path} not found"
        )
    output_dir = Path("out/butterfly") / input_path.stem
    output_dir.mkdir(exist_ok=True, parents=True)
    output_paths = {
        "data": output_dir / f"{body.output_name}.parquet",
        "img": output_dir / f"{body.output_name}.npz",
        "info": output_dir / f"{body.output_name}.json",
    }
    for path in output_paths.values():
        if not body.overwrite and path.exists():
            raise HTTPException(
                status_code=400, detail=f"file {path} already exists"
            )
    data = pl.scan_parquet(input_path)
    start, end = butterfly.adjust_dates(*butterfly.calc_date_limit(data))
    date_start = (
        start
        if body.date_start is None
        else date.fromisoformat(body.date_start)
    )
    date_end = (
        end if body.date_end is None else date.fromisoformat(body.date_end)
    )
    date_interval = "P1M" if body.date_interval is None else body.date_interval
    try:
        info = butterfly.ButterflyInfo(
            body.lat_min,
            body.lat_max,
            date_start,
            date_end,
            butterfly.DateDelta.fromisoformat(date_interval),
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    with (output_paths["info"]).open("w") as f_info:
        f_info.write(info.to_json())
    df = butterfly.calc_lat(data, info)
    df.write_parquet(output_paths["data"])
    img = butterfly.create_image(df, info)
    with (output_paths["img"]).open("wb") as f_img:
        np.savez_compressed(f_img, img=img)
    return ButterflyAggRes(
        output_data=str(output_paths["data"]),
        output_image=str(output_paths["img"]),
        output_info=str(output_paths["info"]),
    )


@router.get("/draw/butterfly", response_model=draw.PreviewRes)
def butterfly_draw(query: draw.PreviewQuery = Depends()) -> draw.PreviewRes:
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
            config = ButterflyDiagram(**json.load(f))
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"config {config_path} is broken"
        ) from e
    with np.load(input_path.with_suffix(".npz")) as f_img:
        img = f_img["img"]
    with input_path.with_suffix(".json").open("r") as f_info:
        info = butterfly.ButterflyInfo.from_dict(json.load(f_info))
    fig = butterfly.draw_butterfly_diagram(img, info, config)
    img = utils.fig_to_base64(fig)
    return draw.PreviewRes(img=img)


@router.post("/draw/butterfly", response_model=draw.SaveRes)
def butterfly_save(body: draw.SaveBody) -> draw.SaveRes:
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
    output_path = input_path.with_name(f"{input_path.stem}.{body.format}")
    if not body.overwrite and output_path.exists():
        raise HTTPException(
            status_code=400, detail=f"file {output_path} already exists"
        )
    try:
        with config_path.open("r") as f:
            config = ButterflyDiagram(**json.load(f))
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"config {config_path} is broken"
        ) from e
    with np.load(input_path.with_suffix(".npz")) as f_img:
        img = f_img["img"]
    with input_path.with_suffix(".json").open("r") as f_info:
        info = butterfly.ButterflyInfo.from_dict(json.load(f_info))
    fig = butterfly.draw_butterfly_diagram(img, info, config)
    fig.savefig(
        output_path,
        format=body.format,
        dpi=body.dpi,
        bbox_inches="tight",
        pad_inches=0.1,
    )
    return draw.SaveRes(output=str(output_path))
