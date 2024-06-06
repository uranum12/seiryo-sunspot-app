<script lang="ts">
  import { FetchError, get, post } from "@/utils/fetch"

  let selected: string[] = []
  let filename = ""

  let submitDisabled: boolean
  $: submitDisabled = selected.length === 0 || filename.trim() === ""

  const getFiles = async (): Promise<string[]> => {
    const res = await get<{ files: string[] }, { path: string; glob: string }>(
      "/api/utils/files",
      { path: "data", glob: "*.csv" }
    )
    return res.files.sort()
  }

  const postAgg = async (): Promise<string> => {
    const res = await post<
      { output: string },
      { files: string[]; filename: string }
    >("/api/agg", { files: selected, filename: filename })
    return res.output
  }

  let filesPromise: Promise<string[]> = getFiles()
  let aggPromise: Promise<string> | undefined = undefined

  const fetchFiles = () => {
    selected = []
    filename = ""
    aggPromise = undefined
    filesPromise = getFiles()
  }

  const submitAgg = () => {
    aggPromise = postAgg()
  }
</script>

{#await filesPromise}
  <p>loading...</p>
{:then files}
  {#if files.length !== 0}
    <div class="container">
      <button class="pure-button" on:click={fetchFiles}>refresh files</button>
      <button
        class="pure-button"
        on:click={() => {
          selected = files
        }}>select all files</button
      >
      <button
        class="pure-button"
        on:click={() => {
          selected = []
        }}>deselect all files</button
      >
    </div>
    <div class="container">
      <div class="pure-u-1 pure-u-sm-2-3 pure-u-md-1-2">
        <form
          class="pure-form pure-form-stacked pure-g"
          on:submit|preventDefault={submitAgg}
        >
          <div class="pure-u-1 border scroll-list">
            {#each files as file}
              <label class="pure-checkbox">
                <input type="checkbox" bind:group={selected} value={file} />
                <span class="file-name">{file.replace("data/", "")}</span>
              </label>
            {/each}
          </div>
          <input
            placeholder="Output File Name"
            required
            class="pure-input-1"
            bind:value={filename}
          />
          <button type="submit" class="pure-button" disabled={submitDisabled}
            >Submit</button
          >
        </form>
      </div>
    </div>
  {:else}
    <div class="container">
      <button class="pure-button" on:click={fetchFiles}
        >retry fetch files</button
      >
    </div>
    <div class="container">
      <div class="border warning">
        <p>no files</p>
      </div>
    </div>
  {/if}
{:catch e}
  <div class="container">
    <button class="pure-button" on:click={fetchFiles}>retry fetch files</button>
  </div>
  <div class="container">
    <div class="border error">
      <p>{e.message}</p>
    </div>
  </div>
{/await}

{#if aggPromise}
  {#await aggPromise}
    <p>loading...</p>
  {:then output}
    <div class="container">
      <div class="border success">
        <p>file {output} generated</p>
      </div>
    </div>
  {:catch e}
    {#if e instanceof FetchError}
      <div class="container">
        <div class="border error">
          <p>{e.detail}</p>
        </div>
      </div>
    {:else}
      <div class="container">
        <div class="border error">
          <p>{e.message}</p>
        </div>
      </div>
    {/if}
  {/await}
{/if}

<style>
  .file-name {
    margin: 0.5rem;
  }
</style>
