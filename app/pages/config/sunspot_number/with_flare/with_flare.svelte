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
  import { schemaSunspotNumberWithFlare } from "@/schemas/sunspot_number_with_flare"

  type SunspotNumberWithFlare = InferOutput<typeof schemaSunspotNumberWithFlare>

  const defaultConfig = "config/sunspot_number/with_flare.json"
  const configPattern = /^config\/sunspot_number\/with_flare\//

  const getFilesConfig = () => {
    return getFiles({
      path: "config/sunspot_number/with_flare",
      glob: "*.json",
    })
  }

  const getConfigWithFlare = (
    params: Parameters<typeof getConfig>[1]
  ): ReturnType<typeof getConfig<SunspotNumberWithFlare>> => {
    return getConfig("/api/sunspot_number/with_flare/config/with_flare", params)
  }

  const postConfigWithFlare = (
    body: Parameters<typeof postConfig<SunspotNumberWithFlare>>[1]
  ): ReturnType<typeof postConfig> => {
    return postConfig("/api/sunspot_number/with_flare/config/with_flare", body)
  }

  const postPreviewWithFlare = (
    body: Parameters<typeof postPreview<SunspotNumberWithFlare>>[1]
  ): ReturnType<typeof postPreview> => {
    return postPreview(
      "/api/sunspot_number/with_flare/config/with_flare/preview",
      body
    )
  }

  let figSize = $state<SunspotNumberWithFlare["figSize"]>()
  let lineSunspot = $state<SunspotNumberWithFlare["lineSunspot"]>()
  let lineFlare = $state<SunspotNumberWithFlare["lineFlare"]>()
  let title = $state<SunspotNumberWithFlare["title"]>()
  let xaxis = $state<SunspotNumberWithFlare["xaxis"]>()
  let yaxisSunspot = $state<SunspotNumberWithFlare["yaxisSunspot"]>()
  let yaxisFlare = $state<SunspotNumberWithFlare["yaxisFlare"]>()
  let legend = $state<SunspotNumberWithFlare["legend"]>()

  const config = $derived<Partial<SunspotNumberWithFlare>>({
    figSize,
    lineSunspot,
    lineFlare,
    title,
    xaxis,
    yaxisSunspot,
    yaxisFlare,
    legend,
  })
</script>

<ConfigPage
  {defaultConfig}
  {configPattern}
  schema={schemaSunspotNumberWithFlare}
  {config}
  {getFilesConfig}
  getConfig={getConfigWithFlare}
  postConfig={postConfigWithFlare}
  postPreview={postPreviewWithFlare}
>
  {#snippet configForm(currentConfig, fonts)}
    {#snippet tabPageFigSize()}
      <FigSize init={currentConfig["figSize"]} bind:value={figSize} />
    {/snippet}
    {#snippet tabPageLineSunspot()}
      <Line init={currentConfig["lineSunspot"]} bind:value={lineSunspot} />
    {/snippet}
    {#snippet tabPageLineFlare()}
      <Line init={currentConfig["lineFlare"]} bind:value={lineFlare} />
    {/snippet}
    {#snippet tabPageTitle()}
      <Title init={currentConfig["title"]} {fonts} bind:value={title} />
    {/snippet}
    {#snippet tabPageXAxis()}
      <Axis init={currentConfig["xaxis"]} {fonts} bind:value={xaxis} />
    {/snippet}
    {#snippet tabPageYAxisSunspot()}
      <Axis
        init={currentConfig["yaxisSunspot"]}
        {fonts}
        bind:value={yaxisSunspot}
      />
    {/snippet}
    {#snippet tabPageYAxisFlare()}
      <Axis
        init={currentConfig["yaxisFlare"]}
        {fonts}
        bind:value={yaxisFlare}
      />
    {/snippet}
    {#snippet tabPageLegend()}
      <Legend init={currentConfig["legend"]} {fonts} bind:value={legend} />
    {/snippet}
    <Tab
      titles={[
        "FigSize",
        "Line Sunspot",
        "Line Flare",
        "Title",
        "X Axis",
        "Y Sunspot Axis",
        "Y Flare Axis",
        "Legend",
      ]}
      pages={[
        tabPageFigSize,
        tabPageLineSunspot,
        tabPageLineFlare,
        tabPageTitle,
        tabPageXAxis,
        tabPageYAxisSunspot,
        tabPageYAxisFlare,
        tabPageLegend,
      ]}
    />
  {/snippet}
</ConfigPage>
