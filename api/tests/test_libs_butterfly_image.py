from datetime import date

import numpy as np
import polars as pl
import pytest

from api.libs import butterfly, butterfly_image


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
    out = butterfly_image.create_line(
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
    out = butterfly_image.create_image(df_in, info)
    np.testing.assert_equal(out, out_img)
