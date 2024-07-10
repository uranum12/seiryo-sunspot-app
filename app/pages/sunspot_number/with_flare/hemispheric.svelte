<script lang="ts">
  import { getFiles } from "@/api/files"
  import DrawPage from "@/pages/common/draw.svelte"

  const defaultConfig = "config/sunspot_number/with_flare_hemispheric.json"

  const imageAlt = "sunspot number with Flare Index Hemispheric"

  const getFilesDraw = () => {
    return getFiles({
      path: "out/sunspot_with_flare",
      glob: "*/with_flare.parquet",
    })
  }

  const getFilesConfig = () => {
    return getFiles({
      path: "config/sunspot_number/with_flare_hemispheric",
      glob: "*.json",
    })
  }

  const drawApiPath = "/api/sunspot_number/with_flare/draw/hemispheric"
</script>

<DrawPage
  {defaultConfig}
  {imageAlt}
  {getFilesDraw}
  {getFilesConfig}
  {drawApiPath}
/>
