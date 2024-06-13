import matplotlib.pyplot as plt
import polars as pl
from matplotlib.figure import Figure


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


def draw_sunspot_number_whole_disk(df: pl.DataFrame) -> Figure:
    fig = plt.figure(figsize=(8, 5))
    ax = fig.add_subplot(111)

    ax.plot(df["date"], df["total"])

    ax.set_title("seiryo's whole-disk sunspot number")
    ax.set_xlabel("date")
    ax.set_ylabel("sunspot number")

    ax.grid()

    fig.tight_layout()

    return fig


def draw_sunspot_number_hemispheric(df: pl.DataFrame) -> Figure:
    fig = plt.figure(figsize=(8, 5))
    ax = fig.add_subplot(111)

    ax.plot(df["date"], df["north"], lw=1, label="north")
    ax.plot(df["date"], df["south"], lw=1, label="south")

    ax.set_title("seiryo's hemispheric sunspot number", y=1.1)
    ax.set_xlabel("date")
    ax.set_ylabel("sunspot number")

    ax.grid()
    ax.legend(
        fancybox=False,
        edgecolor="black",
        framealpha=1,
        loc="lower center",
        bbox_to_anchor=(0.5, 1.02),
        borderaxespad=0,
        ncol=2,
    )

    fig.tight_layout()

    return fig


if __name__ == "__main__":
    from pathlib import Path

    input_file = Path("out/all.parquet")
    output_dir = Path("out/sunspot")
    output_dir.mkdir(exist_ok=True, parents=True)
    df_spot, df_nospot = split(pl.scan_parquet(input_file))
    df_spot = df_spot.pipe(calc_lat).pipe(calc_sn)
    df_nospot = df_nospot.select("date").pipe(fill_sn)
    df_raw = pl.concat([df_spot, df_nospot]).pipe(sort).collect()
    print(df_raw)
    df_raw.write_parquet(output_dir / "raw.parquet")
    df_daily = agg_daily(df_raw)
    print(df_daily)
    df_daily.write_parquet(output_dir / "daily.parquet")
    df_monthly = agg_monthly(df_raw)
    print(df_monthly)
    df_monthly.write_parquet(output_dir / "monthly.parquet")
    fig_whole_disk = draw_sunspot_number_whole_disk(df_monthly)
    fig_whole_disk.savefig(output_dir / "whole_disk.jpg")
    fig_hemispheric = draw_sunspot_number_hemispheric(df_monthly)
    fig_hemispheric.savefig(output_dir / "hemispheric.jpg")
