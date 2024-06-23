import { getFiles } from "@/api/files"

export function getFilesAgg(): ReturnType<typeof getFiles> {
  return getFiles({ path: "out", glob: "*.parquet" })
}

export function getFilesDraw(): ReturnType<typeof getFiles> {
  return getFiles({ path: "out/sunspot", glob: "*/monthly.parquet" })
}

export function getFilesConfigWholeDisk(): ReturnType<typeof getFiles> {
  return getFiles({ path: "config/sunspot_number/whole_disk", glob: "*.json" })
}

export function getFilesConfigHemispheric(): ReturnType<typeof getFiles> {
  return getFiles({ path: "config/sunspot_number/hemispheric", glob: "*.json" })
}
