<script lang="ts">
  type Props = {
    files: string[]
    selected: string[]
    class?: string
  }

  let { files, selected = $bindable(), class: className }: Props = $props()

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
  class="{className} space-y-1 rounded border border-gray-300 p-2"
  class:border-red-300={areaInvalid}
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
