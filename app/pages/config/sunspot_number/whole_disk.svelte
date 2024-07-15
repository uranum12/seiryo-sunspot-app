<script lang="ts">
  import { type InferOutput, safeParse } from "valibot"

  import {
    getConfigWholeDisk,
    postConfigWholeDisk,
    postPreviewConfigWholeDisk,
  } from "@/api/config/sunspot_number"
  import { getFiles } from "@/api/files"
  import Alert from "@/components/alert.svelte"
  import Axis from "@/components/config/axis.svelte"
  import FigSize from "@/components/config/fig_size.svelte"
  import Line from "@/components/config/line.svelte"
  import Title from "@/components/config/title.svelte"
  import ConfirmDialog from "@/components/confirm_dialog.svelte"
  import Tab from "@/components/tab.svelte"
  import { schemaSunspotNumberWholeDisk } from "@/schemas/sunspot_number"
  import { FetchError } from "@/utils/fetch"

  type SunspotNumberWholeDisk = InferOutput<typeof schemaSunspotNumberWholeDisk>

  const getFilesConfig = () => {
    return getFiles({
      path: "config/sunspot_number/whole_disk",
      glob: "*.json",
    })
  }

  const defaultConfig = "config/sunspot_number/whole_disk.json"

  let showConfirmOverwrite = $state<boolean>(false)

  let config = $state<SunspotNumberWholeDisk>()

  let configName = $state<string>(defaultConfig)

  let figSize = $state<SunspotNumberWholeDisk["figSize"]>()
  let line = $state<SunspotNumberWholeDisk["line"]>()
  let title = $state<SunspotNumberWholeDisk["title"]>()
  let xaxis = $state<SunspotNumberWholeDisk["xaxis"]>()
  let yaxis = $state<SunspotNumberWholeDisk["yaxis"]>()

  let outputName = $state<string>("")
  let overwrite = $state<boolean>(false)

  let filesPromise = $state<ReturnType<typeof getFiles>>(getFilesConfig())
  let configPromise = $state<ReturnType<typeof getConfigWholeDisk>>()
  let previewPromise = $state<ReturnType<typeof postPreviewConfigWholeDisk>>()
  let savePromise = $state<ReturnType<typeof postConfigWholeDisk>>()

  const fetchFiles = () => {
    configPromise = undefined
    previewPromise = undefined
    savePromise = undefined
    filesPromise = getFilesConfig()
  }

  const fetchConfig = () => {
    previewPromise = undefined
    savePromise = undefined
    configPromise = getConfigWholeDisk({ configName })
  }

  const fetchPreview = () => {
    savePromise = undefined
    const result = safeParse(schemaSunspotNumberWholeDisk, {
      figSize,
      line,
      title,
      xaxis,
      yaxis,
    })
    if (result.success) {
      previewPromise = postPreviewConfigWholeDisk({ config: result.output })
      config = result.output
    }
  }

  const submitSave = () => {
    if (config) {
      savePromise = postConfigWholeDisk({
        configName: outputName,
        overwrite,
        config,
      })
    }
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

{#await filesPromise}
  <p>loading...</p>
{:then files}
  <section class="space-y-1">
    <select bind:value={configName}>
      <option value={defaultConfig} selected>default</option>
      {#each files as file}
        <option value={file}
          >{file.replace(/^config\/sunspot_number\/whole_disk\//, "")}</option
        >
      {/each}
    </select>
    <button onclick={fetchConfig}>edit</button>
  </section>
{:catch e}
  <section>
    <Alert type="error">
      <p>{e.message}</p>
    </Alert>
  </section>
{/await}

{#if configPromise}
  {#await configPromise}
    <p>loading...</p>
  {:then currentConfig}
    <section class="space-y-1">
      {#snippet tabPageFigSize()}
        <FigSize init={currentConfig["figSize"]} bind:value={figSize} />
      {/snippet}
      {#snippet tabPageLine()}
        <Line init={currentConfig["line"]} labelHidden bind:value={line} />
      {/snippet}
      {#snippet tabPageTitle()}
        <Title
          init={currentConfig["title"]}
          positionHidden
          bind:value={title}
        />
      {/snippet}
      {#snippet tabPageXAxis()}
        <Axis init={currentConfig["xaxis"]} bind:value={xaxis} />
      {/snippet}
      {#snippet tabPageYAxis()}
        <Axis init={currentConfig["yaxis"]} bind:value={yaxis} />
      {/snippet}
      <Tab
        titles={["FigSize", "Line", "Title", "X Axis", "Y Axis"]}
        pages={[
          tabPageFigSize,
          tabPageLine,
          tabPageTitle,
          tabPageXAxis,
          tabPageYAxis,
        ]}
      />
      <button onclick={fetchPreview}>preview</button>
    </section>
  {:catch e}
    <section>
      <Alert type="error">
        <p>{e instanceof FetchError ? e.detail : e.message}</p>
      </Alert>
    </section>
  {/await}
{/if}

{#if previewPromise}
  {#await previewPromise}
    <p>loading...</p>
  {:then preview}
    <section>
      <img
        src={`data:image/png;base64,${preview}`}
        alt="config applied preview"
      />
    </section>

    <section class="space-y-1">
      <input
        required
        placeholder="output config name"
        bind:value={outputName}
      />
      <label>
        <input type="checkbox" bind:checked={overwrite} />
        <span>Overwrite</span>
      </label>
      <button onclick={clickSave}>save</button>
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
        <p>config {output} generated</p>
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
