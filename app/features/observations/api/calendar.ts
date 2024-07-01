import { get } from "@/utils/fetch"

type ObservationDay = {
  date: string
  obs: boolean
}

type CalendarRes = {
  calendar: ObservationDay[][]
}

type CalendarParams = {
  filename: string
  year: number
  month: number
  first?: number
}

export async function getCalendar(
  params: CalendarParams,
): Promise<CalendarRes["calendar"]> {
  const res = await get<CalendarRes, CalendarParams>(
    "/api/observations/calendar",
    params,
  )
  return res.calendar
}
