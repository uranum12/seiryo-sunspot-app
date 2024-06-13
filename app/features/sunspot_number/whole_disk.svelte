<script lang="ts">
  import { onMount } from "svelte"

  import Alert from "@/components/alert.svelte"
  import Container from "@/components/container.svelte"
  import { FetchError } from "@/utils/fetch"

  import { getFilesDraw } from "./api/files"
  import { getDraw, postDraw } from "./api/whole_disk"
  import PreviewForm, {
    type FormInput as PreviewFormInput,
  } from "./components/preview_form.svelte"
  import SaveForm, {
    type FormInput as SaveFormInput,
  } from "./components/save_form.svelte"

  let filename = ""

  let filesPromise: ReturnType<typeof getFilesDraw>
  let previewPromise: ReturnType<typeof getDraw> | undefined
  let savePromise: ReturnType<typeof postDraw> | undefined

  const fetchFiles = () => {
    previewPromise = undefined
    savePromise = undefined
    filesPromise = getFilesDraw()
  }

  const fetchPreview = (e: CustomEvent<PreviewFormInput>) => {
    savePromise = undefined
    filename = e.detail.filename
    previewPromise = getDraw(e.detail)
  }

  const submitSave = (e: CustomEvent<SaveFormInput>) => {
    savePromise = postDraw({ input: filename, ...e.detail })
  }

  onMount(fetchFiles)
</script>

<Container>
  <button class="pure-button" on:click={fetchFiles}>refresh files</button>
</Container>

{#if filesPromise}
  {#await filesPromise}
    <p>loading...</p>
  {:then files}
    {#if files.length !== 0}
      <PreviewForm {files} on:submit={fetchPreview} />
    {:else}
      <Container>
        <Alert severity="warning">
          <p>no files</p>
        </Alert>
      </Container>
    {/if}
  {:catch e}
    <Container>
      <Alert severity="error">
        <p>{e.message}</p>
      </Alert>
    </Container>
  {/await}
{/if}

{#if previewPromise}
  {#await previewPromise}
    <p>loading...</p>
  {:then preview}
    <Container>
      <img
        class="pure-img"
        src={`data:image/png;base64,${preview}`}
        alt="sunspot number whole disk"
      />
    </Container>
    <SaveForm {filename} on:submit={submitSave} />
  {:catch e}
    <Container>
      <Alert severity="error">
        <p>{e instanceof FetchError ? e.detail : e.message}</p>
      </Alert>
    </Container>
  {/await}
{/if}

{#if savePromise}
  {#await savePromise}
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
