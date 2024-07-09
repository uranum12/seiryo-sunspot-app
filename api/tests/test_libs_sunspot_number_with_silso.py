from datetime import date
from pathlib import Path

import polars as pl
import pytest
from polars.testing import assert_frame_equal
from pytest_mock import MockerFixture

from api.libs import sunspot_number_with_silso
from api.libs.config_common import (
    Axis,
    FigSize,
    Legend,
    Line,
    Marker,
    Scatter,
    Text,
    Ticks,
    Title,
)
from api.libs.sunspot_number_with_silso_config import (
    SunspotNumberDiff,
    SunspotNumberRatio,
    SunspotNumberRatioDiff1,
    SunspotNumberRatioDiff2,
    SunspotNumberScatter,
    SunspotNumberWithSilso,
)


@pytest.mark.parametrize(
    ("in_text", "out_date", "out_total"),
    [
        pytest.param(
            "2020 01 2020.042    6.2   0.7   795\n"
            "2020 02 2020.124    0.2   0.1   967\n"
            "2020 03 2020.206    1.5   0.1  1055\n"
            "2020 04 2020.288    5.2   0.6  1234\n"
            "2020 05 2020.373    0.2   0.1  1363\n"
            "2020 06 2020.455    5.8   0.6  1196\n"
            "2020 07 2020.540    6.1   3.7  1548\n"
            "2020 08 2020.624    7.5   4.1  1587\n"
            "2020 09 2020.706    0.6   2.2  1244\n"
            "2020 10 2020.791   14.6   7.4  1215\n"
            "2020 11 2020.873   34.5   8.1  1238\n"
            "2020 12 2020.958   23.1   6.0   998\n",
            [
                date(2020, 1, 1),
                date(2020, 2, 1),
                date(2020, 3, 1),
                date(2020, 4, 1),
                date(2020, 5, 1),
                date(2020, 6, 1),
                date(2020, 7, 1),
                date(2020, 8, 1),
                date(2020, 9, 1),
                date(2020, 10, 1),
                date(2020, 11, 1),
                date(2020, 12, 1),
            ],
            [6.2, 0.2, 1.5, 5.2, 0.2, 5.8, 6.1, 7.5, 0.6, 14.6, 34.5, 23.1],
        ),
        pytest.param(
            "2023 01 2023.042  144.4  29.4   968  \n"
            "2023 02 2023.122  111.3  20.7  1014  \n"
            "2023 03 2023.204  123.3  17.9  1081  \n"
            "2023 04 2023.286   97.6  18.0  1132  \n"
            "2023 05 2023.371  137.4  19.6  1240  \n"
            "2023 06 2023.453  160.5  20.0  1248  \n"
            "2023 07 2023.538  159.1  17.3  1039 *\n"
            "2023 08 2023.623  114.8  15.4  1095 *\n"
            "2023 09 2023.705  133.6  17.6  1140 *\n"
            "2023 10 2023.790   99.4  16.0   958 *\n"
            "2023 11 2023.873  105.4  16.7   809 *\n"
            "2023 12 2023.958  114.2  17.9   619 *\n",
            [
                date(2023, 1, 1),
                date(2023, 2, 1),
                date(2023, 3, 1),
                date(2023, 4, 1),
                date(2023, 5, 1),
                date(2023, 6, 1),
                date(2023, 7, 1),
                date(2023, 8, 1),
                date(2023, 9, 1),
                date(2023, 10, 1),
                date(2023, 11, 1),
                date(2023, 12, 1),
            ],
            [
                144.4,
                111.3,
                123.3,
                97.6,
                137.4,
                160.5,
                159.1,
                114.8,
                133.6,
                99.4,
                105.4,
                114.2,
            ],
        ),
    ],
)
def test_load_silso_data(
    mocker: MockerFixture,
    in_text: str,
    out_date: list[date],
    out_total: list[float],
) -> None:
    m = mocker.mock_open(read_data=in_text)
    mocker.patch("pathlib.Path.open", m)

    df_expected = pl.DataFrame(
        {"date": out_date, "total": out_total},
        schema={"date": pl.Date, "total": pl.Float64},
    )

    df_out = sunspot_number_with_silso.load_silso_data(Path("dummy/path"))

    assert_frame_equal(df_out, df_expected, check_column_order=False)


@pytest.mark.parametrize(
    (
        "in_seiryo_date",
        "in_seiryo_total",
        "in_silso_date",
        "in_silso_total",
        "out_date",
        "out_seiryo",
        "out_silso",
    ),
    [
        pytest.param(
            [date(2020, 1, 1), date(2020, 2, 1), date(2020, 3, 1)],
            [1, 2, 3],
            [date(2020, 1, 1), date(2020, 2, 1), date(2020, 3, 1)],
            [2, 4, 6],
            [date(2020, 1, 1), date(2020, 2, 1), date(2020, 3, 1)],
            [1, 2, 3],
            [2, 4, 6],
        ),
        pytest.param(
            [date(2020, 1, 1), date(2020, 2, 1), date(2020, 3, 1)],
            [1, 2, 3],
            [
                date(2020, 1, 1),
                date(2020, 2, 1),
                date(2020, 3, 1),
                date(2020, 4, 1),
                date(2020, 5, 1),
            ],
            [2, 4, 6, 8, 10],
            [date(2020, 1, 1), date(2020, 2, 1), date(2020, 3, 1)],
            [1, 2, 3],
            [2, 4, 6],
        ),
    ],
)
def test_join_data(
    in_seiryo_date: list[date],
    in_seiryo_total: list[float],
    in_silso_date: list[date],
    in_silso_total: list[float],
    out_date: list[date],
    out_seiryo: list[float],
    out_silso: list[float | None],
) -> None:
    df_in_seiryo = pl.DataFrame(
        {"date": in_seiryo_date, "total": in_seiryo_total},
        schema={"date": pl.Date, "total": pl.Float64},
    )
    df_in_silso = pl.DataFrame(
        {"date": in_silso_date, "total": in_silso_total},
        schema={"date": pl.Date, "total": pl.Float64},
    )
    df_expected = pl.DataFrame(
        {"date": out_date, "seiryo": out_seiryo, "silso": out_silso},
        schema={"date": pl.Date, "seiryo": pl.Float64, "silso": pl.Float64},
    )
    df_out = sunspot_number_with_silso.join_data(df_in_seiryo, df_in_silso)
    assert_frame_equal(df_out, df_expected)


@pytest.mark.parametrize(
    (
        "in_date",
        "in_seiryo",
        "in_silso",
        "out_date",
        "out_seiryo",
        "out_silso",
    ),
    [
        pytest.param(
            [
                date(2020, 1, 1),
                date(2020, 2, 1),
                date(2020, 3, 1),
                date(2020, 4, 1),
                date(2020, 5, 1),
            ],
            [1.2, 2.3, 3.4, 4.5, 5.6],
            [2.4, 4.6, 6.8, 9.0, 11.2],
            [
                date(2020, 1, 1),
                date(2020, 2, 1),
                date(2020, 3, 1),
                date(2020, 4, 1),
                date(2020, 5, 1),
            ],
            [1.2, 2.3, 3.4, 4.5, 5.6],
            [2.4, 4.6, 6.8, 9.0, 11.2],
        ),
        pytest.param(
            [
                date(2020, 1, 1),
                date(2020, 2, 1),
                date(2020, 3, 1),
                date(2020, 4, 1),
                date(2020, 5, 1),
            ],
            [None, 2.3, 3.4, 4.5, 5.6],
            [2.4, 4.6, 6.8, None, None],
            [date(2020, 2, 1), date(2020, 3, 1)],
            [2.3, 3.4],
            [4.6, 6.8],
        ),
    ],
)
def test_truncate_data(
    in_date: list[date],
    in_seiryo: list[float | None],
    in_silso: list[float | None],
    out_date: list[date],
    out_seiryo: list[float],
    out_silso: list[float],
) -> None:
    df_in = pl.DataFrame(
        {"date": in_date, "seiryo": in_seiryo, "silso": in_silso},
        schema={"date": pl.Date, "seiryo": pl.Float64, "silso": pl.Float64},
    )
    df_expected = pl.DataFrame(
        {"date": out_date, "seiryo": out_seiryo, "silso": out_silso},
        schema={"date": pl.Date, "seiryo": pl.Float64, "silso": pl.Float64},
    )
    df_out = sunspot_number_with_silso.truncate_data(df_in)
    assert_frame_equal(df_out, df_expected)


@pytest.mark.parametrize(
    (
        "in_date",
        "in_seiryo",
        "in_silso",
        "in_factor",
        "out_date",
        "out_ratio",
        "out_diff",
    ),
    [
        pytest.param(
            [date(2020, 1, 1), date(2020, 2, 1), date(2020, 3, 1)],
            [1, 2, 3],
            [2, 4, 6],
            0.5,
            [date(2020, 1, 1), date(2020, 2, 1), date(2020, 3, 1)],
            [0.5, 0.5, 0.5],
            [0.0, 0.0, 0.0],
        ),
        pytest.param(
            [date(2020, 1, 1), date(2020, 2, 1), date(2020, 3, 1)],
            [1, 2, 3],
            [3, 4, 5],
            0.5,
            [date(2020, 1, 1), date(2020, 2, 1), date(2020, 3, 1)],
            [0.33333, 0.5, 0.6],
            [-1.0, 0.0, 1.0],
        ),
    ],
)
def test_calc_ratio_and_diff(
    in_date: list[date],
    in_seiryo: list[float],
    in_silso: list[float],
    in_factor: float,
    out_date: list[date],
    out_ratio: list[float],
    out_diff: list[float],
) -> None:
    df_in = pl.DataFrame(
        {"date": in_date, "seiryo": in_seiryo, "silso": in_silso},
        schema={"date": pl.Date, "seiryo": pl.Float64, "silso": pl.Float64},
    )
    df_expected = pl.DataFrame(
        {"date": out_date, "ratio": out_ratio, "diff": out_diff},
        schema={"date": pl.Date, "ratio": pl.Float64, "diff": pl.Float64},
    )
    df_out = sunspot_number_with_silso.calc_ratio_and_diff(df_in, in_factor)
    assert_frame_equal(df_out, df_expected)


def test_calc_factor() -> None:
    df_in = pl.DataFrame(
        {"seiryo": [1, 2, 3, 4, 5], "silso": [2, 4, 6, 8, 10]},
        schema={"seiryo": pl.Float64, "silso": pl.Float64},
    )
    factor_out = sunspot_number_with_silso.calc_factor(df_in)
    assert factor_out == pytest.approx(0.5)


def test_calc_r2() -> None:
    df_in = pl.DataFrame(
        {"seiryo": [1, 2, 3, 4, 5], "silso": [2, 4, 6, 8, 10]},
        schema={"seiryo": pl.Float64, "silso": pl.Float64},
    )
    factor_in = 0.5
    r2_out = sunspot_number_with_silso.calc_r2(df_in, factor_in)
    assert r2_out == pytest.approx(1.0)


def test_draw_sunspot_number_with_silso() -> None:
    df = pl.DataFrame(
        {
            "date": [date(2020, 2, 1), date(2020, 3, 1), date(2020, 4, 1)],
            "seiryo": [1, 2, 3],
            "silso": [2, 4, 6],
        },
        schema={"date": pl.Date, "seiryo": pl.Float64, "silso": pl.Float64},
    )
    config = SunspotNumberWithSilso(
        fig_size=FigSize(width=8.0, height=5.0),
        line_seiryo=Line(
            label="seiryo",
            style="-",
            width=1.0,
            color="C0",
            marker=Marker(marker="o", size=3.0),
        ),
        line_silso=Line(
            label="SILSO",
            style="-",
            width=1.0,
            color="C1",
            marker=Marker(marker="o", size=3.0),
        ),
        title=Title(
            text="seiryo's whole-disk sunspot number",
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
    _ = sunspot_number_with_silso.draw_sunspot_number_with_silso(df, config)


def test_draw_scatter() -> None:
    df = pl.DataFrame(
        {
            "date": [date(2020, 2, 1), date(2020, 3, 1), date(2020, 4, 1)],
            "seiryo": [1, 2, 3],
            "silso": [2, 4, 6],
        },
        schema={"date": pl.Date, "seiryo": pl.Float64, "silso": pl.Float64},
    )
    factor = 0.5
    r2 = 1.0
    config = SunspotNumberScatter(
        fig_size=FigSize(width=8.0, height=5.0),
        line_factor=Line(
            label="",
            style="-",
            width=1.0,
            color="black",
            marker=Marker(marker="o", size=3.0),
        ),
        scatter=Scatter(
            label="",
            color="C0",
            edge_color="C0",
            marker=Marker(marker="o", size=3.0),
        ),
        text_factor=Text(
            x=None,
            y=None,
            math_font_family="cm",
            font_family="Times New Roman",
            font_size=16,
        ),
        text_r2=Text(
            x=None,
            y=None,
            math_font_family="cm",
            font_family="Times New Roman",
            font_size=16,
        ),
        title=Title(
            text="SILSO and seiryo",
            font_family="Times New Roman",
            font_size=16,
            position=1.0,
        ),
        xaxis=Axis(
            title=Title(
                text="SILSO",
                font_family="Times New Roman",
                font_size=16,
                position=1.0,
            ),
            ticks=Ticks(font_family="Times New Roman", font_size=12),
        ),
        yaxis=Axis(
            title=Title(
                text="seiryo",
                font_family="Times New Roman",
                font_size=16,
                position=1.0,
            ),
            ticks=Ticks(font_family="Times New Roman", font_size=12),
        ),
    )
    _ = sunspot_number_with_silso.draw_scatter(df, factor, r2, config)


def test_draw_ratio() -> None:
    df = pl.DataFrame(
        {
            "date": [date(2020, 2, 1), date(2020, 3, 1), date(2020, 4, 1)],
            "ratio": [0.4, 0.5, 0.45],
        },
        schema={"date": pl.Date, "ratio": pl.Float64},
    )
    factor = 0.48
    config = SunspotNumberRatio(
        fig_size=FigSize(width=8.0, height=5.0),
        line_factor=Line(
            label="",
            style="--",
            width=1.0,
            color="black",
            marker=Marker(marker="o", size=3.0),
        ),
        line_ratio=Line(
            label="",
            style="-",
            width=1.0,
            color="C0",
            marker=Marker(marker="o", size=3.0),
        ),
        title=Title(
            text="ratio: seiryo / SILSO",
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
                text="ratio",
                font_family="Times New Roman",
                font_size=16,
                position=1.0,
            ),
            ticks=Ticks(font_family="Times New Roman", font_size=12),
        ),
    )
    _ = sunspot_number_with_silso.draw_ratio(df, factor, config)


def test_draw_diff() -> None:
    df = pl.DataFrame(
        {
            "date": [date(2020, 2, 1), date(2020, 3, 1), date(2020, 4, 1)],
            "diff": [1, -2, 3],
        },
        schema={"date": pl.Date, "diff": pl.Float64},
    )
    config = SunspotNumberDiff(
        fig_size=FigSize(width=8.0, height=5.0),
        line=Line(
            label="",
            style="-",
            width=1.0,
            color="C0",
            marker=Marker(marker="o", size=3.0),
        ),
        title=Title(
            text="difference: seiryo* - SILSO",
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
                text="difference",
                font_family="Times New Roman",
                font_size=16,
                position=1.0,
            ),
            ticks=Ticks(font_family="Times New Roman", font_size=12),
        ),
    )
    _ = sunspot_number_with_silso.draw_diff(df, config)


def test_draw_ratio_and_diff_1() -> None:
    df = pl.DataFrame(
        {
            "date": [date(2020, 2, 1), date(2020, 3, 1), date(2020, 4, 1)],
            "ratio": [0.4, 0.5, 0.45],
            "diff": [1, -2, 3],
        },
        schema={"date": pl.Date, "ratio": pl.Float64, "diff": pl.Float64},
    )
    factor = 0.48
    config = SunspotNumberRatioDiff1(
        fig_size=FigSize(width=8.0, height=8.0),
        line_factor=Line(
            label="",
            style="--",
            width=1.0,
            color="black",
            marker=Marker(marker="o", size=3.0),
        ),
        line_ratio=Line(
            label="",
            style="-",
            width=1.0,
            color="C0",
            marker=Marker(marker="o", size=3.0),
        ),
        line_diff=Line(
            label="",
            style="-",
            width=1.0,
            color="C0",
            marker=Marker(marker="o", size=3.0),
        ),
        title_ratio=Title(
            text="ratio: seiryo / SILSO",
            font_family="Times New Roman",
            font_size=16,
            position=1.0,
        ),
        title_diff=Title(
            text="difference: seiryo* - SILSO",
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
        yaxis_ratio=Axis(
            title=Title(
                text="ratio",
                font_family="Times New Roman",
                font_size=16,
                position=1.0,
            ),
            ticks=Ticks(font_family="Times New Roman", font_size=12),
        ),
        yaxis_diff=Axis(
            title=Title(
                text="difference",
                font_family="Times New Roman",
                font_size=16,
                position=1.0,
            ),
            ticks=Ticks(font_family="Times New Roman", font_size=12),
        ),
    )
    _ = sunspot_number_with_silso.draw_ratio_diff_1(df, factor, config)


def test_draw_ratio_and_diff_2() -> None:
    df = pl.DataFrame(
        {
            "date": [date(2020, 2, 1), date(2020, 3, 1), date(2020, 4, 1)],
            "ratio": [0.4, 0.5, 0.45],
            "diff": [1, -2, 3],
        },
        schema={"date": pl.Date, "ratio": pl.Float64, "diff": pl.Float64},
    )
    config = SunspotNumberRatioDiff2(
        fig_size=FigSize(width=8.0, height=5.0),
        line_ratio=Line(
            label="ratio",
            style="-",
            width=1.0,
            color="C0",
            marker=Marker(marker="o", size=3.0),
        ),
        line_diff=Line(
            label="diff",
            style="-",
            width=1.0,
            color="C1",
            marker=Marker(marker="o", size=3.0),
        ),
        title=Title(
            text="ratio: seiryo / SILSO and difference: seiryo* - SILSO",
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
        yaxis_ratio=Axis(
            title=Title(
                text="ratio",
                font_family="Times New Roman",
                font_size=16,
                position=1.0,
            ),
            ticks=Ticks(font_family="Times New Roman", font_size=12),
        ),
        yaxis_diff=Axis(
            title=Title(
                text="difference",
                font_family="Times New Roman",
                font_size=16,
                position=1.0,
            ),
            ticks=Ticks(font_family="Times New Roman", font_size=12),
        ),
        legend=Legend(font_family="Times New Roman", font_size=12),
    )
    _ = sunspot_number_with_silso.draw_ratio_diff_2(df, config)
