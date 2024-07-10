from pydantic import BaseModel

from api.libs.config_common import Axis, FigSize, Legend, Line, Title


class SunspotNumberWithFlare(BaseModel):
    fig_size: FigSize
    line_sunspot: Line
    line_flare: Line
    title: Title
    xaxis: Axis
    yaxis_sunspot: Axis
    yaxis_flare: Axis
    legend: Legend


class SunspotNumberWithFlareHemispheric(BaseModel):
    fig_size: FigSize
    line_north_sunspot: Line
    line_north_flare: Line
    line_south_sunspot: Line
    line_south_flare: Line
    title_north: Title
    title_south: Title
    xaxis: Axis
    yaxis_north_sunspot: Axis
    yaxis_north_flare: Axis
    yaxis_south_sunspot: Axis
    yaxis_south_flare: Axis
    legend_north: Legend
    legend_south: Legend
