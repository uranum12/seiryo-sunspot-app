<script lang="ts">
  import { getFiles } from "@/api/files"
  import DrawPage from "@/pages/common/draw.svelte"

  const defaultConfig = "config/butterfly/butterfly.json"

  const imageAlt = "butterfly diagram"

  const getFilesDraw = () => {
    return getFiles({ path: "out/butterfly", glob: "**/*.npz" })
  }

  const getFilesConfig = () => {
    return getFiles({ path: "config/butterfly/butterfly", glob: "*.json" })
  }

  const drawApiPath = "/api/butterfly/draw/butterfly"
</script>

<DrawPage
  {defaultConfig}
  {imageAlt}
  {getFilesDraw}
  {getFilesConfig}
  {drawApiPath}
/>
