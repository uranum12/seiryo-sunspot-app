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
  import { schemaSunspotNumberRatio } from "@/schemas/sunspot_number_with_silso"

  type SunspotNumberRatio = InferOutput<typeof schemaSunspotNumberRatio>

  const defaultConfig = "config/sunspot_number/ratio.json"
  const configPattern = /^config\/sunspot_number\/ratio\//

  const getFilesConfig = () => {
    return getFiles({
      path: "config/sunspot_number/ratio",
      glob: "*.json",
    })
  }

  const getConfigRatio = (
    params: Parameters<typeof getConfig>[1]
  ): ReturnType<typeof getConfig<SunspotNumberRatio>> => {
    return getConfig("/api/sunspot_number/with_silso/config/ratio", params)
  }

  const postConfigRatio = (
    body: Parameters<typeof postConfig<SunspotNumberRatio>>[1]
  ): ReturnType<typeof postConfig> => {
    return postConfig("/api/sunspot_number/with_silso/config/ratio", body)
  }

  const postPreviewRatio = (
    body: Parameters<typeof postPreview<SunspotNumberRatio>>[1]
  ): ReturnType<typeof postPreview> => {
    return postPreview(
      "/api/sunspot_number/with_silso/config/ratio/preview",
      body
    )
  }

  let figSize = $state<SunspotNumberRatio["figSize"]>()
  let lineFactor = $state<SunspotNumberRatio["lineFactor"]>()
  let lineRatio = $state<SunspotNumberRatio["lineRatio"]>()
  let title = $state<SunspotNumberRatio["title"]>()
  let xaxis = $state<SunspotNumberRatio["xaxis"]>()
  let yaxis = $state<SunspotNumberRatio["yaxis"]>()

  const config = $derived<Partial<SunspotNumberRatio>>({
    figSize,
    lineFactor,
    lineRatio,
    title,
    xaxis,
    yaxis,
  })
</script>

<ConfigPage
  {defaultConfig}
  {configPattern}
  schema={schemaSunspotNumberRatio}
  {config}
  {getFilesConfig}
  getConfig={getConfigRatio}
  postConfig={postConfigRatio}
  postPreview={postPreviewRatio}
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
      titles={[
        "FigSize",
        "Line Factor",
        "Line Ratio",
        "Title",
        "X Axis",
        "Y Axis",
      ]}
      pages={[
        tabPageFigSize,
        tabPageLineFactor,
        tabPageLineRatio,
        tabPageTitle,
        tabPageXAxis,
        tabPageYAxis,
      ]}
    />
  {/snippet}
</ConfigPage>
