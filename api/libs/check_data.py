import polars as pl


def create_expected_group_numbers(no: int) -> pl.Series:
    return pl.Series(range(1, no + 1), dtype=pl.UInt8)


def find_invalid_group_number(df: pl.DataFrame) -> pl.DataFrame:
    """不正なグループ番号を検索する

    Args:
        df (pl.DataFrame): 黒点群データ

    Returns:
        pl.DataFrame: 不正値を含む行のみの新しいデータフレーム
    """
    return (
        df.lazy()
        .group_by("date")
        .agg(
            pl.col("no").alias("original"),
            pl.col("no")
            .count()
            .map_elements(
                create_expected_group_numbers, return_dtype=pl.List(pl.UInt8)
            )
            .alias("expected"),
        )
        .with_columns(pl.col("original", "expected").list.sort())
        .filter(
            (pl.col("original") != pl.col("expected"))
            & (pl.col("original") != [0])
        )
        .collect()
    )


def find_invalid_lat_range(df: pl.DataFrame, threshold: int) -> pl.DataFrame:
    """不正な範囲に存在する緯度を検索する

    Args:
        df (pl.DataFrame): 黒点群データ
        threshold (int): 緯度の閾値

    Returns:
        pl.DataFrame: 不正値を含む行のみの新しいデータフレーム
    """
    return df.filter(
        pl.any_horizontal(
            ~pl.col("lat_min").abs().is_between(0, threshold),
            ~pl.col("lat_max").abs().is_between(0, threshold),
        )
    )


def find_invalid_lon_range(
    df: pl.DataFrame, min_threshold: int, max_threshold: int
) -> pl.DataFrame:
    """不正な範囲に存在する経度を検索する

    Args:
        df (pl.DataFrame): 黒点群データ
        min_threshold (int): 経度の閾値の最小
        max_threshold (int): 経度の閾値の最大

    Returns:
        pl.DataFrame: 不正値を含む行のみの新しいデータフレーム
    """
    return df.filter(
        pl.any_horizontal(
            ~pl.col("lon_min").is_between(min_threshold, max_threshold),
            ~pl.col("lon_max").is_between(min_threshold, max_threshold),
        )
    )


def find_invalid_lat_interval(df: pl.DataFrame, interval: int) -> pl.DataFrame:
    """不正な間隔を持つ緯度を検索する

    Args:
        df (pl.DataFrame): 黒点群データ
        interval (int): 緯度の間隔の最大値

    Returns:
        pl.DataFrame: 不正値を含む行のみの新しいデータフレーム
    """
    return df.with_columns(
        (pl.col("lat_max") - pl.col("lat_min")).alias("interval")
    ).filter(pl.col("interval") > interval)


def find_invalid_lon_interval(df: pl.DataFrame, interval: int) -> pl.DataFrame:
    """不正な間隔を持つ経度を検索する

    Args:
        df (pl.DataFrame): 黒点群データ
        interval (int): 経度の間隔の最大値

    Returns:
        pl.DataFrame: 不正値を含む行のみの新しいデータフレーム
    """
    return df.with_columns(
        (pl.col("lon_max") - pl.col("lon_min")).alias("interval")
    ).filter(pl.col("interval") > interval)
