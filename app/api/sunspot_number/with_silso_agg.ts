import { post } from "@/utils/fetch"

type AggRes = {
  outputWithSilso: string
  outputFactorR2: string
  outputRatioDiff: string
}

type AggBody = {
  seiryoPath: string
  silsoPath: string
  outputName: string
  overwrite: boolean
}

export async function postAgg(body: AggBody): Promise<AggRes> {
  return await post<AggRes, AggBody>("/api/sunspot_number/with_silso/agg", body)
}
