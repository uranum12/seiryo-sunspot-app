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
  import { schemaSunspotNumberScatter } from "@/schemas/sunspot_number_with_silso"

  type SunspotNumberScatter = InferOutput<typeof schemaSunspotNumberScatter>

  const defaultConfig = "config/sunspot_number/scatter.json"
  const configPattern = /^config\/sunspot_number\/scatter\//

  const getFilesConfig = () => {
    return getFiles({
      path: "config/sunspot_number/scatter",
      glob: "*.json",
    })
  }

  const getConfigScatter = (
    params: Parameters<typeof getConfig>[1]
  ): ReturnType<typeof getConfig<SunspotNumberScatter>> => {
    return getConfig("/api/sunspot_number/with_silso/config/scatter", params)
  }

  const postConfigScatter = (
    body: Parameters<typeof postConfig<SunspotNumberScatter>>[1]
  ): ReturnType<typeof postConfig> => {
    return postConfig("/api/sunspot_number/with_silso/config/scatter", body)
  }

  const postPreviewScatter = (
    body: Parameters<typeof postPreview<SunspotNumberScatter>>[1]
  ): ReturnType<typeof postPreview> => {
    return postPreview(
      "/api/sunspot_number/with_silso/config/scatter/preview",
      body
    )
  }

  let figSize = $state<SunspotNumberScatter["figSize"]>()
  let lineFactor = $state<SunspotNumberScatter["lineFactor"]>()
  let scatter = $state<SunspotNumberScatter["scatter"]>()
  let textFactor = $state<SunspotNumberScatter["textFactor"]>()
  let textR2 = $state<SunspotNumberScatter["textR2"]>()
  let title = $state<SunspotNumberScatter["title"]>()
  let xaxis = $state<SunspotNumberScatter["xaxis"]>()
  let yaxis = $state<SunspotNumberScatter["yaxis"]>()

  const config = $derived<Partial<SunspotNumberScatter>>({
    figSize,
    lineFactor,
    scatter,
    textFactor,
    textR2,
    title,
    xaxis,
    yaxis,
  })
</script>

<ConfigPage
  {defaultConfig}
  {configPattern}
  schema={schemaSunspotNumberScatter}
  {config}
  {getFilesConfig}
  getConfig={getConfigScatter}
  postConfig={postConfigScatter}
  postPreview={postPreviewScatter}
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
    {#snippet tabPageScatter()}
      <Scatter
        init={currentConfig["scatter"]}
        labelHidden
        bind:value={scatter}
      />
    {/snippet}
    {#snippet tabPageTextFactor()}
      <Text
        init={currentConfig["textFactor"]}
        {fonts}
        bind:value={textFactor}
      />
    {/snippet}
    {#snippet tabPageTextR2()}
      <Text init={currentConfig["textR2"]} {fonts} bind:value={textR2} />
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
        "Scatter",
        "Factor Text",
        "R2 Text",
        "Title",
        "X Axis",
        "Y Axis",
      ]}
      pages={[
        tabPageFigSize,
        tabPageLineFactor,
        tabPageScatter,
        tabPageTextFactor,
        tabPageTextR2,
        tabPageTitle,
        tabPageXAxis,
        tabPageYAxis,
      ]}
    />
  {/snippet}
</ConfigPage>
