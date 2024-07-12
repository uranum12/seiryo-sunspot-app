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

export async function postAgg(url: string, body: AggBody): Promise<AggRes> {
  return await post<AggRes, AggBody>(url, body)
}
