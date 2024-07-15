<script lang="ts">
  import type { InferOutput } from "valibot"

  import { getConfig, postConfig, postPreview } from "@/api/config"
  import { getFiles } from "@/api/files"
  import Cmap from "@/components/config/cmap.svelte"
  import ConfigPage from "@/pages/common/config.svelte"
  // biome-ignore lint/style/useImportType: biome dosen't support html template yet.
  import { schemaColorMap } from "@/schemas/butterfly"

  type ColorMap = InferOutput<typeof schemaColorMap>

  const defaultConfig = "config/butterfly/color_map.json"
  const configPattern = /^config\/butterfly\/color_map\//

  const getFilesConfig = () => {
    return getFiles({
      path: "config/butterfly/color_map",
      glob: "*.json",
    })
  }

  const getConfigColorMap = (
    params: Parameters<typeof getConfig>[1]
  ): ReturnType<typeof getConfig<ColorMap>> => {
    return getConfig("/api/butterfly/config/color_map", params)
  }

  const postConfigColorMap = (
    body: Parameters<typeof postConfig<ColorMap>>[1]
  ): ReturnType<typeof postConfig> => {
    return postConfig("/api/butterfly/config/color_map", body)
  }

  const postPreviewColorMap = (
    body: Parameters<typeof postPreview<ColorMap>>[1]
  ): ReturnType<typeof postPreview> => {
    return postPreview("/api/butterfly/config/color_map/preview", body)
  }

  let cmap = $state<ColorMap["cmap"]>()

  const config = $derived<Partial<ColorMap>>({ cmap })
</script>

<ConfigPage
  {defaultConfig}
  {configPattern}
  schema={schemaColorMap}
  {config}
  {getFilesConfig}
  getConfig={getConfigColorMap}
  postConfig={postConfigColorMap}
  postPreview={postPreviewColorMap}
>
  {#snippet configForm(currentConfig, _)}
    <Cmap init={currentConfig["cmap"]} bind:value={cmap} />
  {/snippet}
</ConfigPage>
