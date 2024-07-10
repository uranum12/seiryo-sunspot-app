import { post } from "@/utils/fetch"

type AggRes = {
  outputWithFlare: string
  outputFactors: string
}

type AggBody = {
  seiryoPath: string
  flareFilesNorth: string[]
  flareFilesSouth: string[]
  flareFilesTotal: string[]
  outputName: string
  overwrite: boolean
}

export async function postAgg(body: AggBody): Promise<AggRes> {
  return await post<AggRes, AggBody>("/api/sunspot_number/with_flare/agg", body)
}
