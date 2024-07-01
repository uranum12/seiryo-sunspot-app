import { getFiles } from "@/api/files"

export function getFilesAgg(): ReturnType<typeof getFiles> {
  return getFiles({ path: "out", glob: "*.parquet" })
}

export function getFilesDraw(): ReturnType<typeof getFiles> {
  return getFiles({ path: "out/observations", glob: "*/monthly.parquet" })
}

export function getFilesConfigMonthly(): ReturnType<typeof getFiles> {
  return getFiles({ path: "config/observations/monthly", glob: "*.json" })
}

export function getFilesCalendar(): ReturnType<typeof getFiles> {
  return getFiles({ path: "out/observations", glob: "*/daily.parquet" })
}
