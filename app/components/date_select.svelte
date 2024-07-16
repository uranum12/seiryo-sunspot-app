<script lang="ts">
  import { formatDate, toDate, validateDate } from "@/utils/date"

  type Props = {
    date: string | undefined
    required?: boolean
    dayHidden?: boolean
  }

  let {
    date = $bindable(),
    required = false,
    dayHidden: hidden = false,
  }: Props = $props()

  let year = $state<number>()
  let month = $state<number>()
  let day = $state<number | undefined>(hidden ? 1 : undefined)

  $effect(() => {
    if (year && month && day) {
      if (validateDate(year, month, day)) {
        date = formatDate(toDate(year, month, day))
      } else {
        date = undefined
      }
    }
  })
</script>

<div class="flex justify-between gap-x-1">
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
    {hidden}
    bind:value={day}
  />
</div>
