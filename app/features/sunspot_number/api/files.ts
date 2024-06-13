import { getFiles } from "@/api/files"

export function getFilesAgg(): ReturnType<typeof getFiles> {
  return getFiles({ path: "out", glob: "*.parquet" })
}

export function getFilesDraw(): ReturnType<typeof getFiles> {
  return getFiles({ path: "out/sunspot", glob: "*/monthly.parquet" })
}
