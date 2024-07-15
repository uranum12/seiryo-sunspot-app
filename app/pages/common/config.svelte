<script lang="ts" generics="T">
  import type { Snippet } from "svelte"
  import { type GenericSchema, type InferOutput, safeParse } from "valibot"

  import type {
    getConfig as getConfigType,
    postConfig as postConfigType,
    postPreview as postPreviewType,
  } from "@/api/config"
  import type { getFiles } from "@/api/files"
  import { getFonts } from "@/api/fonts"
  import Alert from "@/components/alert.svelte"
  import ConfirmDialog from "@/components/confirm_dialog.svelte"
  import { FetchError } from "@/utils/fetch"

  type Props = {
    defaultConfig: string
    configPattern: RegExp
    schema: GenericSchema<T>
    config: Partial<T> | undefined
    configForm: Snippet<[T, Awaited<ReturnType<typeof getFonts>>]>
    getFilesConfig: () => ReturnType<typeof getFiles>
    getConfig: (
      params: Parameters<typeof getConfigType>[1]
    ) => ReturnType<typeof getConfigType<T>>
    postConfig: (
      body: Parameters<typeof postConfigType<T>>[1]
    ) => ReturnType<typeof postConfigType>
    postPreview: (
      body: Parameters<typeof postPreviewType<T>>[1]
    ) => ReturnType<typeof postPreviewType>
  }

  let {
    defaultConfig,
    configPattern,
    schema,
    config: configInput,
    configForm,
    getFilesConfig,
    getConfig,
    postConfig,
    postPreview,
  }: Props = $props()

  type Config = InferOutput<typeof schema>

  let showConfirmOverwrite = $state<boolean>(false)

  let config = $state<Config>()

  let configName = $state<string>(defaultConfig)

  let outputName = $state<string>("")
  let overwrite = $state<boolean>(false)

  let filesPromise = $state<ReturnType<typeof getFiles>>(getFilesConfig())
  let fontsPromise = $state<ReturnType<typeof getFonts>>(getFonts())
  let configPromise = $state<ReturnType<typeof getConfig>>()
  let previewPromise = $state<ReturnType<typeof postPreview>>()
  let savePromise = $state<ReturnType<typeof postConfig>>()

  const fetchFiles = () => {
    configPromise = undefined
    previewPromise = undefined
    savePromise = undefined
    filesPromise = getFilesConfig()
  }

  const fetchConfig = () => {
    previewPromise = undefined
    savePromise = undefined
    configPromise = getConfig({ configName })
  }

  const fetchPreview = () => {
    savePromise = undefined
    const result = safeParse(schema, configInput)
    if (result.success) {
      previewPromise = postPreview({ config: result.output })
      config = result.output
    }
  }

  const submitSave = () => {
    if (config) {
      savePromise = postConfig({
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
        <option value={file}>
          {file.replace(configPattern, "")}
        </option>
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
  {#await Promise.all([configPromise, fontsPromise])}
    <p>loading...</p>
  {:then result}
    {@const [currentConfig, fonts] = result}
    <section class="space-y-1">
      {@render configForm(currentConfig, fonts)}
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
