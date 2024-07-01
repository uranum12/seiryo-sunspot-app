from datetime import date

import polars as pl

from api.libs import obs_calendar


def test_create_calendar() -> None:
    year = 2020
    month = 8
    first = 6
    df_in = pl.DataFrame(
        {
            "date": [
                date(2020, 8, 10),
                date(2020, 8, 14),
                date(2020, 8, 15),
                date(2020, 8, 20),
                date(2020, 8, 21),
                date(2020, 8, 21),
                date(2020, 9, 2),
            ],
            "obs": [
                1,  # 8/10
                2,  # 8/14
                0,  # 8/15
                0,  # 8/20
                1,  # 8/21
                0,  # 8/21
                1,  # 9/2
            ],
        },
        schema={"date": pl.Date, "obs": pl.UInt8},
    )
    calendar_expected = obs_calendar.ObsCalendar(
        {
            "year": year,
            "month": month,
            "first_weekday": first,
            "calendar": [
                [
                    obs_calendar.ObsDay(date(2020, 7, 26), 0),
                    obs_calendar.ObsDay(date(2020, 7, 27), 0),
                    obs_calendar.ObsDay(date(2020, 7, 28), 0),
                    obs_calendar.ObsDay(date(2020, 7, 29), 0),
                    obs_calendar.ObsDay(date(2020, 7, 30), 0),
                    obs_calendar.ObsDay(date(2020, 7, 31), 0),
                    obs_calendar.ObsDay(date(2020, 8, 1), 0),
                ],
                [
                    obs_calendar.ObsDay(date(2020, 8, 2), 0),
                    obs_calendar.ObsDay(date(2020, 8, 3), 0),
                    obs_calendar.ObsDay(date(2020, 8, 4), 0),
                    obs_calendar.ObsDay(date(2020, 8, 5), 0),
                    obs_calendar.ObsDay(date(2020, 8, 6), 0),
                    obs_calendar.ObsDay(date(2020, 8, 7), 0),
                    obs_calendar.ObsDay(date(2020, 8, 8), 0),
                ],
                [
                    obs_calendar.ObsDay(date(2020, 8, 9), 0),
                    obs_calendar.ObsDay(date(2020, 8, 10), 1),  # 8/10
                    obs_calendar.ObsDay(date(2020, 8, 11), 0),
                    obs_calendar.ObsDay(date(2020, 8, 12), 0),
                    obs_calendar.ObsDay(date(2020, 8, 13), 0),
                    obs_calendar.ObsDay(date(2020, 8, 14), 2),  # 8/14
                    obs_calendar.ObsDay(date(2020, 8, 15), 0),  # 8/15
                ],
                [
                    obs_calendar.ObsDay(date(2020, 8, 16), 0),
                    obs_calendar.ObsDay(date(2020, 8, 17), 0),
                    obs_calendar.ObsDay(date(2020, 8, 18), 0),
                    obs_calendar.ObsDay(date(2020, 8, 19), 0),
                    obs_calendar.ObsDay(date(2020, 8, 20), 0),  # 8/20
                    obs_calendar.ObsDay(date(2020, 8, 21), 0),  # 8/21
                    obs_calendar.ObsDay(date(2020, 8, 22), 0),
                ],
                [
                    obs_calendar.ObsDay(date(2020, 8, 23), 0),
                    obs_calendar.ObsDay(date(2020, 8, 24), 0),
                    obs_calendar.ObsDay(date(2020, 8, 25), 0),
                    obs_calendar.ObsDay(date(2020, 8, 26), 0),
                    obs_calendar.ObsDay(date(2020, 8, 27), 0),
                    obs_calendar.ObsDay(date(2020, 8, 28), 0),
                    obs_calendar.ObsDay(date(2020, 8, 29), 0),
                ],
                [
                    obs_calendar.ObsDay(date(2020, 8, 30), 0),
                    obs_calendar.ObsDay(date(2020, 8, 31), 0),
                    obs_calendar.ObsDay(date(2020, 9, 1), 0),
                    obs_calendar.ObsDay(date(2020, 9, 2), 1),  # 9/2
                    obs_calendar.ObsDay(date(2020, 9, 3), 0),
                    obs_calendar.ObsDay(date(2020, 9, 4), 0),
                    obs_calendar.ObsDay(date(2020, 9, 5), 0),
                ],
            ],
        }
    )
    calendar = obs_calendar.create_calendar(df_in, year, month, first)
    assert calendar == calendar_expected


def test_print_calendar() -> None:
    df = pl.DataFrame(
        {"date": [], "obs": []}, schema={"date": pl.Date, "obs": pl.UInt8}
    )
    calendar = obs_calendar.create_calendar(df, 2020, 2, 2)
    obs_calendar.print_calendar(calendar)
