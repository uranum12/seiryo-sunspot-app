import json
import shutil
from datetime import date
from pathlib import Path

import numpy as np
import polars as pl
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from api.libs import (
    butterfly,
    butterfly_config,
    butterfly_fromtext,
    butterfly_image,
    butterfly_merge,
    butterfly_trim,
)
from api.routers.config.butterfly import router as router_config
from api.routers.draw.butterfly import router as router_draw


class ButterflyAgg(BaseModel):
    input_name: str
    output_name: str
    overwrite: bool = False


class ButterflyAggRes(BaseModel):
    output_data: str
    output_info: str


class ButterflyTrim(BaseModel):
    input_name: str
    output_name: str
    overwrite: bool = False
    lat_min: int | None = None
    lat_max: int | None = None
    date_start: str | None = None
    date_end: str | None = None


class ButterflyTrimRes(BaseModel):
    output_data: str
    output_info: str


class ButterflyImage(BaseModel):
    input_name: str
    overwrite: bool = False


class ButterflyImageRes(BaseModel):
    output_image: str


class ButterflyImageColor(BaseModel):
    input_name: str
    colors_name: str
    output_name: str
    overwrite: bool = False


class ButterflyImageColorRes(BaseModel):
    output_info: str
    output_image: str


class ButterflyMerge(BaseModel):
    input_names: list[str]
    output_name: str
    overwrite: bool = False


class ButterflyMergeRes(BaseModel):
    output_info: str
    output_img: str


router = APIRouter(prefix="/butterfly", tags=["butterfly"])
router.include_router(router_config)
router.include_router(router_draw)


@router.post("/agg", response_model=ButterflyAggRes)
def butterfly_agg(body: ButterflyAgg) -> ButterflyAggRes:
    input_path = Path(body.input_name)
    if not input_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {input_path} not found"
        )
    output_dir = Path("out/butterfly")
    output_dir.mkdir(exist_ok=True, parents=True)
    output_paths = {
        "data": output_dir / f"{body.output_name}.parquet",
        "info": output_dir / f"{body.output_name}.json",
    }
    for path in output_paths.values():
        if not body.overwrite and path.exists():
            raise HTTPException(
                status_code=400, detail=f"file {path} already exists"
            )
    data = pl.scan_parquet(input_path)
    start, end = butterfly.adjust_dates(*butterfly.calc_date_limit(data))
    try:
        info = butterfly.ButterflyInfo(
            -90, 90, start, end, butterfly.DateDelta(months=1)
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    with (output_paths["info"]).open("w") as f_info:
        f_info.write(info.to_json())
    df = butterfly.calc_lat(data, info)
    df.write_parquet(output_paths["data"])
    return ButterflyAggRes(
        output_data=str(output_paths["data"]),
        output_info=str(output_paths["info"]),
    )


@router.post("/fromtext", response_model=ButterflyAggRes)
def fromtext(body: ButterflyAgg) -> ButterflyAggRes:
    input_path = Path(body.input_name)
    if not input_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {input_path} not found"
        )
    output_dir = Path("out/butterfly")
    output_dir.mkdir(exist_ok=True, parents=True)
    output_paths = {
        "data": output_dir / f"{body.output_name}.parquet",
        "info": output_dir / f"{body.output_name}.json",
    }
    for path in output_paths.values():
        if not body.overwrite and path.exists():
            raise HTTPException(
                status_code=400, detail=f"file {path} already exists"
            )
    start, end, txt = butterfly_fromtext.load_txt_data(input_path)
    lf = butterfly_fromtext.extract_lat(txt)
    try:
        info = butterfly.ButterflyInfo(
            -90, 90, start, end, butterfly.DateDelta(months=1)
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    with (output_paths["info"]).open("w") as f_info:
        f_info.write(info.to_json())
    df = butterfly.calc_lat(lf, info)
    df.write_parquet(output_paths["data"])
    return ButterflyAggRes(
        output_data=str(output_paths["data"]),
        output_info=str(output_paths["info"]),
    )


@router.post("/trim", response_model=ButterflyTrimRes)
def trim_butterfly(body: ButterflyTrim) -> ButterflyTrimRes:
    data_path = Path(body.input_name).with_suffix(".parquet")
    if not data_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {data_path} not found"
        )
    info_path = data_path.with_suffix(".json")
    if not info_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {info_path} not found"
        )
    output_dir = Path("out/butterfly")
    output_dir.mkdir(exist_ok=True, parents=True)
    output_paths = {
        "data": output_dir / f"{body.output_name}.parquet",
        "info": output_dir / f"{body.output_name}.json",
    }
    for path in output_paths.values():
        if not body.overwrite and path.exists():
            raise HTTPException(
                status_code=400, detail=f"file {path} already exists"
            )
    date_start = (
        date.fromisoformat(body.date_start)
        if body.date_start is not None
        else None
    )
    date_end = (
        date.fromisoformat(body.date_end)
        if body.date_end is not None
        else None
    )
    data = pl.read_parquet(data_path)
    with info_path.open("r") as f_info:
        info = butterfly.ButterflyInfo.from_dict(json.load(f_info))
    try:
        trimmed_info = butterfly_trim.trim_info(
            info, body.lat_min, body.lat_max, date_start, date_end
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    with (output_paths["info"]).open("w") as f_info:
        f_info.write(trimmed_info.to_json())
    trimmed_data = butterfly_trim.trim_data(data, trimmed_info)
    trimmed_data.write_parquet(output_paths["data"])
    return ButterflyTrimRes(
        output_data=str(output_paths["data"]),
        output_info=str(output_paths["info"]),
    )


@router.post("/image", response_model=ButterflyImageRes)
def butterfly_img(body: ButterflyImage) -> ButterflyImageRes:
    data_path = Path(body.input_name).with_suffix(".parquet")
    if not data_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {data_path} not found"
        )
    info_path = data_path.with_suffix(".json")
    if not info_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {info_path} not found"
        )
    output_path = Path("out/butterfly") / f"{data_path.stem}.npz"
    if not body.overwrite and output_path.exists():
        raise HTTPException(
            status_code=400, detail=f"file {output_path} already exists"
        )
    df = pl.read_parquet(data_path)
    with info_path.open("r") as f_info:
        info = butterfly.ButterflyInfo.from_dict(json.load(f_info))
    img = butterfly_image.create_image(df, info)
    with output_path.open("wb") as f_img:
        np.savez_compressed(f_img, img=img)
    return ButterflyImageRes(output_image=str(output_path))


@router.post("/image_color", response_model=ButterflyImageColorRes)
def image_color(body: ButterflyImageColor) -> ButterflyImageColorRes:
    info_path = Path(body.input_name).with_suffix(".json")
    if not info_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {info_path} not found"
        )
    img_path = info_path.with_suffix(".npz")
    if not img_path.exists():
        raise HTTPException(
            status_code=404, detail=f"file {img_path} not found"
        )
    colors_path = Path(body.colors_name)
    if not colors_path.exists():
        raise HTTPException(
            status_code=404, detail=f"colors {colors_path} not found"
        )
    output_dir = Path("out/butterfly")
    output_dir.mkdir(exist_ok=True, parents=True)
    output_paths = {
        "info": output_dir / f"{body.output_name}.json",
        "img": output_dir / f"{body.output_name}.npz",
    }
    for path in output_paths.values():
        if not body.overwrite and path.exists():
            raise HTTPException(
                status_code=400, detail=f"file {path} already exists"
            )
    with np.load(img_path) as f_img:
        img = f_img["img"]
    with colors_path.open("r") as f_cmap:
        cmap = butterfly_config.ColorMap(**json.load(f_cmap))
    img_color = butterfly_merge.create_color_image(img, cmap)
    with output_paths["img"].open("wb") as f_img_color:
        np.savez_compressed(f_img_color, img=img_color)
    shutil.copy(info_path, output_paths["info"])
    return ButterflyImageColorRes(
        output_info=str(output_paths["info"]),
        output_image=str(output_paths["img"]),
    )


@router.post("/merge", response_model=ButterflyMergeRes)
def merge(body: ButterflyMerge) -> ButterflyMergeRes:
    data_paths = [
        Path(name).with_suffix(".parquet") for name in body.input_names
    ]
    info_paths = [path.with_suffix(".json") for path in data_paths]
    for path in data_paths + info_paths:
        if not path.exists():
            raise HTTPException(
                status_code=404, detail=f"file {path} not found"
            )
    output_dir = Path("out/butterfly")
    output_dir.mkdir(exist_ok=True, parents=True)
    output_paths = {
        "info": output_dir / f"{body.output_name}.json",
        "img": output_dir / f"{body.output_name}.npz",
    }
    for path in output_paths.values():
        if not body.overwrite and path.exists():
            raise HTTPException(
                status_code=400, detail=f"file {path} already exists"
            )
    info_list: list[butterfly.ButterflyInfo] = []
    for path in info_paths:
        with path.open("r") as f_info:
            info_list.append(
                butterfly.ButterflyInfo.from_dict(json.load(f_info))
            )
    info = butterfly_merge.merge_info(info_list)
    dfl = [pl.read_parquet(path) for path in data_paths]
    img = butterfly_merge.create_merged_image(dfl, info)
    with output_paths["info"].open("w") as f_info:
        f_info.write(info.to_json())
    with output_paths["img"].open("wb") as f_img:
        np.savez_compressed(f_img, img=img)
    return ButterflyMergeRes(
        output_info=str(output_paths["info"]),
        output_img=str(output_paths["img"]),
    )
