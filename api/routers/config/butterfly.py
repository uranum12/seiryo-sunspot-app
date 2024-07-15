import json
from datetime import date
from pathlib import Path

import numpy as np
import polars as pl
from fastapi import APIRouter, Depends, HTTPException

from api.libs import butterfly_draw, butterfly_image, butterfly_merge, utils
from api.libs.butterfly import ButterflyInfo, DateDelta
from api.libs.butterfly_config import ButterflyDiagram, ColorMap
from api.models.config import (
    CreateConfigBody,
    CreateConfigRes,
    GetConfigQuery,
    GetConfigRes,
    PreviewBody,
    PreviewRes,
)
from api.routers.config.common import get_config, post_config

router = APIRouter(prefix="/config")


@router.get("/butterfly", response_model=GetConfigRes[ButterflyDiagram])
def get_butterfly(
    query: GetConfigQuery = Depends(),
) -> GetConfigRes[ButterflyDiagram]:
    return get_config(query, ButterflyDiagram)


@router.post("/butterfly", response_model=CreateConfigRes)
def post_butterfly(
    body: CreateConfigBody[ButterflyDiagram],
) -> CreateConfigRes:
    output_dir = Path("config/butterfly/butterfly")
    return post_config(body, output_dir)


@router.post("/butterfly/preview", response_model=PreviewRes)
def butterfly_preview(body: PreviewBody[ButterflyDiagram]) -> PreviewRes:
    df = pl.DataFrame(
        {
            "date": pl.date_range(
                date(2010, 1, 1), date(2020, 12, 1), "1mo", eager=True
            ),
            "min": [[-10, 5]] * 132,
            "max": [[-5, 10]] * 132,
        }
    )
    info = ButterflyInfo(
        lat_min=-20,
        lat_max=20,
        date_start=date(2010, 1, 1),
        date_end=date(2020, 12, 1),
        date_interval=DateDelta(months=1),
    )
    img = butterfly_image.create_image(df, info)
    try:
        fig = butterfly_draw.draw_butterfly_diagram(img, info, body.config)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    base64_img = utils.fig_to_base64(fig)
    return PreviewRes(img=base64_img)


@router.get("/color_map", response_model=GetConfigRes[ColorMap])
def get_color_map(query: GetConfigQuery = Depends()) -> GetConfigRes[ColorMap]:
    return get_config(query, ColorMap)


@router.post("/color_map", response_model=CreateConfigRes)
def post_color_map(body: CreateConfigBody[ColorMap]) -> CreateConfigRes:
    output_dir = Path("config/butterfly/color_map")
    return post_config(body, output_dir)


@router.post("/color_map/preview", response_model=PreviewRes)
def color_map_preview(body: PreviewBody[ColorMap]) -> PreviewRes:
    img = np.array(
        [
            [8, 0, 2, 2, 2],
            [1, 1, 3, 2, 2],
            [1, 1, 7, 6, 6],
            [1, 1, 5, 4, 4],
            [16, 0, 4, 4, 4],
        ]
    )
    info = ButterflyInfo(
        lat_min=1,
        lat_max=2,
        date_start=date(2010, 2, 1),
        date_end=date(2010, 4, 1),
        date_interval=DateDelta(months=1),
    )
    with Path("config/butterfly/butterfly.json").open("r") as f:
        config = ButterflyDiagram(**json.load(f))
    img_color = butterfly_merge.create_color_image(img, body.config)
    try:
        fig = butterfly_draw.draw_butterfly_diagram(img_color, info, config)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    base64_img = utils.fig_to_base64(fig)
    return PreviewRes(img=base64_img)
