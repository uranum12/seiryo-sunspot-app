import json
from pathlib import Path

import matplotlib as mpl
import numpy as np

mpl.use("Agg")

from seiryo_sunspot_lib import butterfly, butterfly_draw
from seiryo_sunspot_lib.butterfly_config import ButterflyDiagram


def draw_butterfly_diagram(  # noqa: PLR0913
    image_path: str,
    info_path: str,
    config_path: str,
    output_path: str,
    *,
    fmt: str = "png",
    dpi: int | None = None,
) -> None:
    with np.load(Path(image_path)) as f_img:
        img = f_img["img"]
    with Path(info_path).open("r") as f_info:
        info = butterfly.ButterflyInfo.from_dict(json.load(f_info))
    with Path(config_path).open("r") as f_config:
        config = ButterflyDiagram(**json.load(f_config))
    fig = butterfly_draw.draw_butterfly_diagram(img, info, config)
    fig.savefig(
        Path(output_path),
        format=fmt,
        dpi=dpi if dpi is not None else "figure",
        bbox_inches="tight",
        pad_inches=0.1,
    )
