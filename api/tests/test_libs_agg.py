from datetime import date
from random import sample

import polars as pl
import pytest
from polars.testing import assert_frame_equal

from api.libs import agg


@pytest.mark.parametrize(
    ("in_date", "out_date"),
    [
        (
            [date(2020, 8, 10), date(2020, 8, 20), None],
            [date(2020, 8, 10), date(2020, 8, 20), date(2020, 8, 20)],
        ),
        (
            [date(1965, 3, 20), None, None, date(1970, 1, 1), None],
            [
                date(1965, 3, 20),
                date(1965, 3, 20),
                date(1965, 3, 20),
                date(1970, 1, 1),
                date(1970, 1, 1),
            ],
        ),
    ],
)
def test_fill_date(in_date: list[date | None], out_date: list[date]) -> None:
    df_in = pl.LazyFrame({"date": in_date}, schema={"date": pl.Date})
    df_expected = pl.LazyFrame({"date": out_date}, schema={"date": pl.Date})
    df_out = agg.fill_date(df_in)
    assert_frame_equal(df_out, df_expected, check_column_order=False)


@pytest.mark.parametrize(
    ("in_no", "in_num", "out_no", "out_num"),
    [
        ("1", "5", 1, 5),
        ("2", "1", 2, 1),
        ("3", "25", 3, 25),
        ("0", None, 0, None),
    ],
)
def test_convert_number(
    in_no: str, in_num: str | None, out_no: int, out_num: int | None
) -> None:
    df_in = pl.LazyFrame(
        {"no": [in_no], "num": [in_num]},
        schema={"no": pl.Utf8, "num": pl.Utf8},
    )
    df_expected = pl.LazyFrame(
        {"no": [out_no], "num": [out_num]},
        schema={"no": pl.UInt8, "num": pl.UInt16},
    )
    df_out = agg.convert_number(df_in)
    assert_frame_equal(df_out, df_expected, check_column_order=False)


@pytest.mark.parametrize(
    ("in_date", "out_date"),
    [
        ("2020/8/20", date(2020, 8, 20)),
        ("2020-8-20", date(2020, 8, 20)),
        ("2020.8.20", date(2020, 8, 20)),
        ("2020 8 20", date(2020, 8, 20)),
        ("2020/08/20", date(2020, 8, 20)),
        ("2020-08-20", date(2020, 8, 20)),
        ("2020.08.20", date(2020, 8, 20)),
        ("2020 08 20", date(2020, 8, 20)),
        ("1970-01-01", date(1970, 1, 1)),
        ("1965-12-21", date(1965, 12, 21)),
    ],
)
def test_convert_date(in_date: str, out_date: date) -> None:
    df_in = pl.LazyFrame({"date": [in_date]}, schema={"date": pl.Utf8})
    df_expected = pl.LazyFrame({"date": [out_date]}, schema={"date": pl.Date})
    df_out = agg.convert_date(df_in)
    assert_frame_equal(df_out, df_expected, check_column_order=False)


@pytest.mark.parametrize(
    ("in_data", "in_col", "in_dtype", "out_min", "out_max"),
    [
        ("12", "lat", pl.Int8, 12, 12),
        ("+12", "lat", pl.Int8, 12, 12),
        ("-12", "lat", pl.Int8, -12, -12),
        ("1~2", "lat", pl.Int8, 1, 2),
        ("2~1", "lat", pl.Int8, 1, 2),
        ("-2~-1", "lat", pl.Int8, -2, -1),
        ("-1~-2", "lat", pl.Int8, -2, -1),
        ("1~-2", "lat", pl.Int8, -2, 1),
        ("-2~1", "lat", pl.Int8, -2, 1),
        ("+1~-2", "lat", pl.Int8, -2, 1),
        ("p12", "lat", pl.Int8, 12, 12),
        ("m12", "lat", pl.Int8, -12, -12),
        ("P12", "lat", pl.Int8, 12, 12),
        ("M12", "lat", pl.Int8, -12, -12),
        ("p1~p2", "lat", pl.Int8, 1, 2),
        ("m2~m1", "lat", pl.Int8, -2, -1),
        ("m1~m2", "lat", pl.Int8, -2, -1),
        ("N3", "lat", pl.Int8, 3, 3),
        ("S3", "lat", pl.Int8, -3, -3),
        ("N3~4", "lat", pl.Int8, 3, 4),
        ("N4~3", "lat", pl.Int8, 3, 4),
        ("N3~N4", "lat", pl.Int8, 3, 4),
        ("S3~4", "lat", pl.Int8, -4, -3),
        ("S4~3", "lat", pl.Int8, -4, -3),
        ("S3~S4", "lat", pl.Int8, -4, -3),
        ("N1~S2", "lat", pl.Int8, -2, 1),
        ("n3", "lat", pl.Int8, 3, 3),
        ("s3", "lat", pl.Int8, -3, -3),
        ("n3~4", "lat", pl.Int8, 3, 4),
        ("n4~3", "lat", pl.Int8, 3, 4),
        ("n3~n4", "lat", pl.Int8, 3, 4),
        ("s3~4", "lat", pl.Int8, -4, -3),
        ("s4~3", "lat", pl.Int8, -4, -3),
        ("s3~s4", "lat", pl.Int8, -4, -3),
        ("n1~s2", "lat", pl.Int8, -2, 1),
        ("0.5", "lat", pl.Int8, 1, 1),
        ("1.5", "lat", pl.Int8, 2, 2),
        ("2.5", "lat", pl.Int8, 3, 3),
        ("3.5", "lat", pl.Int8, 4, 4),
        ("4.5", "lat", pl.Int8, 5, 5),
        ("5.5", "lat", pl.Int8, 6, 6),
        ("6.5", "lat", pl.Int8, 7, 7),
        ("7.5", "lat", pl.Int8, 8, 8),
        ("8.5", "lat", pl.Int8, 9, 9),
        ("9.5", "lat", pl.Int8, 10, 10),
        ("-0.5", "lat", pl.Int8, -1, -1),
        ("-1.5", "lat", pl.Int8, -2, -2),
        ("-2.5", "lat", pl.Int8, -3, -3),
        ("-3.5", "lat", pl.Int8, -4, -4),
        ("-4.5", "lat", pl.Int8, -5, -5),
        ("m5.5", "lat", pl.Int8, -6, -6),
        ("m6.5", "lat", pl.Int8, -7, -7),
        ("m7.5", "lat", pl.Int8, -8, -8),
        ("m8.5", "lat", pl.Int8, -9, -9),
        ("m9.5", "lat", pl.Int8, -10, -10),
        ("0.3~0.2", "lat", pl.Int8, 0, 0),
        ("1.5~2.5", "lat", pl.Int8, 2, 3),
        ("N3.7~5.5", "lat", pl.Int8, 4, 6),
        ("15", "lon", pl.Int16, 15, 15),
        ("+15", "lon", pl.Int16, 15, 15),
        ("-15", "lon", pl.Int16, -15, -15),
        ("3~4", "lon", pl.Int16, 3, 4),
        ("4~3", "lon", pl.Int16, 3, 4),
        ("-20~-30", "lon", pl.Int16, -30, -20),
        ("-30~-20", "lon", pl.Int16, -30, -20),
        ("+3~4", "lon", pl.Int16, 3, 4),
        ("+3~+4", "lon", pl.Int16, 3, 4),
        ("3~+4", "lon", pl.Int16, 3, 4),
        ("p15", "lon", pl.Int16, 15, 15),
        ("m15", "lon", pl.Int16, -15, -15),
        ("P15", "lon", pl.Int16, 15, 15),
        ("M15", "lon", pl.Int16, -15, -15),
        ("p3~4", "lon", pl.Int16, 3, 4),
        ("m20~m30", "lon", pl.Int16, -30, -20),
        ("m30~m20", "lon", pl.Int16, -30, -20),
        ("W30", "lon", pl.Int16, -30, -30),
        ("E30", "lon", pl.Int16, 30, 30),
        ("E10~12", "lon", pl.Int16, 10, 12),
        ("E12~10", "lon", pl.Int16, 10, 12),
        ("E10~E12", "lon", pl.Int16, 10, 12),
        ("W10~12", "lon", pl.Int16, -12, -10),
        ("W12~10", "lon", pl.Int16, -12, -10),
        ("W10~W12", "lon", pl.Int16, -12, -10),
        ("E3~4", "lon", pl.Int16, 3, 4),
        ("w30", "lon", pl.Int16, -30, -30),
        ("e30", "lon", pl.Int16, 30, 30),
        ("e10~12", "lon", pl.Int16, 10, 12),
        ("e12~10", "lon", pl.Int16, 10, 12),
        ("e10~e12", "lon", pl.Int16, 10, 12),
        ("w10~12", "lon", pl.Int16, -12, -10),
        ("w12~10", "lon", pl.Int16, -12, -10),
        ("w10~w12", "lon", pl.Int16, -12, -10),
        ("e3~4", "lon", pl.Int16, 3, 4),
        ("1.2", "lon", pl.Int16, 1, 1),
        ("2.2", "lon", pl.Int16, 2, 2),
        ("3.2", "lon", pl.Int16, 3, 3),
        ("4.2", "lon", pl.Int16, 4, 4),
        ("5.2", "lon", pl.Int16, 5, 5),
        ("6.2", "lon", pl.Int16, 6, 6),
        ("7.2", "lon", pl.Int16, 7, 7),
        ("8.2", "lon", pl.Int16, 8, 8),
        ("9.2", "lon", pl.Int16, 9, 9),
        ("10.2", "lon", pl.Int16, 10, 10),
        ("-1.2", "lon", pl.Int16, -1, -1),
        ("-2.2", "lon", pl.Int16, -2, -2),
        ("-3.2", "lon", pl.Int16, -3, -3),
        ("-4.2", "lon", pl.Int16, -4, -4),
        ("-5.2", "lon", pl.Int16, -5, -5),
        ("m6.2", "lon", pl.Int16, -6, -6),
        ("m7.2", "lon", pl.Int16, -7, -7),
        ("m8.2", "lon", pl.Int16, -8, -8),
        ("m9.2", "lon", pl.Int16, -9, -9),
        ("m10.2", "lon", pl.Int16, -10, -10),
        ("-0.3~-0.2", "lon", pl.Int16, 0, 0),
        ("12.5~13.5", "lon", pl.Int16, 13, 14),
        ("W4.1~6.5", "lon", pl.Int16, -7, -4),
    ],
)
def test_convert_coord(
    in_data: str,
    in_col: str,
    in_dtype: pl.PolarsDataType,
    out_min: int,
    out_max: int,
) -> None:
    df_in = pl.LazyFrame({in_col: [in_data]}, schema={in_col: pl.Utf8})
    df_expected = pl.LazyFrame(
        {f"{in_col}_min": [out_min], f"{in_col}_max": [out_max]},
        schema={f"{in_col}_min": in_dtype, f"{in_col}_max": in_dtype},
    )
    df_out = agg.convert_coord(df_in, col=in_col, dtype=in_dtype)
    assert_frame_equal(df_out, df_expected, check_column_order=False)


def test_sort_ar_col_order() -> None:
    cols = ["date", "no", "lat_min", "lat_max", "lon_min", "lon_max", "num"]
    df_in = pl.LazyFrame(
        {col_name: [] for col_name in sample(cols, len(cols))}
    )
    df_expected = pl.LazyFrame({col_name: [] for col_name in cols})
    df_out = agg.sort(df_in)
    assert_frame_equal(df_out, df_expected, check_column_order=True)


@pytest.mark.parametrize(
    ("in_date", "in_no", "out_date", "out_no"),
    [
        (
            [date(2000, 4, 2), date(2001, 6, 3), date(2000, 2, 3)],
            [1, 1, 1],
            [date(2000, 2, 3), date(2000, 4, 2), date(2001, 6, 3)],
            [1, 1, 1],
        ),
        (
            [date(1969, 12, 25), date(1965, 8, 10), date(1970, 1, 1)],
            [1, 1, 1],
            [date(1965, 8, 10), date(1969, 12, 25), date(1970, 1, 1)],
            [1, 1, 1],
        ),
        (
            [date(2023, 4, 4), date(2023, 4, 4), date(2023, 4, 4)],
            [3, 1, 2],
            [date(2023, 4, 4), date(2023, 4, 4), date(2023, 4, 4)],
            [1, 2, 3],
        ),
    ],
)
def test_sort_ar_row_order(
    in_date: list[date],
    in_no: list[int],
    out_date: list[date],
    out_no: list[int],
) -> None:
    cols = ["lat_min", "lat_max", "lon_min", "lon_max", "num"]
    df_in = pl.LazyFrame(
        {"date": in_date, "no": in_no},
        schema={"date": pl.Date, "no": pl.UInt8},
    ).with_columns([pl.lit(None).alias(col) for col in cols])
    df_expected = pl.LazyFrame(
        {"date": out_date, "no": out_no},
        schema={"date": pl.Date, "no": pl.UInt8},
    ).with_columns([pl.lit(None).alias(col) for col in cols])
    df_out = agg.sort(df_in)
    assert_frame_equal(
        df_out, df_expected, check_column_order=False, check_row_order=True
    )
