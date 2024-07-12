<script lang="ts">
  import { postImage } from "@/api/butterfly/image"
  import { getFiles } from "@/api/files"
  import Alert from "@/components/alert.svelte"
  import ConfirmDialog from "@/components/confirm_dialog.svelte"
  import { FetchError } from "@/utils/fetch"

  let inputName = $state<string>("")
  let overwrite = $state<boolean>(false)

  let showConfirmOverwrite = $state<boolean>(false)

  const submitDisabled = $derived<boolean>(inputName.trim() === "")

  const getFilesImage = () => {
    return getFiles({ path: "out/butterfly", glob: "*.parquet" })
  }

  let filesPromise = $state<ReturnType<typeof getFiles>>(getFilesImage())
  let imagePromise = $state<ReturnType<typeof postImage>>()

  const fetchFiles = () => {
    imagePromise = undefined
    filesPromise = getFilesImage()
  }

  const submitImage = () => {
    imagePromise = postImage({ inputName, overwrite })
  }

  const clickSubmit = () => {
    if (overwrite) {
      showConfirmOverwrite = true
    } else {
      submitImage()
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
      <select required bind:value={inputName}>
        <option value="" selected disabled>select file</option>
        {#each files.sort() as file}
          <option value={file}>{file.replace(/^out\//, "")}</option>
        {/each}
      </select>
      <label>
        <input type="checkbox" bind:checked={overwrite} />
        <span>Overwrite</span>
      </label>
      <button disabled={submitDisabled} onclick={clickSubmit}>submit</button>
    </section>

    <ConfirmDialog bind:isOpen={showConfirmOverwrite} onConfirm={submitImage}>
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

{#if imagePromise}
  {#await imagePromise}
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
