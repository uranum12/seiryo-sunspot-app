<script lang="ts">
  import DrawPage from "@/pages/common/draw.svelte"

  import {
    getFilesConfigHemispheric as getFilesConfig,
    getFilesDraw,
  } from "./api/files"

  const defaultConfig = "config/sunspot_number/hemispheric.json"

  const imageAlt = "sunspot number hemispheric"

  const drawApiPath = "/api/sunspot_number/draw/hemispheric"
</script>

<DrawPage
  {defaultConfig}
  {imageAlt}
  {getFilesDraw}
  {getFilesConfig}
  {drawApiPath}
/>
