<script lang="ts">
  import clsx from "clsx"
  import { untrack } from "svelte"

  import Alert from "@/components/alert.svelte"
  import Filter from "@/components/filter.svelte"

  type Props = {
    class?: string
    files: string[]
    selected: string[]
  }

  let { class: className, files, selected = $bindable() }: Props = $props()

  let checked = $state<string[]>([])
  let filter = $state<string>("")

  const filtered = $derived(
    files.filter((file) => file.replace(/^data\//, "").includes(filter)).sort()
  )
  const hidden = $derived(files.filter((file) => !filtered.includes(file)))
  const fileSelectInvalid = $derived(selected.length === 0)

  $effect(() => {
    checked = filtered.filter((file) => untrack(() => selected).includes(file))
  })

  $effect(() => {
    selected = untrack<string[]>(() => selected)
      .filter((file) => hidden.includes(file))
      .concat(checked)
  })

  const selectAll = () => {
    checked = filtered
  }

  const deselectAll = () => {
    checked = []
  }
</script>

<div class={clsx("space-y-1", className)}>
  <Filter bind:filter />
  {#if filtered.length === 0}
    <Alert type="warning">
      <p>no files matched</p>
    </Alert>
  {:else}
    <div>
      <button onclick={selectAll}>select all files</button>
      <button onclick={deselectAll}>deselect all files</button>
    </div>

    <div
      class={clsx(
        "max-h-96 overflow-y-auto rounded border p-2",
        fileSelectInvalid ? "border-red-300" : "border-gray-300"
      )}
    >
      {#each filtered as file}
        <label>
          <input type="checkbox" bind:group={checked} value={file} />
          <span class="ml-1">{file.replace(/^data\//, "")}</span>
        </label>
      {/each}
    </div>
  {/if}
</div>
