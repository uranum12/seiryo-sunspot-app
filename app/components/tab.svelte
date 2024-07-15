<script lang="ts">
  import type { Snippet } from "svelte"

  type Props = {
    titles: string[]
    pages: Snippet[]
    class?: string
  }

  let { titles, pages, class: className }: Props = $props()

  let tabNumber = $state<number>(0)

  const tabClick = (i: number) => {
    tabNumber = i
  }
</script>

<div class={className}>
  <div class="flex gap-x-2 px-2">
    {#each titles as title, i}
      <button
        class="rounded-b-none border-2 border-b-0 border-gray-300"
        class:!border-blue-300={tabNumber === i}
        onclick={() => tabClick(i)}
      >
        {title}
      </button>
    {/each}
  </div>
  <div class="rounded border border-gray-300 p-2">
    {#each pages as page, i}
      <div class:hidden={tabNumber !== i}>
        {@render page()}
      </div>
    {/each}
  </div>
</div>
