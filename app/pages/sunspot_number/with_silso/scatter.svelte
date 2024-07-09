<script lang="ts">
  import { getFiles } from "@/api/files"
  import DrawPage from "@/pages/common/draw.svelte"

  const defaultConfig = "config/sunspot_number/scatter.json"

  const imageAlt = "sunspot number SILSO and seiryo scatter diagram"

  const getFilesDraw = () => {
    return getFiles({
      path: "out/sunspot_with_silso",
      glob: "*/with_silso.parquet",
    })
  }

  const getFilesConfig = () => {
    return getFiles({
      path: "config/sunspot_number/scatter",
      glob: "*.json",
    })
  }

  const drawApiPath = "/api/sunspot_number/with_silso/draw/scatter"
</script>

<DrawPage
  {defaultConfig}
  {imageAlt}
  {getFilesDraw}
  {getFilesConfig}
  {drawApiPath}
/>
