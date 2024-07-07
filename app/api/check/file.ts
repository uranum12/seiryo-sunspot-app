import { get } from "@/utils/fetch"

export type ErrorHeader = {
  type: "header"
  header: string[]
}

export type ErrorRow = {
  type: "row"
  line: number
  over: string[]
}

export type ErrorField = {
  type: "field"
  line: number
  fields: string[]
}

export type CheckFileError = ErrorHeader | ErrorRow | ErrorField

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

export function isErrorHeader(error: CheckFileError): error is ErrorHeader {
  return error.type === "header"
}

export function isErrorRow(error: CheckFileError): error is ErrorRow {
  return error.type === "row"
}

export function isErrorField(error: CheckFileError): error is ErrorField {
  return error.type === "field"
}
