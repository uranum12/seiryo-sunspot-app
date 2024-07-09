from pydantic import BaseModel

from api.libs.config_common import (
    Axis,
    FigSize,
    Legend,
    Line,
    Scatter,
    Text,
    Title,
)


class SunspotNumberWithSilso(BaseModel):
    fig_size: FigSize
    line_seiryo: Line
    line_silso: Line
    title: Title
    xaxis: Axis
    yaxis: Axis
    legend: Legend


class SunspotNumberScatter(BaseModel):
    fig_size: FigSize
    line_factor: Line
    scatter: Scatter
    text_factor: Text
    text_r2: Text
    title: Title
    xaxis: Axis
    yaxis: Axis


class SunspotNumberRatio(BaseModel):
    fig_size: FigSize
    line_factor: Line
    line_ratio: Line
    title: Title
    xaxis: Axis
    yaxis: Axis


class SunspotNumberDiff(BaseModel):
    fig_size: FigSize
    line: Line
    title: Title
    xaxis: Axis
    yaxis: Axis


class SunspotNumberRatioDiff1(BaseModel):
    fig_size: FigSize
    line_factor: Line
    line_ratio: Line
    line_diff: Line
    title_ratio: Title
    title_diff: Title
    xaxis: Axis
    yaxis_ratio: Axis
    yaxis_diff: Axis


class SunspotNumberRatioDiff2(BaseModel):
    fig_size: FigSize
    line_ratio: Line
    line_diff: Line
    title: Title
    xaxis: Axis
    yaxis_ratio: Axis
    yaxis_diff: Axis
    legend: Legend
