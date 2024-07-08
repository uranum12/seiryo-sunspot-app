<script lang="ts">
  import {
    addMonths,
    getDate,
    getDay,
    getMonth,
    getYear,
    isSameMonth,
    subMonths,
    toDate,
  } from "date-fns"

  import { getFiles } from "@/api/files"
  import { getCalendar } from "@/api/observations/calendar"
  import Alert from "@/components/alert.svelte"
  import DateSelect from "@/components/date_select.svelte"
  import { formatDate, fromDate } from "@/utils/date"
  import { FetchError } from "@/utils/fetch"

  let filename = $state<string>("")
  let date = $state<string>()

  let first = $state<number>(0)

  let currentDate = $state<Date>()

  const getFilesCalendar = () => {
    return getFiles({ path: "out/observations", glob: "*/daily.parquet" })
  }

  let filesPromise = $state<ReturnType<typeof getFiles>>(getFilesCalendar())
  let calendarPromise = $state<ReturnType<typeof getCalendar>>()

  const submitDisabled = $derived(filename.trim() === "" || !date)

  const fetchFiles = () => {
    filesPromise = getFilesCalendar()
  }

  const submitCalendar = () => {
    if (date) {
      currentDate = toDate(date)
      const { day, ...rest } = fromDate(currentDate)
      calendarPromise = getCalendar({
        filename,
        year: rest.year,
        month: rest.month,
      })
    }
  }

  const week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

  const getWeek = () => {
    return [...week.slice(first), ...week.slice(0, first)]
  }

  const nextMonth = () => {
    if (date) {
      date = formatDate(addMonths(date, 1))
      submitCalendar()
    }
  }

  const previousMonth = () => {
    if (date) {
      date = formatDate(subMonths(date, 1))
      submitCalendar()
    }
  }
</script>

<section>
  <button onclick={fetchFiles}>refresh files</button>
</section>

{#await filesPromise}
  <p>loading...</p>
{:then files}
  <section class="space-y-1">
    <select required bind:value={filename}>
      <option value="" selected disabled>select file</option>
      {#each files.sort() as file}
        <option value={file}>{file.replace(/^out\//, "")}</option>
      {/each}
    </select>
    <DateSelect bind:date required dayHidden />
    <button disabled={submitDisabled} onclick={submitCalendar}>submit</button>
  </section>
{:catch e}
  <section>
    <Alert type="error">
      <p>{e.message}</p>
    </Alert>
  </section>
{/await}

{#if currentDate}
  <section>
    <div class="flex justify-between">
      <button onclick={previousMonth}>previous month</button>
      <div>{`${getYear(currentDate)}/${getMonth(currentDate) + 1}`}</div>
      <button onclick={nextMonth}>next month</button>
    </div>
  </section>

  {#if calendarPromise}
    {#await calendarPromise}
      <p>loading...</p>
    {:then calendar}
      <section>
        <table>
          <thead>
            <tr>
              {#each getWeek() as week}
                <th>
                  {week}
                </th>
              {/each}
            </tr>
          </thead>
          <tbody>
            {#each calendar as week}
              <tr>
                {#each week as day}
                  {@const weekday = getDay(day.date)}
                  <td
                    class:bg-gray-200={!day.obs}
                    class:text-blue-500={weekday === 6}
                    class:text-red-500={weekday === 0}
                  >
                    <span
                      class:opacity-40={!isSameMonth(day.date, currentDate)}
                    >
                      {getDate(day.date)}
                    </span>
                  </td>
                {/each}
              </tr>
            {/each}
          </tbody>
        </table>
      </section>
    {:catch e}
      <section>
        <Alert type="error">
          <p>{e instanceof FetchError ? e.detail : e.message}</p>
        </Alert>
      </section>
    {/await}
  {/if}
{/if}
