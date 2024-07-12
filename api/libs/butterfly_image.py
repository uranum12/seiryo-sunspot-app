import numpy as np
import numpy.typing as npt
import polars as pl

from api.libs.butterfly import ButterflyInfo


def create_line(
    data_min: list[int], data_max: list[int], lat_min: int, lat_max: int
) -> npt.NDArray[np.uint8]:
    """蝶形図の一列分のデータを作成する

    Args:
        data_min (list[int]): データの最小値
        data_max (list[int]): データの最大値
        lat_min (int): 緯度の最小値
        lat_max (int): 緯度の最大値

    Returns:
        npt.NDArray[np.uint8]: 一列分のデータ
    """
    # numpy配列に変換
    arr_min = np.array(data_min)
    arr_max = np.array(data_max)

    # 範囲外のインデックス
    index_outer = (arr_max < lat_min) | (lat_max < arr_min)

    # 範囲外のデータを除去
    arr_min = arr_min[~index_outer]
    arr_max = arr_max[~index_outer]

    # 緯度のインデックスの最大値
    max_index = 2 * (lat_max - lat_min)

    # 赤道のインデックス
    equator_index = 2 * lat_max

    # 行のインデックス
    index_min = equator_index - arr_max * 2
    index_max = equator_index - arr_min * 2 + 1

    # 範囲内に収まるよう調整
    index_min = np.clip(index_min, 0, max_index)
    index_max = np.clip(index_max, 1, max_index + 1)

    # 行を埋める
    line = np.zeros(max_index + 1, dtype=np.uint8)
    for i_min, i_max in zip(index_min, index_max, strict=False):
        line[i_min:i_max] = 1

    return line


def create_image(
    df: pl.DataFrame, info: ButterflyInfo
) -> npt.NDArray[np.uint8]:
    """緯度データから蝶形図のデータを作成する

    Args:
        df (pl.DataFrame): 緯度データ
        info (ButterflyInfo): 蝶形図の情報

    Returns:
        npt.NDArray[np.uint8]: 蝶形図の画像データ
    """
    lines: list[npt.NDArray[np.uint8]] = []
    for data in df.iter_rows(named=True):
        data_min: list[int] = data["min"]
        data_max: list[int] = data["max"]
        line = create_line(data_min, data_max, info.lat_min, info.lat_max)
        lines.append(line.reshape(-1, 1))
    return np.hstack(lines)
