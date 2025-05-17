import json
from pathlib import Path

import matplotlib as mpl
import polars as pl

mpl.use("Agg")

from seiryo_sunspot_lib import sunspot_number
from seiryo_sunspot_lib.sunspot_number_config import (
    SunspotNumberHemispheric,
    SunspotNumberWholeDisk,
)


def draw_sunspot_number_whole_disk(
    data_path: str,
    config_path: str,
    output_path: str,
    *,
    fmt: str = "png",
    dpi: int | None = None,
) -> None:
    df = pl.read_parquet(Path(data_path))
    with Path(config_path).open("r") as f_config:
        config = SunspotNumberWholeDisk(**json.load(f_config))
    fig = sunspot_number.draw_sunspot_number_whole_disk(df, config)
    fig.savefig(
        Path(output_path),
        format=fmt,
        dpi=dpi if dpi is not None else "figure",
        bbox_inches="tight",
        pad_inches=0.1,
    )


def draw_sunspot_number_hemispheric(
    data_path: str,
    config_path: str,
    output_path: str,
    *,
    fmt: str = "png",
    dpi: int | None = None,
) -> None:
    df = pl.read_parquet(Path(data_path))
    with Path(config_path).open("r") as f_config:
        config = SunspotNumberHemispheric(**json.load(f_config))
    fig = sunspot_number.draw_sunspot_number_hemispheric(df, config)
    fig.savefig(
        Path(output_path),
        format=fmt,
        dpi=dpi if dpi is not None else "figure",
        bbox_inches="tight",
        pad_inches=0.1,
    )
