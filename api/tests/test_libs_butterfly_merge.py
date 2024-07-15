from datetime import date

import numpy as np
import polars as pl
import pytest

from api.libs import butterfly, butterfly_merge


def test_merge_info() -> None:
    info1 = butterfly.ButterflyInfo(
        -10,
        50,
        date(2020, 1, 1),
        date(2020, 2, 2),
        butterfly.DateDelta(months=1),
    )
    info2 = butterfly.ButterflyInfo(
        -40,
        40,
        date(2010, 5, 1),
        date(2011, 12, 1),
        butterfly.DateDelta(months=1),
    )
    info_expected = butterfly.ButterflyInfo(
        -40,
        50,
        date(2010, 5, 1),
        date(2020, 2, 2),
        butterfly.DateDelta(months=1),
    )
    info_merged = butterfly_merge.merge_info([info1, info2])
    assert info_merged == info_expected


def test_merge_info_with_error() -> None:
    info1 = butterfly.ButterflyInfo(
        -10,
        50,
        date(2020, 1, 1),
        date(2020, 2, 2),
        butterfly.DateDelta(months=1),
    )
    info2 = butterfly.ButterflyInfo(
        -40,
        40,
        date(2010, 5, 1),
        date(2011, 12, 1),
        butterfly.DateDelta(days=1),
    )
    with pytest.raises(ValueError, match="Date interval must be equal"):
        _ = butterfly_merge.merge_info([info1, info2])


@pytest.mark.parametrize(
    ("in_data", "out_img"),
    [
        pytest.param(
            [
                {
                    "date": [
                        date(2020, 2, 1),
                        date(2020, 2, 2),
                        date(2020, 2, 3),
                        date(2020, 2, 4),
                        date(2020, 2, 5),
                    ],
                    "min": [[], [-2, 1], [0], [-1, 1], [-1]],
                    "max": [[], [-1, 2], [1], [-1, 1], [2]],
                },
                {
                    "date": [
                        date(2020, 2, 1),
                        date(2020, 2, 2),
                        date(2020, 2, 3),
                        date(2020, 2, 4),
                        date(2020, 2, 5),
                    ],
                    "min": [[0], [0], [-4], [-1, 1], [0]],
                    "max": [[0], [1], [-2], [0, 2], [1]],
                },
            ],
            [
                [0, 1, 0, 2, 1],  # +2
                [0, 1, 0, 2, 1],
                [0, 3, 1, 3, 3],  # +1
                [0, 2, 1, 0, 3],
                [2, 2, 1, 2, 3],  # 0
                [0, 0, 0, 2, 1],
                [0, 1, 0, 3, 1],  # -1
                [0, 1, 0, 0, 0],
                [0, 1, 2, 0, 0],  # -2
            ],
        ),
        pytest.param(
            [
                {
                    "date": [date(2020, 2, 1), date(2020, 2, 2)],
                    "min": [[1], [1]],
                    "max": [[1], [1]],
                },
                {
                    "date": [date(2020, 2, 2), date(2020, 2, 3)],
                    "min": [[0], [0]],
                    "max": [[0], [0]],
                },
                {
                    "date": [date(2020, 2, 3), date(2020, 2, 4)],
                    "min": [[-1], [-1]],
                    "max": [[-1], [-1]],
                },
                {
                    "date": [date(2020, 2, 4), date(2020, 2, 5)],
                    "min": [[-2], [-2]],
                    "max": [[-2], [-2]],
                },
                {
                    "date": [date(2020, 2, 5), date(2020, 2, 6)],
                    "min": [[2], [2]],
                    "max": [[2], [2]],
                },
            ],
            [
                [0, 0, 0, 0, 16],  # +2
                [0, 0, 0, 0, 0],
                [1, 1, 0, 0, 0],  # +1
                [0, 0, 0, 0, 0],
                [0, 2, 2, 0, 0],  # 0
                [0, 0, 0, 0, 0],
                [0, 0, 4, 4, 0],  # -1
                [0, 0, 0, 0, 0],
                [0, 0, 0, 8, 8],  # -2
            ],
        ),
    ],
)
def test_create_merged_image(
    in_data: list[dict[str, list]], out_img: list[list[int]]
) -> None:
    dfl_in = [
        pl.DataFrame(
            data,
            schema={
                "date": pl.Date,
                "min": pl.List(pl.Int8),
                "max": pl.List(pl.Int8),
            },
        )
        for data in in_data
    ]
    info = butterfly.ButterflyInfo.from_dict(
        {
            "lat_min": -2,
            "lat_max": 2,
            "date_start": "2020-02-01",
            "date_end": "2020-02-05",
            "date_interval": "P1D",
        }
    )
    out = butterfly_merge.create_merged_image(dfl_in, info)
    np.testing.assert_equal(out, out_img)


@pytest.mark.parametrize(
    ("in_img", "in_cmap", "out_img"),
    [
        pytest.param(
            [[0, 0, 0], [0, 1, 2], [3, 2, 1]],
            [
                butterfly_merge.Color(red=0xFF, green=0x00, blue=0x00),
                butterfly_merge.Color(red=0x00, green=0xFF, blue=0x00),
                butterfly_merge.Color(red=0x00, green=0x00, blue=0xFF),
            ],
            [
                [[0xFF, 0xFF, 0xFF], [0xFF, 0xFF, 0xFF], [0xFF, 0xFF, 0xFF]],
                [[0xFF, 0xFF, 0xFF], [0xFF, 0x00, 0x00], [0x00, 0xFF, 0x00]],
                [[0x00, 0x00, 0xFF], [0x00, 0xFF, 0x00], [0xFF, 0x00, 0x00]],
            ],
        ),
        pytest.param(
            [[1, 2, 4], [1, 2, 4], [1, 2, 4]],
            [
                butterfly_merge.Color(red=0xFF, green=0x00, blue=0x00),
                butterfly_merge.Color(red=0x00, green=0xFF, blue=0x00),
                butterfly_merge.Color(red=0x00, green=0x00, blue=0xFF),
                butterfly_merge.Color(red=0xFF, green=0xFF, blue=0x00),
                butterfly_merge.Color(red=0xFF, green=0x00, blue=0xFF),
                butterfly_merge.Color(red=0x00, green=0xFF, blue=0xFF),
            ],
            [
                [[0xFF, 0x00, 0x00], [0x00, 0xFF, 0x00], [0xFF, 0xFF, 0x00]],
                [[0xFF, 0x00, 0x00], [0x00, 0xFF, 0x00], [0xFF, 0xFF, 0x00]],
                [[0xFF, 0x00, 0x00], [0x00, 0xFF, 0x00], [0xFF, 0xFF, 0x00]],
            ],
        ),
    ],
)
def test_create_color_image(
    in_img: list[list[int]],
    in_cmap: list[butterfly_merge.Color],
    out_img: list[list[list[int]]],
) -> None:
    out = butterfly_merge.create_color_image(
        np.array(in_img, dtype=np.uint16), in_cmap
    )
    np.testing.assert_equal(out, out_img)
