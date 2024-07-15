import { object } from "valibot"

import {
  schemaAxis,
  schemaBar,
  schemaFigSize,
  schemaTitle,
} from "@/schemas/common"

export const schemaObservationsMonthly = object({
  figSize: schemaFigSize,
  bar: schemaBar,
  title: schemaTitle,
  xaxis: schemaAxis,
  yaxis: schemaAxis,
})
