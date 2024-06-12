<script lang="ts">
  import Alert from "@/components/alert.svelte"

  export let files: string[]
  export let selected: string[]

  const selectAll = () => {
    selected = files
  }

  const deselectAll = () => {
    selected = []
  }
</script>

{#if files.length === 0}
  <Alert severity="warning">
    <p>no files</p>
  </Alert>
{:else}
  <div>
    <button class="pure-button" on:click={selectAll}>select all files</button>
    <button class="pure-button" on:click={deselectAll}
      >deselect all files</button
    >
  </div>

  <div class="pure-u-1 scroll-box">
    {#each files.sort() as file}
      <label>
        <input type="checkbox" bind:group={selected} value={file} />
        <span class="file-name">{file.replace(/^data\//, "")}</span>
      </label>
    {/each}
  </div>
{/if}

<style>
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
