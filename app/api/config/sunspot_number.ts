import type { InferOutput } from "valibot"

import { getConfig, postConfig, postPreview } from "@/api/config/common"
import type { schemaSunspotNumberWholeDisk } from "@/schemas/sunspot_number"

type SunspotNumberWholeDisk = InferOutput<typeof schemaSunspotNumberWholeDisk>

export async function getConfigWholeDisk(
  params: Parameters<typeof getConfig>[1],
): ReturnType<typeof getConfig<SunspotNumberWholeDisk>> {
  return await getConfig("/api/sunspot_number/config/whole_disk", params)
}

export async function postConfigWholeDisk(
  body: Parameters<typeof postConfig<SunspotNumberWholeDisk>>[1],
): ReturnType<typeof postConfig> {
  return await postConfig("/api/sunspot_number/config/whole_disk", body)
}

export async function postPreviewConfigWholeDisk(
  body: Parameters<typeof postPreview<SunspotNumberWholeDisk>>[1],
): ReturnType<typeof postPreview> {
  return await postPreview(
    "/api/sunspot_number/config/whole_disk/preview",
    body,
  )
}
