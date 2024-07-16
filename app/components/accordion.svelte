<script lang="ts">
  import type { Snippet } from "svelte"

  type Props = {
    summary: string
    children: Snippet
  }

  let { summary, children }: Props = $props()
</script>

<details class="group w-full rounded border border-gray-300">
  <summary
    class="border-gray-300 p-2 focus:outline-blue-500 group-open:border-b"
  >
    {summary}
  </summary>
  <div class="p-2">
    {@render children()}
  </div>
</details>
