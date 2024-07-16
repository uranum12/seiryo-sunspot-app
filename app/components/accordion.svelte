<script lang="ts">
  import clsx from "clsx"
  import type { Snippet } from "svelte"

  type Props = {
    summary: string
    class?: string
    children: Snippet
  }

  let { summary, class: className, children }: Props = $props()
</script>

<details class={clsx("group w-full rounded border border-gray-300", className)}>
  <summary
    class="border-gray-300 p-2 focus:outline-blue-500 group-open:border-b"
  >
    {summary}
  </summary>
  <div class="p-2">
    {@render children()}
  </div>
</details>
