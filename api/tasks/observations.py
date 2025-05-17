import json
from pathlib import Path

import matplotlib as mpl
import polars as pl

mpl.use("Agg")

from seiryo_sunspot_lib import observations
from seiryo_sunspot_lib.observations_config import ObservationsMonthly


def draw_monthly_obs_days(
    data_path: str,
    config_path: str,
    output_path: str,
    *,
    fmt: str = "png",
    dpi: int | None = None,
) -> None:
    df = pl.read_parquet(Path(data_path))
    with Path(config_path).open("r") as f_config:
        config = ObservationsMonthly(**json.load(f_config))
    fig = observations.draw_monthly_obs_days(df, config)
    fig.savefig(
        Path(output_path),
        format=fmt,
        dpi=dpi if dpi is not None else "figure",
        bbox_inches="tight",
        pad_inches=0.1,
    )
