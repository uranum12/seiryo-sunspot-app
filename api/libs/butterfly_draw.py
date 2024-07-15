from datetime import date

import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
import polars as pl
from matplotlib.figure import Figure

from api.libs.butterfly import ButterflyInfo
from api.libs.butterfly_config import ButterflyDiagram


def create_date_index(
    start: date, end: date, interval: str
) -> npt.NDArray[np.datetime64]:
    """蝶形図の日付のインデックスを作成する

    Args:
        start (date): 開始日
        end (date): 終了日
        interval (str): 期間

    Returns:
        npt.NDArray[np.datetime64]: 日付のインデックス
    """
    return pl.date_range(start, end, interval, eager=True).to_numpy()


def create_lat_index(lat_min: int, lat_max: int) -> npt.NDArray[np.int8]:
    """緯度のインデックスを作成する

    Args:
        lat_min (int): 緯度の最小値
        lat_max (int): 緯度の最大値

    Returns:
        npt.NDArray[np.int8]: 緯度のインデックス
    """
    lat_range = np.arange(lat_min, lat_max + 1, 1, dtype=np.int8)[::-1]
    return np.insert(np.abs(lat_range), np.arange(1, len(lat_range)), -1)


def draw_butterfly_diagram(
    img: npt.NDArray[np.uint8], info: ButterflyInfo, config: ButterflyDiagram
) -> Figure:
    """蝶形図データを基に画像を作成する

    Args:
        img (npt.NDArray[np.uint8]): 蝶形図のデータ
        info (ButterflyInfo): 蝶形図の情報
        config (ButterflyDiagram): グラフの設定

    Returns:
        Figure: 作成した蝶形図
    """
    date_index = create_date_index(
        info.date_start, info.date_end, info.date_interval.to_interval()
    )
    lat_index = create_lat_index(info.lat_min, info.lat_max)

    xlabel = [
        (i, f"{d.year}")
        for i, d in enumerate(item.item() for item in date_index)
        if d.month == 1 and d.year % config.index.year_interval == 0
    ]
    ylabel = [
        (i, n)
        for i, n in enumerate(lat_index)
        if n % config.index.lat_interval == 0
    ]

    fig = plt.figure(figsize=(config.fig_size.width, config.fig_size.height))
    ax = fig.add_subplot(111)

    ax.imshow(img, cmap=config.image.cmap, aspect=config.image.aspect)

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

    ax.set_xticks([i[0] for i in xlabel])
    ax.set_xticklabels(
        [i[1] for i in xlabel],
        fontfamily=config.xaxis.ticks.font_family,
        fontsize=config.xaxis.ticks.font_size,
    )

    ax.set_ylabel(
        config.yaxis.title.text,
        fontfamily=config.yaxis.title.font_family,
        fontsize=config.yaxis.title.font_size,
    )

    ax.set_yticks([i[0] for i in ylabel])
    ax.set_yticklabels(
        [i[1] for i in ylabel],
        fontfamily=config.yaxis.ticks.font_family,
        fontsize=config.yaxis.ticks.font_size,
    )

    return fig
