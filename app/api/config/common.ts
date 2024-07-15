import { get, post } from "@/utils/fetch"

type GetConfigRes<T> = {
  config: T
}

type GetConfigParams = {
  configName: string
}

export async function getConfig<T>(
  url: string,
  params: GetConfigParams,
): Promise<GetConfigRes<T>["config"]> {
  const res = await get<GetConfigRes<T>, GetConfigParams>(url, params)
  return res.config
}

type PostConfigRes = {
  output: string
}

type PostConfigBody<T> = {
  configName: string
  overwrite: boolean
  config: T
}

export async function postConfig<T>(
  url: string,
  body: PostConfigBody<T>,
): Promise<PostConfigRes["output"]> {
  const res = await post<PostConfigRes, PostConfigBody<T>>(url, body)
  return res.output
}

type PostPreviewRes = {
  img: string
}

type PostPreviewBody<T> = {
  config: T
}

export async function postPreview<T>(
  url: string,
  body: PostPreviewBody<T>,
): Promise<PostPreviewRes["img"]> {
  const res = await post<PostPreviewRes, PostPreviewBody<T>>(url, body)
  return res.img
}
