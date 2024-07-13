<script lang="ts">
  import { postMerge } from "@/api/butterfly/merge"
  import { getFiles } from "@/api/files"
  import Alert from "@/components/alert.svelte"
  import ConfirmDialog from "@/components/confirm_dialog.svelte"
  import OrderedFileSelect from "@/components/ordered_file_select.svelte"
  import { FetchError } from "@/utils/fetch"

  let inputNames = $state<string[]>([])
  let outputName = $state<string>("")
  let overwrite = $state<boolean>(false)

  let showConfirmOverwrite = $state<boolean>(false)

  const submitDisabled = $derived<boolean>(
    inputNames.length === 0 || outputName.trim() === ""
  )

  const getFilesMerge = () => {
    return getFiles({ path: "out/butterfly", glob: "*.parquet" })
  }

  let filesPromise = $state<ReturnType<typeof getFiles>>(getFilesMerge())
  let mergePromise = $state<ReturnType<typeof postMerge>>()

  const fetchFiles = () => {
    mergePromise = undefined
    filesPromise = getFilesMerge()
  }

  const submitMerge = () => {
    mergePromise = postMerge({
      inputNames,
      outputName,
      overwrite,
    })
  }

  const clickSubmit = () => {
    if (overwrite) {
      showConfirmOverwrite = true
    } else {
      submitMerge()
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
      <OrderedFileSelect {files} bind:selected={inputNames} />
      <input placeholder="output file name" required bind:value={outputName} />
      <label>
        <input type="checkbox" bind:checked={overwrite} />
        <span>Overwrite</span>
      </label>
      <button disabled={submitDisabled} onclick={clickSubmit}>submit</button>
    </section>

    <ConfirmDialog bind:isOpen={showConfirmOverwrite} onConfirm={submitMerge}>
      Are you sure you want me to overwrite file ?
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

{#if mergePromise}
  {#await mergePromise}
    <p>loading...</p>
  {:then output}
    <section>
      <Alert type="success">
        <p>file {output.outputInfo} generated</p>
        <p>file {output.outputImg} generated</p>
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
