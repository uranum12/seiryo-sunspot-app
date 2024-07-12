import json
from dataclasses import asdict, dataclass, fields
from datetime import date

import polars as pl


@dataclass(frozen=True, slots=True, kw_only=True)
class DateDelta:
    """日付の間隔"""

    years: int = 0
    months: int = 0
    days: int = 0

    def __post_init__(self: "DateDelta") -> None:
        """初期化後の入力値チェック

        Raises:
            ValueError: 入力値が不正値の時に送出
        """
        values = self.to_dict().values()
        if all(value == 0 for value in values):
            msg = "all parameters cannot be zero"
            raise ValueError(msg)
        if any(value < 0 for value in values):
            msg = "parameters cannot be negative"
            raise ValueError(msg)

    def to_dict(self: "DateDelta") -> dict[str, int]:
        """辞書へ変換

        Returns:
            dict[str, int]: 変換後の辞書
        """
        return asdict(self)

    def _format_time(self: "DateDelta", time: int, unit: str) -> str:
        return f"{time}{unit}" if time != 0 else ""

    def to_interval(self: "DateDelta") -> str:
        """Polarsが受け取る期間の文字列へ変換

        Returns:
            str: 変換後の文字列
        """
        years = self._format_time(self.years, "y")
        months = self._format_time(self.months, "mo")
        days = self._format_time(self.days, "d")
        return f"{years}{months}{days}"

    def isoformat(self: "DateDelta") -> str:
        """ISO8601の形式へ変換

        Returns:
            str: 変換後の文字列
        """
        years = self._format_time(self.years, "Y")
        months = self._format_time(self.months, "M")
        days = self._format_time(self.days, "D")
        return f"P{years}{months}{days}"

    @classmethod
    def fromisoformat(cls: type["DateDelta"], data: str) -> "DateDelta":
        data = data.removeprefix("P")
        if "Y" in data:
            y_s, data = data.split("Y")
            y = int(y_s)
        else:
            y = 0
        if "M" in data:
            m_s, data = data.split("M")
            m = int(m_s)
        else:
            m = 0
        if "D" in data:
            d_s, data = data.split("D")
            d = int(d_s)
        else:
            d = 0
        return cls(years=y, months=m, days=d)


@dataclass(frozen=True, slots=True)
class ButterflyInfo:
    """蝶形図の情報"""

    lat_min: int
    lat_max: int
    date_start: date
    date_end: date
    date_interval: DateDelta

    def __post_init__(self: "ButterflyInfo") -> None:
        """初期化後の入力値チェック

        Raises:
            ValueError: 入力値が不正値の時に送出
        """
        if self.lat_min > self.lat_max:
            msg = "latitude minimum value cannot be greater than maximum value"
            raise ValueError(msg)
        if self.date_start > self.date_end:
            msg = "start date cannot be later than end date"
            raise ValueError(msg)

    def to_dict(self: "ButterflyInfo") -> dict[str, int | date | DateDelta]:
        """辞書へ変換

        Returns:
            dict[str, int | date | DateDelta]: 変換後の辞書
        """
        return {
            field.name: getattr(self, field.name) for field in fields(self)
        }

    def to_json(self: "ButterflyInfo") -> str:
        return json.dumps(
            self.to_dict(), default=lambda o: o.isoformat(), indent=2
        )

    @classmethod
    def from_dict(cls: type["ButterflyInfo"], data: dict) -> "ButterflyInfo":
        return cls(
            data["lat_min"],
            data["lat_max"],
            date.fromisoformat(data["date_start"]),
            date.fromisoformat(data["date_end"]),
            DateDelta.fromisoformat(data["date_interval"]),
        )


def calc_date_limit(df: pl.LazyFrame) -> tuple[date, date]:
    """日付の開始日と最終日を算出する

    Args:
        df (pl.LazyFrame): 黒点群データ

    Returns:
        tuple[date, date]: 開始日と最終日
    """
    date_range: dict[str, date] = (
        df.select(pl.min("date").alias("start"), pl.max("date").alias("end"))
        .collect()
        .to_dicts()[0]
    )
    return date_range["start"], date_range["end"]


def adjust_dates(start: date, end: date) -> tuple[date, date]:
    """日付の範囲を月初めに調整する

    Args:
        start (date): 開始日
        end (date): 最終日

    Returns:
        tuple[date, date]: 開始日と最終日
    """
    return start.replace(day=1), end.replace(day=1)


def agg_lat(df: pl.LazyFrame, interval: str) -> pl.LazyFrame:
    """緯度を期間ごとに集計.

    Args:
        df (pl.LazyFrame): 黒点群データ
        interval (str): 区切る期間

    Returns:
        pl.LazyFrame: 緯度データ
    """
    return (
        df.with_columns(pl.col("date").dt.truncate(interval))
        .drop_nulls()
        .group_by("date")
        .agg("lat_min", "lat_max")
        .rename({"lat_max": "max", "lat_min": "min"})
    )


def fill_lat(
    df: pl.LazyFrame, start: date, end: date, interval: str
) -> pl.LazyFrame:
    """範囲内の空白を空データで埋める

    Args:
        df (pl.LazyFrame): 緯度データ
        start (date): 開始日
        end (date): 終了日
        interval (str): 区切る期間

    Returns:
        pl.LazyFrame: 緯度データ
    """
    return (
        pl.LazyFrame({"date": pl.date_range(start, end, interval, eager=True)})
        .join(df, on="date", how="left", coalesce=True)
        .with_columns(pl.col("min", "max").fill_null(pl.lit([])))
        .sort("date")
    )


def calc_lat(df: pl.LazyFrame, info: ButterflyInfo) -> pl.DataFrame:
    """緯度データを算出する

    Args:
        df (pl.LazyFrame): 黒点群データ
        info (ButterflyInfo): 蝶形図の情報

    Returns:
        pl.DataFrame: 緯度データ
    """
    return (
        df.pipe(agg_lat, interval=info.date_interval.to_interval())
        .pipe(
            fill_lat,
            start=info.date_start,
            end=info.date_end,
            interval=info.date_interval.to_interval(),
        )
        .collect()
    )
