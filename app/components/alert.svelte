<script lang="ts">
  import clsx from "clsx"
  import type { Snippet } from "svelte"

  type Props = {
    type: "success" | "warning" | "error"
    class?: string
    children: Snippet
  }

  let { type: severity, class: className, children }: Props = $props()
</script>

<div
  class={clsx(
    "rounded border px-4 py-3",
    severity === "success" && "border-green-400",
    severity === "warning" && "border-yellow-400",
    severity === "error" && "border-red-400",
    className
  )}
>
  {@render children()}
</div>
