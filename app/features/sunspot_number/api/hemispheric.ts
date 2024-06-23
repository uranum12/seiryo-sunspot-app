import { get, post } from "@/utils/fetch"

type GetDrawRes = {
  img: string
}

type GetDrawParams = {
  filename: string
  configName: string
}

export async function getDraw(
  params: GetDrawParams,
): Promise<GetDrawRes["img"]> {
  const res = await get<GetDrawRes, GetDrawParams>(
    "/api/sunspot_number/draw/hemispheric",
    params,
  )
  return res.img
}

type PostDrawRes = {
  output: string
}

type PostDrawBody = {
  input: string
  format: string
  config: string
  dpi: number
  overwrite: boolean
}

export async function postDraw(
  body: PostDrawBody,
): Promise<PostDrawRes["output"]> {
  const res = await post<PostDrawRes, PostDrawBody>(
    "/api/sunspot_number/draw/hemispheric",
    body,
  )
  return res.output
}
