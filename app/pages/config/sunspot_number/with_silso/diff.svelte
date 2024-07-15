<script lang="ts">
  import type { InferOutput } from "valibot"

  import { getConfig, postConfig, postPreview } from "@/api/config"
  import { getFiles } from "@/api/files"
  import Axis from "@/components/config/axis.svelte"
  import FigSize from "@/components/config/fig_size.svelte"
  import Line from "@/components/config/line.svelte"
  import Title from "@/components/config/title.svelte"
  import Tab from "@/components/tab.svelte"
  import ConfigPage from "@/pages/common/config.svelte"
  // biome-ignore lint/style/useImportType: biome dosen't support html template yet.
  import { schemaSunspotNumberDiff } from "@/schemas/sunspot_number_with_silso"

  type SunspotNumberDiff = InferOutput<typeof schemaSunspotNumberDiff>

  const defaultConfig = "config/sunspot_number/diff.json"
  const configPattern = /^config\/sunspot_number\/diff\//

  const getFilesConfig = () => {
    return getFiles({
      path: "config/sunspot_number/diff",
      glob: "*.json",
    })
  }

  const getConfigDiff = (
    params: Parameters<typeof getConfig>[1]
  ): ReturnType<typeof getConfig<SunspotNumberDiff>> => {
    return getConfig("/api/sunspot_number/with_silso/config/diff", params)
  }

  const postConfigDiff = (
    body: Parameters<typeof postConfig<SunspotNumberDiff>>[1]
  ): ReturnType<typeof postConfig> => {
    return postConfig("/api/sunspot_number/with_silso/config/diff", body)
  }

  const postPreviewDiff = (
    body: Parameters<typeof postPreview<SunspotNumberDiff>>[1]
  ): ReturnType<typeof postPreview> => {
    return postPreview(
      "/api/sunspot_number/with_silso/config/diff/preview",
      body
    )
  }

  let figSize = $state<SunspotNumberDiff["figSize"]>()
  let line = $state<SunspotNumberDiff["line"]>()
  let title = $state<SunspotNumberDiff["title"]>()
  let xaxis = $state<SunspotNumberDiff["xaxis"]>()
  let yaxis = $state<SunspotNumberDiff["yaxis"]>()

  const config = $derived<Partial<SunspotNumberDiff>>({
    figSize,
    line,
    title,
    xaxis,
    yaxis,
  })
</script>

<ConfigPage
  {defaultConfig}
  {configPattern}
  schema={schemaSunspotNumberDiff}
  {config}
  {getFilesConfig}
  getConfig={getConfigDiff}
  postConfig={postConfigDiff}
  postPreview={postPreviewDiff}
>
  {#snippet configForm(currentConfig, fonts)}
    {#snippet tabPageFigSize()}
      <FigSize init={currentConfig["figSize"]} bind:value={figSize} />
    {/snippet}
    {#snippet tabPageLine()}
      <Line init={currentConfig["line"]} labelHidden bind:value={line} />
    {/snippet}
    {#snippet tabPageTitle()}
      <Title
        init={currentConfig["title"]}
        {fonts}
        positionHidden
        bind:value={title}
      />
    {/snippet}
    {#snippet tabPageXAxis()}
      <Axis init={currentConfig["xaxis"]} {fonts} bind:value={xaxis} />
    {/snippet}
    {#snippet tabPageYAxis()}
      <Axis init={currentConfig["yaxis"]} {fonts} bind:value={yaxis} />
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
  {/snippet}
</ConfigPage>
