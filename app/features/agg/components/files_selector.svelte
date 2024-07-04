<script lang="ts">
  import { untrack } from "svelte"

  import Accordion from "@/components/accordion.svelte"
  import Alert from "@/components/alert.svelte"

  type Props = {
    files: string[]
    selected: string[]
  }

  let { files, selected = $bindable() }: Props = $props()

  let filtered = $state<string[]>(files.sort())
  let checked = $state<string[]>([])
  let filter = $state<string>("")

  const hidden = $derived(files.filter((file) => !filtered.includes(file)))

  $effect(() => {
    selected = untrack<string[]>(() => selected)
      .filter((file) => hidden.includes(file))
      .concat(checked)
  })

  const filterApply = () => {
    filtered = files.filter((file) =>
      file.replace(/^data\//, "").includes(filter)
    )
    checked = selected.filter((file) => filtered.includes(file))
  }

  const filterClear = () => {
    filter = ""
    filterApply()
  }

  const selectAll = () => {
    checked = filtered
  }

  const deselectAll = () => {
    checked = []
  }
</script>

<Accordion class="mb-1" summary="filter">
  <input bind:value={filter} class="mb-1" />
  <button onclick={filterApply}>apply</button>
  <button onclick={filterClear}>clear</button>
</Accordion>

{#if filtered.length === 0}
  <Alert type="warning">
    <p>no files matched</p>
  </Alert>
{:else}
  <div class="mb-1">
    <button onclick={selectAll}>select all files</button>
    <button onclick={deselectAll}>deselect all files</button>
  </div>

  <div class="p-2 border rounded border-gray-300 overflow-y-auto max-h-96">
    {#each filtered as file}
      <label>
        <input type="checkbox" bind:group={checked} value={file} />
        <span class="ml-1">{file.replace(/^data\//, "")}</span>
      </label>
    {/each}
  </div>
{/if}
