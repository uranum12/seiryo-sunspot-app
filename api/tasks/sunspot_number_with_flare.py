import json
from pathlib import Path

import matplotlib as mpl
import polars as pl

mpl.use("Agg")

from seiryo_sunspot_lib import sunspot_number_with_flare
from seiryo_sunspot_lib.sunspot_number_with_flare_config import (
    SunspotNumberWithFlare,
    SunspotNumberWithFlareHemispheric,
)


def draw_sunspot_number_with_flare(  # noqa: PLR0913
    data_path: str,
    factors_path: str | None,
    config_path: str,
    output_path: str,
    *,
    fmt: str = "png",
    dpi: int | None = None,
) -> None:
    df = pl.read_parquet(Path(data_path))
    if factors_path is not None:
        with Path(factors_path).open("r") as f_factors:
            json_data = json.load(f_factors)
            factor = json_data["total"]
    else:
        factor = None
    with Path(config_path).open("r") as f_config:
        config = SunspotNumberWithFlare(**json.load(f_config))
    fig = sunspot_number_with_flare.draw_sunspot_number_with_flare(
        df, config, factor=factor
    )
    fig.savefig(
        Path(output_path),
        format=fmt,
        dpi=dpi if dpi is not None else "figure",
        bbox_inches="tight",
        pad_inches=0.1,
    )


def draw_sunspot_number_with_flare_hemispheric(  # noqa: PLR0913
    data_path: str,
    factors_path: str | None,
    config_path: str,
    output_path: str,
    *,
    fmt: str = "png",
    dpi: int | None = None,
) -> None:
    df = pl.read_parquet(Path(data_path))
    if factors_path is not None:
        with Path(factors_path).open("r") as f_factors:
            json_data = json.load(f_factors)
            factor_north = json_data["north"]
            factor_south = json_data["south"]
    else:
        factor_north = None
        factor_south = None
    with Path(config_path).open("r") as f_config:
        config = SunspotNumberWithFlareHemispheric(**json.load(f_config))
    fig = sunspot_number_with_flare.draw_sunspot_number_with_flare_hemispheric(
        df, config, factor_north=factor_north, factor_south=factor_south
    )
    fig.savefig(
        Path(output_path),
        format=fmt,
        dpi=dpi if dpi is not None else "figure",
        bbox_inches="tight",
        pad_inches=0.1,
    )
