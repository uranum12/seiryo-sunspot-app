<script lang="ts">
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

<div class="{className} space-y-1">
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
      class="max-h-96 overflow-y-auto rounded border border-gray-300 p-2"
      class:!border-red-300={fileSelectInvalid}
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
