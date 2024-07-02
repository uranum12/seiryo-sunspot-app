import { post } from "@/utils/fetch"

type AggRes = {
  outputData: string
  outputImage: string
  outputInfo: string
}

type AggBody = {
  inputName: string
  outputName: string
  overwrite: boolean
  latMin?: number
  latMax?: number
  dateStart?: string
  dateEnd?: string
  dateInterval?: string
}

export async function postAgg(body: AggBody): Promise<AggRes> {
  return await post<AggRes, AggBody>("/api/butterfly/agg", body)
}
