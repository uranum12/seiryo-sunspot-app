<script lang="ts">
  import Alert from "@/components/alert.svelte"
  import ConfirmDialog from "@/components/confirm_dialog.svelte"
  import Container from "@/components/container.svelte"
  import ScrollBox from "@/components/scroll_box.svelte"
  import { FetchError, get, post } from "@/utils/fetch"

  let selected: string[] = []
  let filename = ""
  let overwrite = false

  let showConfirmOverwrite = false

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
      { files: string[]; filename: string; overwrite: boolean }
    >("/api/agg", { files: selected, filename: filename, overwrite: overwrite })
    return res.output
  }

  let filesPromise: Promise<string[]> = getFiles()
  let aggPromise: Promise<string> | undefined

  const fetchFiles = () => {
    selected = []
    filename = ""
    overwrite = false
    aggPromise = undefined
    filesPromise = getFiles()
  }

  const submitAgg = () => {
    if (overwrite) {
      aggPromise = undefined
      showConfirmOverwrite = true
    } else {
      aggPromise = postAgg()
    }
  }

  const okOverwrite = () => {
    aggPromise = postAgg()
  }
</script>

{#await filesPromise}
  <p>loading...</p>
{:then files}
  {#if files.length !== 0}
    <Container>
      <button class="pure-button" on:click={fetchFiles}>refresh files</button>
      <button class="pure-button" on:click={() => (selected = files)}
        >select all files</button
      >
      <button class="pure-button" on:click={() => (selected = [])}
        >deselect all files</button
      >
    </Container>
    <Container>
      <div class="pure-u-1 pure-u-sm-2-3 pure-u-md-1-2">
        <form
          class="pure-form pure-form-stacked pure-g"
          on:submit|preventDefault={submitAgg}
        >
          <div class="pure-u-1">
            <ScrollBox>
              {#each files as file}
                <label class="pure-checkbox">
                  <input type="checkbox" bind:group={selected} value={file} />
                  <span class="file-name">{file.replace("data/", "")}</span>
                </label>
              {/each}
            </ScrollBox>
          </div>
          <input
            placeholder="Output File Name"
            required
            class="pure-input-1"
            bind:value={filename}
          />
          <label class="pure-checkbox pure-u-1">
            <input type="checkbox" bind:checked={overwrite} />
            <span>Overwrite</span>
          </label>
          <button type="submit" class="pure-button" disabled={submitDisabled}
            >Submit</button
          >
        </form>
      </div>
    </Container>
    <ConfirmDialog bind:isOpen={showConfirmOverwrite} on:ok={okOverwrite}>
      Are you sure you want me to overwrite file {filename}.parquet ?
    </ConfirmDialog>
  {:else}
    <Container>
      <button class="pure-button" on:click={fetchFiles}
        >retry fetch files</button
      >
    </Container>
    <Container>
      <Alert severity="warning">
        <p>no files</p>
      </Alert>
    </Container>
  {/if}
{:catch e}
  <Container>
    <button class="pure-button" on:click={fetchFiles}>retry fetch files</button>
  </Container>
  <Container>
    <Alert severity="error">
      <p>{e.message}</p>
    </Alert>
  </Container>
{/await}

{#if aggPromise}
  {#await aggPromise}
    <p>loading...</p>
  {:then output}
    <Container>
      <Alert severity="success">
        <p>file {output} generated</p>
      </Alert>
    </Container>
  {:catch e}
    <Container>
      <Alert severity="error">
        <p>{e instanceof FetchError ? e.detail : e.message}</p>
      </Alert>
    </Container>
  {/await}
{/if}

<style>
  .file-name {
    margin: 0.5rem;
  }
</style>
