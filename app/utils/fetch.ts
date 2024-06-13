import { toCamelCase, toSnakeCase } from "./convert_case"

export class FetchError extends Error {
  public status: number
  public detail: string

  constructor(status: number, detail: string) {
    super(`HTTP Error: ${status} ${detail}`)
    this.status = status
    this.detail = detail
  }
}

function buildBody<T = object>(body: T): string | null {
  if (!body) {
    return null
  }

  return JSON.stringify(toSnakeCase(body))
}

function buildPathWithParams<T = object>(path: string, params?: T): string {
  if (!params || Object.keys(params).length === 0) {
    return path
  }

  for (const key in params) {
    if (params[key] === undefined) {
      delete params[key]
    }
  }

  const urlSearchParams = new URLSearchParams(params)
  return `${path}?${urlSearchParams.toString()}`
}

export async function http<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(path, options)

  if (!res.ok) {
    const data: { detail: string } = await res.json()
    throw new FetchError(res.status, data.detail)
  }

  return toCamelCase(await res.json())
}

export function get<T, U = object>(path: string, params?: U): Promise<T> {
  return http<T>(
    buildPathWithParams(path, params ? toSnakeCase(params) : undefined),
  )
}

export function post<T, U>(path: string, body: U): Promise<T> {
  return http<T>(path, {
    method: "POST",
    body: buildBody(body),
    headers: {
      "Content-Type": "application/json",
    },
  })
}
