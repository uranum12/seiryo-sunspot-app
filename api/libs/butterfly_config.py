from pydantic import BaseModel

from api.libs.config_common import Axis, FigSize, Image, Title


class Index(BaseModel):
    year_inteerval: int
    lat_interval: int


class ButterflyDiagram(BaseModel):
    fig_size: FigSize
    index: Index
    image: Image
    title: Title
    xaxis: Axis
    yaxis: Axis
