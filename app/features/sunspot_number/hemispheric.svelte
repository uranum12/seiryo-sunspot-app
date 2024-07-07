<script lang="ts">
  import { getFiles } from "@/api/files"
  import DrawPage from "@/pages/common/draw.svelte"

  const defaultConfig = "config/sunspot_number/hemispheric.json"

  const imageAlt = "sunspot number hemispheric"

  const getFilesDraw = () => {
    return getFiles({ path: "out/sunspot", glob: "*/monthly.parquet" })
  }

  const getFilesConfig = () => {
    return getFiles({
      path: "config/sunspot_number/hemispheric",
      glob: "*.json",
    })
  }

  const drawApiPath = "/api/sunspot_number/draw/hemispheric"
</script>

<DrawPage
  {defaultConfig}
  {imageAlt}
  {getFilesDraw}
  {getFilesConfig}
  {drawApiPath}
/>
