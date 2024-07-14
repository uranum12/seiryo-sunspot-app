import type { InferOutput } from "valibot"

import type { schemaSunspotNumberWholeDisk } from "@/schemas/sunspot_number"
import { get, post } from "@/utils/fetch"

type SunspotNumberWholeDisk = InferOutput<typeof schemaSunspotNumberWholeDisk>

type GetConfigWholeDiskRes = {
  config: SunspotNumberWholeDisk
}

type GetConfigWholeDiskParams = {
  configName: string
}

export async function getConfigWholeDisk(
  params: GetConfigWholeDiskParams,
): Promise<GetConfigWholeDiskRes["config"]> {
  const res = await get<GetConfigWholeDiskRes, GetConfigWholeDiskParams>(
    "/api/sunspot_number/config/whole_disk",
    params,
  )
  return res.config
}

type PostConfigWholeDiskRes = {
  output: string
}

type PostConfigWholeDiskBody = {
  configName: string
  overwrite: boolean
  config: SunspotNumberWholeDisk
}

export async function postConfigWholeDisk(
  body: PostConfigWholeDiskBody,
): Promise<PostConfigWholeDiskRes["output"]> {
  const res = await post<PostConfigWholeDiskRes, PostConfigWholeDiskBody>(
    "/api/sunspot_number/config/whole_disk",
    body,
  )
  return res.output
}

type PostPreviewConfigWholeDiskRes = {
  img: string
}

type PostPreviewConfigWholeDiskBody = {
  config: SunspotNumberWholeDisk
}

export async function postPreviewConfigWholeDisk(
  body: PostPreviewConfigWholeDiskBody,
): Promise<PostPreviewConfigWholeDiskRes["img"]> {
  const res = await post<
    PostPreviewConfigWholeDiskRes,
    PostPreviewConfigWholeDiskBody
  >("/api/sunspot_number/config/whole_disk/preview", body)
  return res.img
}
