import { getFiles as get } from "@/api/files"

export function getFiles(): ReturnType<typeof get> {
  return get({ path: "data", glob: "*.csv" })
}
