<script lang="ts">
  import { untrack } from "svelte"

  import Accordion from "@/components/accordion.svelte"
  import Alert from "@/components/alert.svelte"

  type Props = {
    class?: string
    files: string[]
    selected: string[]
  }

  let { class: className, files, selected = $bindable() }: Props = $props()

  let filtered = $state<string[]>(files.sort())
  let checked = $state<string[]>([])
  let filter = $state<string>("")

  const hidden = $derived(files.filter((file) => !filtered.includes(file)))
  const fileSelectInvalid = $derived(selected.length === 0)

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

<div class="{className} space-y-1">
  <Accordion summary="filter">
    <input bind:value={filter} class="mb-1" />
    <button onclick={filterApply}>apply</button>
    <button onclick={filterClear}>clear</button>
  </Accordion>

  {#if filtered.length === 0}
    <Alert type="warning">
      <p>no files matched</p>
    </Alert>
  {:else}
    <div>
      <button onclick={selectAll}>select all files</button>
      <button onclick={deselectAll}>deselect all files</button>
    </div>

    <div
      class="max-h-96 overflow-y-auto rounded border border-gray-300 p-2"
      class:!border-red-300={fileSelectInvalid}
    >
      {#each filtered as file}
        <label>
          <input type="checkbox" bind:group={checked} value={file} />
          <span class="ml-1">{file.replace(/^data\//, "")}</span>
        </label>
      {/each}
    </div>
  {/if}
</div>
