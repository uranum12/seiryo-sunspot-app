from calendar import Calendar
from datetime import date
from itertools import cycle, islice
from typing import NamedTuple, TypedDict

import polars as pl
from more_itertools import chunked


class ObsDay(NamedTuple):
    date: date
    obs: int


class ObsCalendar(TypedDict):
    year: int
    month: int
    first_weekday: int
    calendar: list[list[ObsDay]]


def create_calendar(
    df: pl.DataFrame, year: int, month: int, first_weekday: int = 0
) -> ObsCalendar:
    c = Calendar(firstweekday=first_weekday)

    calendar: list[list[ObsDay]] = []
    for week in chunked(c.itermonthdates(year, month), 7):
        calendar.append([])
        for day in week:
            df_obs = df.filter(pl.col("date") == day)
            obs = df_obs.item(0, "obs") if df_obs.height == 1 else 0
            calendar[-1].append(ObsDay(day, obs))

    return {
        "year": year,
        "month": month,
        "first_weekday": first_weekday,
        "calendar": calendar,
    }


def print_calendar(calendar: ObsCalendar) -> None:
    print(f"            {calendar['year']}/{calendar['month']}")
    print(
        *islice(
            cycle(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]),
            calendar["first_weekday"],
            calendar["first_weekday"] + 7,
        )
    )
    for week in calendar["calendar"]:
        for day in week:
            if day.date.month == calendar["month"]:
                obs = "*" if day.obs == 1 else " "
                print(f"{obs}{day.date.day: <3}", end="")
            else:
                print("    ", end="")
        print()
