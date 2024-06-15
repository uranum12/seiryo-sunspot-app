<script lang="ts">
  import type { Snippet } from "svelte"

  type Props = {
    children: Snippet
  }

  let { children }: Props = $props()
</script>

<div class="container">
  {@render children()}
</div>

<style>
  .container {
    margin: 1rem auto;
    max-width: 64rem;
  }
</style>
