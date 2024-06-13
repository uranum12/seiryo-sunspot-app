type Case<T> = T extends Record<string, unknown>
  ? { [K in keyof T]: Case<T[K]> }
  : T extends (infer U)[]
    ? U extends Record<string, unknown>
      ? Case<U>[]
      : T
    : T

export function toCamelCase<T extends Record<string, unknown>>(
  obj: T,
): Case<T> {
  if (Array.isArray(obj)) {
    return obj.map(toCamelCase) as unknown as Case<T>
  }
  if (obj !== null && typeof obj === "object") {
    return Object.fromEntries(
      Object.entries(obj).map(([key, value]) => [
        key.replace(/([-_][a-z])/g, (group) =>
          group.toUpperCase().replace("_", ""),
        ),
        toCamelCase(value as Record<string, unknown>),
      ]),
    ) as unknown as Case<T>
  }
  return obj as Case<T>
}

export function toSnakeCase<T extends Record<string, unknown>>(
  obj: T,
): Case<T> {
  if (Array.isArray(obj)) {
    return obj.map(toSnakeCase) as unknown as Case<T>
  }
  if (obj !== null && typeof obj === "object") {
    return Object.fromEntries(
      Object.entries(obj).map(([key, value]) => [
        key.replace(/[A-Z]/g, (letter) => `_${letter.toLowerCase()}`),
        toSnakeCase(value as Record<string, unknown>),
      ]),
    ) as unknown as Case<T>
  }
  return obj as Case<T>
}
