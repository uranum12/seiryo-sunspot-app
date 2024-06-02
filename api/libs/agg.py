import polars as pl


def fill_date(df: pl.LazyFrame) -> pl.LazyFrame:
    return df.with_columns(pl.col("date").forward_fill())


def convert_number(df: pl.LazyFrame) -> pl.LazyFrame:
    return df.cast({"no": pl.UInt8, "num": pl.UInt16})


def convert_date(df: pl.LazyFrame) -> pl.LazyFrame:
    return df.with_columns(
        pl.col("date").str.replace_all(r"([-/\.])", " ").str.split(by=" ")
    ).with_columns(
        pl.date(
            pl.col("date").list.get(0),
            pl.col("date").list.get(1),
            pl.col("date").list.get(2),
        )
    )


def convert_coord(
    df: pl.LazyFrame, *, col: str, dtype: pl.PolarsDataType
) -> pl.LazyFrame:
    pat_left_sign = r"(?P<left_sign>[nsewpm+-]?)"
    pat_left = r"(?P<left>\d{1,2}(?:\.\d+)?)"
    pat_left = f"{pat_left_sign}{pat_left}"
    pat_right_sign = r"(?P<right_sign>[nsewpm+-]?)"
    pat_right = r"(?P<right>\d{1,2}(?:\.\d+)?)"
    pat_right = f"{pat_right_sign}{pat_right}"
    pat = f"(?i)(?:ND|{pat_left}(?:~{pat_right})?)"
    return (
        df.with_columns(
            # 正規表現で構造体へ分解
            pl.col(col).str.extract_groups(pat)
        )
        .unnest(col)  # 構造体から列へ分解
        .with_columns(
            # 符号の文字を小文字へ変換
            pl.col("left_sign", "right_sign").str.to_lowercase()
        )
        .with_columns(
            # 右の符号と数値が存在しなければ左で埋める
            pl.col("right_sign").fill_null(pl.col("left_sign")),
            pl.col("right").fill_null(pl.col("left")),
        )
        .with_columns(
            # 右の符号が存在せず、左の符号が東西南北のマイナスの場合
            # 右の符号を左の符号で埋める
            pl.when(
                pl.col("right_sign").eq("")
                & pl.col("left_sign").is_in({"s", "w"})
            )
            .then(pl.lit("-"))
            .otherwise(pl.col("right_sign"))
            .alias("right_sign")
        )
        .collect()
        .lazy()
        .with_columns(
            # 文字の符号を数式の符号へ変換
            pl.col("left_sign", "right_sign").str.replace_many(
                ["n", "s", "e", "w", "p", "m"], ["+", "-", "+", "-", "+", "-"]
            )
        )
        .with_columns(
            # 符号を数値へ反映
            pl.concat_str("left_sign", "left").alias("left"),
            pl.concat_str("right_sign", "right").alias("right"),
        )
        .with_columns(
            # 文字列から小数へ変換し、四捨五入
            pl.col("left", "right").cast(pl.Float64).round()
        )
        .with_columns(
            # 最大値と最小値を算出し、整数へ変換
            pl.min_horizontal("left", "right").cast(dtype).alias(f"{col}_min"),
            pl.max_horizontal("left", "right").cast(dtype).alias(f"{col}_max"),
        )
        .drop("left_sign", "right_sign", "left", "right")
    )


def sort(df: pl.LazyFrame) -> pl.LazyFrame:
    return df.select(
        ["date", "no", "lat_min", "lat_max", "lon_min", "lon_max", "num"]
    ).sort("date", "no")
