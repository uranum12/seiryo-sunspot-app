<script lang="ts">
  import DrawPage from "@/pages/common/draw.svelte"

  import { getFilesConfig, getFilesDraw } from "./api/files"

  const defaultConfig = "config/butterfly/butterfly.json"

  const imageAlt = "butterfly diagram"

  const drawApiPath = "/api/butterfly/draw/butterfly"
</script>

<DrawPage
  {defaultConfig}
  {imageAlt}
  {getFilesDraw}
  {getFilesConfig}
  {drawApiPath}
/>
