import json
from pathlib import Path

import matplotlib as mpl
import polars as pl

mpl.use("Agg")

from api.libs import sunspot_number_with_silso
from api.libs.sunspot_number_with_silso_config import (
    SunspotNumberDiff,
    SunspotNumberRatio,
    SunspotNumberRatioDiff1,
    SunspotNumberRatioDiff2,
    SunspotNumberScatter,
    SunspotNumberWithSilso,
)


def draw_sunspot_number_with_silso(
    data_path: str,
    config_path: str,
    output_path: str,
    *,
    fmt: str = "png",
    dpi: int | None = None,
) -> None:
    df = pl.read_parquet(Path(data_path))
    with Path(config_path).open("r") as f_config:
        config = SunspotNumberWithSilso(**json.load(f_config))
    fig = sunspot_number_with_silso.draw_sunspot_number_with_silso(df, config)
    fig.savefig(
        Path(output_path),
        format=fmt,
        dpi=dpi if dpi is not None else "figure",
        bbox_inches="tight",
        pad_inches=0.1,
    )


def draw_scatter(  # noqa: PLR0913
    data_path: str,
    factor_r2_path: str,
    config_path: str,
    output_path: str,
    *,
    fmt: str = "png",
    dpi: int | None = None,
) -> None:
    df = pl.read_parquet(Path(data_path))
    with Path(factor_r2_path).open("r") as f_factor_r2:
        json_data = json.load(f_factor_r2)
        factor = json_data["factor"]
        r2 = json_data["r2"]
    with Path(config_path).open("r") as f_config:
        config = SunspotNumberScatter(**json.load(f_config))
    fig = sunspot_number_with_silso.draw_scatter(df, factor, r2, config)
    fig.savefig(
        Path(output_path),
        format=fmt,
        dpi=dpi if dpi is not None else "figure",
        bbox_inches="tight",
        pad_inches=0.1,
    )


def draw_ratio(  # noqa: PLR0913
    data_path: str,
    factor_r2_path: str,
    config_path: str,
    output_path: str,
    *,
    fmt: str = "png",
    dpi: int | None = None,
) -> None:
    df = pl.read_parquet(Path(data_path))
    with Path(factor_r2_path).open("r") as f_factor_r2:
        json_data = json.load(f_factor_r2)
        factor = json_data["factor"]
    with Path(config_path).open("r") as f_config:
        config = SunspotNumberRatio(**json.load(f_config))
    fig = sunspot_number_with_silso.draw_ratio(df, factor, config)
    fig.savefig(
        Path(output_path),
        format=fmt,
        dpi=dpi if dpi is not None else "figure",
        bbox_inches="tight",
        pad_inches=0.1,
    )


def draw_diff(
    data_path: str,
    config_path: str,
    output_path: str,
    *,
    fmt: str = "png",
    dpi: int | None = None,
) -> None:
    df = pl.read_parquet(Path(data_path))
    with Path(config_path).open("r") as f_config:
        config = SunspotNumberDiff(**json.load(f_config))
    fig = sunspot_number_with_silso.draw_diff(df, config)
    fig.savefig(
        Path(output_path),
        format=fmt,
        dpi=dpi if dpi is not None else "figure",
        bbox_inches="tight",
        pad_inches=0.1,
    )


def draw_ratio_diff_1(  # noqa: PLR0913
    data_path: str,
    factor_r2_path: str,
    config_path: str,
    output_path: str,
    *,
    fmt: str = "png",
    dpi: int | None = None,
) -> None:
    df = pl.read_parquet(Path(data_path))
    with Path(factor_r2_path).open("r") as f_factor_r2:
        json_data = json.load(f_factor_r2)
        factor = json_data["factor"]
    with Path(config_path).open("r") as f_config:
        config = SunspotNumberRatioDiff1(**json.load(f_config))
    fig = sunspot_number_with_silso.draw_ratio_diff_1(df, factor, config)
    fig.savefig(
        Path(output_path),
        format=fmt,
        dpi=dpi if dpi is not None else "figure",
        bbox_inches="tight",
        pad_inches=0.1,
    )


def draw_ratio_diff_2(
    data_path: str,
    config_path: str,
    output_path: str,
    *,
    fmt: str = "png",
    dpi: int | None = None,
) -> None:
    df = pl.read_parquet(Path(data_path))
    with Path(config_path).open("r") as f_config:
        config = SunspotNumberRatioDiff2(**json.load(f_config))
    fig = sunspot_number_with_silso.draw_ratio_diff_2(df, config)
    fig.savefig(
        Path(output_path),
        format=fmt,
        dpi=dpi if dpi is not None else "figure",
        bbox_inches="tight",
        pad_inches=0.1,
    )
