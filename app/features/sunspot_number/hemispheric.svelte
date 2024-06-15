<script lang="ts">
  import Alert from "@/components/alert.svelte"
  import Container from "@/components/container.svelte"
  import { FetchError } from "@/utils/fetch"

  import { getFilesDraw } from "./api/files"
  import { getDraw, postDraw } from "./api/hemispheric"
  import PreviewForm, {
    type FormInput as PreviewFormInput,
  } from "./components/preview_form.svelte"
  import SaveForm, {
    type FormInput as SaveFormInput,
  } from "./components/save_form.svelte"

  let filename = $state<string>("")

  let filesPromise = $state<ReturnType<typeof getFilesDraw>>(getFilesDraw())
  let previewPromise = $state<ReturnType<typeof getDraw> | undefined>(undefined)
  let savePromise = $state<ReturnType<typeof postDraw> | undefined>(undefined)

  const fetchFiles = () => {
    previewPromise = undefined
    savePromise = undefined
    filesPromise = getFilesDraw()
  }

  const fetchPreview = (input: PreviewFormInput) => {
    savePromise = undefined
    filename = input.filename
    previewPromise = getDraw(input)
  }

  const submitSave = (input: SaveFormInput) => {
    savePromise = postDraw({ input: filename, ...input })
  }
</script>

<Container>
  <button class="pure-button" onclick={fetchFiles}>refresh files</button>
</Container>

{#if filesPromise}
  {#await filesPromise}
    <p>loading...</p>
  {:then files}
    {#if files.length !== 0}
      <PreviewForm {files} onSubmit={fetchPreview} />
    {:else}
      <Container>
        <Alert type="warning">
          <p>no files</p>
        </Alert>
      </Container>
    {/if}
  {:catch e}
    <Container>
      <Alert type="error">
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
        alt="sunspot number hemispheric"
      />
    </Container>
    <SaveForm {filename} onSubmit={submitSave} />
  {:catch e}
    <Container>
      <Alert type="error">
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
      <Alert type="success">
        <p>file {output} generated</p>
      </Alert>
    </Container>
  {:catch e}
    <Container>
      <Alert type="error">
        <p>{e instanceof FetchError ? e.detail : e.message}</p>
      </Alert>
    </Container>
  {/await}
{/if}
