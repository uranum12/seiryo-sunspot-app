<script lang="ts">
  import { getDate, getMonth, getYear } from "date-fns"

  type Props = {
    date: string | undefined
    class?: string
    required?: boolean
  }

  let {
    date = $bindable(),
    class: className,
    required = false,
  }: Props = $props()

  let year = $state<number>()
  let month = $state<number>()
  let day = $state<number>()

  const validateDate = (year: number, month: number, day: number) => {
    const dt = new Date(year, month - 1, day)
    return (
      getYear(dt) === year && getMonth(dt) === month - 1 && getDate(dt) === day
    )
  }

  $effect(() => {
    if (year && month && day) {
      if (validateDate(year, month, day)) {
        date = `${year}-${month.toString().padStart(2, "0")}-${day.toString().padStart(2, "0")}`
      } else {
        date = undefined
      }
    }
  })
</script>

<div class="{className} flex justify-between">
  <input
    type="number"
    min="1000"
    max="3000"
    placeholder="year"
    {required}
    bind:value={year}
  />
  <input
    type="number"
    class="mx-1"
    min="1"
    max="12"
    placeholder="month"
    {required}
    bind:value={month}
  />
  <input
    type="number"
    min="1"
    max="31"
    placeholder="day"
    {required}
    bind:value={day}
  />
</div>
