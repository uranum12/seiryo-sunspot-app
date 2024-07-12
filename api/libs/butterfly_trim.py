from datetime import date

import polars as pl

from api.libs.butterfly import ButterflyInfo, fill_lat


def trim_info(
    info: ButterflyInfo,
    lat_min: int | None = None,
    lat_max: int | None = None,
    date_start: date | None = None,
    date_end: date | None = None,
) -> ButterflyInfo:
    return ButterflyInfo(
        lat_min if lat_min is not None else info.lat_min,
        lat_max if lat_max is not None else info.lat_max,
        date_start if date_start is not None else info.date_start,
        date_end if date_end is not None else info.date_end,
        info.date_interval,
    )


def trim_data(df: pl.DataFrame, info: ButterflyInfo) -> pl.DataFrame:
    return (
        df.lazy()
        .filter(pl.col("date").is_between(info.date_start, info.date_end))
        .pipe(
            fill_lat,
            start=info.date_start,
            end=info.date_end,
            interval=info.date_interval.to_interval(),
        )
        .collect()
    )
