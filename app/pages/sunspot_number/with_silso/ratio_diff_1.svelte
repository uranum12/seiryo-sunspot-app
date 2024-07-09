<script lang="ts">
  import { getFiles } from "@/api/files"
  import DrawPage from "@/pages/common/draw.svelte"

  const defaultConfig = "config/sunspot_number/ratio_diff_1.json"

  const imageAlt = "sunspot number ratio and difference"

  const getFilesDraw = () => {
    return getFiles({
      path: "out/sunspot_with_silso",
      glob: "*/ratio_diff.parquet",
    })
  }

  const getFilesConfig = () => {
    return getFiles({
      path: "config/sunspot_number/ratio_diff_1",
      glob: "*.json",
    })
  }

  const drawApiPath = "/api/sunspot_number/with_silso/draw/ratio_diff_1"
</script>

<DrawPage
  {defaultConfig}
  {imageAlt}
  {getFilesDraw}
  {getFilesConfig}
  {drawApiPath}
/>
