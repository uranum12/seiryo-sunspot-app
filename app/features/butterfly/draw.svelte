<script lang="ts">
  import Alert from "@/components/alert.svelte"
  import { FetchError } from "@/utils/fetch"

  import PreviewForm, {
    type FormInput as PreviewFormInput,
  } from "@/components/preview_form.svelte"
  import SaveForm, {
    type FormInput as SaveFormInput,
  } from "@/components/save_form.svelte"
  import { getDraw, postDraw } from "./api/draw"
  import { getFilesConfig, getFilesDraw } from "./api/files"

  const defaultConfig = "config/butterfly/butterfly.json"

  let filename = $state<string>("")
  let config = $state<string>("")

  let filesPromise = $state<ReturnType<typeof getFilesDraw>>(getFilesDraw())
  let configsPromise =
    $state<ReturnType<typeof getFilesConfig>>(getFilesConfig())
  let previewPromise = $state<ReturnType<typeof getDraw>>()
  let savePromise = $state<ReturnType<typeof postDraw>>()

  const fetchFiles = () => {
    previewPromise = undefined
    savePromise = undefined
    filesPromise = getFilesDraw()
    configsPromise = getFilesConfig()
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

<section>
  <button onclick={fetchFiles}>refresh files</button>
</section>

{#await Promise.all([filesPromise, configsPromise])}
  <p>loading...</p>
{:then result}
  {@const [files, configs] = result}
  {#if files.length !== 0}
    <PreviewForm {files} {configs} {defaultConfig} onSubmit={fetchPreview} />
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

{#if previewPromise}
  {#await previewPromise}
    <p>loading...</p>
  {:then preview}
    <section>
      <img src={`data:image/png;base64,${preview}`} alt="butterfly diagram" />
    </section>
    <SaveForm onSubmit={submitSave} />
  {:catch e}
    <section>
      <Alert type="error">
        <p>{e instanceof FetchError ? e.detail : e.message}</p>
      </Alert>
    </section>
  {/await}
{/if}

{#if savePromise}
  {#await savePromise}
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
