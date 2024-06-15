<script lang="ts">
  import type { Snippet } from "svelte"

  type Props = {
    summary: string
    children: Snippet
  }

  let { summary, children }: Props = $props()
</script>

<details>
  <summary>
    {summary}
  </summary>
  <div>
    {@render children()}
  </div>
</details>

<style>
  details {
    box-sizing: border-box;
    border: 1px solid #ccc;
    border-radius: 4px;
    width: 100%;
    margin: 0.25rem 0;
  }
  summary {
    padding: 0.5rem;
  }
  div {
    padding: 0.5rem;
  }
  details[open] summary {
    border-bottom: 1px solid #ccc;
  }
</style>
