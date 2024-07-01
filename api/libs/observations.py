from datetime import date

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import polars as pl
from dateutil.relativedelta import relativedelta
from matplotlib.figure import Figure

from api.libs.observations_config import ObservationsMonthly


def calc_date_range(df: pl.LazyFrame) -> tuple[date, date]:
    """日付の開始日と最終日を算出する

    Args:
        df (pl.LazyFrame): 黒点数データ

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
    """日付の範囲を月ごとに調整する

    Args:
        start (date): 開始日
        end (date): 最終日

    Returns:
        tuple[date, date]: 開始日と最終日
    """
    start = start.replace(day=1)
    end += relativedelta(months=1, day=1, days=-1)
    return start, end


def calc_dayly_obs(df: pl.LazyFrame, start: date, end: date) -> pl.LazyFrame:
    """日ごとの観測日数を算出する

    Args:
        df (pl.LazyFrame): 黒点数データ
        start (date): 開始日
        end (date): 終了日

    Returns:
        pl.LazyFrame: 日ごとの観測
    """

    return (
        pl.LazyFrame(
            {"date": pl.date_range(start, end, interval="1d", eager=True)}
        )
        .join(
            df.select(pl.col("date").unique()).with_columns(
                pl.lit(1).alias("obs")
            ),
            on="date",
            how="left",
            coalesce=True,
        )
        .with_columns(pl.col("obs").fill_null(0).cast(pl.UInt8))
    )


def calc_monthly_obs(df: pl.LazyFrame) -> pl.LazyFrame:
    """月ごとの観測日数を算出する

    Args:
        df (pl.LazyFrame): 日ごとの観測日数データ

    Returns:
        pl.LazyFrame: 月ごとの観測日数
    """
    return (
        df.with_columns(pl.col("date").dt.truncate("1mo"))
        .group_by("date")
        .agg(pl.col("obs").sum().cast(pl.UInt8))
        .sort("date")
    )


def draw_monthly_obs_days(
    df: pl.DataFrame, config: ObservationsMonthly
) -> Figure:
    """月ごとの観測日数のグラフを作成する

    Args:
        df (pl.DataFrame): 月ごとの観測日数
        config (ObservationsDays): グラフの設定

    Returns:
        Figure: 作成したグラフ
    """
    date_min: date = df.select(pl.min("date")).item()
    date_max: date = df.select(pl.max("date")).item()
    date_min = date_min.replace(month=1, day=1)
    date_max = date_max.replace(month=1, day=1) + relativedelta(years=1)
    date_num_min = float(mdates.date2num(date_min))
    date_num_max = float(mdates.date2num(date_max))
    date_margin = (date_num_max - date_num_min) * 0.05
    obs_max: int = df.select(pl.max("obs")).item()
    obs_margin = obs_max * 0.05

    fig = plt.figure(figsize=(config.fig_size.width, config.fig_size.height))
    ax = fig.add_subplot(111)

    ax.bar(
        df["date"], df["obs"], width=config.bar.width, color=config.bar.color
    )

    ax.set_title(
        config.title.text,
        fontfamily=config.title.font_family,
        fontsize=config.title.font_size,
    )

    ax.set_xlabel(
        config.xaxis.title.text,
        fontfamily=config.xaxis.title.font_family,
        fontsize=config.xaxis.title.font_size,
    )

    ax.xaxis.set_major_locator(locator := mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))
    ax.set_xticks(ax.get_xticks())
    ax.set_xticklabels(
        ax.get_xticklabels(),
        fontfamily=config.xaxis.ticks.font_family,
        fontsize=config.xaxis.ticks.font_size,
    )

    ax.set_ylabel(
        config.yaxis.title.text,
        fontfamily=config.yaxis.title.font_family,
        fontsize=config.yaxis.title.font_size,
    )

    ax.set_yticks(ax.get_yticks())
    ax.set_yticklabels(
        ax.get_yticklabels(),
        fontfamily=config.yaxis.ticks.font_family,
        fontsize=config.yaxis.ticks.font_size,
    )

    ax.set_xlim(date_num_min - date_margin, date_num_max + date_margin)
    ax.set_ylim(0, obs_max + obs_margin)

    fig.tight_layout()

    return fig
