import { get } from "@/utils/fetch"

type FilesRes = {
  files: string[]
}

type FilesParams = {
  path: string
  glob: string
}

export async function getFiles(): Promise<string[]> {
  const res = await get<FilesRes, FilesParams>("/api/utils/files", {
    path: "data",
    glob: "*.csv",
  })
  return res.files
}
