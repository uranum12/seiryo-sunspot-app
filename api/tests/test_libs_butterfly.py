from datetime import date

import numpy as np
import polars as pl
import pytest
from polars.testing import assert_frame_equal

from api.libs import butterfly
from api.libs.butterfly_config import ButterflyDiagram, Index
from api.libs.config_common import Axis, FigSize, Image, Ticks, Title


@pytest.mark.parametrize(
    (
        "in_years",
        "in_months",
        "in_days",
        "out_dict",
        "out_interval",
        "out_isoformat",
    ),
    [
        (0, 1, 0, {"years": 0, "months": 1, "days": 0}, "1mo", "P1M"),
        (1, 2, 3, {"years": 1, "months": 2, "days": 3}, "1y2mo3d", "P1Y2M3D"),
    ],
)
def test_date_delta(
    in_years: int,
    in_months: int,
    in_days: int,
    out_dict: dict,
    out_interval: str,
    out_isoformat: str,
) -> None:
    date_delta = butterfly.DateDelta(
        years=in_years, months=in_months, days=in_days
    )
    assert date_delta.to_dict() == out_dict
    assert date_delta.to_interval() == out_interval
    assert date_delta.isoformat() == out_isoformat


@pytest.mark.parametrize(
    ("in_str", "out_years", "out_months", "out_days"),
    [
        pytest.param("P1Y2M3D", 1, 2, 3),
        pytest.param("P1Y", 1, 0, 0),
        pytest.param("P1M", 0, 1, 0),
        pytest.param("P1D", 0, 0, 1),
        pytest.param("P12Y3D", 12, 0, 3),
    ],
)
def test_date_delta_fromisoformat(
    in_str: str, out_years: int, out_months: int, out_days: int
) -> None:
    delta_expected = butterfly.DateDelta(
        years=out_years, months=out_months, days=out_days
    )
    delta_out = butterfly.DateDelta.fromisoformat(in_str)
    assert delta_out == delta_expected


@pytest.mark.parametrize(
    ("in_years", "in_months", "in_days", "out_error_msg"),
    [
        (0, 0, 0, "all parameters cannot be zero"),
        (-1, 1, 1, "parameters cannot be negative"),
    ],
)
def test_date_delta_whith_error(
    in_years: int, in_months: int, in_days: int, out_error_msg: str
) -> None:
    with pytest.raises(ValueError, match=out_error_msg):
        _ = butterfly.DateDelta(years=in_years, months=in_months, days=in_days)


def test_butterfly_info() -> None:
    info = butterfly.ButterflyInfo(
        -50,
        50,
        date(2020, 2, 2),
        date(2020, 5, 5),
        butterfly.DateDelta(days=1),
    )
    dict_expected = {
        "lat_min": -50,
        "lat_max": 50,
        "date_start": date(2020, 2, 2),
        "date_end": date(2020, 5, 5),
        "date_interval": butterfly.DateDelta(days=1),
    }
    json_expected = (
        "{\n"
        '  "lat_min": -50,\n'
        '  "lat_max": 50,\n'
        '  "date_start": "2020-02-02",\n'
        '  "date_end": "2020-05-05",\n'
        '  "date_interval": "P1D"\n'
        "}"
    )
    assert info.to_dict() == dict_expected
    assert info.to_json() == json_expected


@pytest.mark.parametrize(
    (
        "in_dict",
        "out_lat_min",
        "out_lat_max",
        "out_date_start",
        "out_date_end",
        "out_date_interval",
    ),
    [
        pytest.param(
            {
                "lat_min": -12,
                "lat_max": 12,
                "date_start": "2020-02-02",
                "date_end": "2020-12-12",
                "date_interval": "P1M",
            },
            -12,
            12,
            date(2020, 2, 2),
            date(2020, 12, 12),
            butterfly.DateDelta(months=1),
        ),
        pytest.param(
            {
                "lat_min": 3,
                "lat_max": 12,
                "date_start": "1960-02-02",
                "date_end": "2020-12-12",
                "date_interval": "P1D",
            },
            3,
            12,
            date(1960, 2, 2),
            date(2020, 12, 12),
            butterfly.DateDelta(days=1),
        ),
    ],
)
def test_butterfly_info_from_dict(
    in_dict: dict[str, int | str],
    out_lat_min: int,
    out_lat_max: int,
    out_date_start: date,
    out_date_end: date,
    out_date_interval: butterfly.DateDelta,
) -> None:
    info_expected = butterfly.ButterflyInfo(
        out_lat_min,
        out_lat_max,
        out_date_start,
        out_date_end,
        out_date_interval,
    )
    info_out = butterfly.ButterflyInfo.from_dict(in_dict)
    assert info_out == info_expected


@pytest.mark.parametrize(
    (
        "in_lat_min",
        "in_lat_max",
        "in_date_start",
        "in_date_end",
        "out_error_msg",
    ),
    [
        (
            5,
            -5,
            date(2020, 2, 2),
            date(2020, 5, 5),
            "latitude minimum value cannot be greater than maximum value",
        ),
        (
            -50,
            50,
            date(2020, 5, 5),
            date(2020, 2, 2),
            "start date cannot be later than end date",
        ),
    ],
)
def test_butterfly_info_whith_error(
    in_lat_min: int,
    in_lat_max: int,
    in_date_start: date,
    in_date_end: date,
    out_error_msg: str,
) -> None:
    with pytest.raises(ValueError, match=out_error_msg):
        _ = butterfly.ButterflyInfo(
            in_lat_min,
            in_lat_max,
            in_date_start,
            in_date_end,
            butterfly.DateDelta(years=1),
        )


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
def test_calc_date_limit(
    in_date: list[date], out_start: date, out_end: date
) -> None:
    df = pl.LazyFrame({"date": in_date}, schema={"date": pl.Date})
    start, end = butterfly.calc_date_limit(df)
    assert start == out_start
    assert end == out_end


@pytest.mark.parametrize(
    ("in_start", "in_end", "out_start", "out_end"),
    [
        (
            date(2020, 3, 3),
            date(2020, 5, 5),
            date(2020, 3, 1),
            date(2020, 5, 1),
        ),
        (
            date(2020, 1, 1),
            date(2020, 2, 2),
            date(2020, 1, 1),
            date(2020, 2, 1),
        ),
        (
            date(2020, 12, 25),
            date(2021, 2, 1),
            date(2020, 12, 1),
            date(2021, 2, 1),
        ),
    ],
)
def test_adjust_dates(
    in_start: date, in_end: date, out_start: date, out_end: date
) -> None:
    start, end = butterfly.adjust_dates(in_start, in_end)
    assert start == out_start
    assert end == out_end


@pytest.mark.parametrize(
    (
        "in_date",
        "in_lat_min",
        "in_lat_max",
        "in_interval",
        "out_date",
        "out_min",
        "out_max",
    ),
    [
        (
            [
                date(2020, 2, 2),
                date(2020, 2, 5),
                date(2020, 2, 6),
                date(2020, 2, 8),
                date(2020, 2, 4),
            ],
            [1, 2, 3, 4, 5],
            [6, 7, 8, 9, 10],
            "1mo",  # 1 month
            [date(2020, 2, 1)],
            [[1, 2, 3, 4, 5]],
            [[6, 7, 8, 9, 10]],
        ),
        (
            [
                date(2020, 2, 2),
                date(2020, 2, 5),
                date(2020, 4, 6),
                date(2020, 4, 8),
                date(2020, 4, 4),
            ],
            [1, 2, 3, 4, 5],
            [6, 7, 8, 9, 10],
            "1mo",  # 1 month
            [date(2020, 2, 1), date(2020, 4, 1)],
            [[1, 2], [3, 4, 5]],
            [[6, 7], [8, 9, 10]],
        ),
    ],
)
def test_agg_lat(
    in_date: list[date],
    in_lat_min: list[int],
    in_lat_max: list[int],
    in_interval: str,
    out_date: list[date],
    out_min: list[list[int]],
    out_max: list[list[int]],
) -> None:
    df_in = pl.LazyFrame(
        {"date": in_date, "lat_min": in_lat_min, "lat_max": in_lat_max},
        schema={"date": pl.Date, "lat_min": pl.Int8, "lat_max": pl.Int8},
    )
    df_expected = pl.LazyFrame(
        {"date": out_date, "min": out_min, "max": out_max},
        schema={
            "date": pl.Date,
            "min": pl.List(pl.Int8),
            "max": pl.List(pl.Int8),
        },
    )
    df_out = butterfly.agg_lat(df_in, in_interval).sort("date")
    assert_frame_equal(df_out, df_expected)


@pytest.mark.parametrize(
    (
        "in_date",
        "in_min",
        "in_max",
        "in_start",
        "in_end",
        "in_interval",
        "out_date",
        "out_min",
        "out_max",
    ),
    [
        (
            [date(2020, 1, 1), date(2020, 2, 1), date(2020, 4, 1)],
            [[1, 2], [3, 4], [5, 6]],
            [[1, 2], [3, 4], [5, 6]],
            date(2020, 1, 1),
            date(2020, 5, 1),
            "1mo",  # 1 month
            [
                date(2020, 1, 1),
                date(2020, 2, 1),
                date(2020, 3, 1),
                date(2020, 4, 1),
                date(2020, 5, 1),
            ],
            [[1, 2], [3, 4], [], [5, 6], []],
            [[1, 2], [3, 4], [], [5, 6], []],
        ),
        (
            [date(2020, 1, 1), date(2020, 2, 1), date(2020, 4, 1)],
            [[1, 2], [3, 4], [5, 6]],
            [[1, 2], [3, 4], [5, 6]],
            date(2020, 2, 1),
            date(2020, 6, 1),
            "1mo",  # 1 month
            [
                date(2020, 2, 1),
                date(2020, 3, 1),
                date(2020, 4, 1),
                date(2020, 5, 1),
                date(2020, 6, 1),
            ],
            [[3, 4], [], [5, 6], [], []],
            [[3, 4], [], [5, 6], [], []],
        ),
    ],
)
def test_fill_lat(
    in_date: list[date],
    in_min: list[list[int]],
    in_max: list[list[int]],
    in_start: date,
    in_end: date,
    in_interval: str,
    out_date: list[date],
    out_min: list[list[int]],
    out_max: list[list[int]],
) -> None:
    df_in = pl.LazyFrame(
        {"date": in_date, "min": in_min, "max": in_max},
        schema={
            "date": pl.Date,
            "min": pl.List(pl.Int8),
            "max": pl.List(pl.Int8),
        },
    )
    df_expected = pl.LazyFrame(
        {"date": out_date, "min": out_min, "max": out_max},
        schema={
            "date": pl.Date,
            "min": pl.List(pl.Int8),
            "max": pl.List(pl.Int8),
        },
    )
    df_out = butterfly.fill_lat(df_in, in_start, in_end, in_interval)
    assert_frame_equal(df_out, df_expected)


def test_calc_lat() -> None:
    df_in = pl.LazyFrame(
        {
            "date": [date(2020, 2, 2), date(2020, 2, 20), date(2020, 3, 3)],
            "lat_min": [1, 2, 3],
            "lat_max": [4, 5, 6],
        },
        schema={"date": pl.Date, "lat_min": pl.Int8, "lat_max": pl.Int8},
    )
    info = butterfly.ButterflyInfo(
        0, 0, date(2020, 1, 1), date(2020, 3, 1), butterfly.DateDelta(months=1)
    )
    df_expected = pl.DataFrame(
        {
            "date": [date(2020, 1, 1), date(2020, 2, 1), date(2020, 3, 1)],
            "min": [[], [1, 2], [3]],
            "max": [[], [4, 5], [6]],
        },
        schema={
            "date": pl.Date,
            "min": pl.List(pl.Int8),
            "max": pl.List(pl.Int8),
        },
    )
    df_out = butterfly.calc_lat(df_in, info)
    assert_frame_equal(df_out, df_expected)


@pytest.mark.parametrize(
    ("in_data_min", "in_data_max", "in_lat_min", "in_lat_max", "out_line"),
    [
        (
            [2, -3, 4],
            [3, -2, 4],
            -5,
            5,
            # 5    4     3     2     1     0     1     2     3     4     5
            [0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
        ),
        (
            [-5, -4, -1, 2, 3],
            [-4, -3, 1, 4, 4],
            -5,
            5,
            # 5    4     3     2     1     0     1     2     3     4     5
            [0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1],
        ),
        (
            [-8, -6, 0, 2, 3],
            [-7, -4, 0, 4, 10],
            -5,
            5,
            # 5    4     3     2     1     0     1     2     3     4     5
            [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
        ),
        (
            [-2, 1],
            [-1, 1],
            -2,
            3,
            # 3    2     1     0     1     2
            [0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1],
        ),
        (
            [4],
            [4],
            2,
            5,
            # 5    4     3     2
            [0, 0, 1, 0, 0, 0, 0],
        ),
        (
            [1, -4],
            [4, -1],
            -1,
            1,
            # 1    0     1
            [1, 0, 0, 0, 1],
        ),
        (
            [4, -4],
            [4, -4],
            -1,
            1,
            # 1    0     1
            [0, 0, 0, 0, 0],
        ),
        (
            [],
            [],
            -1,
            1,
            # 1    0     1
            [0, 0, 0, 0, 0],
        ),
    ],
)
def test_create_line(
    in_data_min: list[int],
    in_data_max: list[int],
    in_lat_min: int,
    in_lat_max: int,
    out_line: list[int],
) -> None:
    out = butterfly.create_line(
        in_data_min, in_data_max, in_lat_min, in_lat_max
    )
    np.testing.assert_equal(out, out_line)


@pytest.mark.parametrize(
    ("in_min", "in_max", "in_lat_min", "in_lat_max", "out_img"),
    [
        (
            [[1, -2], [], [-1, 1]],
            [[1, -1], [], [2, 4]],
            -1,
            1,
            [
                [1, 0, 1],  # +1
                [0, 0, 1],
                [0, 0, 1],  # 0
                [0, 0, 1],
                [1, 0, 1],  # -1
            ],
        ),
        (
            [[1, -2], [], [-1, 1]],
            [[1, -1], [], [2, 4]],
            -2,
            2,
            [
                [0, 0, 1],  # +2
                [0, 0, 1],
                [1, 0, 1],  # +1
                [0, 0, 1],
                [0, 0, 1],  # 0
                [0, 0, 1],
                [1, 0, 1],  # -1
                [1, 0, 0],
                [1, 0, 0],  # -2
            ],
        ),
    ],
)
def test_create_image(
    in_min: list[list[int]],
    in_max: list[list[int]],
    in_lat_min: int,
    in_lat_max: int,
    out_img: list[list[int]],
) -> None:
    df_in = pl.DataFrame(
        {"min": in_min, "max": in_max},
        schema={"min": pl.List(pl.Int8), "max": pl.List(pl.Int8)},
    )
    info = butterfly.ButterflyInfo(
        in_lat_min,
        in_lat_max,
        date(2020, 2, 2),
        date(2020, 2, 2),
        butterfly.DateDelta(years=100),
    )
    out = butterfly.create_image(df_in, info)
    np.testing.assert_equal(out, out_img)


@pytest.mark.parametrize(
    ("in_start", "in_end", "in_interval", "out_index"),
    [
        (
            date(2020, 4, 4),
            date(2020, 4, 6),
            "1d",
            [
                np.datetime64("2020-04-04"),
                np.datetime64("2020-04-05"),
                np.datetime64("2020-04-06"),
            ],
        ),
        (
            date(2020, 2, 28),
            date(2020, 3, 5),
            "2d",
            [
                np.datetime64("2020-02-28"),
                np.datetime64("2020-03-01"),
                np.datetime64("2020-03-03"),
                np.datetime64("2020-03-05"),
            ],
        ),
        (
            date(2021, 2, 28),
            date(2021, 3, 4),
            "3d",
            [np.datetime64("2021-02-28"), np.datetime64("2021-03-03")],
        ),
        (
            date(2020, 4, 4),
            date(2020, 7, 16),
            "2mo",
            [np.datetime64("2020-04-04"), np.datetime64("2020-06-04")],
        ),
        (
            date(1969, 11, 1),
            date(1970, 2, 2),
            "1mo",
            [
                np.datetime64("1969-11-01"),
                np.datetime64("1969-12-01"),
                np.datetime64("1970-01-01"),
                np.datetime64("1970-02-01"),
            ],
        ),
        (
            date(2020, 2, 28),
            date(2020, 4, 1),
            "1mo1d",
            [np.datetime64("2020-02-28"), np.datetime64("2020-03-29")],
        ),
        (
            date(2020, 4, 1),
            date(2023, 12, 4),
            "1y2mo3d",
            [
                np.datetime64("2020-04-01"),
                np.datetime64("2021-06-04"),
                np.datetime64("2022-08-07"),
                np.datetime64("2023-10-10"),
            ],
        ),
    ],
)
def test_create_date_index(
    in_start: date, in_end: date, in_interval: str, out_index: list[date]
) -> None:
    out = butterfly.create_date_index(in_start, in_end, in_interval)
    np.testing.assert_equal(out, out_index)


@pytest.mark.parametrize(
    ("in_lat_min", "in_lat_max", "out_index"),
    [
        (-3, 2, [2, -1, 1, -1, 0, -1, 1, -1, 2, -1, 3]),  # S3 ~ N2
        (1, 4, [4, -1, 3, -1, 2, -1, 1]),  # N1 ~ N4
        (-3, -1, [1, -1, 2, -1, 3]),  # S3 ~ S1
    ],
)
def test_create_lat_index(
    in_lat_min: int, in_lat_max: int, out_index: list[int]
) -> None:
    out = butterfly.create_lat_index(in_lat_min, in_lat_max)
    np.testing.assert_equal(out, out_index)


def test_draw_butterfly_diagram() -> None:
    img = np.array([[1, 1, 0], [1, 0, 0], [1, 1, 1]])
    info = butterfly.ButterflyInfo(
        1, 2, date(2020, 2, 1), date(2020, 4, 1), butterfly.DateDelta(months=1)
    )
    config = ButterflyDiagram(
        fig_size=FigSize(width=8.0, height=5.0),
        index=Index(year_inteerval=10, lat_interval=10),
        image=Image(cmap="binary", aspect=1.0),
        title=Title(
            text="butterfly diagram",
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
                text="latitude",
                font_family="Times New Roman",
                font_size=16,
                position=1.0,
            ),
            ticks=Ticks(font_family="Times New Roman", font_size=12),
        ),
    )
    _ = butterfly.draw_butterfly_diagram(img, info, config)
