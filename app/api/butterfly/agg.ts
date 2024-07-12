import { post } from "@/utils/fetch"

type AggRes = {
  outputData: string
  outputInfo: string
}

type AggBody = {
  inputName: string
  outputName: string
  overwrite: boolean
}

export async function postAgg(body: AggBody): Promise<AggRes> {
  return await post<AggRes, AggBody>("/api/butterfly/agg", body)
}
