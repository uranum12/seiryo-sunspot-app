<script lang="ts">
  import { getFiles } from "@/api/files"
  import DrawPage from "@/pages/common/draw.svelte"

  const defaultConfig = "config/observations/monthly.json"

  const imageAlt = "observations monthly"

  const getFilesDraw = () => {
    return getFiles({ path: "out/observations", glob: "*/monthly.parquet" })
  }

  const getFilesConfig = () => {
    return getFiles({ path: "config/observations/monthly", glob: "*.json" })
  }

  const drawApiPath = "/api/observations/draw/monthly"
</script>

<DrawPage
  {defaultConfig}
  {imageAlt}
  {getFilesDraw}
  {getFilesConfig}
  {drawApiPath}
/>
