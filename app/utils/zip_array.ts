import type {
  getCheckDataGroupNumber,
  getCheckDataLatInterval,
  getCheckDataLatRange,
  getCheckDataLonInterval,
  getCheckDataLonRange,
} from "@/api/check/data"

type GroupNumber = [string, number[], number[]]

export function zipGroupNumber(
  res: Awaited<ReturnType<typeof getCheckDataGroupNumber>>,
): GroupNumber[] {
  const len = res.date.length
  const result: GroupNumber[] = []
  for (let i = 0; i < len; i++) {
    result.push([res.date[i], res.original[i], res.expected[i]])
  }
  return result
}

type Range = [string, number, number, number]

export function zipLatRange(
  res: Awaited<ReturnType<typeof getCheckDataLatRange>>,
): Range[] {
  const len = res.date.length
  const result: Range[] = []
  for (let i = 0; i < len; i++) {
    result.push([res.date[i], res.no[i], res.latMin[i], res.latMax[i]])
  }
  return result
}

export function zipLonRange(
  res: Awaited<ReturnType<typeof getCheckDataLonRange>>,
): Range[] {
  const len = res.date.length
  const result: Range[] = []
  for (let i = 0; i < len; i++) {
    result.push([res.date[i], res.no[i], res.lonMin[i], res.lonMax[i]])
  }
  return result
}
type Interval = [string, number, number, number, number]

export function zipLatInterval(
  res: Awaited<ReturnType<typeof getCheckDataLatInterval>>,
): Interval[] {
  const len = res.date.length
  const result: Interval[] = []
  for (let i = 0; i < len; i++) {
    result.push([
      res.date[i],
      res.no[i],
      res.latMin[i],
      res.latMax[i],
      res.interval[i],
    ])
  }
  return result
}

export function zipLonInterval(
  res: Awaited<ReturnType<typeof getCheckDataLonInterval>>,
): Interval[] {
  const len = res.date.length
  const result: Interval[] = []
  for (let i = 0; i < len; i++) {
    result.push([
      res.date[i],
      res.no[i],
      res.lonMin[i],
      res.lonMax[i],
      res.interval[i],
    ])
  }
  return result
}
