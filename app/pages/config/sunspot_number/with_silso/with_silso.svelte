<script lang="ts">
  import type { InferOutput } from "valibot"

  import { getConfig, postConfig, postPreview } from "@/api/config"
  import { getFiles } from "@/api/files"
  import Axis from "@/components/config/axis.svelte"
  import FigSize from "@/components/config/fig_size.svelte"
  import Legend from "@/components/config/legend.svelte"
  import Line from "@/components/config/line.svelte"
  import Title from "@/components/config/title.svelte"
  import Tab from "@/components/tab.svelte"
  import ConfigPage from "@/pages/common/config.svelte"
  // biome-ignore lint/style/useImportType: biome dosen't support html template yet.
  import { schemaSunspotNumberWithSilso } from "@/schemas/sunspot_number_with_silso"

  type SunspotNumberWithSilso = InferOutput<typeof schemaSunspotNumberWithSilso>

  const defaultConfig = "config/sunspot_number/with_silso.json"
  const configPattern = /^config\/sunspot_number\/with_silso\//

  const getFilesConfig = () => {
    return getFiles({
      path: "config/sunspot_number/with_silso",
      glob: "*.json",
    })
  }

  const getConfigWithSilso = (
    params: Parameters<typeof getConfig>[1]
  ): ReturnType<typeof getConfig<SunspotNumberWithSilso>> => {
    return getConfig("/api/sunspot_number/with_silso/config/with_silso", params)
  }

  const postConfigWithSilso = (
    body: Parameters<typeof postConfig<SunspotNumberWithSilso>>[1]
  ): ReturnType<typeof postConfig> => {
    return postConfig("/api/sunspot_number/with_silso/config/with_silso", body)
  }

  const postPreviewWithSilso = (
    body: Parameters<typeof postPreview<SunspotNumberWithSilso>>[1]
  ): ReturnType<typeof postPreview> => {
    return postPreview(
      "/api/sunspot_number/with_silso/config/with_silso/preview",
      body
    )
  }

  let figSize = $state<SunspotNumberWithSilso["figSize"]>()
  let lineSeiryo = $state<SunspotNumberWithSilso["lineSeiryo"]>()
  let lineSilso = $state<SunspotNumberWithSilso["lineSilso"]>()
  let title = $state<SunspotNumberWithSilso["title"]>()
  let xaxis = $state<SunspotNumberWithSilso["xaxis"]>()
  let yaxis = $state<SunspotNumberWithSilso["yaxis"]>()
  let legend = $state<SunspotNumberWithSilso["legend"]>()

  const config = $derived<Partial<SunspotNumberWithSilso>>({
    figSize,
    lineSeiryo,
    lineSilso,
    title,
    xaxis,
    yaxis,
    legend,
  })
</script>

<ConfigPage
  {defaultConfig}
  {configPattern}
  schema={schemaSunspotNumberWithSilso}
  {config}
  {getFilesConfig}
  getConfig={getConfigWithSilso}
  postConfig={postConfigWithSilso}
  postPreview={postPreviewWithSilso}
>
  {#snippet configForm(currentConfig, fonts)}
    {#snippet tabPageFigSize()}
      <FigSize init={currentConfig["figSize"]} bind:value={figSize} />
    {/snippet}
    {#snippet tabPageLineSeiryo()}
      <Line init={currentConfig["lineSeiryo"]} bind:value={lineSeiryo} />
    {/snippet}
    {#snippet tabPageLineSilso()}
      <Line init={currentConfig["lineSilso"]} bind:value={lineSilso} />
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
    {#snippet tabPageLegend()}
      <Legend init={currentConfig["legend"]} {fonts} bind:value={legend} />
    {/snippet}
    <Tab
      titles={[
        "FigSize",
        "Line Seiryo",
        "Line SILSO",
        "Title",
        "X Axis",
        "Y Axis",
        "Legend",
      ]}
      pages={[
        tabPageFigSize,
        tabPageLineSeiryo,
        tabPageLineSilso,
        tabPageTitle,
        tabPageXAxis,
        tabPageYAxis,
        tabPageLegend,
      ]}
    />
  {/snippet}
</ConfigPage>
