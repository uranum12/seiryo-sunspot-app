<script lang="ts">
  import DrawPage from "@/pages/common/draw.svelte"

  import {
    getFilesConfigWholeDisk as getFilesConfig,
    getFilesDraw,
  } from "./api/files"

  const defaultConfig = "config/sunspot_number/whole_disk.json"

  const imageAlt = "sunspot number whole-disk"

  const drawApiPath = "/api/sunspot_number/draw/whole_disk"
</script>

<DrawPage
  {defaultConfig}
  {imageAlt}
  {getFilesDraw}
  {getFilesConfig}
  {drawApiPath}
/>
