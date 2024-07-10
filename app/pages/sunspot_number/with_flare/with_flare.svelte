<script lang="ts">
  import { getFiles } from "@/api/files"
  import DrawPage from "@/pages/common/draw.svelte"

  const defaultConfig = "config/sunspot_number/with_flare.json"

  const imageAlt = "sunspot number with Flare Index"

  const getFilesDraw = () => {
    return getFiles({
      path: "out/sunspot_with_flare",
      glob: "*/with_flare.parquet",
    })
  }

  const getFilesConfig = () => {
    return getFiles({
      path: "config/sunspot_number/with_flare",
      glob: "*.json",
    })
  }

  const drawApiPath = "/api/sunspot_number/with_flare/draw/with_flare"
</script>

<DrawPage
  {defaultConfig}
  {imageAlt}
  {getFilesDraw}
  {getFilesConfig}
  {drawApiPath}
/>
