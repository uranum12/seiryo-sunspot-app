<script lang="ts">
  import Accordion from "./accordion.svelte"

  type Props = {
    filter: string
  }

  let { filter = $bindable() }: Props = $props()

  let filterInput = $state<string>("")

  const filterApply = () => {
    filter = filterInput
  }

  const filterClear = () => {
    filterInput = ""
    filterApply()
  }
</script>

<Accordion summary="filter">
  <input bind:value={filterInput} class="mb-1" />
  <button onclick={filterApply}>apply</button>
  <button onclick={filterClear}>clear</button>
</Accordion>
