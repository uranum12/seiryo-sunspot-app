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
  import { schemaSunspotNumberWithFlareHemispheric } from "@/schemas/sunspot_number_with_flare"

  type SunspotNumberWithFlareHemispheric = InferOutput<
    typeof schemaSunspotNumberWithFlareHemispheric
  >

  const defaultConfig = "config/sunspot_number/with_flare_hemispheric.json"
  const configPattern = /^config\/sunspot_number\/with_flare_hemispheric\//

  const getFilesConfig = () => {
    return getFiles({
      path: "config/sunspot_number/with_flare_hemispheric",
      glob: "*.json",
    })
  }

  const getConfigWithFlareHemispheric = (
    params: Parameters<typeof getConfig>[1]
  ): ReturnType<typeof getConfig<SunspotNumberWithFlareHemispheric>> => {
    return getConfig(
      "/api/sunspot_number/with_flare/config/hemispheric",
      params
    )
  }

  const postConfigWithFlareHemispheric = (
    body: Parameters<typeof postConfig<SunspotNumberWithFlareHemispheric>>[1]
  ): ReturnType<typeof postConfig> => {
    return postConfig("/api/sunspot_number/with_flare/config/hemispheric", body)
  }

  const postPreviewWithFlareHemispheric = (
    body: Parameters<typeof postPreview<SunspotNumberWithFlareHemispheric>>[1]
  ): ReturnType<typeof postPreview> => {
    return postPreview(
      "/api/sunspot_number/with_flare/config/hemispheric/preview",
      body
    )
  }

  let figSize = $state<SunspotNumberWithFlareHemispheric["figSize"]>()
  let lineNorthSunspot =
    $state<SunspotNumberWithFlareHemispheric["lineNorthSunspot"]>()
  let lineNorthFlare =
    $state<SunspotNumberWithFlareHemispheric["lineNorthFlare"]>()
  let lineSouthSunspot =
    $state<SunspotNumberWithFlareHemispheric["lineSouthSunspot"]>()
  let lineSouthFlare =
    $state<SunspotNumberWithFlareHemispheric["lineSouthFlare"]>()
  let titleNorth = $state<SunspotNumberWithFlareHemispheric["titleNorth"]>()
  let titleSouth = $state<SunspotNumberWithFlareHemispheric["titleSouth"]>()
  let xaxis = $state<SunspotNumberWithFlareHemispheric["xaxis"]>()
  let yaxisNorthSunspot =
    $state<SunspotNumberWithFlareHemispheric["yaxisNorthSunspot"]>()
  let yaxisNorthFlare =
    $state<SunspotNumberWithFlareHemispheric["yaxisNorthFlare"]>()
  let yaxisSouthSunspot =
    $state<SunspotNumberWithFlareHemispheric["yaxisSouthSunspot"]>()
  let yaxisSouthFlare =
    $state<SunspotNumberWithFlareHemispheric["yaxisSouthFlare"]>()
  let legendNorth = $state<SunspotNumberWithFlareHemispheric["legendNorth"]>()
  let legendSouth = $state<SunspotNumberWithFlareHemispheric["legendSouth"]>()

  const config = $derived<Partial<SunspotNumberWithFlareHemispheric>>({
    figSize,
    lineNorthSunspot,
    lineNorthFlare,
    lineSouthSunspot,
    lineSouthFlare,
    titleNorth,
    titleSouth,
    xaxis,
    yaxisNorthSunspot,
    yaxisNorthFlare,
    yaxisSouthSunspot,
    yaxisSouthFlare,
    legendNorth,
    legendSouth,
  })
</script>

<ConfigPage
  {defaultConfig}
  {configPattern}
  schema={schemaSunspotNumberWithFlareHemispheric}
  {config}
  {getFilesConfig}
  getConfig={getConfigWithFlareHemispheric}
  postConfig={postConfigWithFlareHemispheric}
  postPreview={postPreviewWithFlareHemispheric}
>
  {#snippet configForm(currentConfig, fonts)}
    {#snippet tabPageFigSize()}
      <FigSize init={currentConfig["figSize"]} bind:value={figSize} />
    {/snippet}
    {#snippet tabPageLineNorthSunspot()}
      <Line
        init={currentConfig["lineNorthSunspot"]}
        bind:value={lineNorthSunspot}
      />
    {/snippet}
    {#snippet tabPageLineNorthFlare()}
      <Line
        init={currentConfig["lineNorthFlare"]}
        bind:value={lineNorthFlare}
      />
    {/snippet}
    {#snippet tabPageLineSouthSunspot()}
      <Line
        init={currentConfig["lineSouthSunspot"]}
        bind:value={lineSouthSunspot}
      />
    {/snippet}
    {#snippet tabPagelineSouthFlare()}
      <Line
        init={currentConfig["lineSouthFlare"]}
        bind:value={lineSouthFlare}
      />
    {/snippet}
    {#snippet tabPageTitleNorth()}
      <Title
        init={currentConfig["titleNorth"]}
        {fonts}
        bind:value={titleNorth}
      />
    {/snippet}
    {#snippet tabPageTitleSouth()}
      <Title
        init={currentConfig["titleSouth"]}
        {fonts}
        bind:value={titleSouth}
      />
    {/snippet}
    {#snippet tabPageXAxis()}
      <Axis init={currentConfig["xaxis"]} {fonts} bind:value={xaxis} />
    {/snippet}
    {#snippet tabPageYAxisNorthSunspot()}
      <Axis
        init={currentConfig["yaxisNorthSunspot"]}
        {fonts}
        bind:value={yaxisNorthSunspot}
      />
    {/snippet}
    {#snippet tabPageYAxisNorthFlare()}
      <Axis
        init={currentConfig["yaxisNorthFlare"]}
        {fonts}
        bind:value={yaxisNorthFlare}
      />
    {/snippet}
    {#snippet tabPageYAxisSouthSunspot()}
      <Axis
        init={currentConfig["yaxisSouthSunspot"]}
        {fonts}
        bind:value={yaxisSouthSunspot}
      />
    {/snippet}
    {#snippet tabPageYAxisSouthFlare()}
      <Axis
        init={currentConfig["yaxisSouthFlare"]}
        {fonts}
        bind:value={yaxisSouthFlare}
      />
    {/snippet}
    {#snippet tabPageLegendNorth()}
      <Legend
        init={currentConfig["legendNorth"]}
        {fonts}
        bind:value={legendNorth}
      />
    {/snippet}
    {#snippet tabPageLegendSouth()}
      <Legend
        init={currentConfig["legendSouth"]}
        {fonts}
        bind:value={legendSouth}
      />
    {/snippet}
    <Tab
      titles={[
        "FigSize",
        "Line North Sunspot",
        "Line North Flare Index",
        "Line South Sunspot",
        "Line South Flare Index",
        "North Title",
        "South Title",
        "X Axis",
        "Y North Sunspot Axis",
        "Y North Flare Index Axis",
        "Y South Sunspot Axis",
        "Y South Flare Index Axis",
        "North Legend",
        "South Legend",
      ]}
      pages={[
        tabPageFigSize,
        tabPageLineNorthSunspot,
        tabPageLineNorthFlare,
        tabPageLineSouthSunspot,
        tabPagelineSouthFlare,
        tabPageTitleNorth,
        tabPageTitleSouth,
        tabPageXAxis,
        tabPageYAxisNorthSunspot,
        tabPageYAxisNorthFlare,
        tabPageYAxisSouthSunspot,
        tabPageYAxisSouthFlare,
        tabPageLegendNorth,
        tabPageLegendSouth,
      ]}
    />
  {/snippet}
</ConfigPage>
