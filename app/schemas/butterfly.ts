import {
  array,
  integer,
  maxValue,
  minValue,
  number,
  object,
  pipe,
} from "valibot"

import {
  schemaAxis,
  schemaFigSize,
  schemaImage,
  schemaTitle,
} from "@/schemas/common"

export const schemaIndex = object({
  yearInterval: pipe(number(), integer(), minValue(1)),
  latInterval: pipe(number(), integer(), minValue(1)),
})

export const schemaButterfyDiagram = object({
  figSize: schemaFigSize,
  index: schemaIndex,
  image: schemaImage,
  title: schemaTitle,
  xaxis: schemaAxis,
  yaxis: schemaAxis,
})

export const schemaColor = object({
  red: pipe(number(), integer(), minValue(0), maxValue(0xff)),
  green: pipe(number(), integer(), minValue(0), maxValue(0xff)),
  blue: pipe(number(), integer(), minValue(0), maxValue(0xff)),
})

export const schemaCmap = array(schemaColor)

export const schemaColorMap = object({
  cmap: schemaCmap,
})
