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
  import { schemaSunspotNumberRatioDiff2 } from "@/schemas/sunspot_number_with_silso"

  type SunspotNumberRatioDiff2 = InferOutput<
    typeof schemaSunspotNumberRatioDiff2
  >

  const defaultConfig = "config/sunspot_number/ratio_diff_2.json"
  const configPattern = /^config\/sunspot_number\/ratio_diff_2\//

  const getFilesConfig = () => {
    return getFiles({
      path: "config/sunspot_number/ratio_diff_2",
      glob: "*.json",
    })
  }

  const getConfigRatioDiff2 = (
    params: Parameters<typeof getConfig>[1]
  ): ReturnType<typeof getConfig<SunspotNumberRatioDiff2>> => {
    return getConfig(
      "/api/sunspot_number/with_silso/config/ratio_diff_2",
      params
    )
  }

  const postConfigRatioDiff2 = (
    body: Parameters<typeof postConfig<SunspotNumberRatioDiff2>>[1]
  ): ReturnType<typeof postConfig> => {
    return postConfig(
      "/api/sunspot_number/with_silso/config/ratio_diff_2",
      body
    )
  }

  const postPreviewRatioDiff2 = (
    body: Parameters<typeof postPreview<SunspotNumberRatioDiff2>>[1]
  ): ReturnType<typeof postPreview> => {
    return postPreview(
      "/api/sunspot_number/with_silso/config/ratio_diff_2/preview",
      body
    )
  }

  let figSize = $state<SunspotNumberRatioDiff2["figSize"]>()
  let lineRatio = $state<SunspotNumberRatioDiff2["lineRatio"]>()
  let lineDiff = $state<SunspotNumberRatioDiff2["lineDiff"]>()
  let title = $state<SunspotNumberRatioDiff2["title"]>()
  let xaxis = $state<SunspotNumberRatioDiff2["xaxis"]>()
  let yaxisRatio = $state<SunspotNumberRatioDiff2["yaxisRatio"]>()
  let yaxisDiff = $state<SunspotNumberRatioDiff2["yaxisDiff"]>()
  let legend = $state<SunspotNumberRatioDiff2["legend"]>()

  const config = $derived<Partial<SunspotNumberRatioDiff2>>({
    figSize,
    lineRatio,
    lineDiff,
    title,
    xaxis,
    yaxisRatio,
    yaxisDiff,
    legend,
  })
</script>

<ConfigPage
  {defaultConfig}
  {configPattern}
  schema={schemaSunspotNumberRatioDiff2}
  {config}
  {getFilesConfig}
  getConfig={getConfigRatioDiff2}
  postConfig={postConfigRatioDiff2}
  postPreview={postPreviewRatioDiff2}
>
  {#snippet configForm(currentConfig, fonts)}
    {#snippet tabPageFigSize()}
      <FigSize init={currentConfig["figSize"]} bind:value={figSize} />
    {/snippet}
    {#snippet tabPageLineRatio()}
      <Line init={currentConfig["lineRatio"]} bind:value={lineRatio} />
    {/snippet}
    {#snippet tabPageLineDiff()}
      <Line init={currentConfig["lineDiff"]} bind:value={lineDiff} />
    {/snippet}
    {#snippet tabPageTitle()}
      <Title init={currentConfig["title"]} {fonts} bind:value={title} />
    {/snippet}
    {#snippet tabPageXAxis()}
      <Axis init={currentConfig["xaxis"]} {fonts} bind:value={xaxis} />
    {/snippet}
    {#snippet tabPageYAxisRatio()}
      <Axis
        init={currentConfig["yaxisRatio"]}
        {fonts}
        bind:value={yaxisRatio}
      />
    {/snippet}
    {#snippet tabPageYAxisDiff()}
      <Axis init={currentConfig["yaxisDiff"]} {fonts} bind:value={yaxisDiff} />
    {/snippet}
    {#snippet tabPageLegend()}
      <Legend init={currentConfig["legend"]} {fonts} bind:value={legend} />
    {/snippet}
    <Tab
      titles={[
        "FigSize",
        "Line Ratio",
        "Line Diff",
        "Title",
        "X Axis",
        "Y Ratio Axis",
        "Y Diff Axis",
        "Legend",
      ]}
      pages={[
        tabPageFigSize,
        tabPageLineRatio,
        tabPageLineDiff,
        tabPageTitle,
        tabPageXAxis,
        tabPageYAxisRatio,
        tabPageYAxisDiff,
        tabPageLegend,
      ]}
    />
  {/snippet}
</ConfigPage>
