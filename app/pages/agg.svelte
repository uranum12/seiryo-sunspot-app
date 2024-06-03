<script lang="ts">
  import axios, { type AxiosError } from "axios"
  import { onMount } from "svelte"

  type File = {
    name: string
    path: string
    select: boolean
  }

  let files: File[] = []
  let filename = ""
  let loading = false
  let submitDisabled: boolean
  let output = ""
  let error = ""

  $: submitDisabled =
    files.filter((file) => file.select).length === 0 || filename === ""

  const getFiles = () => {
    files = []
    filename = ""
    loading = true
    output = ""
    error = ""
    axios
      .get<{ files: string[] }>("/api/utils/files", {
        params: { path: "data", glob: "*.csv" },
      })
      .then((res) => {
        const paths = res.data.files
        files = paths.sort().map((path) => ({
          name: path.replace("data/", ""),
          path: path,
          select: false,
        }))
      })
      .catch((e: AxiosError) => {
        error = e.message
      })
      .finally(() => {
        loading = false
      })
  }

  const selectAllFiles = () => {
    files = files.map((file) => ({ ...file, select: true }))
  }

  const deselectAllFiles = () => {
    files = files.map((file) => ({ ...file, select: false }))
  }

  const submitFiles = () => {
    axios
      .post<{ output: string }>("/api/agg", {
        files: files.filter((file) => file.select).map((file) => file.path),
        filename: filename,
      })
      .then((res) => {
        output = res.data.output
        error = ""
      })
      .catch((e: AxiosError<{ detail: string }>) => {
        if (e.response) {
          error = e.response.data.detail
        } else {
          error = e.message
        }
      })
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
  {#if loading}
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
              <input type="checkbox" bind:checked={file.select} />
              <span class="file-name">{file.name}</span>
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
