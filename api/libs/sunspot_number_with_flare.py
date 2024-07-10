from datetime import date
from pathlib import Path
from re import compile

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import polars as pl
from dateutil.relativedelta import relativedelta
from matplotlib.figure import Figure
from scipy import optimize

from api.libs.sunspot_number_with_flare_config import (
    SunspotNumberWithFlare,
    SunspotNumberWithFlareHemispheric,
)


def load_flare_file(path: Path) -> pl.DataFrame:
    with path.open("r") as f:
        lines = [line.strip() for line in f if line.strip()]
    pat_year = compile(r"(\d{4})")
    for line in lines:
        if match := pat_year.match(line):
            year = int(match.group())
            break
    else:
        msg = "cannot find year"
        raise ValueError(msg)
    mean_line = [
        line.replace("Mean", "").split()
        for line in lines
        if line.startswith("Mean")
    ]
    dates: list[date] = []
    indexes: list[float] = []
    for i, d in enumerate(mean_line[0]):
        dates.append(date(year, i + 1, 1))
        indexes.append(float(d))
    return pl.DataFrame({"date": dates, "index": indexes})


def load_flare_files(
    files_north: list[Path], files_south: list[Path], files_total: list[Path]
) -> pl.DataFrame:
    df_north = pl.concat(
        load_flare_file(file).lazy() for file in files_north
    ).rename({"index": "north"})
    df_south = pl.concat(
        load_flare_file(file).lazy() for file in files_south
    ).rename({"index": "south"})
    df_total = pl.concat(
        load_flare_file(file).lazy() for file in files_total
    ).rename({"index": "total"})
    return (
        df_north.join(df_south, on="date", how="full", coalesce=True)
        .join(df_total, on="date", how="full", coalesce=True)
        .sort("date")
        .collect()
    )


def load_flare_data(path: Path) -> pl.DataFrame:
    files_north = list(path.glob("*north*.txt"))
    files_south = list(path.glob("*south*.txt"))
    files_total = list(path.glob("*total*.txt"))
    return load_flare_files(files_north, files_south, files_total)


def join_data(df_seiryo: pl.DataFrame, df_flare: pl.DataFrame) -> pl.DataFrame:
    return (
        df_seiryo.lazy()
        .rename(
            {
                "north": "seiryo_north",
                "south": "seiryo_south",
                "total": "seiryo_total",
            }
        )
        .join(
            df_flare.lazy().rename(
                {
                    "north": "flare_north",
                    "south": "flare_south",
                    "total": "flare_total",
                }
            ),
            on="date",
            how="left",
            coalesce=True,
        )
        .collect()
    )


def calc_factors(df: pl.DataFrame) -> dict[str, float]:
    factors: dict[str, float] = {}
    for hemisphere in ["north", "south", "total"]:
        df_truncated = (
            df.lazy()
            .select(f"seiryo_{hemisphere}", f"flare_{hemisphere}")
            .drop_nulls()
            .collect()
        )
        popt, _ = optimize.curve_fit(
            lambda x, a: x * a,
            df_truncated[f"seiryo_{hemisphere}"],
            df_truncated[f"flare_{hemisphere}"],
        )
        factors[hemisphere] = popt[0]
    return factors


def draw_sunspot_number_with_flare(
    df: pl.DataFrame,
    config: SunspotNumberWithFlare,
    *,
    factor: float | None = None,
) -> Figure:
    date_min: date = df.select(pl.min("date")).item()
    date_max: date = df.select(pl.max("date")).item()
    date_min = date_min.replace(month=1, day=1)
    date_max = date_max.replace(month=1, day=1) + relativedelta(years=1)
    date_num_min = float(mdates.date2num(date_min))
    date_num_max = float(mdates.date2num(date_max))
    date_margin = (date_num_max - date_num_min) * 0.05
    sunspot_max: float = df.select(pl.max("seiryo_total")).item()
    sunspot_margin = sunspot_max * 0.05
    flare_max: float = (
        sunspot_max * factor
        if factor is not None
        else df.select(pl.max("flare_total")).item()
    )
    flare_margin = flare_max * 0.05

    fig = plt.figure(figsize=(config.fig_size.width, config.fig_size.height))
    ax1 = fig.add_subplot(111)

    ax1.plot(
        df["date"],
        df["seiryo_total"],
        ls=config.line_sunspot.style,
        lw=config.line_sunspot.width,
        c=config.line_sunspot.color,
        label=config.line_sunspot.label,
        marker=config.line_sunspot.marker.marker,
        ms=config.line_sunspot.marker.size,
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
        config.yaxis_sunspot.title.text,
        fontfamily=config.yaxis_sunspot.title.font_family,
        fontsize=config.yaxis_sunspot.title.font_size,
    )

    ax1.set_yticks(ax1.get_yticks())
    ax1.set_yticklabels(
        ax1.get_yticklabels(),
        fontfamily=config.yaxis_sunspot.ticks.font_family,
        fontsize=config.yaxis_sunspot.ticks.font_size,
    )

    ax1.grid()

    ax1.set_xlim(date_num_min - date_margin, date_num_max + date_margin)
    ax1.set_ylim(-sunspot_margin, sunspot_max + sunspot_margin)

    ax2 = ax1.twinx()

    ax2.plot(  # type: ignore[attr-defined]
        df["date"],
        df["flare_total"],
        ls=config.line_flare.style,
        lw=config.line_flare.width,
        c=config.line_flare.color,
        label=config.line_flare.label,
        marker=config.line_flare.marker.marker,
        ms=config.line_flare.marker.size,
    )

    ax2.set_ylabel(
        config.yaxis_flare.title.text,
        fontfamily=config.yaxis_flare.title.font_family,
        fontsize=config.yaxis_flare.title.font_size,
    )

    ax2.set_yticks(ax2.get_yticks())
    ax2.set_yticklabels(
        ax2.get_yticklabels(),
        fontfamily=config.yaxis_flare.ticks.font_family,
        fontsize=config.yaxis_flare.ticks.font_size,
    )

    ax2.set_ylim(-flare_margin, flare_max + flare_margin)

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


def draw_sunspot_number_with_flare_hemispheric(  # noqa: PLR0915
    df: pl.DataFrame,
    config: SunspotNumberWithFlareHemispheric,
    *,
    factor_north: float | None = None,
    factor_south: float | None = None,
) -> Figure:
    date_min: date = df.select(pl.min("date")).item()
    date_max: date = df.select(pl.max("date")).item()
    date_min = date_min.replace(month=1, day=1)
    date_max = date_max.replace(month=1, day=1) + relativedelta(years=1)
    date_num_min = float(mdates.date2num(date_min))
    date_num_max = float(mdates.date2num(date_max))
    date_margin = (date_num_max - date_num_min) * 0.05
    sunspot_north_max: float = df.select(pl.max("seiryo_north")).item()
    sunspot_north_margin = sunspot_north_max * 0.05
    flare_north_max: float = (
        sunspot_north_max * factor_north
        if factor_north is not None
        else df.select(pl.max("flare_north")).item()
    )
    flare_north_margin = flare_north_max * 0.05
    sunspot_south_max: float = df.select(pl.max("seiryo_south")).item()
    sunspot_south_margin = sunspot_south_max * 0.05
    flare_south_max: float = (
        sunspot_south_max * factor_south
        if factor_south is not None
        else df.select(pl.max("flare_south")).item()
    )
    flare_south_margin = flare_south_max * 0.05

    fig = plt.figure(figsize=(config.fig_size.width, config.fig_size.height))
    ax1 = fig.add_subplot(211)
    ax1_twin = ax1.twinx()

    ax1.plot(
        df["date"],
        df["seiryo_north"],
        ls=config.line_north_sunspot.style,
        lw=config.line_north_sunspot.width,
        c=config.line_north_sunspot.color,
        label=config.line_north_sunspot.label,
        marker=config.line_north_sunspot.marker.marker,
        ms=config.line_north_sunspot.marker.size,
    )

    ax1_twin.plot(  # type: ignore[attr-defined]
        df["date"],
        df["flare_north"],
        ls=config.line_north_flare.style,
        lw=config.line_north_flare.width,
        c=config.line_north_flare.color,
        label=config.line_north_flare.label,
        marker=config.line_north_flare.marker.marker,
        ms=config.line_north_flare.marker.size,
    )

    ax1.set_title(
        config.title_north.text,
        fontfamily=config.title_north.font_family,
        fontsize=config.title_north.font_size,
        y=config.title_north.position,
    )

    ax1.set_ylabel(
        config.yaxis_north_sunspot.title.text,
        fontfamily=config.yaxis_north_sunspot.title.font_family,
        fontsize=config.yaxis_north_sunspot.title.font_size,
    )

    ax1.set_yticks(ax1.get_yticks())
    ax1.set_yticklabels(
        ax1.get_yticklabels(),
        fontfamily=config.yaxis_north_sunspot.ticks.font_family,
        fontsize=config.yaxis_north_sunspot.ticks.font_size,
    )

    ax1_twin.set_ylabel(
        config.yaxis_north_flare.title.text,
        fontfamily=config.yaxis_north_flare.title.font_family,
        fontsize=config.yaxis_north_flare.title.font_size,
    )

    ax1_twin.set_yticks(ax1_twin.get_yticks())
    ax1_twin.set_yticklabels(
        ax1_twin.get_yticklabels(),
        fontfamily=config.yaxis_north_flare.ticks.font_family,
        fontsize=config.yaxis_north_flare.ticks.font_size,
    )

    ax1.set_ylim(
        -sunspot_north_margin, sunspot_north_max + sunspot_north_margin
    )
    ax1_twin.set_ylim(
        -flare_north_margin, flare_north_max + flare_north_margin
    )

    ax1.tick_params(bottom=False, labelbottom=False)
    ax1.grid()
    ax1_twin.grid()

    h1, l1 = ax1.get_legend_handles_labels()
    h1_twin, l1_twin = ax1_twin.get_legend_handles_labels()  # type: ignore[attr-defined]
    ax1.legend(
        h1 + h1_twin,
        l1 + l1_twin,
        fancybox=False,
        edgecolor="black",
        framealpha=1,
        loc="lower center",
        bbox_to_anchor=(0.5, 1.02),
        borderaxespad=0,
        ncol=2,
        prop={
            "family": config.legend_north.font_family,
            "size": config.legend_north.font_size,
        },
    )

    ax2 = fig.add_subplot(212, sharex=ax1)
    ax2_twin = ax2.twinx()

    ax2.plot(
        df["date"],
        df["seiryo_south"],
        ls=config.line_south_sunspot.style,
        lw=config.line_south_sunspot.width,
        c=config.line_south_sunspot.color,
        label=config.line_south_sunspot.label,
        marker=config.line_south_sunspot.marker.marker,
        ms=config.line_south_sunspot.marker.size,
    )

    ax2_twin.plot(  # type: ignore[attr-defined]
        df["date"],
        df["flare_south"],
        ls=config.line_south_flare.style,
        lw=config.line_south_flare.width,
        c=config.line_south_flare.color,
        label=config.line_south_flare.label,
        marker=config.line_south_flare.marker.marker,
        ms=config.line_south_flare.marker.size,
    )

    ax2.set_title(
        config.title_south.text,
        fontfamily=config.title_south.font_family,
        fontsize=config.title_south.font_size,
        y=config.title_south.position,
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
        config.yaxis_north_sunspot.title.text,
        fontfamily=config.yaxis_north_sunspot.title.font_family,
        fontsize=config.yaxis_north_sunspot.title.font_size,
    )

    ax2.set_yticks(ax2.get_yticks())
    ax2.set_yticklabels(
        ax2.get_yticklabels(),
        fontfamily=config.yaxis_north_sunspot.ticks.font_family,
        fontsize=config.yaxis_north_sunspot.ticks.font_size,
    )

    ax2_twin.set_ylabel(
        config.yaxis_north_flare.title.text,
        fontfamily=config.yaxis_north_flare.title.font_family,
        fontsize=config.yaxis_north_flare.title.font_size,
    )

    ax2_twin.set_yticks(ax2_twin.get_yticks())
    ax2_twin.set_yticklabels(
        ax2_twin.get_yticklabels(),
        fontfamily=config.yaxis_north_flare.ticks.font_family,
        fontsize=config.yaxis_north_flare.ticks.font_size,
    )

    ax2.set_xlim(date_num_min - date_margin, date_num_max + date_margin)
    ax2.set_ylim(
        -sunspot_south_margin, sunspot_south_max + sunspot_south_margin
    )
    ax2_twin.set_ylim(
        -flare_south_margin, flare_south_max + flare_south_margin
    )

    ax2.grid()
    ax2_twin.grid()

    h2, l2 = ax2.get_legend_handles_labels()
    h2_twin, l2_twin = ax2_twin.get_legend_handles_labels()  # type: ignore[attr-defined]
    ax2.legend(
        h2 + h2_twin,
        l2 + l2_twin,
        fancybox=False,
        edgecolor="black",
        framealpha=1,
        loc="lower center",
        bbox_to_anchor=(0.5, 1.02),
        borderaxespad=0,
        ncol=2,
        prop={
            "family": config.legend_south.font_family,
            "size": config.legend_south.font_size,
        },
    )

    fig.tight_layout()

    return fig
