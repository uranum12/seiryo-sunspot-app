<script lang="ts">
  import type { InferOutput } from "valibot"

  import { getConfig, postConfig, postPreview } from "@/api/config"
  import { getFiles } from "@/api/files"
  import Axis from "@/components/config/axis.svelte"
  import FigSize from "@/components/config/fig_size.svelte"
  import Line from "@/components/config/line.svelte"
  import Scatter from "@/components/config/scatter.svelte"
  import Text from "@/components/config/text.svelte"
  import Title from "@/components/config/title.svelte"
  import Tab from "@/components/tab.svelte"
  import ConfigPage from "@/pages/common/config.svelte"
  // biome-ignore lint/style/useImportType: biome dosen't support html template yet.
  import { schemaSunspotNumberRatioDiff1 } from "@/schemas/sunspot_number_with_silso"

  type SunspotNumberRatioDiff1 = InferOutput<
    typeof schemaSunspotNumberRatioDiff1
  >

  const defaultConfig = "config/sunspot_number/ratio_diff_1.json"
  const configPattern = /^config\/sunspot_number\/ratio_diff_1\//

  const getFilesConfig = () => {
    return getFiles({
      path: "config/sunspot_number/ratio_diff_1",
      glob: "*.json",
    })
  }

  const getConfigRatioDiff1 = (
    params: Parameters<typeof getConfig>[1]
  ): ReturnType<typeof getConfig<SunspotNumberRatioDiff1>> => {
    return getConfig(
      "/api/sunspot_number/with_silso/config/ratio_diff_1",
      params
    )
  }

  const postConfigRatioDiff1 = (
    body: Parameters<typeof postConfig<SunspotNumberRatioDiff1>>[1]
  ): ReturnType<typeof postConfig> => {
    return postConfig(
      "/api/sunspot_number/with_silso/config/ratio_diff_1",
      body
    )
  }

  const postPreviewRatioDiff1 = (
    body: Parameters<typeof postPreview<SunspotNumberRatioDiff1>>[1]
  ): ReturnType<typeof postPreview> => {
    return postPreview(
      "/api/sunspot_number/with_silso/config/ratio_diff_1/preview",
      body
    )
  }

  let figSize = $state<SunspotNumberRatioDiff1["figSize"]>()
  let lineFactor = $state<SunspotNumberRatioDiff1["lineFactor"]>()
  let lineRatio = $state<SunspotNumberRatioDiff1["lineRatio"]>()
  let lineDiff = $state<SunspotNumberRatioDiff1["lineDiff"]>()
  let titleRatio = $state<SunspotNumberRatioDiff1["titleRatio"]>()
  let titleDiff = $state<SunspotNumberRatioDiff1["titleDiff"]>()
  let xaxis = $state<SunspotNumberRatioDiff1["xaxis"]>()
  let yaxisRatio = $state<SunspotNumberRatioDiff1["yaxisRatio"]>()
  let yaxisDiff = $state<SunspotNumberRatioDiff1["yaxisDiff"]>()

  const config = $derived<Partial<SunspotNumberRatioDiff1>>({
    figSize,
    lineFactor,
    lineRatio,
    lineDiff,
    titleRatio,
    titleDiff,
    xaxis,
    yaxisRatio,
    yaxisDiff,
  })
</script>

<ConfigPage
  {defaultConfig}
  {configPattern}
  schema={schemaSunspotNumberRatioDiff1}
  {config}
  {getFilesConfig}
  getConfig={getConfigRatioDiff1}
  postConfig={postConfigRatioDiff1}
  postPreview={postPreviewRatioDiff1}
>
  {#snippet configForm(currentConfig, fonts)}
    {#snippet tabPageFigSize()}
      <FigSize init={currentConfig["figSize"]} bind:value={figSize} />
    {/snippet}
    {#snippet tabPageLineFactor()}
      <Line
        init={currentConfig["lineFactor"]}
        labelHidden
        bind:value={lineFactor}
      />
    {/snippet}
    {#snippet tabPageLineRatio()}
      <Line
        init={currentConfig["lineRatio"]}
        labelHidden
        bind:value={lineRatio}
      />
    {/snippet}
    {#snippet tabPageLineDiff()}
      <Line
        init={currentConfig["lineDiff"]}
        labelHidden
        bind:value={lineDiff}
      />
    {/snippet}
    {#snippet tabPageTitleRatio()}
      <Title
        init={currentConfig["titleRatio"]}
        {fonts}
        bind:value={titleRatio}
      />
    {/snippet}
    {#snippet tabPageTitleDiff()}
      <Title init={currentConfig["titleDiff"]} {fonts} bind:value={titleDiff} />
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
    <Tab
      titles={[
        "FigSize",
        "Line Factor",
        "Line Ratio",
        "Line Diff",
        "Title Ratio",
        "Title Diff",
        "X Axis",
        "Y Ratio Axis",
        "Y Diff Axis",
      ]}
      pages={[
        tabPageFigSize,
        tabPageLineFactor,
        tabPageLineRatio,
        tabPageLineDiff,
        tabPageTitleRatio,
        tabPageTitleDiff,
        tabPageXAxis,
        tabPageYAxisRatio,
        tabPageYAxisDiff,
      ]}
    />
  {/snippet}
</ConfigPage>
