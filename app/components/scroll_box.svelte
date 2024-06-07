<div class="scroll-box">
  <slot />
</div>

<style>
  .scroll-box {
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 0 1rem;
    max-height: 32rem;
    overflow-y: auto;
  }
</style>
