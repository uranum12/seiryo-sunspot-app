<script lang="ts">
  import { getDraw, postDraw } from "@/api/draw"
  import type { getFiles } from "@/api/files"
  import Alert from "@/components/alert.svelte"
  import PreviewForm, {
    type FormInput as PreviewFormInput,
  } from "@/components/preview_form.svelte"
  import SaveForm, {
    type FormInput as SaveFormInput,
  } from "@/components/save_form.svelte"
  import { FetchError } from "@/utils/fetch"

  type Props = {
    defaultConfig: string
    imageAlt: string
    getFilesDraw: () => ReturnType<typeof getFiles>
    getFilesConfig: () => ReturnType<typeof getFiles>
    drawApiPath: string
  }

  let {
    defaultConfig,
    imageAlt,
    getFilesDraw,
    getFilesConfig,
    drawApiPath,
  }: Props = $props()

  let filename = $state<string>("")
  let config = $state<string>("")

  let filesPromise = $state<ReturnType<typeof getFiles>>(getFilesDraw())
  let configPromise = $state<ReturnType<typeof getFiles>>(getFilesConfig())
  let previewPromise = $state<ReturnType<typeof getDraw>>()
  let savePromise = $state<ReturnType<typeof postDraw>>()

  const fetchFiles = () => {
    previewPromise = undefined
    savePromise = undefined
    filesPromise = getFilesDraw()
    configPromise = getFilesConfig()
  }

  const fetchPreview = (input: PreviewFormInput) => {
    savePromise = undefined
    filename = input.filename
    config = input.configName
    previewPromise = getDraw(drawApiPath, input)
  }

  const submitSave = (input: SaveFormInput) => {
    savePromise = postDraw(drawApiPath, { input: filename, config, ...input })
  }
</script>

<section>
  <button onclick={fetchFiles}>refresh files</button>
</section>

{#await Promise.all([filesPromise, configPromise])}
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
      <img src={`data:image/png;base64,${preview}`} alt="{imageAlt} preview" />
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
