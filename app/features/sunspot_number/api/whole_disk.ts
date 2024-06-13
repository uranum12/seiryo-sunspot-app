import { get, post } from "@/utils/fetch"

type GetDrawRes = {
  img: string
}

type GetDrawParams = {
  filename: string
}

export async function getDraw(params: GetDrawParams): Promise<string> {
  const res = await get<GetDrawRes, GetDrawParams>(
    "/api/sunspot_number/draw/whole_disk",
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
  dpi: number
  overwrite: boolean
}

export async function postDraw(body: PostDrawBody): Promise<string> {
  const res = await post<PostDrawRes, PostDrawBody>(
    "/api/sunspot_number/draw/whole_disk",
    body,
  )
  return res.output
}
