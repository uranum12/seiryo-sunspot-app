<script lang="ts">
  import Accordion from "./accordion.svelte"

  type Props = {
    class?: string
    filter: string
  }

  let { class: className, filter = $bindable() }: Props = $props()

  let filterInput = $state<string>("")

  const filterApply = () => {
    filter = filterInput
  }

  const filterClear = () => {
    filterInput = ""
    filterApply()
  }
</script>

<Accordion class={className} summary="filter">
  <input bind:value={filterInput} class="mb-1" />
  <button onclick={filterApply}>apply</button>
  <button onclick={filterClear}>clear</button>
</Accordion>
