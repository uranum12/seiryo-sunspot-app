import { object } from "valibot"

import {
  schemaAxis,
  schemaFigSize,
  schemaLegend,
  schemaLine,
  schemaScatter,
  schemaText,
  schemaTitle,
} from "@/schemas/common"

export const schemaSunspotNumberWithSilso = object({
  figSize: schemaFigSize,
  lineSeiryo: schemaLine,
  lineSilso: schemaLine,
  title: schemaTitle,
  xaxis: schemaAxis,
  yaxis: schemaAxis,
  legend: schemaLegend,
})

export const schemaSunspotNumberScatter = object({
  figSize: schemaFigSize,
  lineFactor: schemaLine,
  scatter: schemaScatter,
  textFactor: schemaText,
  textR2: schemaText,
  title: schemaTitle,
  xaxis: schemaAxis,
  yaxis: schemaAxis,
})

export const schemaSunspotNumberRatio = object({
  figSize: schemaFigSize,
  lineFactor: schemaLine,
  lineRatio: schemaLine,
  title: schemaTitle,
  xaxis: schemaAxis,
  yaxis: schemaAxis,
})

export const schemaSunspotNumberDiff = object({
  figSize: schemaFigSize,
  line: schemaLine,
  title: schemaTitle,
  xaxis: schemaAxis,
  yaxis: schemaAxis,
})

export const schemaSunspotNumberRatioDiff1 = object({
  figSize: schemaFigSize,
  lineFactor: schemaLine,
  lineRatio: schemaLine,
  lineDiff: schemaLine,
  titleRatio: schemaTitle,
  titleDiff: schemaTitle,
  xaxis: schemaAxis,
  yaxisRatio: schemaAxis,
  yaxisDiff: schemaAxis,
})

export const schemaSunspotNumberRatioDiff2 = object({
  figSize: schemaFigSize,
  lineRatio: schemaLine,
  lineDiff: schemaLine,
  title: schemaTitle,
  xaxis: schemaAxis,
  yaxisRatio: schemaAxis,
  yaxisDiff: schemaAxis,
  legend: schemaLegend,
})
