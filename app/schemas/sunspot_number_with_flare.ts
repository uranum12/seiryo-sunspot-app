import { object } from "valibot"

import {
  schemaAxis,
  schemaFigSize,
  schemaLegend,
  schemaLine,
  schemaTitle,
} from "@/schemas/common"

export const schemaSunspotNumberWithFlare = object({
  figSize: schemaFigSize,
  lineSunspot: schemaLine,
  lineFlare: schemaLine,
  title: schemaTitle,
  xaxis: schemaAxis,
  yaxisSunspot: schemaAxis,
  yaxisFlare: schemaAxis,
  legend: schemaLegend,
})

export const schemaSunspotNumberWithFlareHemispheric = object({
  figSize: schemaFigSize,
  lineNorthSunspot: schemaLine,
  lineNorthFlare: schemaLine,
  lineSouthSunspot: schemaLine,
  lineSouthFlare: schemaLine,
  titleNorth: schemaTitle,
  titleSouth: schemaTitle,
  xaxis: schemaAxis,
  yaxisNorthSunspot: schemaAxis,
  yaxisNorthFlare: schemaAxis,
  yaxisSouthSunspot: schemaAxis,
  yaxisSouthFlare: schemaAxis,
  legendNorth: schemaLegend,
  legendSouth: schemaLegend,
})
