<script lang="ts">
  import {
    addMonths,
    getDate,
    getDay,
    getMonth,
    getYear,
    isSameMonth,
    isSaturday,
    isSunday,
    subMonths,
  } from "date-fns"
  import { untrack } from "svelte"

  import Alert from "@/components/alert.svelte"
  import Container from "@/components/container.svelte"
  import { FetchError } from "@/utils/fetch"

  import { getCalendar } from "./api/calendar"
  import { getFilesCalendar } from "./api/files"

  let filename = $state<string>("")
  let year = $state<number>()
  let month = $state<number>()

  let date = $state<Date>()

  let first = $state<number>(0)

  let filesPromise =
    $state<ReturnType<typeof getFilesCalendar>>(getFilesCalendar())
  let calendarPromise = $state<ReturnType<typeof getCalendar>>()

  const submitDisabled = $derived<boolean>(filename.trim() === "")

  const fetchFiles = () => {
    filesPromise = getFilesCalendar()
  }

  const submitCalendar = () => {
    if (year && month) {
      date = new Date(year, month - 1)
    }
  }

  const week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

  const getWeek = () => {
    return [...week.slice(first), ...week.slice(0, first)]
  }

  const nextMonth = () => {
    if (date) {
      date = addMonths(date, 1)
    }
  }

  const previousMonth = () => {
    if (date) {
      date = subMonths(date, 1)
    }
  }

  $effect(() => {
    if (date) {
      calendarPromise = getCalendar({
        filename: untrack(() => filename),
        year: getYear(date),
        month: getMonth(date) + 1,
      })
    }
  })
</script>

<Container>
  <button onclick={fetchFiles}>refresh files</button>
</Container>

{#await filesPromise}
  <p>loading...</p>
{:then files}
  <Container>
    <select class="mb-1" bind:value={filename}>
      <option value="" selected disabled>select file</option>
      {#each files.sort() as file}
        <option value={file}>{file.replace(/^out\//, "")}</option>
      {/each}
    </select>
    <div class="mb-1 flex justify-between">
      <input
        type="number"
        class="mr-1"
        placeholder="year"
        min="1000"
        max="3000"
        bind:value={year}
      />
      <input
        type="number"
        placeholder="month"
        min="1"
        max="12"
        bind:value={month}
      />
    </div>
    <button disabled={submitDisabled} onclick={submitCalendar}>submit</button>
  </Container>
{:catch e}
  <Container>
    <Alert type="error">
      <p>{e.message}</p>
    </Alert>
  </Container>
{/await}

{#if calendarPromise && date}
  {#await calendarPromise}
    <p>loading...</p>
  {:then calendar}
    <Container>
      <div class="mb-1 flex justify-between">
        <button onclick={previousMonth}>previous month</button>
        <div>{`${getYear(date)}-${getMonth(date) + 1}`}</div>
        <button onclick={nextMonth}>next month</button>
      </div>
      <table
        class="w-full table-fixed break-words border rounded border-gray-300 border-separate border-spacing-0 overflow-hidden"
      >
        <thead>
          <tr>
            {#each getWeek() as week}
              <th class="p-2 border-r border-gray-300 last:border-r-0">
                {week}
              </th>
            {/each}
          </tr>
        </thead>
        <tbody>
          {#each calendar as week}
            <tr class="group">
              {#each week as day}
                {@const weekday = getDay(day.date)}
                <td
                  class="p-2 border-r border-t border-gray-300 group-first:border-t-2 last:border-r-0 text-center"
                  class:bg-gray-200={!day.obs}
                  class:text-blue-500={weekday === 6}
                  class:text-red-500={weekday === 0}
                >
                  <span class:opacity-40={!isSameMonth(day.date, date)}>
                    {getDate(day.date)}
                  </span>
                </td>
              {/each}
            </tr>
          {/each}
        </tbody>
      </table>
    </Container>
  {:catch e}
    <Container>
      <Alert type="error">
        <p>{e instanceof FetchError ? e.detail : e.message}</p>
      </Alert>
    </Container>
  {/await}
{/if}
