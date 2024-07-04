<script lang="ts">
  import type { Snippet } from "svelte"

  type Props = {
    children: Snippet
  }

  let { children }: Props = $props()
</script>

<div class="mx-auto my-4 max-w-5xl">
  {@render children()}
</div>
