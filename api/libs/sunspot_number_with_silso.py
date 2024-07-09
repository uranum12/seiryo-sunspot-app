from pathlib import Path
from typing import TYPE_CHECKING

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import polars as pl
from dateutil.relativedelta import relativedelta
from matplotlib.figure import Figure
from scipy import optimize
from sklearn import metrics

from api.libs.sunspot_number_with_silso_config import (
    SunspotNumberDiff,
    SunspotNumberRatio,
    SunspotNumberRatioDiff1,
    SunspotNumberRatioDiff2,
    SunspotNumberScatter,
    SunspotNumberWithSilso,
)

if TYPE_CHECKING:
    from datetime import date


def load_silso_data(path: Path) -> pl.DataFrame:
    with path.open() as f:
        data = [i.split() for i in f.read().split("\n") if i]
    return (
        pl.LazyFrame(
            {
                "year": [int(i[0]) for i in data],
                "month": [int(i[1]) for i in data],
                "total": [float(i[3]) for i in data],
            }
        )
        .with_columns(
            pl.date(pl.col("year"), pl.col("month"), 1).alias("date")
        )
        .drop("year", "month")
        .collect()
    )


def join_data(df_seiryo: pl.DataFrame, df_silso: pl.DataFrame) -> pl.DataFrame:
    return (
        df_seiryo.lazy()
        .select("date", "total")
        .rename({"total": "seiryo"})
        .join(
            df_silso.lazy().select("date", "total").rename({"total": "silso"}),
            on="date",
            how="left",
            coalesce=True,
        )
        .collect()
    )


def truncate_data(df: pl.DataFrame) -> pl.DataFrame:
    return df.drop_nulls()


def calc_ratio_and_diff(df: pl.DataFrame, factor: float) -> pl.DataFrame:
    return (
        df.lazy()
        .select(
            "date",
            (pl.col("seiryo") / pl.col("silso")).alias("ratio"),
            (pl.col("seiryo") / factor - pl.col("silso")).alias("diff"),
        )
        .sort("date")
        .collect()
    )


def calc_factor(df: pl.DataFrame) -> float:
    popt, _ = optimize.curve_fit(lambda x, a: x * a, df["silso"], df["seiryo"])
    return popt[0]


def calc_r2(df: pl.DataFrame, factor: float) -> float:
    r2 = metrics.r2_score(df["seiryo"], df["silso"] * factor)
    return float(r2)


def draw_sunspot_number_with_silso(
    df: pl.DataFrame, config: SunspotNumberWithSilso
) -> Figure:
    date_min: date = df.select(pl.min("date")).item()
    date_max: date = df.select(pl.max("date")).item()
    date_min = date_min.replace(month=1, day=1)
    date_max = date_max.replace(month=1, day=1) + relativedelta(years=1)
    date_num_min = float(mdates.date2num(date_min))
    date_num_max = float(mdates.date2num(date_max))
    date_margin = (date_num_max - date_num_min) * 0.05
    seiryo_max: float = df.select(pl.max("seiryo")).item()
    silso_max: float = df.select(pl.max("silso")).item()
    sunspot_max = max(seiryo_max, silso_max)
    sunspot_margin = sunspot_max * 0.05

    fig = plt.figure(figsize=(config.fig_size.width, config.fig_size.height))
    ax = fig.add_subplot(111)

    ax.plot(
        df["date"],
        df["seiryo"],
        ls=config.line_seiryo.style,
        lw=config.line_seiryo.width,
        c=config.line_seiryo.color,
        label=config.line_seiryo.label,
        marker=config.line_seiryo.marker.marker,
        ms=config.line_seiryo.marker.size,
    )
    ax.plot(
        df["date"],
        df["silso"],
        ls=config.line_silso.style,
        lw=config.line_silso.width,
        c=config.line_silso.color,
        label=config.line_silso.label,
        marker=config.line_silso.marker.marker,
        ms=config.line_silso.marker.size,
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


def draw_scatter(
    df: pl.DataFrame, factor: float, r2: float, config: SunspotNumberScatter
) -> Figure:
    silso_min: float = df.select(pl.min("silso")).item()
    silso_max: float = df.select(pl.max("silso")).item()
    silso_margin = (silso_max - silso_min) * 0.05
    seiryo_min: float = df.select(pl.min("seiryo")).item()
    seiryo_max: float = df.select(pl.max("seiryo")).item()
    seiryo_margin = (seiryo_max - seiryo_min) * 0.05

    fig = plt.figure(figsize=(config.fig_size.width, config.fig_size.height))
    ax = fig.add_subplot(111)

    ax.plot(
        [0, silso_max + silso_margin],
        np.poly1d([factor, 0])([0, silso_max + silso_margin]),
        ls=config.line_factor.style,
        lw=config.line_factor.width,
        c=config.line_factor.color,
        zorder=1,
    )
    ax.scatter(
        df["silso"],
        df["seiryo"],
        s=config.scatter.marker.size,
        c=config.scatter.color,
        edgecolors=config.scatter.edge_color,
        marker=config.scatter.marker.marker,
        zorder=2,
    )

    ax.text(
        silso_max * 0.8
        if config.text_factor.x is None
        else config.text_factor.x,
        seiryo_max * 0.25
        if config.text_factor.y is None
        else config.text_factor.y,
        f"$y={factor:.5f}x$",
        math_fontfamily=config.text_factor.math_font_family,
        fontfamily=config.text_factor.font_family,
        fontsize=config.text_factor.font_size,
    )
    ax.text(
        silso_max * 0.8 if config.text_r2.x is None else config.text_r2.x,
        seiryo_max * 0.15 if config.text_r2.y is None else config.text_r2.y,
        f"$R^2={r2:.5f}$",
        math_fontfamily=config.text_r2.math_font_family,
        fontfamily=config.text_r2.font_family,
        fontsize=config.text_r2.font_size,
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

    ax.set_xlim(silso_min - silso_margin, silso_max + silso_margin)
    ax.set_ylim(seiryo_min - seiryo_margin, seiryo_max + seiryo_margin)

    ax.grid()

    fig.tight_layout()

    return fig


def draw_ratio(
    df: pl.DataFrame, factor: float, config: SunspotNumberRatio
) -> Figure:
    date_min: date = df.select(pl.min("date")).item()
    date_max: date = df.select(pl.max("date")).item()
    date_min = date_min.replace(month=1, day=1)
    date_max = date_max.replace(month=1, day=1) + relativedelta(years=1)
    date_num_min = float(mdates.date2num(date_min))
    date_num_max = float(mdates.date2num(date_max))
    date_margin = (date_num_max - date_num_min) * 0.05
    ratio_min: float = df.select(pl.min("ratio")).item()
    ratio_max: float = df.select(pl.max("ratio")).item()
    ratio_margin = (ratio_max - ratio_min) * 0.05

    fig = plt.figure(figsize=(config.fig_size.width, config.fig_size.height))
    ax = fig.add_subplot(111)

    ax.axhline(
        y=factor,
        ls=config.line_factor.style,
        lw=config.line_factor.width,
        c=config.line_factor.color,
        zorder=1,
    )
    ax.plot(
        df["date"],
        df["ratio"],
        ls=config.line_ratio.style,
        lw=config.line_ratio.width,
        c=config.line_ratio.color,
        marker=config.line_ratio.marker.marker,
        ms=config.line_ratio.marker.size,
        zorder=2,
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
    ax.set_ylim(ratio_min - ratio_margin, ratio_max + ratio_margin)

    ax.grid()

    fig.tight_layout()

    return fig


def draw_diff(df: pl.DataFrame, config: SunspotNumberDiff) -> Figure:
    date_min: date = df.select(pl.min("date")).item()
    date_max: date = df.select(pl.max("date")).item()
    date_min = date_min.replace(month=1, day=1)
    date_max = date_max.replace(month=1, day=1) + relativedelta(years=1)
    date_num_min = float(mdates.date2num(date_min))
    date_num_max = float(mdates.date2num(date_max))
    date_margin = (date_num_max - date_num_min) * 0.05
    diff_min: float = df.select(pl.min("diff")).item()
    diff_max: float = df.select(pl.max("diff")).item()
    diff_margin = (diff_max - diff_min) * 0.05

    fig = plt.figure(figsize=(config.fig_size.width, config.fig_size.height))
    ax = fig.add_subplot(111)

    ax.plot(
        df["date"],
        df["diff"],
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
    ax.set_ylim(diff_min - diff_margin, diff_max + diff_margin)

    ax.grid()

    fig.tight_layout()

    return fig


def draw_ratio_diff_1(
    df: pl.DataFrame, factor: float, config: SunspotNumberRatioDiff1
) -> Figure:
    date_min: date = df.select(pl.min("date")).item()
    date_max: date = df.select(pl.max("date")).item()
    date_min = date_min.replace(month=1, day=1)
    date_max = date_max.replace(month=1, day=1) + relativedelta(years=1)
    date_num_min = float(mdates.date2num(date_min))
    date_num_max = float(mdates.date2num(date_max))
    date_margin = (date_num_max - date_num_min) * 0.05
    ratio_min: float = df.select(pl.min("ratio")).item()
    ratio_max: float = df.select(pl.max("ratio")).item()
    ratio_margin = (ratio_max - ratio_min) * 0.05
    diff_min: float = df.select(pl.min("diff")).item()
    diff_max: float = df.select(pl.max("diff")).item()
    diff_margin = (diff_max - diff_min) * 0.05

    fig = plt.figure(figsize=(config.fig_size.width, config.fig_size.height))
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212, sharex=ax1)

    ax1.axhline(
        y=factor,
        ls=config.line_factor.style,
        lw=config.line_factor.width,
        c=config.line_factor.color,
        zorder=1,
    )
    ax1.plot(
        df["date"],
        df["ratio"],
        ls=config.line_ratio.style,
        lw=config.line_ratio.width,
        c=config.line_ratio.color,
        marker=config.line_ratio.marker.marker,
        ms=config.line_ratio.marker.size,
        zorder=2,
    )

    ax1.set_title(
        config.title_ratio.text,
        fontfamily=config.title_ratio.font_family,
        fontsize=config.title_ratio.font_size,
    )

    ax1.set_ylabel(
        config.yaxis_ratio.title.text,
        fontfamily=config.yaxis_ratio.title.font_family,
        fontsize=config.yaxis_ratio.title.font_size,
    )

    ax1.set_yticks(ax1.get_yticks())
    ax1.set_yticklabels(
        ax1.get_yticklabels(),
        fontfamily=config.yaxis_ratio.ticks.font_family,
        fontsize=config.yaxis_ratio.ticks.font_size,
    )

    ax1.set_ylim(ratio_min - ratio_margin, ratio_max + ratio_margin)

    ax1.tick_params(bottom=False, labelbottom=False)
    ax1.grid()

    ax2.plot(
        df["date"],
        df["diff"],
        ls=config.line_diff.style,
        lw=config.line_diff.width,
        c=config.line_diff.color,
        marker=config.line_diff.marker.marker,
        ms=config.line_diff.marker.size,
    )

    ax2.set_title(
        config.title_diff.text,
        fontfamily=config.title_diff.font_family,
        fontsize=config.title_diff.font_size,
    )

    ax2.set_xlabel(
        config.xaxis.title.text,
        fontfamily=config.xaxis.title.font_family,
        fontsize=config.xaxis.title.font_size,
    )

    ax2.xaxis.set_major_locator(locator := mdates.AutoDateLocator())
    ax2.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))
    ax2.set_xticks(ax2.get_xticks())
    ax2.set_xticklabels(
        ax2.get_xticklabels(),
        fontfamily=config.xaxis.ticks.font_family,
        fontsize=config.xaxis.ticks.font_size,
    )

    ax2.set_ylabel(
        config.yaxis_diff.title.text,
        fontfamily=config.yaxis_diff.title.font_family,
        fontsize=config.yaxis_diff.title.font_size,
    )

    ax2.set_yticks(ax2.get_yticks())
    ax2.set_yticklabels(
        ax2.get_yticklabels(),
        fontfamily=config.yaxis_diff.ticks.font_family,
        fontsize=config.yaxis_diff.ticks.font_size,
    )

    ax2.set_xlim(date_num_min - date_margin, date_num_max + date_margin)
    ax2.set_ylim(diff_min - diff_margin, diff_max + diff_margin)

    ax2.grid()

    fig.tight_layout()

    return fig


def draw_ratio_diff_2(
    df: pl.DataFrame, config: SunspotNumberRatioDiff2
) -> Figure:
    date_min: date = df.select(pl.min("date")).item()
    date_max: date = df.select(pl.max("date")).item()
    date_min = date_min.replace(month=1, day=1)
    date_max = date_max.replace(month=1, day=1) + relativedelta(years=1)
    date_num_min = float(mdates.date2num(date_min))
    date_num_max = float(mdates.date2num(date_max))
    date_margin = (date_num_max - date_num_min) * 0.05
    ratio_min: float = df.select(pl.min("ratio")).item()
    ratio_max: float = df.select(pl.max("ratio")).item()
    ratio_margin = (ratio_max - ratio_min) * 0.05
    diff_min: float = df.select(pl.min("diff")).item()
    diff_max: float = df.select(pl.max("diff")).item()
    diff_margin = (diff_max - diff_min) * 0.05

    fig = plt.figure(figsize=(config.fig_size.width, config.fig_size.height))
    ax1 = fig.add_subplot(111)

    ax1.plot(
        df["date"],
        df["ratio"],
        ls=config.line_ratio.style,
        lw=config.line_ratio.width,
        c=config.line_ratio.color,
        label=config.line_ratio.label,
        marker=config.line_ratio.marker.marker,
        ms=config.line_ratio.marker.size,
    )

    ax1.set_title(
        config.title.text,
        fontfamily=config.title.font_family,
        fontsize=config.title.font_size,
        y=config.title.position,
    )

    ax1.set_xlabel(
        config.xaxis.title.text,
        fontfamily=config.xaxis.title.font_family,
        fontsize=config.title.font_size,
    )

    ax1.xaxis.set_major_locator(locator := mdates.AutoDateLocator())
    ax1.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))
    ax1.set_xticks(ax1.get_xticks())
    ax1.set_xticklabels(
        ax1.get_xticklabels(),
        fontfamily=config.xaxis.ticks.font_family,
        fontsize=config.xaxis.ticks.font_size,
    )

    ax1.set_ylabel(
        config.yaxis_ratio.title.text,
        fontfamily=config.yaxis_ratio.title.font_family,
        fontsize=config.yaxis_ratio.title.font_size,
    )

    ax1.set_yticks(ax1.get_yticks())
    ax1.set_yticklabels(
        ax1.get_yticklabels(),
        fontfamily=config.yaxis_ratio.ticks.font_family,
        fontsize=config.yaxis_ratio.ticks.font_size,
    )

    ax1.set_xlim(date_num_min - date_margin, date_num_max + date_margin)
    ax1.set_ylim(ratio_min - ratio_margin, ratio_max + ratio_margin)

    ax1.grid()

    ax2 = ax1.twinx()

    ax2.plot(  # type: ignore[attr-defined]
        df["date"],
        df["diff"],
        ls=config.line_diff.style,
        lw=config.line_diff.width,
        c=config.line_diff.color,
        label=config.line_diff.label,
        marker=config.line_diff.marker.marker,
        ms=config.line_diff.marker.size,
    )

    ax2.set_ylabel(
        config.yaxis_diff.title.text,
        fontfamily=config.yaxis_diff.title.font_family,
        fontsize=config.yaxis_diff.title.font_size,
    )

    ax2.set_yticks(ax2.get_yticks())
    ax2.set_yticklabels(
        ax2.get_yticklabels(),
        fontfamily=config.yaxis_diff.ticks.font_family,
        fontsize=config.yaxis_diff.ticks.font_size,
    )

    ax2.set_ylim(diff_min - diff_margin, diff_max + diff_margin)

    ax2.grid()

    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()  # type: ignore[attr-defined]
    ax1.legend(
        h1 + h2,
        l1 + l2,
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
