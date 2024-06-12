<details>
  <summary>
    <slot name="summary" />
  </summary>
  <div>
    <slot />
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
