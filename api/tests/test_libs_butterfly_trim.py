from datetime import date

import polars as pl
from polars.testing import assert_frame_equal

from api.libs import butterfly_trim
from api.libs.butterfly import ButterflyInfo, DateDelta


def test_trim_info() -> None:
    info_in = ButterflyInfo(
        -10, 10, date(2020, 2, 1), date(2020, 5, 1), DateDelta(months=1)
    )
    info_expected = ButterflyInfo(
        -5, 10, date(2020, 2, 1), date(2020, 12, 1), DateDelta(months=1)
    )
    info_out = butterfly_trim.trim_info(
        info_in, lat_min=-5, date_end=date(2020, 12, 1)
    )
    assert info_out == info_expected


def test_trim_data() -> None:
    df_in = pl.DataFrame(
        {
            "date": [
                date(2020, 1, 1),
                date(2020, 2, 1),
                date(2020, 3, 1),
                date(2020, 4, 1),
                date(2020, 5, 1),
            ],
            "min": [[1], [2], [3], [4], [5]],
            "max": [[11], [22], [33], [44], [55]],
        },
        schema={
            "date": pl.Date,
            "min": pl.List(pl.Int8),
            "max": pl.List(pl.Int8),
        },
    )
    df_expected = pl.DataFrame(
        {
            "date": [
                date(2020, 2, 1),
                date(2020, 3, 1),
                date(2020, 4, 1),
                date(2020, 5, 1),
                date(2020, 6, 1),
                date(2020, 7, 1),
            ],
            "min": [[2], [3], [4], [5], [], []],
            "max": [[22], [33], [44], [55], [], []],
        },
        schema={
            "date": pl.Date,
            "min": pl.List(pl.Int8),
            "max": pl.List(pl.Int8),
        },
    )
    info = ButterflyInfo(
        10, 50, date(2020, 2, 1), date(2020, 7, 1), DateDelta(months=1)
    )
    df_out = butterfly_trim.trim_data(df_in, info)
    assert_frame_equal(df_out, df_expected)
