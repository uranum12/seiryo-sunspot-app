from pydantic import BaseModel

from libs.config_common import Axis, FigSize, Legend, Line, Title


class SunspotNumberWholeDisk(BaseModel):
    fig_size: FigSize
    line: Line
    title: Title
    xaxis: Axis
    yaxis: Axis


class SunspotNumberHemispheric(BaseModel):
    fig_size: FigSize
    line_north: Line
    line_south: Line
    title: Title
    xaxis: Axis
    yaxis: Axis
    legend: Legend
