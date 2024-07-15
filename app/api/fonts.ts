import { get } from "@/utils/fetch"

type FontsRes = {
  names: string[]
}

export async function getFonts(): Promise<FontsRes["names"]> {
  const res = await get<FontsRes>("/api/utils/fonts")
  return res.names
}
