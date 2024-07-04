<script lang="ts">
  type Props = {
    interval: string | undefined
    required?: boolean
  }

  let { interval = $bindable(), required }: Props = $props()

  let years = $state<string>()
  let months = $state<string>()
  let days = $state<string>()

  $effect(() => {
    if (years || months || days) {
      const yearsString = years ? `${years}Y` : ""
      const monthsString = months ? `${months}M` : ""
      const daysString = days ? `${days}D` : ""
      interval = `P${yearsString}${monthsString}${daysString}`
    } else {
      interval = undefined
    }
  })
</script>

<div class="flex justify-content">
  <input
    type="number"
    min="1"
    placeholder="years"
    {required}
    bind:value={years}
  />
  <input
    type="number"
    class="mx-1"
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
