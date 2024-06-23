from datetime import date
from random import sample

import polars as pl
import pytest
from polars.testing import assert_frame_equal

from api.libs import sunspot_number
from api.libs.config_common import (
    Axis,
    FigSize,
    Legend,
    Line,
    Marker,
    Ticks,
    Title,
)
from api.libs.sunspot_number_config import (
    SunspotNumberHemispheric,
    SunspotNumberWholeDisk,
)


@pytest.mark.parametrize(
    ("in_no", "out_no_spot", "out_no_nospot"),
    [
        ([0, 1, 2, 3, 4], [1, 2, 3, 4], [0]),
        ([1, 2, 3], [1, 2, 3], []),
        ([0, 1, 0, 1, 0, 0, 1, 2, 3], [1, 1, 1, 2, 3], [0, 0, 0, 0]),
        ([0, 0, 0, 0], [], [0, 0, 0, 0]),
    ],
)
def test_split(
    in_no: list[int], out_no_spot: list[int], out_no_nospot: list[int]
) -> None:
    df_in = pl.LazyFrame({"no": in_no}, schema={"no": pl.UInt8})
    df_expected_spot = pl.LazyFrame(
        {"no": out_no_spot}, schema={"no": pl.UInt8}
    )
    df_expected_nospot = pl.LazyFrame(
        {"no": out_no_nospot}, schema={"no": pl.UInt8}
    )
    df_out_spot, df_out_nospot = sunspot_number.split(df_in)
    assert_frame_equal(df_out_spot, df_expected_spot, check_column_order=False)
    assert_frame_equal(
        df_out_nospot, df_expected_nospot, check_column_order=False
    )


@pytest.mark.parametrize(
    ("in_lat_min", "in_lat_max", "out_lat"),
    [
        (8, 8, "N"),
        (-3, -3, "S"),
        (2, 3, "N"),
        (-1, 5, "N"),
        (-2, 2, "N"),
        (-3, -1, "S"),
        (-3, 1, "S"),
        (0, 0, "N"),
    ],
)
def test_calc_lat(in_lat_min: int, in_lat_max: int, out_lat: str) -> None:
    df_in = pl.LazyFrame(
        {"lat_min": [in_lat_min], "lat_max": [in_lat_max]},
        schema={"lat_min": pl.Int8, "lat_max": pl.Int8},
    )
    df_expected = pl.LazyFrame({"lat": [out_lat]}, schema={"lat": pl.Utf8})
    df_out = sunspot_number.calc_lat(df_in)
    assert_frame_equal(df_out, df_expected, check_column_order=False)


@pytest.mark.parametrize(
    (
        "in_date",
        "in_lat",
        "in_num",
        "out_date",
        "out_ng",
        "out_nf",
        "out_sg",
        "out_sf",
        "out_tg",
        "out_tf",
    ),
    [
        (
            [date(2020, 8, 1), date(2020, 8, 1), date(2020, 8, 1)],
            ["N", "N", "S"],
            [5, 6, 8],
            [date(2020, 8, 1)],
            [2],
            [11],
            [1],
            [8],
            [3],
            [19],
        ),
        (
            [date(1965, 4, 5), date(1965, 4, 5), date(1965, 4, 5)],
            ["N", "S", "S"],
            [4, 8, 12],
            [date(1965, 4, 5)],
            [1],
            [4],
            [2],
            [20],
            [3],
            [24],
        ),
        (
            [date(2000, 12, 24), date(2000, 12, 24), date(2000, 12, 25)],
            ["S", "S", "S"],
            [1, 2, 2],
            [date(2000, 12, 24), date(2000, 12, 25)],
            [0, 0],
            [0, 0],
            [2, 1],
            [3, 2],
            [2, 1],
            [3, 2],
        ),
    ],
)
def test_calc_sn(
    in_date: list[date],
    in_lat: list[str],
    in_num: list[int],
    out_date: list[date],
    out_ng: list[int],
    out_nf: list[int],
    out_sg: list[int],
    out_sf: list[int],
    out_tg: list[int],
    out_tf: list[int],
) -> None:
    df_in = pl.LazyFrame(
        {"date": in_date, "lat": in_lat, "num": in_num},
        schema={"date": pl.Date, "lat": pl.Utf8, "num": pl.UInt16},
    )
    df_expected = pl.LazyFrame(
        {
            "date": out_date,
            "ng": out_ng,
            "nf": out_nf,
            "sg": out_sg,
            "sf": out_sf,
            "tg": out_tg,
            "tf": out_tf,
        },
        schema={
            "date": pl.Date,
            "ng": pl.UInt8,
            "nf": pl.UInt16,
            "sg": pl.UInt8,
            "sf": pl.UInt16,
            "tg": pl.UInt8,
            "tf": pl.UInt16,
        },
    )
    df_out = sunspot_number.calc_sn(df_in)
    assert_frame_equal(
        df_out, df_expected, check_column_order=False, check_row_order=False
    )


@pytest.mark.parametrize(
    "date_list",
    [
        [date(2020, 4, 5), date(2020, 4, 6), date(2020, 4, 8)],
        [date(2000, 4, 2), date(2001, 6, 3), date(2000, 2, 3)],
        [date(1969, 12, 25), date(1965, 8, 10), date(1970, 1, 1)],
    ],
)
def test_fill_sn(date_list: list[date]) -> None:
    df_in = pl.LazyFrame({"date": date_list}, schema={"date": pl.Date})
    df_expected = pl.LazyFrame(
        {
            "date": date_list,
            "ng": [0] * len(date_list),
            "nf": [0] * len(date_list),
            "sg": [0] * len(date_list),
            "sf": [0] * len(date_list),
            "tg": [0] * len(date_list),
            "tf": [0] * len(date_list),
        },
        schema={
            "date": pl.Date,
            "ng": pl.UInt8,
            "nf": pl.UInt16,
            "sg": pl.UInt8,
            "sf": pl.UInt16,
            "tg": pl.UInt8,
            "tf": pl.UInt16,
        },
    )
    df_out = sunspot_number.fill_sn(df_in)
    assert_frame_equal(
        df_out, df_expected, check_column_order=False, check_row_order=False
    )


def test_sort_sn_col_order() -> None:
    cols = ["date", "ng", "nf", "sg", "sf", "tg", "tf"]
    df_in = pl.LazyFrame(
        {col_name: [] for col_name in sample(cols, len(cols))}
    )
    df_expected = pl.LazyFrame({col_name: [] for col_name in cols})
    df_out = sunspot_number.sort(df_in)
    assert_frame_equal(df_out, df_expected, check_column_order=True)


@pytest.mark.parametrize(
    ("in_date", "out_date"),
    [
        (
            [date(2000, 4, 2), date(2001, 6, 3), date(2000, 2, 3)],
            [date(2000, 2, 3), date(2000, 4, 2), date(2001, 6, 3)],
        ),
        (
            [date(1969, 12, 25), date(1965, 8, 10), date(1970, 1, 1)],
            [date(1965, 8, 10), date(1969, 12, 25), date(1970, 1, 1)],
        ),
    ],
)
def test_sort_sn_row_order(in_date: list[date], out_date: list[date]) -> None:
    cols = ["ng", "nf", "sg", "sf", "tg", "tf"]
    df_in = pl.LazyFrame(
        {"date": in_date}, schema={"date": pl.Date}
    ).with_columns([pl.lit(None).alias(col) for col in cols])
    df_expected = pl.LazyFrame(
        {"date": out_date}, schema={"date": pl.Date}
    ).with_columns([pl.lit(None).alias(col) for col in cols])
    df_out = sunspot_number.sort(df_in)
    assert_frame_equal(
        df_out, df_expected, check_column_order=False, check_row_order=True
    )


@pytest.mark.parametrize(
    (
        "in_date",
        "in_ng",
        "in_nf",
        "in_sg",
        "in_sf",
        "in_tg",
        "in_tf",
        "out_date",
        "out_north",
        "out_south",
        "out_total",
    ),
    [
        pytest.param(
            [
                date(2020, 2, 1),
                date(2020, 2, 2),
                date(2020, 2, 3),
                date(2020, 2, 4),
                date(2020, 2, 5),
            ],
            [1, 2, 3, 4, 5],
            [2, 4, 6, 8, 10],
            [3, 2, 1, 0, 0],
            [9, 6, 3, 0, 0],
            [4, 4, 4, 4, 5],
            [11, 10, 9, 8, 10],
            [
                date(2020, 2, 1),
                date(2020, 2, 2),
                date(2020, 2, 3),
                date(2020, 2, 4),
                date(2020, 2, 5),
            ],
            [12, 24, 36, 48, 60],
            [39, 26, 13, 0, 0],
            [51, 50, 49, 48, 60],
        ),
        pytest.param(
            [
                date(2020, 1, 30),
                date(2020, 1, 31),
                date(2020, 2, 1),
                date(2020, 2, 2),
                date(2020, 2, 3),
            ],
            [1, 2, 3, 4, 5],
            [2, 4, 6, 8, 10],
            [3, 2, 1, 0, 0],
            [9, 6, 3, 0, 0],
            [4, 4, 4, 4, 4],
            [11, 10, 9, 8, 7],
            [
                date(2020, 1, 30),
                date(2020, 1, 31),
                date(2020, 2, 1),
                date(2020, 2, 2),
                date(2020, 2, 3),
            ],
            [12, 24, 36, 48, 60],
            [39, 26, 13, 0, 0],
            [51, 50, 49, 48, 47],
        ),
    ],
)
def test_agg_daily(
    in_date: list[date],
    in_ng: list[int],
    in_nf: list[int],
    in_sg: list[int],
    in_sf: list[int],
    in_tg: list[int],
    in_tf: list[int],
    out_date: list[date],
    out_north: list[int],
    out_south: list[int],
    out_total: list[int],
) -> None:
    df_in = pl.DataFrame(
        {
            "date": in_date,
            "ng": in_ng,
            "nf": in_nf,
            "sg": in_sg,
            "sf": in_sf,
            "tg": in_tg,
            "tf": in_tf,
        },
        schema={
            "date": pl.Date,
            "ng": pl.UInt8,
            "nf": pl.UInt16,
            "sg": pl.UInt8,
            "sf": pl.UInt16,
            "tg": pl.UInt8,
            "tf": pl.UInt16,
        },
    )
    df_expected = pl.DataFrame(
        {
            "date": out_date,
            "north": out_north,
            "south": out_south,
            "total": out_total,
        },
        schema={
            "date": pl.Date,
            "north": pl.Int16,
            "south": pl.Int16,
            "total": pl.Int16,
        },
    )
    df_out = sunspot_number.agg_daily(df_in)
    assert_frame_equal(df_out, df_expected)


@pytest.mark.parametrize(
    (
        "in_date",
        "in_ng",
        "in_nf",
        "in_sg",
        "in_sf",
        "in_tg",
        "in_tf",
        "out_date",
        "out_north",
        "out_south",
        "out_total",
    ),
    [
        pytest.param(
            [
                date(2020, 2, 1),
                date(2020, 2, 2),
                date(2020, 2, 3),
                date(2020, 2, 4),
                date(2020, 2, 5),
            ],
            [1, 2, 3, 4, 5],
            [2, 4, 6, 8, 10],
            [3, 2, 1, 0, 0],
            [9, 6, 3, 0, 0],
            [4, 4, 4, 4, 5],
            [11, 10, 9, 8, 10],
            [date(2020, 2, 1)],
            [36.0],
            [15.6],
            [51.6],
        ),
        pytest.param(
            [
                date(2020, 1, 30),
                date(2020, 1, 31),
                date(2020, 2, 1),
                date(2020, 2, 2),
                date(2020, 2, 3),
            ],
            [1, 2, 3, 4, 5],
            [2, 4, 6, 8, 10],
            [3, 2, 1, 0, 0],
            [9, 6, 3, 0, 0],
            [4, 4, 4, 4, 4],
            [11, 10, 9, 8, 7],
            [date(2020, 1, 1), date(2020, 2, 1)],
            [18.0, 48.0],
            [32.5, 4.33333],
            [50.5, 48.0],
        ),
    ],
)
def test_agg_monthly(
    in_date: list[date],
    in_ng: list[int],
    in_nf: list[int],
    in_sg: list[int],
    in_sf: list[int],
    in_tg: list[int],
    in_tf: list[int],
    out_date: list[date],
    out_north: list[float],
    out_south: list[float],
    out_total: list[float],
) -> None:
    df_in = pl.DataFrame(
        {
            "date": in_date,
            "ng": in_ng,
            "nf": in_nf,
            "sg": in_sg,
            "sf": in_sf,
            "tg": in_tg,
            "tf": in_tf,
        },
        schema={
            "date": pl.Date,
            "ng": pl.UInt8,
            "nf": pl.UInt16,
            "sg": pl.UInt8,
            "sf": pl.UInt16,
            "tg": pl.UInt8,
            "tf": pl.UInt16,
        },
    )
    df_expected = pl.DataFrame(
        {
            "date": out_date,
            "north": out_north,
            "south": out_south,
            "total": out_total,
        },
        schema={
            "date": pl.Date,
            "north": pl.Float64,
            "south": pl.Float64,
            "total": pl.Float64,
        },
    )
    df_out = sunspot_number.agg_monthly(df_in)
    assert_frame_equal(df_out, df_expected)


def test_draw_sunspot_number_whole_disk() -> None:
    df = pl.DataFrame(
        {
            "date": [date(2020, 2, 1), date(2020, 3, 1), date(2020, 4, 1)],
            "total": [1, 2, 3],
        },
        schema={"date": pl.Date, "total": pl.Float64},
    )
    config = SunspotNumberWholeDisk(
        fig_size=FigSize(width=8.0, height=5.0),
        line=Line(
            label="",
            style="-",
            width=1.0,
            color="C0",
            marker=Marker(marker="o", size=3.0),
        ),
        title=Title(
            text="seiryo's whole-disk sunspot number",
            font_family="Times New Roman",
            font_size=16,
            position=1.0,
        ),
        xaxis=Axis(
            title=Title(
                text="date",
                font_family="Times New Roman",
                font_size=16,
                position=1.0,
            ),
            ticks=Ticks(font_family="Times New Roman", font_size=12),
        ),
        yaxis=Axis(
            title=Title(
                text="sunspot number",
                font_family="Times New Roman",
                font_size=16,
                position=1.0,
            ),
            ticks=Ticks(font_family="Times New Roman", font_size=12),
        ),
    )
    _ = sunspot_number.draw_sunspot_number_whole_disk(df, config)


def test_draw_sunspot_number_hemispheric() -> None:
    df = pl.DataFrame(
        {
            "date": [date(2020, 2, 1), date(2020, 3, 1), date(2020, 4, 1)],
            "north": [1, 2, 3],
            "south": [2, 1, 3],
        },
        schema={"date": pl.Date, "north": pl.Float64, "south": pl.Float64},
    )
    config = SunspotNumberHemispheric(
        fig_size=FigSize(width=8.0, height=5.0),
        line_north=Line(
            label="north",
            style="-",
            width=1.0,
            color="C0",
            marker=Marker(marker="o", size=3.0),
        ),
        line_south=Line(
            label="south",
            style="-",
            width=1.0,
            color="C1",
            marker=Marker(marker="o", size=3.0),
        ),
        title=Title(
            text="seiryo's hemispheric sunspot number",
            font_family="Times New Roman",
            font_size=16,
            position=1.1,
        ),
        xaxis=Axis(
            title=Title(
                text="date",
                font_family="Times New Roman",
                font_size=16,
                position=1.0,
            ),
            ticks=Ticks(font_family="Times New Roman", font_size=12),
        ),
        yaxis=Axis(
            title=Title(
                text="sunspot number",
                font_family="Times New Roman",
                font_size=16,
                position=1.0,
            ),
            ticks=Ticks(font_family="Times New Roman", font_size=12),
        ),
        legend=Legend(font_family="Times New Roman", font_size=12),
    )
    _ = sunspot_number.draw_sunspot_number_hemispheric(df, config)
