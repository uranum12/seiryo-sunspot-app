<script lang="ts">
  import { getDraw, postDraw } from "@/api/draw"
  import type { getFiles } from "@/api/files"
  import Alert from "@/components/alert.svelte"
  import ConfirmDialog from "@/components/confirm_dialog.svelte"
  import formatList from "@/constants/format_list.json"
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

  // preview form
  let fileNamePreview = $state<string>("")
  let configNamePreview = $state<string>(defaultConfig)

  // save form
  let fileNameSave = $state<string>("")
  let configNameSave = $state<string>("")
  let format = $state<string>("")
  let dpi = $state<number>(300)
  let overwrite = $state<boolean>(false)

  let showConfirmOverwrite = $state<boolean>(false)

  const submitPreviewDisabled = $derived<boolean>(fileNamePreview.trim() === "")
  const submitSaveDisabled = $derived(format === "" || !dpi)

  let filesPromise = $state<ReturnType<typeof getFiles>>(getFilesDraw())
  let configPromise = $state<ReturnType<typeof getFiles>>(getFilesConfig())
  let previewPromise = $state<ReturnType<typeof getDraw>>()
  let savePromise = $state<ReturnType<typeof postDraw>>()

  const fetchFiles = () => {
    fileNamePreview = ""
    configNamePreview = defaultConfig
    previewPromise = undefined
    savePromise = undefined
    filesPromise = getFilesDraw()
    configPromise = getFilesConfig()
  }

  const fetchPreview = () => {
    fileNameSave = fileNamePreview
    configNameSave = configNamePreview
    savePromise = undefined
    previewPromise = getDraw(drawApiPath, {
      filename: fileNamePreview,
      configName: configNamePreview,
    })
  }

  const submitSave = () => {
    savePromise = postDraw(drawApiPath, {
      input: fileNameSave,
      config: configNameSave,
      format,
      dpi,
      overwrite,
    })
  }

  const clickSave = () => {
    if (overwrite) {
      showConfirmOverwrite = true
    } else {
      submitSave()
    }
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
    <section class="space-y-1">
      <select required bind:value={fileNamePreview}>
        <option value="" selected disabled>select file</option>
        {#each files.sort() as file}
          <option value={file}>{file.replace(/^out\//, "")}</option>
        {/each}
      </select>
      <select required bind:value={configNamePreview}>
        <option value={defaultConfig} selected>default</option>
        {#each configs.sort() as config}
          <option value={config}>{config.replace(/^config\//, "")}</option>
        {/each}
      </select>
      <button disabled={submitPreviewDisabled} onclick={fetchPreview}>
        preview
      </button>
    </section>
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

    <section class="space-y-1">
      <select required bind:value={format}>
        <option value="" selected disabled>select file format</option>
        {#each formatList as format}
          <option value={format.format}>
            {format.description} ({format.format})
          </option>
        {/each}
      </select>
      <input type="number" required placeholder="dpi" bind:value={dpi} />
      <label>
        <input type="checkbox" bind:checked={overwrite} />
        <span>Overwrite</span>
      </label>
      <button disabled={submitSaveDisabled} onclick={clickSave}>submit</button>
    </section>

    <ConfirmDialog bind:isOpen={showConfirmOverwrite} onConfirm={submitSave}>
      Are you sure you want me to overwrite file ?
    </ConfirmDialog>
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
