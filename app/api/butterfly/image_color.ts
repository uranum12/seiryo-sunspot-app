import { post } from "@/utils/fetch"

type ImageColorRes = {
  outputInfo: string
  outputImage: string
}

type ImageColorBody = {
  inputName: string
  colorsName: string
  outputName: string
  overwrite: boolean
}

export async function postImageColor(
  body: ImageColorBody,
): Promise<ImageColorRes> {
  return await post<ImageColorRes, ImageColorBody>(
    "/api/butterfly/image_color",
    body,
  )
}
