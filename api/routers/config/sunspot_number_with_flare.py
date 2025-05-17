from datetime import date
from pathlib import Path

import numpy as np
import polars as pl
from fastapi import APIRouter, Depends, HTTPException
from seiryo_sunspot_lib import sunspot_number_with_flare
from seiryo_sunspot_lib.sunspot_number_with_flare_config import (
    SunspotNumberWithFlare,
    SunspotNumberWithFlareHemispheric,
)

from api.libs import utils
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


@router.get("/with_flare", response_model=GetConfigRes[SunspotNumberWithFlare])
def get_with_flare(
    query: GetConfigQuery = Depends(),
) -> GetConfigRes[SunspotNumberWithFlare]:
    return get_config(query, SunspotNumberWithFlare)


@router.post("/with_flare", response_model=CreateConfigRes)
def post_with_flare(
    body: CreateConfigBody[SunspotNumberWithFlare],
) -> CreateConfigRes:
    output_dir = Path("config/sunspot_number/with_flare")
    return post_config(body, output_dir)


@router.post("/with_flare/preview", response_model=PreviewRes)
def with_flare_preview(
    body: PreviewBody[SunspotNumberWithFlare],
) -> PreviewRes:
    df = pl.DataFrame(
        {
            "date": pl.date_range(
                date(2010, 1, 1), date(2020, 12, 1), "1mo", eager=True
            ),
            "seiryo_total": (1 - np.cos(np.linspace(-1, 7, 132))) * 70,
            "flare_total": (1 - np.cos(np.linspace(-0.5, 7.5, 132))) * 100,
        }
    )
    try:
        fig = sunspot_number_with_flare.draw_sunspot_number_with_flare(
            df, body.config, factor=1.42857
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    img = utils.fig_to_base64(fig)
    return PreviewRes(img=img)


@router.get(
    "/hemispheric",
    response_model=GetConfigRes[SunspotNumberWithFlareHemispheric],
)
def get_hemispheric(
    query: GetConfigQuery = Depends(),
) -> GetConfigRes[SunspotNumberWithFlareHemispheric]:
    return get_config(query, SunspotNumberWithFlareHemispheric)


@router.post("/hemispheric", response_model=CreateConfigRes)
def post_hemispheric(
    body: CreateConfigBody[SunspotNumberWithFlareHemispheric],
) -> CreateConfigRes:
    output_dir = Path("config/sunspot_number/hemispheric")
    return post_config(body, output_dir)


@router.post("/hemispheric/preview", response_model=PreviewRes)
def hemispheric_preview(
    body: PreviewBody[SunspotNumberWithFlareHemispheric],
) -> PreviewRes:
    df = pl.DataFrame(
        {
            "date": pl.date_range(
                date(2010, 1, 1), date(2020, 12, 1), "1mo", eager=True
            ),
            "seiryo_north": (1 - np.cos(np.linspace(-1, 7, 132))) * 70,
            "seiryo_south": (1 - np.cos(np.linspace(-1, 7, 132))) * 70,
            "flare_north": (1 - np.cos(np.linspace(-0.5, 7.5, 132))) * 100,
            "flare_south": (1 - np.cos(np.linspace(-0.5, 7.5, 132))) * 100,
        }
    )
    try:
        fig = sunspot_number_with_flare.draw_sunspot_number_with_flare_hemispheric(  # noqa: E501
            df, body.config, factor_north=1.42857, factor_south=1.42857
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    img = utils.fig_to_base64(fig)
    return PreviewRes(img=img)
