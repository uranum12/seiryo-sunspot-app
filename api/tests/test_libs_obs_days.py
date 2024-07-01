from datetime import date

import polars as pl
import pytest
from polars.testing import assert_frame_equal

from api.libs import obs_days
from api.libs.config_common import Axis, Bar, FigSize, Ticks, Title
from api.libs.obs_days_config import ObservationsMonthly


@pytest.mark.parametrize(
    ("in_date", "out_start", "out_end"),
    [
        (
            [
                date(2020, 2, 2),
                date(2020, 1, 1),
                date(2020, 3, 3),
                date(2020, 5, 5),
                date(2020, 4, 4),
            ],
            date(2020, 1, 1),
            date(2020, 5, 5),
        ),
        (
            [
                date(2020, 3, 3),
                date(2020, 3, 3),
                date(2020, 5, 5),
                date(2020, 3, 3),
                date(2020, 12, 25),
            ],
            date(2020, 3, 3),
            date(2020, 12, 25),
        ),
        ([date(2020, 2, 2)], date(2020, 2, 2), date(2020, 2, 2)),
    ],
)
def test_calc_date_range(
    in_date: list[date], out_start: date, out_end: date
) -> None:
    df = pl.LazyFrame({"date": in_date}, schema={"date": pl.Date})
    start, end = obs_days.calc_date_range(df)
    assert start == out_start
    assert end == out_end


@pytest.mark.parametrize(
    ("in_start", "in_end", "out_start", "out_end"),
    [
        (
            date(2020, 3, 3),
            date(2020, 5, 5),
            date(2020, 3, 1),
            date(2020, 5, 31),
        ),
        (
            date(2020, 1, 1),
            date(2020, 2, 2),
            date(2020, 1, 1),
            date(2020, 2, 29),
        ),
        (
            date(2020, 12, 25),
            date(2021, 2, 2),
            date(2020, 12, 1),
            date(2021, 2, 28),
        ),
    ],
)
def test_adjust_dates(
    in_start: date, in_end: date, out_start: date, out_end: date
) -> None:
    start, end = obs_days.adjust_dates(in_start, in_end)
    assert start == out_start
    assert end == out_end


@pytest.mark.parametrize(
    ("in_date", "in_start", "in_end", "out_date", "out_obs"),
    [
        (
            [
                date(2020, 2, 2),
                date(2020, 2, 5),
                date(2020, 2, 6),
                date(2020, 2, 8),
                date(2020, 2, 4),
            ],
            date(2020, 2, 1),
            date(2020, 2, 10),
            [
                date(2020, 2, 1),
                date(2020, 2, 2),
                date(2020, 2, 3),
                date(2020, 2, 4),
                date(2020, 2, 5),
                date(2020, 2, 6),
                date(2020, 2, 7),
                date(2020, 2, 8),
                date(2020, 2, 9),
                date(2020, 2, 10),
            ],
            [
                0,  # 2/1
                1,  # 2/2
                0,  # 2/3
                1,  # 2/4
                1,  # 2/5
                1,  # 2/6
                0,  # 2/7
                1,  # 2/8
                0,  # 2/9
                0,  # 2/10
            ],
        ),
        (
            [
                date(2020, 2, 2),
                date(2020, 2, 5),
                date(2020, 2, 6),
                date(2020, 2, 8),
                date(2020, 2, 4),
            ],
            date(2020, 2, 3),
            date(2020, 2, 5),
            [date(2020, 2, 3), date(2020, 2, 4), date(2020, 2, 5)],
            [
                0,  # 2/3
                1,  # 2/4
                1,  # 2/5
            ],
        ),
        (
            [
                date(2020, 8, 10),
                date(2020, 8, 10),
                date(2020, 8, 12),
                date(2020, 8, 12),
                date(2020, 8, 12),
                date(2020, 8, 15),
                date(2020, 8, 15),
            ],
            date(2020, 8, 10),
            date(2020, 8, 15),
            [
                date(2020, 8, 10),
                date(2020, 8, 11),
                date(2020, 8, 12),
                date(2020, 8, 13),
                date(2020, 8, 14),
                date(2020, 8, 15),
            ],
            [
                1,  # 8/10
                0,  # 8/11
                1,  # 8/12
                0,  # 8/13
                0,  # 8/14
                1,  # 8/15
            ],
        ),
    ],
)
def test_calc_dayly_obs(
    in_date: list[date],
    in_start: date,
    in_end: date,
    out_date: list[date],
    out_obs: list[int],
) -> None:
    df_in = pl.LazyFrame({"date": in_date}, schema={"date": pl.Date})
    df_expected = pl.LazyFrame(
        {"date": out_date, "obs": out_obs},
        schema={"date": pl.Date, "obs": pl.UInt8},
    )
    df_out = obs_days.calc_dayly_obs(df_in, in_start, in_end)
    assert_frame_equal(df_out, df_expected)


@pytest.mark.parametrize(
    ("in_date", "in_obs", "out_date", "out_obs"),
    [
        (
            [
                date(2020, 5, 30),
                date(2020, 5, 31),
                date(2020, 6, 1),
                date(2020, 6, 2),
                date(2020, 6, 3),
            ],
            [
                1,  # 5/30
                1,  # 5/31
                0,  # 6/1
                1,  # 6/2
                0,  # 6/3
            ],
            [date(2020, 5, 1), date(2020, 6, 1)],
            [2, 1],
        ),
        (
            [
                date(2020, 5, 30),
                date(2020, 5, 31),
                date(2020, 6, 1),
                date(2020, 8, 7),
                date(2020, 8, 8),
            ],
            [
                1,  # 5/30
                1,  # 5/31
                0,  # 6/1
                1,  # 8/7
                0,  # 8/8
            ],
            [date(2020, 5, 1), date(2020, 6, 1), date(2020, 8, 1)],
            [2, 0, 1],
        ),
    ],
)
def test_calc_monthly_obs(
    in_date: list[date],
    in_obs: list[int],
    out_date: list[date],
    out_obs: list[int],
) -> None:
    df_in = pl.LazyFrame(
        {"date": in_date, "obs": in_obs},
        schema={"date": pl.Date, "obs": pl.UInt8},
    )
    df_expected = pl.LazyFrame(
        {"date": out_date, "obs": out_obs},
        schema={"date": pl.Date, "obs": pl.UInt8},
    )
    df_out = obs_days.calc_monthly_obs(df_in)
    assert_frame_equal(df_out, df_expected)


def test_draw_monthly_obs_days() -> None:
    df = pl.DataFrame(
        {
            "date": [date(2020, 1, 1), date(2020, 2, 1), date(2020, 3, 1)],
            "obs": [3, 0, 2],
        },
        schema={"date": pl.Date, "obs": pl.UInt8},
    )
    config = ObservationsMonthly(
        fig_size=FigSize(width=8.0, height=5.0),
        bar=Bar(label="", width=15.0, color="C0"),
        title=Title(
            text="observations days per month",
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
                text="observations days",
                font_family="Times New Roman",
                font_size=16,
                position=1.0,
            ),
            ticks=Ticks(font_family="Times New Roman", font_size=12),
        ),
    )
    _ = obs_days.draw_monthly_obs_days(df, config)
