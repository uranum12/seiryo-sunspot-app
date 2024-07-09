import { get } from "@/utils/fetch"

type FinderResult = {
  path: string
  lines: number[]
}

type FinderRes = {
  result: FinderResult[]
}

type FinderParams = {
  year: number
  month: number
  day: number
}

export async function getFinder(
  params: FinderParams,
): Promise<FinderRes["result"]> {
  const res = await get<FinderRes, FinderParams>("/api/check/finder", params)
  return res.result
}
