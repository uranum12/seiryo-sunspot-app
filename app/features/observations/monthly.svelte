<script lang="ts">
  import DrawPage from "@/pages/common/draw.svelte"

  import {
    getFilesConfigMonthly as getFilesConfig,
    getFilesDraw,
  } from "./api/files"

  const defaultConfig = "config/observations/monthly.json"

  const imageAlt = "observations monthly"

  const drawApiPath = "/api/observations/draw/monthly"
</script>

<DrawPage
  {defaultConfig}
  {imageAlt}
  {getFilesDraw}
  {getFilesConfig}
  {drawApiPath}
/>
