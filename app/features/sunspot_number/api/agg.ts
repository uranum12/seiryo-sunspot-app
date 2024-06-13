import { post } from "@/utils/fetch"

type AggRes = {
  outputRaw: string
  outputDaily: string
  outputMonthly: string
}

type AggBody = {
  filename: string
  overwrite: boolean
}

export async function postAgg(body: AggBody): Promise<AggRes> {
  return await post<AggRes, AggBody>("/api/sunspot_number/agg", body)
}
