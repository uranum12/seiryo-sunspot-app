<script lang="ts">
  import { getFiles } from "@/api/files"
  import AggCommon from "@/pages/butterfly/agg_common.svelte"

  const postUrl = "/api/butterfly/fromtext"

  const getFilesAgg = () => {
    return getFiles({ path: "data", glob: "*.txt" })
  }
</script>

<AggCommon {postUrl} {getFilesAgg} />
