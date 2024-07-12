from datetime import date

import numpy as np
import pytest

from api.libs import butterfly, butterfly_draw
from api.libs.butterfly_config import ButterflyDiagram, Index
from api.libs.config_common import Axis, FigSize, Image, Ticks, Title


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
    out = butterfly_draw.create_date_index(in_start, in_end, in_interval)
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
    out = butterfly_draw.create_lat_index(in_lat_min, in_lat_max)
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
    _ = butterfly_draw.draw_butterfly_diagram(img, info, config)
