import numpy as np
import numpy.typing as npt
import polars as pl

from api.libs import butterfly, butterfly_image
from api.libs.butterfly import ButterflyInfo
from api.libs.butterfly_config import ColorMap


def merge_info(info_list: list[ButterflyInfo]) -> ButterflyInfo:
    if len({info.date_interval for info in info_list}) != 1:
        msg = "Date interval must be equal"
        raise ValueError(msg)
    lat_min = min(info.lat_min for info in info_list)
    lat_max = max(info.lat_max for info in info_list)
    date_start = min(info.date_start for info in info_list)
    date_end = max(info.date_end for info in info_list)
    return ButterflyInfo(
        lat_min, lat_max, date_start, date_end, info_list[0].date_interval
    )


def calc_lat_size(info: ButterflyInfo) -> int:
    return (info.lat_max - info.lat_min) * 2 + 1


def calc_date_size(info: ButterflyInfo) -> int:
    return pl.date_range(
        info.date_start,
        info.date_end,
        info.date_interval.to_interval(),
        eager=True,
    ).len()


def create_merged_image(
    dfl: list[pl.DataFrame], info: ButterflyInfo
) -> npt.NDArray[np.uint16]:
    lat_size = calc_lat_size(info)
    date_size = calc_date_size(info)
    img: npt.NDArray[np.uint16] = np.zeros(
        (lat_size, date_size), dtype=np.uint16
    )
    for i, df in enumerate(dfl):
        img = img + (
            butterfly_image.create_image(
                butterfly.fill_lat(
                    df.lazy(),
                    info.date_start,
                    info.date_end,
                    info.date_interval.to_interval(),
                ).collect(),
                info,
            )
            << i
        ).astype(np.uint16)
    return img


def create_color_image(
    img: npt.NDArray[np.uint16], cmap: ColorMap
) -> npt.NDArray[np.uint8]:
    img_merged = np.full((*img.shape, 3), 0xFF, dtype=np.uint8)
    for i, c in enumerate(cmap.cmap, 1):
        img_merged[img == i] = (c.red, c.green, c.blue)
    return img_merged
