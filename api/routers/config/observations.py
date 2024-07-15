from datetime import date
from pathlib import Path

import numpy as np
import polars as pl
from fastapi import APIRouter, Depends, HTTPException

from api.libs import observations, utils
from api.libs.observations_config import ObservationsMonthly
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


@router.get("/monthly", response_model=GetConfigRes[ObservationsMonthly])
def get_monthly(
    query: GetConfigQuery = Depends(),
) -> GetConfigRes[ObservationsMonthly]:
    return get_config(query, ObservationsMonthly)


@router.post("/monthly", response_model=CreateConfigRes)
def post_monthly(
    body: CreateConfigBody[ObservationsMonthly],
) -> CreateConfigRes:
    output_dir = Path("config/observations/monthly")
    return post_config(body, output_dir)


@router.post("/monthly/preview", response_model=PreviewRes)
def monthly_preview(body: PreviewBody[ObservationsMonthly]) -> PreviewRes:
    df = pl.DataFrame(
        {
            "date": pl.date_range(
                date(2010, 1, 1), date(2015, 12, 1), "1mo", eager=True
            ),
            "obs": np.round(20 + np.sin(np.linspace(1, 15, 72)) * 3),
        }
    )
    try:
        fig = observations.draw_monthly_obs_days(df, body.config)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    img = utils.fig_to_base64(fig)
    return PreviewRes(img=img)
