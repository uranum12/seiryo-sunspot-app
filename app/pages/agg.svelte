<script lang="ts">
  import { onMount } from "svelte"

  import { FetchError, get, post } from "@/utils/fetch"

  let files: string[] = []
  let selected: string[] = []
  let filename = ""
  let loadingFiles = false
  let submitDisabled: boolean
  let output = ""
  let error = ""
  let loadingAgg = false

  $: submitDisabled = selected.length === 0 || filename === ""

  const getFiles = () => {
    files = []
    selected = []
    filename = ""
    loadingFiles = true
    output = ""
    error = ""
    get<{ files: string[] }, { path: string; glob: string }>(
      "/api/utils/files",
      { path: "data", glob: "*.csv" }
    )
      .then((res) => {
        files = res.files.sort()
      })
      .catch((e) => {
        error = e.message
      })
      .finally(() => {
        loadingFiles = false
      })
    // axios
    //   .get<{ files: string[] }>("/api/utils/files", {
    //     params: { path: "data", glob: "*.csv" },
    //   })
    //   .then((res) => {
    //     files = res.data.files.sort()
    //   })
    //   .catch((e: AxiosError) => {
    //     error = e.message
    //   })
    //   .finally(() => {
    //     loadingFiles = false
    //   })
  }

  const selectAllFiles = () => {
    selected = files
  }

  const deselectAllFiles = () => {
    selected = []
  }

  const submitFiles = () => {
    loadingAgg = true
    post<{ files: string[]; filename: string }, { output: string }>(
      "/api/agg",
      { files: selected, filename: filename }
    )
      .then((res) => {
        output = res.output
        error = ""
      })
      .catch((e) => {
        if (e instanceof FetchError) {
          error = e.detail
        } else {
          error = e.message
        }
      })
      .finally(() => {
        loadingAgg = false
      })
    // axios
    //   .post<{ output: string }>("/api/agg", {
    //     files: selected,
    //     filename: filename,
    //   })
    //   .then((res) => {
    //     output = res.data.output
    //     error = ""
    //   })
    //   .catch((e: AxiosError<{ detail: string }>) => {
    //     if (e.response) {
    //       error = e.response.data.detail
    //     } else {
    //       error = e.message
    //     }
    //   })
    //   .finally(() => {
    //     loadingAgg = false
    //   })
  }

  onMount(getFiles)
</script>

<div class="container">
  <button class="pure-button" on:click={getFiles}>refresh files</button>
  {#if files.length !== 0}
    <button class="pure-button" on:click={selectAllFiles}
      >select all files</button
    >
    <button class="pure-button" on:click={deselectAllFiles}
      >deselect all files</button
    >
  {/if}
</div>

<div class="container">
  {#if loadingFiles}
    <p>loading...</p>
  {:else if files.length === 0}
    <div class="border warning">
      <p>no files</p>
    </div>
  {:else}
    <form
      class="pure-form pure-form-stacked pure-g"
      on:submit|preventDefault={submitFiles}
    >
      <div class="pure-u-1 pure-u-sm-2-3 pure-u-md-1-2">
        <div class="border scroll-list">
          {#each files as file}
            <label class="pure-checkbox">
              <input type="checkbox" bind:group={selected} value={file} />
              <span class="file-name">{file.replace("data/", "")}</span>
            </label>
          {/each}
        </div>
        <input
          placeholder="output file name"
          required
          class="pure-input-1"
          bind:value={filename}
        />
        <button class="pure-button" disabled={submitDisabled}>submit</button>
      </div>
    </form>
  {/if}
</div>

{#if loadingAgg}
  <p>loading...</p>
{/if}

{#if output !== ""}
  <div class="container border success">
    <p>file {output} generated</p>
  </div>
{/if}

{#if error !== ""}
  <div class="container border error">
    <p>{error}</p>
  </div>
{/if}

<style>
  .file-name {
    margin: 0.5rem;
  }
</style>
