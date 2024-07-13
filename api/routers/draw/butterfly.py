import json
from pathlib import Path

import numpy as np
from fastapi import APIRouter, Depends, HTTPException

from api.libs import butterfly, butterfly_draw, utils
from api.libs.butterfly_config import ButterflyDiagram
from api.models.draw import PreviewQuery, PreviewRes, SaveBody, SaveRes

router = APIRouter(prefix="/draw")


@router.get("/butterfly", response_model=PreviewRes)
def draw_butterfly(query: PreviewQuery = Depends()) -> PreviewRes:
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
    fig = butterfly_draw.draw_butterfly_diagram(img, info, config)
    img = utils.fig_to_base64(fig)
    return PreviewRes(img=img)


@router.post("/butterfly", response_model=SaveRes)
def save_butterfly(body: SaveBody) -> SaveRes:
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
    fig = butterfly_draw.draw_butterfly_diagram(img, info, config)
    fig.savefig(
        output_path,
        format=body.format,
        dpi=body.dpi,
        bbox_inches="tight",
        pad_inches=0.1,
    )
    return SaveRes(output=str(output_path))
