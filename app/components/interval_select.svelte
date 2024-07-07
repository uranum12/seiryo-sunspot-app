<script lang="ts">
  import { formatDuration } from "@/utils/date"

  type Props = {
    interval: string | undefined
    required?: boolean
  }

  let { interval = $bindable(), required }: Props = $props()

  let years = $state<number>()
  let months = $state<number>()
  let days = $state<number>()

  $effect(() => {
    if (years || months || days) {
      interval = formatDuration(years, months, days)
    } else {
      interval = undefined
    }
  })
</script>

<div class="justify-content flex gap-x-1">
  <input
    type="number"
    min="1"
    placeholder="years"
    {required}
    bind:value={years}
  />
  <input
    type="number"
    min="1"
    placeholder="months"
    {required}
    bind:value={months}
  />
  <input
    type="number"
    min="1"
    placeholder="days"
    {required}
    bind:value={days}
  />
</div>
