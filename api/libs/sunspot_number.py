from typing import TYPE_CHECKING

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import polars as pl
from dateutil.relativedelta import relativedelta
from matplotlib.figure import Figure

from api.libs.sunspot_number_config import (
    SunspotNumberHemispheric,
    SunspotNumberWholeDisk,
)

if TYPE_CHECKING:
    from datetime import date


def split(df: pl.LazyFrame) -> tuple[pl.LazyFrame, pl.LazyFrame]:
    df_spot = df.filter(~pl.col("no").eq(0))
    df_nospot = df.filter(pl.col("no").eq(0))

    return df_spot, df_nospot


def calc_lat(df: pl.LazyFrame) -> pl.LazyFrame:
    return (
        df.with_columns(  # 緯度の中央値を算出
            ((pl.col("lat_min") + pl.col("lat_max")) / 2).alias("lat")
        )
        .with_columns(  # 緯度の中央値をもとに北半球と南半球を分類
            pl.when(pl.col("lat") >= 0)
            .then(pl.lit("N"))
            .otherwise(pl.lit("S"))
            .alias("lat")
        )
        .drop("lat_min", "lat_max")
    )


def calc_sn(df: pl.LazyFrame) -> pl.LazyFrame:
    return (
        df.group_by("date")  # 日付ごとに集計
        .agg(
            # 北半球と南半球を分類
            pl.col("num").filter(pl.col("lat").eq("N")).alias("n"),
            pl.col("num").filter(pl.col("lat").eq("S")).alias("s"),
            # 黒点数、黒点群数の合計値を算出
            pl.col("num").count().cast(pl.UInt8).alias("tg"),
            pl.col("num").sum().cast(pl.UInt16).alias("tf"),
        )
        .with_columns(
            # 北半球、南半球それぞれの黒点数、黒点群数を算出
            pl.col("n").list.len().cast(pl.UInt8).alias("ng"),
            pl.col("n").list.sum().cast(pl.UInt16).alias("nf"),
            pl.col("s").list.len().cast(pl.UInt8).alias("sg"),
            pl.col("s").list.sum().cast(pl.UInt16).alias("sf"),
        )
        .drop("n", "s")
    )


def fill_sn(df: pl.LazyFrame) -> pl.LazyFrame:
    return df.with_columns(
        *[pl.lit(0).cast(pl.UInt8).alias(col) for col in ["ng", "sg", "tg"]],
        *[pl.lit(0).cast(pl.UInt16).alias(col) for col in ["nf", "sf", "tf"]],
    )


def sort(df: pl.LazyFrame) -> pl.LazyFrame:
    return df.select(["date", "ng", "nf", "sg", "sf", "tg", "tf"]).sort("date")


def agg_daily(df: pl.DataFrame) -> pl.DataFrame:
    return (
        df.lazy()
        .select(
            pl.col("date"),
            (pl.col("ng").cast(pl.UInt16) * 10 + pl.col("nf"))
            .cast(pl.Int16)
            .alias("north"),
            (pl.col("sg").cast(pl.UInt16) * 10 + pl.col("sf"))
            .cast(pl.Int16)
            .alias("south"),
            (pl.col("tg").cast(pl.UInt16) * 10 + pl.col("tf"))
            .cast(pl.Int16)
            .alias("total"),
        )
        .sort("date")
        .collect()
    )


def agg_monthly(df: pl.DataFrame) -> pl.DataFrame:
    return (
        df.lazy()
        .select(
            pl.col("date").dt.truncate("1mo"),
            (pl.col("ng").cast(pl.UInt16) * 10 + pl.col("nf")).alias("north"),
            (pl.col("sg").cast(pl.UInt16) * 10 + pl.col("sf")).alias("south"),
            (pl.col("tg").cast(pl.UInt16) * 10 + pl.col("tf")).alias("total"),
        )
        .group_by("date")
        .mean()
        .sort("date")
        .collect()
    )


def draw_sunspot_number_whole_disk(
    df: pl.DataFrame, config: SunspotNumberWholeDisk
) -> Figure:
    date_min: date = df.select(pl.min("date")).item()
    date_max: date = df.select(pl.max("date")).item()
    date_min = date_min.replace(month=1, day=1)
    date_max = date_max.replace(month=1, day=1) + relativedelta(years=1)
    date_num_min = float(mdates.date2num(date_min))
    date_num_max = float(mdates.date2num(date_max))
    date_margin = (date_num_max - date_num_min) * 0.05
    total_max: float = df.select(pl.max("total")).item()
    total_margin = total_max * 0.05

    fig = plt.figure(figsize=(config.fig_size.width, config.fig_size.height))
    ax = fig.add_subplot(111)

    ax.plot(
        df["date"],
        df["total"],
        ls=config.line.style,
        lw=config.line.width,
        c=config.line.color,
        marker=config.line.marker.marker,
        ms=config.line.marker.size,
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
    ax.set_ylim(-total_margin, total_max + total_margin)

    ax.grid()

    fig.tight_layout()

    return fig


def draw_sunspot_number_hemispheric(
    df: pl.DataFrame, config: SunspotNumberHemispheric
) -> Figure:
    date_min: date = df.select(pl.min("date")).item()
    date_max: date = df.select(pl.max("date")).item()
    date_min = date_min.replace(month=1, day=1)
    date_max = date_max.replace(month=1, day=1) + relativedelta(years=1)
    date_num_min = float(mdates.date2num(date_min))
    date_num_max = float(mdates.date2num(date_max))
    date_margin = (date_num_max - date_num_min) * 0.05
    north_max: float = df.select(pl.max("north")).item()
    south_max: float = df.select(pl.max("south")).item()
    sunspot_max = max(north_max, south_max)
    sunspot_margin = sunspot_max * 0.05

    fig = plt.figure(figsize=(config.fig_size.width, config.fig_size.height))
    ax = fig.add_subplot(111)

    ax.plot(
        df["date"],
        df["north"],
        ls=config.line_north.style,
        lw=config.line_north.width,
        c=config.line_north.color,
        label=config.line_north.label,
        marker=config.line_north.marker.marker,
        ms=config.line_north.marker.size,
    )
    ax.plot(
        df["date"],
        df["south"],
        ls=config.line_south.style,
        lw=config.line_south.width,
        c=config.line_south.color,
        label=config.line_south.label,
        marker=config.line_south.marker.marker,
        ms=config.line_south.marker.size,
    )

    ax.set_title(
        config.title.text,
        fontfamily=config.title.font_family,
        fontsize=config.title.font_size,
        y=config.title.position,
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
    ax.set_ylim(-sunspot_margin, sunspot_max + sunspot_margin)

    ax.grid()
    ax.legend(
        fancybox=False,
        edgecolor="black",
        framealpha=1,
        loc="lower center",
        bbox_to_anchor=(0.5, 1.02),
        borderaxespad=0,
        ncol=2,
        prop={
            "family": config.legend.font_family,
            "size": config.legend.font_size,
        },
    )

    fig.tight_layout()

    return fig
