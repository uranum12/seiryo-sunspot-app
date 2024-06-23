from pydantic import BaseModel


class FigSize(BaseModel):
    width: float
    height: float


class Marker(BaseModel):
    marker: str
    size: float


class Line(BaseModel):
    label: str
    style: str
    width: float
    color: str
    marker: Marker


class Bar(BaseModel):
    label: str
    width: float
    color: str


class Scatter(BaseModel):
    label: str
    color: str
    edge_color: str
    marker: Marker


class Image(BaseModel):
    cmap: str
    aspect: float


class Title(BaseModel):
    text: str
    font_family: str
    font_size: int
    position: float


class Ticks(BaseModel):
    font_family: str
    font_size: int


class Axis(BaseModel):
    title: Title
    ticks: Ticks


class Text(BaseModel):
    x: float | None
    y: float | None
    math_font_family: str
    font_family: str
    font_size: int


class Legend(BaseModel):
    font_family: str
    font_size: int
