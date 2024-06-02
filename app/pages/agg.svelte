<script lang="ts">
import axios, { type AxiosError, type AxiosResponse } from "axios"
import { onMount } from "svelte"

interface File {
  name: string
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
    .get("/api/agg/files")
    .then((res: AxiosResponse<{ files: string[] }>) => {
      const names = res.data.files
      files = names.sort().map((name) => ({ name: name, select: false }))
    })
    .catch((e: AxiosError) => {
      error = e.message
    })
    .finally(() => {
      loading = false
    })
}

const selectAllFiles = () => {
  files = files.map((file) => ({ name: file.name, select: true }))
}

const deselectAllFiles = () => {
  files = files.map((file) => ({ name: file.name, select: false }))
}

const submitFiles = async (e: Event) => {
  e.preventDefault()
  axios
    .post("/api/agg", {
      files: files.filter((file) => file.select).map((file) => file.name),
      filename: filename,
    })
    .then((res: AxiosResponse<{ output: string }>) => {
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
    <form class="pure-form pure-form-stacked pure-g" on:submit={submitFiles}>
      <div class="pure-u-1 pure-u-sm-2-3 pure-u-md-1-2">
        <div class="scroll-list">
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
