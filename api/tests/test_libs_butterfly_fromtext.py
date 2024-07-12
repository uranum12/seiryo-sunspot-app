from datetime import date
from pathlib import Path

import polars as pl
import pytest
from polars.testing import assert_frame_equal
from pytest_mock import MockerFixture

from api.libs import butterfly_fromtext


@pytest.mark.parametrize(
    ("in_text", "out_start", "out_end", "out_txt"),
    [
        pytest.param(
            "//Data File for Butterfly Diagram\n"
            ">>1953/03-2016/06\n"
            "\n"
            "<----data---->\n"
            "1953/03/N:3-5 10-10\n"
            "1953/03/S:8-8 18-18\n"
            "1953/04/N:4-4 6-6\n"
            "1953/04/S:7-8\n"
            "1953/05/N:\n"
            "1953/05/S:\n"
            "1953/06/N:\n"
            "1953/06/S:\n"
            "1953/07/N:\n"
            "1953/07/S:10-13\n",
            date(1953, 3, 1),
            date(2016, 6, 1),
            [
                "1953/03/N:3-5 10-10",
                "1953/03/S:8-8 18-18",
                "1953/04/N:4-4 6-6",
                "1953/04/S:7-8",
                "1953/05/N:",
                "1953/05/S:",
                "1953/06/N:",
                "1953/06/S:",
                "1953/07/N:",
                "1953/07/S:10-13",
            ],
        ),
        pytest.param(
            "//Data File for Butterfly Diagram\n"
            ">>1950/09-2023/12\n"
            "\n"
            "<----data---->\n"
            "1950/09/N:21-22 26-28\n"
            "1950/09/S:1-2 4-5 8-10 14-16 20-21 25-26\n"
            "1950/10/N:\n"
            "1950/10/S:\n"
            "1950/11/N:\n"
            "1950/11/S:\n"
            "1950/12/N:\n"
            "1950/12/S:\n",
            date(1950, 9, 1),
            date(2023, 12, 1),
            [
                "1950/09/N:21-22 26-28",
                "1950/09/S:1-2 4-5 8-10 14-16 20-21 25-26",
                "1950/10/N:",
                "1950/10/S:",
                "1950/11/N:",
                "1950/11/S:",
                "1950/12/N:",
                "1950/12/S:",
            ],
        ),
    ],
)
def test_load_txt_data(
    mocker: MockerFixture,
    in_text: str,
    out_start: date,
    out_end: date,
    out_txt: list[str],
) -> None:
    m = mocker.mock_open(read_data=in_text)
    mocker.patch("pathlib.Path.open", m)

    start, end, txt = butterfly_fromtext.load_txt_data(Path("dummy/path"))
    assert start == out_start
    assert end == out_end
    assert txt == out_txt


@pytest.mark.parametrize(
    ("in_text"),
    [
        pytest.param(
            "//Data File for Butterfly Diagram\n"
            "\n"
            ">>1953/03-2016/06\n"
            "\n"
            "<----data---->\n"
            "1953/03/N:3-5 10-10\n"
            "1953/03/S:8-8 18-18\n"
        ),
        pytest.param(
            "//Data File for Butterfly Diagram\n"
            ">> 1950/09-2023/12\n"
            "\n"
            "<----data---->\n"
            "1950/09/N:21-22 26-28\n"
            "1950/09/S:1-2 4-5 8-10 14-16 20-21 25-26\n"
        ),
    ],
)
def test_load_txt_data_with_error(mocker: MockerFixture, in_text: str) -> None:
    m = mocker.mock_open(read_data=in_text)
    mocker.patch("pathlib.Path.open", m)

    with pytest.raises(ValueError, match="invalid date range data"):
        _ = butterfly_fromtext.load_txt_data(Path("dummy/path"))


@pytest.mark.parametrize(
    ("in_txt", "out_date", "out_lat_min", "out_lat_max"),
    [
        pytest.param(
            ["2020/01/N:1-2", "2020/01/S:1-2"],
            [date(2020, 1, 1), date(2020, 1, 1)],
            [-2, 1],
            [-1, 2],
        ),
        pytest.param(
            ["2020/12/N:12-15 0-3", "2020/12/S:"],
            [date(2020, 12, 1), date(2020, 12, 1)],
            [12, 0],
            [15, 3],
        ),
        pytest.param(
            [
                "2020/03/N:2-2",
                "2020/03/S:",
                "2020/04/N:1-1",
                "2020/04/S:",
                "2020/05/N:",
                "2020/05/S:",
            ],
            [date(2020, 3, 1), date(2020, 4, 1)],
            [2, 1],
            [2, 1],
        ),
    ],
)
def test_extract_lat(
    in_txt: list[str],
    out_date: list[date],
    out_lat_min: list[int],
    out_lat_max: list[int],
) -> None:
    df_expected = pl.LazyFrame(
        {"date": out_date, "lat_min": out_lat_min, "lat_max": out_lat_max},
        schema={"date": pl.Date, "lat_min": pl.Int8, "lat_max": pl.Int8},
    )
    df_out = butterfly_fromtext.extract_lat(in_txt)
    assert_frame_equal(df_out, df_expected, check_row_order=False)
