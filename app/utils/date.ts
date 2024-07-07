import { formatISO, getDate, getMonth, getYear } from "date-fns"

export function toDate(year: number, month: number, day?: number) {
  return new Date(year, month - 1, day)
}

export function fromDate(date: Date) {
  return {
    year: getYear(date),
    month: getMonth(date) + 1,
    day: getDate(date),
  }
}

export function validateDate(year: number, month: number, day: number) {
  const date = toDate(year, month, day)
  return (
    getYear(date) === year &&
    getMonth(date) === month - 1 &&
    getDate(date) === day
  )
}

export function formatDate(date: Date) {
  return formatISO(date, { representation: "date" })
}

export function formatDuration(years?: number, months?: number, days?: number) {
  const yearsString = years ? `${years}Y` : ""
  const monthsString = months ? `${months}M` : ""
  const daysString = days ? `${days}D` : ""
  return `P${yearsString}${monthsString}${daysString}`
}
