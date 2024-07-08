import { get } from "@/utils/fetch"

type ErrorHeader = {
  type: "header"
  header: string[]
}

type ErrorRow = {
  type: "row"
  line: number
  over: string[]
}

type ErrorField = {
  type: "field"
  line: number
  fields: string[]
}

type CheckFileError = ErrorHeader | ErrorRow | ErrorField

type CheckFileRes = {
  errors: CheckFileError[]
}

type CheckFileParams = {
  input: string
}

export async function getCheckFile(
  params: CheckFileParams,
): Promise<CheckFileRes["errors"]> {
  const res = await get<CheckFileRes, CheckFileParams>(
    "/api/check/file",
    params,
  )
  return res.errors
}
