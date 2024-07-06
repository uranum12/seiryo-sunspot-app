<script lang="ts">
  import {
    addMonths,
    getDate,
    getDay,
    getMonth,
    getYear,
    isSameMonth,
    subMonths,
  } from "date-fns"
  import { untrack } from "svelte"

  import Alert from "@/components/alert.svelte"
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

  const submitDisabled = $derived(filename.trim() === "" || !year || !month)

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

<section>
  <button onclick={fetchFiles}>refresh files</button>
</section>

{#await filesPromise}
  <p>loading...</p>
{:then files}
  <section>
    <select class="mb-1" required bind:value={filename}>
      <option value="" selected disabled>select file</option>
      {#each files.sort() as file}
        <option value={file}>{file.replace(/^out\//, "")}</option>
      {/each}
    </select>
    <div class="mb-1 flex justify-between">
      <input
        type="number"
        class="mr-1"
        required
        placeholder="year"
        min="1000"
        max="3000"
        bind:value={year}
      />
      <input
        type="number"
        required
        placeholder="month"
        min="1"
        max="12"
        bind:value={month}
      />
    </div>
    <button disabled={submitDisabled} onclick={submitCalendar}>submit</button>
  </section>
{:catch e}
  <section>
    <Alert type="error">
      <p>{e.message}</p>
    </Alert>
  </section>
{/await}

{#if calendarPromise && date}
  {#await calendarPromise}
    <p>loading...</p>
  {:then calendar}
    <section>
      <div class="mb-1 flex justify-between">
        <button onclick={previousMonth}>previous month</button>
        <div>{`${getYear(date)}-${getMonth(date) + 1}`}</div>
        <button onclick={nextMonth}>next month</button>
      </div>
      <table
        class="w-full table-fixed border-separate border-spacing-0 overflow-hidden break-words rounded border border-gray-300"
      >
        <thead>
          <tr>
            {#each getWeek() as week}
              <th class="border-r border-gray-300 p-2 last:border-r-0">
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
                  class="border-r border-t border-gray-300 p-2 text-center last:border-r-0 group-first:border-t-2"
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
    </section>
  {:catch e}
    <section>
      <Alert type="error">
        <p>{e instanceof FetchError ? e.detail : e.message}</p>
      </Alert>
    </section>
  {/await}
{/if}
