from pydantic import BaseModel, Field

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


class Color(BaseModel):
    red: int = Field(..., ge=0, le=0xFF)
    green: int = Field(..., ge=0, le=0xFF)
    blue: int = Field(..., ge=0, le=0xFF)
