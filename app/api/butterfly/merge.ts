import { post } from "@/utils/fetch"

type MergeRes = {
  outputInfo: string
  outputImg: string
}

type MergeBody = {
  inputNames: string[]
  outputName: string
  overwrite: boolean
}

export async function postMerge(body: MergeBody): Promise<MergeRes> {
  return await post<MergeRes, MergeBody>("/api/butterfly/merge", body)
}
