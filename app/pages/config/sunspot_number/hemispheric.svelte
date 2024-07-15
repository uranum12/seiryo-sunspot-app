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
  import Legend from "@/components/config/legend.svelte"
  // biome-ignore lint/style/useImportType: biome dosen't support html template yet.
  import { schemaSunspotNumberHemispheric } from "@/schemas/sunspot_number"

  type SunspotNumberHemispheric = InferOutput<
    typeof schemaSunspotNumberHemispheric
  >

  const defaultConfig = "config/sunspot_number/hemispheric.json"
  const configPattern = /^config\/sunspot_number\/hemispheric\//

  const getFilesConfig = () => {
    return getFiles({
      path: "config/sunspot_number/hemispheric",
      glob: "*.json",
    })
  }

  const getConfigHemispheric = (
    params: Parameters<typeof getConfig>[1]
  ): ReturnType<typeof getConfig<SunspotNumberHemispheric>> => {
    return getConfig("/api/sunspot_number/config/hemispheric", params)
  }

  const postConfigHemispheric = (
    body: Parameters<typeof postConfig<SunspotNumberHemispheric>>[1]
  ): ReturnType<typeof postConfig> => {
    return postConfig("/api/sunspot_number/config/hemispheric", body)
  }

  const postPreviewHemispheric = (
    body: Parameters<typeof postPreview<SunspotNumberHemispheric>>[1]
  ): ReturnType<typeof postPreview> => {
    return postPreview("/api/sunspot_number/config/hemispheric/preview", body)
  }

  let figSize = $state<SunspotNumberHemispheric["figSize"]>()
  let lineNorth = $state<SunspotNumberHemispheric["lineNorth"]>()
  let lineSouth = $state<SunspotNumberHemispheric["lineSouth"]>()
  let title = $state<SunspotNumberHemispheric["title"]>()
  let xaxis = $state<SunspotNumberHemispheric["xaxis"]>()
  let yaxis = $state<SunspotNumberHemispheric["yaxis"]>()
  let legend = $state<SunspotNumberHemispheric["legend"]>()

  const config = $derived<Partial<SunspotNumberHemispheric>>({
    figSize,
    lineNorth,
    lineSouth,
    title,
    xaxis,
    yaxis,
    legend,
  })
</script>

<ConfigPage
  {defaultConfig}
  {configPattern}
  schema={schemaSunspotNumberHemispheric}
  {config}
  {getFilesConfig}
  getConfig={getConfigHemispheric}
  postConfig={postConfigHemispheric}
  postPreview={postPreviewHemispheric}
>
  {#snippet configForm(currentConfig, fonts)}
    {#snippet tabPageFigSize()}
      <FigSize init={currentConfig["figSize"]} bind:value={figSize} />
    {/snippet}
    {#snippet tabPageLineNorth()}
      <Line init={currentConfig["lineNorth"]} bind:value={lineNorth} />
    {/snippet}
    {#snippet tabPageLineSouth()}
      <Line init={currentConfig["lineSouth"]} bind:value={lineSouth} />
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
        "North Line",
        "South Line",
        "Title",
        "X Axis",
        "Y Axis",
        "Legend",
      ]}
      pages={[
        tabPageFigSize,
        tabPageLineNorth,
        tabPageLineSouth,
        tabPageTitle,
        tabPageXAxis,
        tabPageYAxis,
        tabPageLegend,
      ]}
    />
  {/snippet}
</ConfigPage>
