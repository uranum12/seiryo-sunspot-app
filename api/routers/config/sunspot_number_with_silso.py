from datetime import date
from pathlib import Path

import numpy as np
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


@router.get("/with_silso", response_model=GetConfigRes[SunspotNumberWithSilso])
def get_with_silso(
    query: GetConfigQuery = Depends(),
) -> GetConfigRes[SunspotNumberWithSilso]:
    return get_config(query, SunspotNumberWithSilso)


@router.post("/with_silso", response_model=CreateConfigRes)
def post_with_silso(
    body: CreateConfigBody[SunspotNumberWithSilso],
) -> CreateConfigRes:
    output_dir = Path("config/sunspot_number/with_silso")
    return post_config(body, output_dir)


@router.post("/with_silso/preview", response_model=PreviewRes)
def with_silso_preview(
    body: PreviewBody[SunspotNumberWithSilso],
) -> PreviewRes:
    df = pl.DataFrame(
        {
            "date": pl.date_range(
                date(2010, 1, 1), date(2020, 12, 1), "1mo", eager=True
            ),
            "seiryo": (1 - np.cos(np.linspace(-1, 7, 132))) * 100,
            "silso": (1 - np.cos(np.linspace(-0.5, 7.5, 132))) * 100,
        }
    )
    try:
        fig = sunspot_number_with_silso.draw_sunspot_number_with_silso(
            df, body.config
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    img = utils.fig_to_base64(fig)
    return PreviewRes(img=img)


@router.get("/scatter", response_model=GetConfigRes[SunspotNumberScatter])
def get_scatter(
    query: GetConfigQuery = Depends(),
) -> GetConfigRes[SunspotNumberScatter]:
    return get_config(query, SunspotNumberScatter)


@router.post("/scatter", response_model=CreateConfigRes)
def post_scatter(
    body: CreateConfigBody[SunspotNumberScatter],
) -> CreateConfigRes:
    output_dir = Path("config/sunspot_number/scatter")
    return post_config(body, output_dir)


@router.post("/scatter/preview", response_model=PreviewRes)
def scatter_preview(body: PreviewBody[SunspotNumberScatter]) -> PreviewRes:
    df = pl.DataFrame(
        {
            "seiryo": np.abs(
                np.linspace(0, 123.456, 200)
                + np.sin(np.linspace(1, 200, 200)) * np.linspace(1, 10, 200)
            ),
            "silso": np.abs(
                np.linspace(0, 100, 200)
                + np.cos(np.linspace(1, 200, 200)) * np.linspace(1, 10, 200)
            ),
        }
    )
    factor = 1.23456
    r2 = 0.87654
    try:
        fig = sunspot_number_with_silso.draw_scatter(
            df, factor, r2, body.config
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    img = utils.fig_to_base64(fig)
    return PreviewRes(img=img)


@router.get("/ratio", response_model=GetConfigRes[SunspotNumberRatio])
def get_ratio(
    query: GetConfigQuery = Depends(),
) -> GetConfigRes[SunspotNumberRatio]:
    return get_config(query, SunspotNumberRatio)


@router.post("/ratio", response_model=CreateConfigRes)
def post_ratio(body: CreateConfigBody[SunspotNumberRatio]) -> CreateConfigRes:
    output_dir = Path("config/sunspot_number/ratio")
    return post_config(body, output_dir)


@router.post("/ratio/preview", response_model=PreviewRes)
def ratio_preview(body: PreviewBody[SunspotNumberRatio]) -> PreviewRes:
    df = pl.DataFrame(
        {
            "date": pl.date_range(
                date(2010, 1, 1), date(2020, 12, 1), "1mo", eager=True
            ),
            "ratio": 1.23456
            + np.cos(np.linspace(-0.5, 3.5, 132)) * np.tile([1, -1], 66),
        }
    )
    factor = 1.23456
    try:
        fig = sunspot_number_with_silso.draw_ratio(df, factor, body.config)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    img = utils.fig_to_base64(fig)
    return PreviewRes(img=img)


@router.get("/diff", response_model=GetConfigRes[SunspotNumberDiff])
def get_diff(
    query: GetConfigQuery = Depends(),
) -> GetConfigRes[SunspotNumberDiff]:
    return get_config(query, SunspotNumberDiff)


@router.post("/diff", response_model=CreateConfigRes)
def post_diff(body: CreateConfigBody[SunspotNumberDiff]) -> CreateConfigRes:
    output_dir = Path("config/sunspot_number/diff")
    return post_config(body, output_dir)


@router.post("/diff/preview", response_model=PreviewRes)
def diff_preview(body: PreviewBody[SunspotNumberDiff]) -> PreviewRes:
    df = pl.DataFrame(
        {
            "date": pl.date_range(
                date(2010, 1, 1), date(2020, 12, 1), "1mo", eager=True
            ),
            "diff": np.sin(np.linspace(-0.5, 3.5, 132))
            * np.tile([1, -1], 66)
            * 50,
        }
    )
    try:
        fig = sunspot_number_with_silso.draw_diff(df, body.config)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    img = utils.fig_to_base64(fig)
    return PreviewRes(img=img)


@router.get(
    "/ratio_diff_1", response_model=GetConfigRes[SunspotNumberRatioDiff1]
)
def get_ratio_diff_1(
    query: GetConfigQuery = Depends(),
) -> GetConfigRes[SunspotNumberRatioDiff1]:
    return get_config(query, SunspotNumberRatioDiff1)


@router.post("/ratio_diff_1", response_model=CreateConfigRes)
def post_ratio_diff_1(
    body: CreateConfigBody[SunspotNumberRatioDiff1],
) -> CreateConfigRes:
    output_dir = Path("config/sunspot_number/ratio_diff_1")
    return post_config(body, output_dir)


@router.post("/ratio_diff_1/preview", response_model=PreviewRes)
def ratio_diff_1_preview(
    body: PreviewBody[SunspotNumberRatioDiff1],
) -> PreviewRes:
    df = pl.DataFrame(
        {
            "date": pl.date_range(
                date(2010, 1, 1), date(2020, 12, 1), "1mo", eager=True
            ),
            "ratio": 1.23456
            + np.cos(np.linspace(-0.5, 3.5, 132)) * np.tile([1, -1], 66),
            "diff": np.sin(np.linspace(-0.5, 3.5, 132))
            * np.tile([1, -1], 66)
            * 50,
        }
    )
    factor = 1.23456
    try:
        fig = sunspot_number_with_silso.draw_ratio_diff_1(
            df, factor, body.config
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    img = utils.fig_to_base64(fig)
    return PreviewRes(img=img)


@router.get(
    "/ratio_diff_2", response_model=GetConfigRes[SunspotNumberRatioDiff2]
)
def get_ratio_diff_2(
    query: GetConfigQuery = Depends(),
) -> GetConfigRes[SunspotNumberRatioDiff2]:
    return get_config(query, SunspotNumberRatioDiff2)


@router.post("/ratio_diff_2", response_model=CreateConfigRes)
def post_ratio_diff_2(
    body: CreateConfigBody[SunspotNumberRatioDiff2],
) -> CreateConfigRes:
    output_dir = Path("config/sunspot_number/ratio_diff_2")
    return post_config(body, output_dir)


@router.post("/ratio_diff_2/preview", response_model=PreviewRes)
def ratio_diff_2_preview(
    body: PreviewBody[SunspotNumberRatioDiff2],
) -> PreviewRes:
    df = pl.DataFrame(
        {
            "date": pl.date_range(
                date(2010, 1, 1), date(2020, 12, 1), "1mo", eager=True
            ),
            "ratio": 1.23456
            + np.cos(np.linspace(-0.5, 3.5, 132)) * np.tile([1, -1], 66),
            "diff": np.sin(np.linspace(-0.5, 3.5, 132))
            * np.tile([1, -1], 66)
            * 50,
        }
    )
    try:
        fig = sunspot_number_with_silso.draw_ratio_diff_2(df, body.config)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    img = utils.fig_to_base64(fig)
    return PreviewRes(img=img)
