<script lang="ts">
  export let severity: "success" | "warning" | "error"
</script>

<div class="alert {severity}">
  <slot />
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
