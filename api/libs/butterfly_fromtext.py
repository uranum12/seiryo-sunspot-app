from datetime import date
from pathlib import Path
from re import match

import polars as pl


def load_txt_data(path: Path) -> tuple[date, date, list[str]]:
    with path.open("r") as f:
        lines = f.read().splitlines()
    if m := match(r">>(\d+)/(\d+)-(\d+)/(\d+)", lines[1]):
        start = date(int(m.group(1)), int(m.group(2)), 1)
        end = date(int(m.group(3)), int(m.group(4)), 1)
    else:
        msg = "invalid date range data"
        raise ValueError(msg)
    return start, end, lines[4:]


def extract_lat(txt: list[str]) -> pl.LazyFrame:
    pat = (
        r"(?P<year>\d+)/(?P<month>\d+)/(?<ns>[NS]):"
        r"(?P<lat>\d+-\d+(?: \d+-\d+)*)?"
    )
    return (
        pl.LazyFrame({"txt": txt})
        .select(pl.col("txt").str.extract_groups(pat))
        .unnest("txt")
        .with_columns(
            pl.col("lat")
            .str.split(by=" ")
            .list.eval(pl.element().str.split(by="-"))
        )
        .explode("lat")
        .drop_nulls()
        .cast({"lat": pl.List(pl.Int8)})
        .with_columns(
            pl.when(pl.col("ns").eq("N"))
            .then(pl.col("lat"))
            .otherwise(pl.col("lat").list.eval(-pl.element()))
        )
        .select(
            pl.date("year", "month", 1).alias("date"),
            pl.col("lat").list.min().alias("lat_min"),
            pl.col("lat").list.max().alias("lat_max"),
        )
    )
