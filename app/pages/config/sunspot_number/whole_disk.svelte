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
  import { schemaSunspotNumberWholeDisk } from "@/schemas/sunspot_number"

  type SunspotNumberWholeDisk = InferOutput<typeof schemaSunspotNumberWholeDisk>

  const defaultConfig = "config/sunspot_number/whole_disk.json"
  const configPattern = /^config\/sunspot_number\/whole_disk\//

  const getFilesConfig = () => {
    return getFiles({
      path: "config/sunspot_number/whole_disk",
      glob: "*.json",
    })
  }

  const getConfigWholeDisk = (
    params: Parameters<typeof getConfig>[1]
  ): ReturnType<typeof getConfig<SunspotNumberWholeDisk>> => {
    return getConfig("/api/sunspot_number/config/whole_disk", params)
  }

  const postConfigWholeDisk = (
    body: Parameters<typeof postConfig<SunspotNumberWholeDisk>>[1]
  ): ReturnType<typeof postConfig> => {
    return postConfig("/api/sunspot_number/config/whole_disk", body)
  }

  const postPreviewWholeDisk = (
    body: Parameters<typeof postPreview<SunspotNumberWholeDisk>>[1]
  ): ReturnType<typeof postPreview> => {
    return postPreview("/api/sunspot_number/config/whole_disk/preview", body)
  }

  let figSize = $state<SunspotNumberWholeDisk["figSize"]>()
  let line = $state<SunspotNumberWholeDisk["line"]>()
  let title = $state<SunspotNumberWholeDisk["title"]>()
  let xaxis = $state<SunspotNumberWholeDisk["xaxis"]>()
  let yaxis = $state<SunspotNumberWholeDisk["yaxis"]>()

  const config = $derived<Partial<SunspotNumberWholeDisk>>({
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
  schema={schemaSunspotNumberWholeDisk}
  {config}
  {getFilesConfig}
  getConfig={getConfigWholeDisk}
  postConfig={postConfigWholeDisk}
  postPreview={postPreviewWholeDisk}
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
