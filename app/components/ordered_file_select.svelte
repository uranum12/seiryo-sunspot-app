<script lang="ts">
  import clsx from "clsx"

  type Props = {
    files: string[]
    selected: string[]
  }

  let { files, selected = $bindable() }: Props = $props()

  let selectedFiles = $state<string[]>([""])

  const availableFiles = $derived(
    files.filter((file) => !selectedFiles.includes(file))
  )
  const addDisabled = $derived(
    selectedFiles[selectedFiles.length - 1].trim() === "" ||
      selectedFiles.length === files.length
  )
  const removeDisabled = $derived(selectedFiles.length <= 1)

  const areaInvalid = $derived(
    selectedFiles.filter((file) => file === "").length !== 0 ||
      selectedFiles.length === 0
  )

  $effect(() => {
    selected = selectedFiles.filter((file) => file !== "")
  })

  const addFile = () => {
    selectedFiles = [...selectedFiles, ""]
  }

  const removeLastFile = () => {
    selectedFiles = selectedFiles.slice(0, -1)
  }

  const resetFiles = () => {
    selectedFiles = [""]
  }
</script>

<div
  class={clsx(
    "space-y-1 rounded border p-2",
    areaInvalid ? "border-red-300" : "border-gray-300"
  )}
>
  {#each selectedFiles as _, index}
    <div class="flex items-baseline">
      <span class="w-8 text-lg">{`${index + 1}.`}</span>
      <select required bind:value={selectedFiles[index]}>
        <option value="" selected disabled>select file</option>
        {#each files.sort() as file}
          <option value={file} hidden={!availableFiles.includes(file)}
            >{file}</option
          >
        {/each}
      </select>
    </div>
  {/each}
  <button disabled={addDisabled} onclick={addFile}>append file</button>
  <button disabled={removeDisabled} onclick={removeLastFile}
    >remove last file</button
  >
  <button onclick={resetFiles}>reset</button>
</div>
