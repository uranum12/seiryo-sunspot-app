<script lang="ts">
  import clsx from "clsx"
  import type { Snippet } from "svelte"

  type Props = {
    type: "success" | "warning" | "error"
    children: Snippet
  }

  let { type: severity, children }: Props = $props()
</script>

<div
  class={clsx(
    "rounded border px-4 py-3",
    severity === "success" && "border-green-400",
    severity === "warning" && "border-yellow-400",
    severity === "error" && "border-red-400"
  )}
>
  {@render children()}
</div>
