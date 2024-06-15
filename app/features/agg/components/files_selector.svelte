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

<Accordion>
  {#snippet summary()}
    <span>filter</span>
  {/snippet}
  <input class="pure-input-1 filter-input" bind:value={filter} />
  <button class="pure-button" onclick={filterApply}>apply</button>
  <button class="pure-button" onclick={filterClear}>clear</button>
</Accordion>

{#if filtered.length === 0}
  <Alert severity="warning">
    <p>no files matched</p>
  </Alert>
{:else}
  <div>
    <button class="pure-button" onclick={selectAll}>select all files</button>
    <button class="pure-button" onclick={deselectAll}>deselect all files</button
    >
  </div>

  <div class="pure-u-1 scroll-box">
    {#each filtered as file}
      <label>
        <input type="checkbox" bind:group={checked} value={file} />
        <span class="file-name">{file.replace(/^data\//, "")}</span>
      </label>
    {/each}
  </div>
{/if}

<style>
  .filter-input {
    margin-top: 0 !important;
  }
  .scroll-box {
    box-sizing: border-box;
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 0 1rem;
    margin: 0.25rem 0;
    max-height: 32rem;
    overflow-y: auto;
  }
  .file-name {
    margin: 0.5rem;
  }
</style>
