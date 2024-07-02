import { getFiles } from "@/api/files"

export function getFilesAgg(): ReturnType<typeof getFiles> {
  return getFiles({ path: "out", glob: "*.parquet" })
}

export function getFilesDraw(): ReturnType<typeof getFiles> {
  return getFiles({ path: "out/butterfly", glob: "**/*.npz" })
}

export function getFilesConfig(): ReturnType<typeof getFiles> {
  return getFiles({ path: "config/butterfly/butterfly", glob: "*.json" })
}
