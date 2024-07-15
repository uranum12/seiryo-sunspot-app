from datetime import date
from pathlib import Path

import numpy as np
import polars as pl
from fastapi import APIRouter, Depends, HTTPException

from api.libs import sunspot_number, utils
from api.libs.sunspot_number_config import (
    SunspotNumberHemispheric,
    SunspotNumberWholeDisk,
)
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


@router.get("/whole_disk", response_model=GetConfigRes[SunspotNumberWholeDisk])
def get_whole_disk(
    query: GetConfigQuery = Depends(),
) -> GetConfigRes[SunspotNumberWholeDisk]:
    return get_config(query, SunspotNumberWholeDisk)


@router.post("/whole_disk", response_model=CreateConfigRes)
def post_whole_disk(
    body: CreateConfigBody[SunspotNumberWholeDisk],
) -> CreateConfigRes:
    output_dir = Path("config/sunspot_number/whole_disk")
    return post_config(body, output_dir)


@router.post("/whole_disk/preview", response_model=PreviewRes)
def whole_disk_preview(
    body: PreviewBody[SunspotNumberWholeDisk],
) -> PreviewRes:
    df = pl.DataFrame(
        {
            "date": pl.date_range(
                date(2010, 1, 1), date(2020, 12, 1), "1mo", eager=True
            ),
            "total": (1 - np.cos(np.linspace(-1, 7, 132))) * 100,
        }
    )
    try:
        fig = sunspot_number.draw_sunspot_number_whole_disk(df, body.config)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    img = utils.fig_to_base64(fig)
    return PreviewRes(img=img)


@router.get(
    "/hemispheric", response_model=GetConfigRes[SunspotNumberHemispheric]
)
def get_hemispheric(
    query: GetConfigQuery = Depends(),
) -> GetConfigRes[SunspotNumberHemispheric]:
    return get_config(query, SunspotNumberHemispheric)


@router.post("/hemispheric", response_model=CreateConfigRes)
def post_hemispheric(
    body: CreateConfigBody[SunspotNumberHemispheric],
) -> CreateConfigRes:
    output_dir = Path("config/sunspot_number/hemispheric")
    return post_config(body, output_dir)


@router.post("/hemispheric/preview", response_model=PreviewRes)
def hemispheric_preview(
    body: PreviewBody[SunspotNumberHemispheric],
) -> PreviewRes:
    df = pl.DataFrame(
        {
            "date": pl.date_range(
                date(2010, 1, 1), date(2020, 12, 1), "1mo", eager=True
            ),
            "north": (1 - np.cos(np.linspace(-1, 7, 132))) * 100,
            "south": (1 - np.cos(np.linspace(-0.5, 7.5, 132))) * 100,
        }
    )
    try:
        fig = sunspot_number.draw_sunspot_number_hemispheric(df, body.config)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    img = utils.fig_to_base64(fig)
    return PreviewRes(img=img)
