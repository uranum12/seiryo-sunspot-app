<script lang="ts">
  import clsx from "clsx"
  import type { Snippet } from "svelte"

  type Props = {
    titles: string[]
    pages: Snippet[]
  }

  let { titles, pages }: Props = $props()

  let tabNumber = $state<number>(0)

  const tabClick = (i: number) => {
    tabNumber = i
  }
</script>

<div>
  <div class="px-2">
    <div class="scrollbar-none flex gap-x-2 overflow-x-auto whitespace-nowrap">
      {#each titles as title, i}
        <button
          class={clsx(
            "rounded-b-none border-2 border-b-0",
            tabNumber === i ? "border-blue-300" : "border-gray-300"
          )}
          onclick={() => tabClick(i)}
        >
          {title}
        </button>
      {/each}
    </div>
  </div>
  <div class="rounded border border-gray-300 p-2">
    {#each pages as page, i}
      <div class:hidden={tabNumber !== i}>
        {@render page()}
      </div>
    {/each}
  </div>
</div>
