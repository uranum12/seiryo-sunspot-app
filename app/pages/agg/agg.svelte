<script lang="ts">
  import { postAgg } from "@/api/agg/agg"
  import { getFiles } from "@/api/files"
  import Alert from "@/components/alert.svelte"
  import ConfirmDialog from "@/components/confirm_dialog.svelte"
  import FileSelect from "@/components/file_select.svelte"
  import { FetchError } from "@/utils/fetch"

  let selected = $state<string[]>([])
  let filename = $state<string>("")
  let overwrite = $state<boolean>(false)

  let showConfirmOverwrite = $state<boolean>(false)

  const submitDisabled = $derived(
    selected.length === 0 || filename.trim() === ""
  )

  const getFilesAgg = () => {
    return getFiles({ path: "data", glob: "*.csv" })
  }

  let filesPromise = $state<ReturnType<typeof getFiles>>(getFilesAgg())
  let aggPromise = $state<ReturnType<typeof postAgg> | undefined>(undefined)

  const fetchFiles = () => {
    aggPromise = undefined
    filesPromise = getFilesAgg()
  }

  const submitAgg = () => {
    aggPromise = postAgg({
      files: selected,
      filename,
      overwrite,
    })
  }

  const clickSubmit = () => {
    if (overwrite) {
      showConfirmOverwrite = true
    } else {
      submitAgg()
    }
  }
</script>

<section>
  <button onclick={fetchFiles}>refresh files</button>
</section>

{#await filesPromise}
  <p>loading...</p>
{:then files}
  {#if files.length !== 0}
    <section class="space-y-1">
      <FileSelect {files} bind:selected />
      <input placeholder="output file name" required bind:value={filename} />
      <label>
        <input type="checkbox" bind:checked={overwrite} />
        <span>Overwrite</span>
      </label>
      <button disabled={submitDisabled} onclick={clickSubmit}>submit</button>
    </section>

    <ConfirmDialog bind:isOpen={showConfirmOverwrite} onConfirm={submitAgg}>
      Are you sure you want me to overwrite file {filename}.parquet ?
    </ConfirmDialog>
  {:else}
    <section>
      <Alert type="warning">
        <p>no files</p>
      </Alert>
    </section>
  {/if}
{:catch e}
  <section>
    <Alert type="error">
      <p>{e.message}</p>
    </Alert>
  </section>
{/await}

{#if aggPromise}
  {#await aggPromise}
    <p>loading...</p>
  {:then output}
    <section>
      <Alert type="success">
        <p>file {output} generated</p>
      </Alert>
    </section>
  {:catch e}
    <section>
      <Alert type="error">
        <p>{e instanceof FetchError ? e.detail : e.message}</p>
      </Alert>
    </section>
  {/await}
{/if}
