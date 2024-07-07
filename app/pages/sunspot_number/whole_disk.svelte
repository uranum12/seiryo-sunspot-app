<script lang="ts">
  import { getFiles } from "@/api/files"
  import DrawPage from "@/pages/common/draw.svelte"

  const defaultConfig = "config/sunspot_number/whole_disk.json"

  const imageAlt = "sunspot number whole-disk"

  const getFilesDraw = () => {
    return getFiles({ path: "out/sunspot", glob: "*/monthly.parquet" })
  }

  const getFilesConfig = () => {
    return getFiles({
      path: "config/sunspot_number/whole_disk",
      glob: "*.json",
    })
  }

  const drawApiPath = "/api/sunspot_number/draw/whole_disk"
</script>

<DrawPage
  {defaultConfig}
  {imageAlt}
  {getFilesDraw}
  {getFilesConfig}
  {drawApiPath}
/>
