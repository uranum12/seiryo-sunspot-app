import { post } from "@/utils/fetch"

type AggRes = {
  output: string
}

type AggBody = {
  files: string[]
  filename: string
  overwrite: boolean
}

export async function postAgg(body: AggBody): Promise<AggRes["output"]> {
  const res = await post<AggRes, AggBody>("/api/agg", body)
  return res.output
}
