import { get } from "@/utils/fetch"

type FilesRes = {
  files: string[]
}

type FilesParams = {
  path: string
  glob: string
}

export async function getFiles(
  params: FilesParams,
): Promise<FilesRes["files"]> {
  const res = await get<FilesRes, FilesParams>("/api/utils/files", params)
  return res.files
}
