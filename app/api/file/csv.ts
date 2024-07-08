import { get } from "@/utils/fetch"

type FileCsvRes = {
  data: (string | null)[][]
}

type FileCsvParams = {
  input: string
}

export async function getFileCsv(
  params: FileCsvParams,
): Promise<FileCsvRes["data"]> {
  const res = await get<FileCsvRes, FileCsvParams>(
    "/api/utils/file/csv",
    params,
  )
  return res.data
}
