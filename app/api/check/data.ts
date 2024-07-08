import { get } from "@/utils/fetch"

type CheckDataGroupNumberRes = {
  date: string[]
  original: number[][]
  expected: number[][]
}

type CheckDataGroupNumberParams = {
  input: string
}

export async function getCheckDataGroupNumber(
  params: CheckDataGroupNumberParams,
): Promise<CheckDataGroupNumberRes> {
  return await get<CheckDataGroupNumberRes, CheckDataGroupNumberParams>(
    "/api/check/data/group_number",
    params,
  )
}

type CheckDataLatRangeRes = {
  date: string[]
  no: number[]
  latMin: number[]
  latMax: number[]
}

type CheckDataLatRangeParams = {
  input: string
  threshold: number
}

export async function getCheckDataLatRange(
  params: CheckDataLatRangeParams,
): Promise<CheckDataLatRangeRes> {
  return await get<CheckDataLatRangeRes, CheckDataLatRangeParams>(
    "/api/check/data/lat_range",
    params,
  )
}

type CheckDataLonRangeRes = {
  date: string[]
  no: number[]
  lonMin: number[]
  lonMax: number[]
}

type CheckDataLonRangeParams = {
  input: string
  minThreshold: number
  maxThreshold: number
}

export async function getCheckDataLonRange(
  params: CheckDataLonRangeParams,
): Promise<CheckDataLonRangeRes> {
  return await get<CheckDataLonRangeRes, CheckDataLonRangeParams>(
    "/api/check/data/lon_range",
    params,
  )
}

type CheckDataLatIntervalRes = {
  date: string[]
  no: number[]
  latMin: number[]
  latMax: number[]
  interval: number[]
}

type CheckDataLatIntervalParams = {
  input: string
  interval: number
}

export async function getCheckDataLatInterval(
  params: CheckDataLatIntervalParams,
): Promise<CheckDataLatIntervalRes> {
  return await get<CheckDataLatIntervalRes, CheckDataLatIntervalParams>(
    "/api/check/data/lat_interval",
    params,
  )
}

type CheckDataLonIntervalRes = {
  date: string[]
  no: number[]
  lonMin: number[]
  lonMax: number[]
  interval: number[]
}

type CheckDataLonIntervalParams = {
  input: string
  interval: number
}

export async function getCheckDataLonInterval(
  params: CheckDataLonIntervalParams,
): Promise<CheckDataLonIntervalRes> {
  return await get<CheckDataLonIntervalRes, CheckDataLonIntervalParams>(
    "/api/check/data/lon_interval",
    params,
  )
}
