import { get } from "@/utils/fetch"

type FilesRes = {
  files: string[]
}

type FilesParams = {
  path: string
  glob: string
}

export async function getFilesAgg(): Promise<string[]> {
  const res = await get<FilesRes, FilesParams>("/api/utils/files", {
    path: "out",
    glob: "*.parquet",
  })
  return res.files
}

export async function getFilesDraw(): Promise<string[]> {
  const res = await get<FilesRes, FilesParams>("/api/utils/files", {
    path: "out/sunspot",
    glob: "*/monthly.parquet",
  })
  return res.files
}
