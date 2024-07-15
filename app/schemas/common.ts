import {
  integer,
  minValue,
  nonEmpty,
  nullish,
  number,
  object,
  pipe,
  string,
  trim,
} from "valibot"

export const schemaFigSize = object({
  width: pipe(number(), minValue(1)),
  height: pipe(number(), minValue(1)),
})

export const schemaMarker = object({
  marker: pipe(string(), trim(), nonEmpty()),
  size: pipe(number(), minValue(0.01)),
})

export const schemaLine = object({
  label: pipe(string(), trim()),
  style: pipe(string(), trim(), nonEmpty()),
  width: pipe(number(), minValue(0.01)),
  color: pipe(string(), trim(), nonEmpty()),
  marker: schemaMarker,
})

export const schemaBar = object({
  label: pipe(string(), trim()),
  width: pipe(number(), minValue(0.01)),
  color: pipe(string(), trim(), nonEmpty()),
})

export const schemaScatter = object({
  label: pipe(string(), trim()),
  color: pipe(string(), trim(), nonEmpty()),
  edgeColor: pipe(string(), trim(), nonEmpty()),
  marker: schemaMarker,
})

export const schemaImage = object({
  cmap: pipe(string(), trim(), nonEmpty()),
  aspect: pipe(number(), minValue(0.01)),
})

export const schemaTitle = object({
  text: pipe(string(), trim()),
  fontFamily: pipe(string(), trim(), nonEmpty()),
  fontSize: pipe(number(), integer(), minValue(1)),
  position: number(),
})

export const schemaTicks = object({
  fontFamily: pipe(string(), trim(), nonEmpty()),
  fontSize: pipe(number(), integer(), minValue(1)),
})

export const schemaAxis = object({
  title: schemaTitle,
  ticks: schemaTicks,
})

export const schemaText = object({
  x: nullish(pipe(number(), minValue(0.01))),
  y: nullish(pipe(number(), minValue(0.01))),
  mathFontFamily: pipe(string(), trim(), nonEmpty()),
  fontFamily: pipe(string(), trim(), nonEmpty()),
  fontSize: pipe(number(), integer(), minValue(1)),
})

export const schemaLegend = object({
  fontFamily: pipe(string(), trim(), nonEmpty()),
  fontSize: pipe(number(), integer(), minValue(1)),
})
