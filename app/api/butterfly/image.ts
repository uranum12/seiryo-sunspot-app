import { post } from "@/utils/fetch"

type ImageRes = {
  outputImage: string
}

type ImageBody = {
  inputName: string
  overwrite: boolean
}

export async function postImage(
  body: ImageBody,
): Promise<ImageRes["outputImage"]> {
  const res = await post<ImageRes, ImageBody>("/api/butterfly/image", body)
  return res.outputImage
}
