<script lang="ts">
  import type { Snippet } from "svelte"

  type Props = {
    severity: "success" | "warning" | "error"
    children: Snippet
  }

  let { severity, children }: Props = $props()
</script>

<div class="alert {severity}">
  {@render children()}
</div>

<style>
  .alert {
    border: 1px solid;
    border-radius: 4px;
    padding: 0 1rem;
  }

  .success {
    border-color: limegreen;
  }

  .warning {
    border-color: orange;
  }

  .error {
    border-color: coral;
  }
</style>
