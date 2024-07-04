<script lang="ts">
  import Alert from "@/components/alert.svelte"
  import Container from "@/components/container.svelte"
  import { FetchError } from "@/utils/fetch"

  import {
    getFilesConfigWholeDisk as getConfigs,
    getFilesDraw,
  } from "./api/files"
  import { getDraw, postDraw } from "./api/whole_disk"
  import PreviewForm, {
    type FormInput as PreviewFormInput,
  } from "@/components/preview_form.svelte"
  import SaveForm, {
    type FormInput as SaveFormInput,
  } from "@/components/save_form.svelte"

  const defaultConfig = "config/sunspot_number/whole_disk.json"

  let filename = $state<string>("")
  let config = $state<string>("")

  let filesPromise = $state<ReturnType<typeof getFilesDraw>>(getFilesDraw())
  let configsPromise = $state<ReturnType<typeof getConfigs>>(getConfigs())
  let previewPromise = $state<ReturnType<typeof getDraw>>()
  let savePromise = $state<ReturnType<typeof postDraw>>()

  const fetchFiles = () => {
    previewPromise = undefined
    savePromise = undefined
    filesPromise = getFilesDraw()
    configsPromise = getConfigs()
  }

  const fetchPreview = (input: PreviewFormInput) => {
    savePromise = undefined
    filename = input.filename
    config = input.configName
    previewPromise = getDraw(input)
  }

  const submitSave = (input: SaveFormInput) => {
    savePromise = postDraw({ input: filename, config, ...input })
  }
</script>

<Container>
  <button onclick={fetchFiles}>refresh files</button>
</Container>

{#await Promise.all([filesPromise, configsPromise])}
  <p>loading...</p>
{:then result}
  {@const [files, configs] = result}
  {#if files.length !== 0}
    <PreviewForm {files} {configs} {defaultConfig} onSubmit={fetchPreview} />
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

{#if previewPromise}
  {#await previewPromise}
    <p>loading...</p>
  {:then preview}
    <Container>
      <img
        src={`data:image/png;base64,${preview}`}
        alt="sunspot number whole disk"
      />
    </Container>
    <SaveForm onSubmit={submitSave} />
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
