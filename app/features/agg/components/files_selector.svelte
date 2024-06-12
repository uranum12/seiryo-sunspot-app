<script lang="ts">
  import Accordion from "@/components/accordion.svelte"
  import Alert from "@/components/alert.svelte"

  export let files: string[]
  export let selected: string[]

  let filtered: string[] = files.sort()
  let filter = ""

  const filterApply = () => {
    filtered = files.filter((file) =>
      file.replace(/^data\//, "").includes(filter)
    )
  }

  const filterClear = () => {
    filter = ""
    filterApply()
  }

  const selectAll = () => {
    selected = selected.concat(filtered)
  }

  const deselectAll = () => {
    selected = selected.filter((file) => !filtered.includes(file))
  }
</script>

<Accordion>
  <span slot="summary">filter</span>
  <input class="pure-input-1 filter-input" bind:value={filter} />
  <button class="pure-button" on:click={filterApply}>apply</button>
  <button class="pure-button" on:click={filterClear}>clear</button>
</Accordion>

{#if filtered.length === 0}
  <Alert severity="warning">
    <p>no files matched</p>
  </Alert>
{:else}
  <div>
    <button class="pure-button" on:click={selectAll}>select all files</button>
    <button class="pure-button" on:click={deselectAll}
      >deselect all files</button
    >
  </div>

  <div class="pure-u-1 scroll-box">
    {#each filtered as file}
      <label>
        <input type="checkbox" bind:group={selected} value={file} />
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
