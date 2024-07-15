<script lang="ts">
  import type { InferOutput } from "valibot"

  import { getConfig, postConfig, postPreview } from "@/api/config"
  import { getFiles } from "@/api/files"
  import Axis from "@/components/config/axis.svelte"
  import Bar from "@/components/config/bar.svelte"
  import FigSize from "@/components/config/fig_size.svelte"
  import Title from "@/components/config/title.svelte"
  import Tab from "@/components/tab.svelte"
  import ConfigPage from "@/pages/common/config.svelte"
  // biome-ignore lint/style/useImportType: biome dosen't support html template yet.
  import { schemaObservationsMonthly } from "@/schemas/observations"

  type ObservationsMonthly = InferOutput<typeof schemaObservationsMonthly>

  const defaultConfig = "config/observations/monthly.json"
  const configPattern = /^config\/observations\/monthly\//

  const getFilesConfig = () => {
    return getFiles({
      path: "config/observations/monthly",
      glob: "*.json",
    })
  }

  const getConfigMonthly = (
    params: Parameters<typeof getConfig>[1]
  ): ReturnType<typeof getConfig<ObservationsMonthly>> => {
    return getConfig("/api/observations/config/monthly", params)
  }

  const postConfigMonthly = (
    body: Parameters<typeof postConfig<ObservationsMonthly>>[1]
  ): ReturnType<typeof postConfig> => {
    return postConfig("/api/observations/config/monthly", body)
  }

  const postPreviewMonthly = (
    body: Parameters<typeof postPreview<ObservationsMonthly>>[1]
  ): ReturnType<typeof postPreview> => {
    return postPreview("/api/observations/config/monthly/preview", body)
  }

  let figSize = $state<ObservationsMonthly["figSize"]>()
  let bar = $state<ObservationsMonthly["bar"]>()
  let title = $state<ObservationsMonthly["title"]>()
  let xaxis = $state<ObservationsMonthly["xaxis"]>()
  let yaxis = $state<ObservationsMonthly["yaxis"]>()

  const config = $derived<Partial<ObservationsMonthly>>({
    figSize,
    bar,
    title,
    xaxis,
    yaxis,
  })
</script>

<ConfigPage
  {defaultConfig}
  {configPattern}
  schema={schemaObservationsMonthly}
  {config}
  {getFilesConfig}
  getConfig={getConfigMonthly}
  postConfig={postConfigMonthly}
  postPreview={postPreviewMonthly}
>
  {#snippet configForm(currentConfig, fonts)}
    {#snippet tabPageFigSize()}
      <FigSize init={currentConfig["figSize"]} bind:value={figSize} />
    {/snippet}
    {#snippet tabPageBar()}
      <Bar init={currentConfig["bar"]} labelHidden bind:value={bar} />
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
      titles={["FigSize", "Bar", "Title", "X Axis", "Y Axis"]}
      pages={[
        tabPageFigSize,
        tabPageBar,
        tabPageTitle,
        tabPageXAxis,
        tabPageYAxis,
      ]}
    />
  {/snippet}
</ConfigPage>
