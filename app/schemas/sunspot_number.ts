import { object } from "valibot"

import {
  schemaAxis,
  schemaFigSize,
  schemaLegend,
  schemaLine,
  schemaTitle,
} from "@/schemas/common"

export const schemaSunspotNumberWholeDisk = object({
  figSize: schemaFigSize,
  line: schemaLine,
  title: schemaTitle,
  xaxis: schemaAxis,
  yaxis: schemaAxis,
})

export const schemaSunspotNumberHemispheric = object({
  figSize: schemaFigSize,
  lineNorth: schemaLine,
  lineSouth: schemaLine,
  title: schemaTitle,
  xaxis: schemaAxis,
  yaxis: schemaAxis,
  legend: schemaLegend,
})
