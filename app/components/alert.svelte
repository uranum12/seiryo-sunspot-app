<script lang="ts">
  import type { Snippet } from "svelte"

  type Props = {
    type: "success" | "warning" | "error"
    class?: string
    children: Snippet
  }

  let { type: severity, class: className, children }: Props = $props()
</script>

<div
  class="{className} border rounded px-4 py-3"
  class:border-green-400={severity === "success"}
  class:border-yellow-400={severity === "warning"}
  class:border-red-400={severity === "error"}
>
  {@render children()}
</div>
