<script lang="ts">
  import { getFiles } from "@/api/files"
  import DrawPage from "@/pages/common/draw.svelte"

  const defaultConfig = "config/sunspot_number/diff.json"

  const imageAlt = "sunspot number diff seiryo* - SILSO"

  const getFilesDraw = () => {
    return getFiles({
      path: "out/sunspot_with_silso",
      glob: "*/ratio_diff.parquet",
    })
  }

  const getFilesConfig = () => {
    return getFiles({
      path: "config/sunspot_number/diff",
      glob: "*.json",
    })
  }

  const drawApiPath = "/api/sunspot_number/with_silso/draw/diff"
</script>

<DrawPage
  {defaultConfig}
  {imageAlt}
  {getFilesDraw}
  {getFilesConfig}
  {drawApiPath}
/>
