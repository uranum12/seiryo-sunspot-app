<script lang="ts">
  import {
    addMonths,
    getDate,
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
  <button class="pure-button" onclick={fetchFiles}>refresh files</button>
</Container>

{#await filesPromise}
  <p>loading...</p>
{:then files}
  <Container>
    <div class="pure-form pure-form-stacked">
      <select class="pure-input-1" bind:value={filename}>
        <option value="" selected disabled>select file</option>
        {#each files.sort() as file}
          <option value={file}>{file.replace(/^out\//, "")}</option>
        {/each}
      </select>
      <input
        type="number"
        class="pure-input-1"
        placeholder="year"
        min="1000"
        max="3000"
        bind:value={year}
      />
      <input
        type="number"
        class="pure-input-1"
        placeholder="month"
        min="1"
        max="12"
        bind:value={month}
      />
      <button
        class="pure-button"
        disabled={submitDisabled}
        onclick={submitCalendar}
      >
        submit
      </button>
    </div>
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
      <div class="calendar-nav">
        <button class="pure-button" onclick={previousMonth}>
          previous month
        </button>
        <div>{`${getYear(date)}-${getMonth(date) + 1}`}</div>
        <button class="pure-button" onclick={nextMonth}>next month</button>
      </div>
      <table class="pure-table pure-table-bordered">
        <thead>
          <tr>
            {#each getWeek() as week}
              <th>{week}</th>
            {/each}
          </tr>
        </thead>
        <tbody>
          {#each calendar as week}
            <tr>
              {#each week as day}
                <td
                  class:not-observed={!day.obs}
                  class:saturday={isSaturday(day.date)}
                  class:sunday={isSunday(day.date)}
                >
                  <span class:out-of-month={!isSameMonth(day.date, date)}>
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

<style>
  table {
    width: 100%;
    table-layout: fixed;
    overflow-wrap: break-word;
  }

  .calendar-nav {
    margin-bottom: 4px;
    display: flex;
    justify-content: space-between;
  }

  .not-observed {
    background-color: lightgray;
  }

  .saturday {
    color: blue;
  }

  .sunday {
    color: red;
  }

  .out-of-month {
    opacity: 0.4;
  }
</style>
