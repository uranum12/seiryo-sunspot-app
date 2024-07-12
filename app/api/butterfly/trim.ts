import { post } from "@/utils/fetch"

type TrimRes = {
  outputData: string
  outputInfo: string
}

type TrimBody = {
  inputName: string
  outputName: string
  overwrite: boolean
  latMin?: number
  latMax?: number
  dateStart?: string
  dateEnd?: string
}

export async function postTrim(body: TrimBody): Promise<TrimRes> {
  return await post<TrimRes, TrimBody>("/api/butterfly/trim", body)
}
