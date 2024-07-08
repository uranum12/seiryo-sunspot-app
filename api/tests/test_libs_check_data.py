from datetime import date

import polars as pl
import pytest
from polars.testing import assert_frame_equal, assert_series_equal

from api.libs import check_data


@pytest.mark.parametrize(
    ("in_no", "out_no"),
    [
        pytest.param(1, [1]),
        pytest.param(3, [1, 2, 3]),
        pytest.param(5, [1, 2, 3, 4, 5]),
    ],
)
def test_create_expected_group_numbers(in_no: int, out_no: list[int]) -> None:
    s_out = check_data.create_expected_group_numbers(in_no)
    s_expected = pl.Series(out_no, dtype=pl.UInt8)
    assert_series_equal(s_out, s_expected)


@pytest.mark.parametrize(
    ("in_date", "in_no", "out_date", "out_original", "out_expected"),
    [
        (
            [date(2020, 8, 20), date(2020, 8, 20), date(2020, 8, 20)],
            [1, 2, 1],
            [date(2020, 8, 20)],
            [[1, 1, 2]],
            [[1, 2, 3]],
        ),
        (
            [date(2020, 2, 2), date(2020, 2, 2), date(2020, 3, 3)],
            [1, 1, 2],
            [date(2020, 2, 2), date(2020, 3, 3)],
            [[1, 1], [2]],
            [[1, 2], [1]],
        ),
        (
            [date(2020, 12, 24), date(2020, 12, 24), date(2020, 12, 25)],
            [1, 2, 1],
            [],
            [],
            [],
        ),
        (
            [date(2020, 8, 20), date(2020, 8, 21), date(2020, 8, 22)],
            [0, 0, 1],
            [],
            [],
            [],
        ),
    ],
)
def test_find_invalid_group_number(
    in_date: list[date],
    in_no: list[int],
    out_date: list[date],
    out_original: list[int],
    out_expected: list[int],
) -> None:
    df_in = pl.DataFrame(
        {"date": in_date, "no": in_no},
        schema={"date": pl.Date, "no": pl.UInt8},
    )
    df_expected = pl.DataFrame(
        {"date": out_date, "original": out_original, "expected": out_expected},
        schema={
            "date": pl.Date,
            "original": pl.List(pl.UInt8),
            "expected": pl.List(pl.UInt8),
        },
    )
    df_out = check_data.find_invalid_group_number(df_in).sort("date")
    assert_frame_equal(df_out, df_expected, check_column_order=False)


@pytest.mark.parametrize(
    ("in_lat_min", "in_lat_max", "in_threshold", "out_lat_min", "out_lat_max"),
    [
        (
            [10, 20, 30, 40, 50],
            [-50, -40, -30, -20, -10],
            40,
            [10, 50],
            [-50, -10],
        ),
        ([1, 2, 3, 4, 5], [-5, -4, -3, -2, -1], 10, [], []),
    ],
)
def test_find_invalid_lat_range(
    in_lat_min: list[int],
    in_lat_max: list[int],
    in_threshold: int,
    out_lat_min: list[int],
    out_lat_max: list[int],
) -> None:
    df_in = pl.DataFrame(
        {"lat_min": in_lat_min, "lat_max": in_lat_max},
        schema={"lat_min": pl.Int8, "lat_max": pl.Int8},
    )
    df_expected = pl.DataFrame(
        {"lat_min": out_lat_min, "lat_max": out_lat_max},
        schema={"lat_min": pl.Int8, "lat_max": pl.Int8},
    )
    df_out = check_data.find_invalid_lat_range(df_in, in_threshold)
    assert_frame_equal(
        df_out, df_expected, check_column_order=False, check_row_order=False
    )


@pytest.mark.parametrize(
    (
        "in_lon_min",
        "in_lon_max",
        "in_min_threshold",
        "in_max_threshold",
        "out_lon_min",
        "out_lon_max",
    ),
    [
        (
            [10, 20, 30, 40, 50],
            [-50, -40, -30, -20, -10],
            -30,
            40,
            [10, 20, 50],
            [-50, -40, -10],
        ),
        ([1, 2, 3, 4, 5], [-5, -4, -3, -2, -1], -10, 10, [], []),
    ],
)
def test_find_invalid_lon_range(
    in_lon_min: list[int],
    in_lon_max: list[int],
    in_min_threshold: int,
    in_max_threshold: int,
    out_lon_min: list[int],
    out_lon_max: list[int],
) -> None:
    df_in = pl.DataFrame(
        {"lon_min": in_lon_min, "lon_max": in_lon_max},
        schema={"lon_min": pl.Int8, "lon_max": pl.Int8},
    )
    df_expected = pl.DataFrame(
        {"lon_min": out_lon_min, "lon_max": out_lon_max},
        schema={"lon_min": pl.Int8, "lon_max": pl.Int8},
    )
    df_out = check_data.find_invalid_lon_range(
        df_in, in_min_threshold, in_max_threshold
    )
    assert_frame_equal(
        df_out, df_expected, check_column_order=False, check_row_order=False
    )


@pytest.mark.parametrize(
    (
        "in_lat_min",
        "in_lat_max",
        "in_interval",
        "out_lat_min",
        "out_lat_max",
        "out_interval",
    ),
    [
        (
            [10, 10, 10, 10, 10],
            [10, 20, 30, 40, 50],
            20,
            [10, 10],
            [40, 50],
            [30, 40],
        ),
        ([1, 1, 1, 1, 1], [1, 2, 3, 4, 5], 10, [], [], []),
    ],
)
def test_find_invalid_lat_interval(
    in_lat_min: list[int],
    in_lat_max: list[int],
    in_interval: int,
    out_lat_min: list[int],
    out_lat_max: list[int],
    out_interval: list[int],
) -> None:
    df_in = pl.DataFrame(
        {"lat_min": in_lat_min, "lat_max": in_lat_max},
        schema={"lat_min": pl.Int8, "lat_max": pl.Int8},
    )
    df_expected = pl.DataFrame(
        {
            "lat_min": out_lat_min,
            "lat_max": out_lat_max,
            "interval": out_interval,
        },
        schema={"lat_min": pl.Int8, "lat_max": pl.Int8, "interval": pl.Int8},
    )
    df_out = check_data.find_invalid_lat_interval(df_in, in_interval)
    assert_frame_equal(
        df_out, df_expected, check_column_order=False, check_row_order=False
    )


@pytest.mark.parametrize(
    (
        "in_lon_min",
        "in_lon_max",
        "in_interval",
        "out_lon_min",
        "out_lon_max",
        "out_interval",
    ),
    [
        (
            [10, 10, 10, 10, 10],
            [10, 20, 30, 40, 50],
            20,
            [10, 10],
            [40, 50],
            [30, 40],
        ),
        ([1, 1, 1, 1, 1], [1, 2, 3, 4, 5], 10, [], [], []),
    ],
)
def test_find_invalid_lon_interval(
    in_lon_min: list[int],
    in_lon_max: list[int],
    in_interval: int,
    out_lon_min: list[int],
    out_lon_max: list[int],
    out_interval: list[int],
) -> None:
    df_in = pl.DataFrame(
        {"lon_min": in_lon_min, "lon_max": in_lon_max},
        schema={"lon_min": pl.Int8, "lon_max": pl.Int8},
    )
    df_expected = pl.DataFrame(
        {
            "lon_min": out_lon_min,
            "lon_max": out_lon_max,
            "interval": out_interval,
        },
        schema={"lon_min": pl.Int8, "lon_max": pl.Int8, "interval": pl.Int8},
    )
    df_out = check_data.find_invalid_lon_interval(df_in, in_interval)
    assert_frame_equal(
        df_out, df_expected, check_column_order=False, check_row_order=False
    )
