<script lang="ts">
  import type { Snippet } from "svelte"

  type Props = {
    summary: string
    class?: string
    children: Snippet
  }

  let { summary, class: className, children }: Props = $props()
</script>

<details class="{className} w-full border rounded border-gray-300 group">
  <summary
    class="p-2 border-gray-300 focus:outline-blue-500 group-open:border-b"
  >
    {summary}
  </summary>
  <div class="p-2">
    {@render children()}
  </div>
</details>
