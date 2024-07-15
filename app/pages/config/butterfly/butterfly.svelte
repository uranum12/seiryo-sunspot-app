<script lang="ts">
  import type { InferOutput } from "valibot"

  import { getConfig, postConfig, postPreview } from "@/api/config"
  import { getFiles } from "@/api/files"
  import Axis from "@/components/config/axis.svelte"
  import FigSize from "@/components/config/fig_size.svelte"
  import Image from "@/components/config/image.svelte"
  import Index from "@/components/config/index.svelte"
  import Title from "@/components/config/title.svelte"
  import Tab from "@/components/tab.svelte"
  import ConfigPage from "@/pages/common/config.svelte"
  // biome-ignore lint/style/useImportType: biome dosen't support html template yet.
  import { schemaButterfyDiagram } from "@/schemas/butterfly"

  type ButterflyDiagram = InferOutput<typeof schemaButterfyDiagram>

  const defaultConfig = "config/butterfly/butterfly.json"
  const configPattern = /^config\/butterfly\/butterfly\//

  const getFilesConfig = () => {
    return getFiles({
      path: "config/butterfly/butterfly",
      glob: "*.json",
    })
  }

  const getConfigButterfly = (
    params: Parameters<typeof getConfig>[1]
  ): ReturnType<typeof getConfig<ButterflyDiagram>> => {
    return getConfig("/api/butterfly/config/butterfly", params)
  }

  const postConfigButterfly = (
    body: Parameters<typeof postConfig<ButterflyDiagram>>[1]
  ): ReturnType<typeof postConfig> => {
    return postConfig("/api/butterfly/config/butterfly", body)
  }

  const postPreviewButterfly = (
    body: Parameters<typeof postPreview<ButterflyDiagram>>[1]
  ): ReturnType<typeof postPreview> => {
    return postPreview("/api/butterfly/config/butterfly/preview", body)
  }

  let figSize = $state<ButterflyDiagram["figSize"]>()
  let index = $state<ButterflyDiagram["index"]>()
  let image = $state<ButterflyDiagram["image"]>()
  let title = $state<ButterflyDiagram["title"]>()
  let xaxis = $state<ButterflyDiagram["xaxis"]>()
  let yaxis = $state<ButterflyDiagram["yaxis"]>()

  const config = $derived<Partial<ButterflyDiagram>>({
    figSize,
    index,
    image,
    title,
    xaxis,
    yaxis,
  })
</script>

<ConfigPage
  {defaultConfig}
  {configPattern}
  schema={schemaButterfyDiagram}
  {config}
  {getFilesConfig}
  getConfig={getConfigButterfly}
  postConfig={postConfigButterfly}
  postPreview={postPreviewButterfly}
>
  {#snippet configForm(currentConfig, fonts)}
    {#snippet tabPageFigSize()}
      <FigSize init={currentConfig["figSize"]} bind:value={figSize} />
    {/snippet}
    {#snippet tabPageIndex()}
      <Index init={currentConfig["index"]} bind:value={index} />
    {/snippet}
    {#snippet tabPageImage()}
      <Image init={currentConfig["image"]} bind:value={image} />
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
        "Index Interval",
        "Image",
        "Title",
        "X Axis",
        "Y Axis",
      ]}
      pages={[
        tabPageFigSize,
        tabPageIndex,
        tabPageImage,
        tabPageTitle,
        tabPageXAxis,
        tabPageYAxis,
      ]}
    />
  {/snippet}
</ConfigPage>
