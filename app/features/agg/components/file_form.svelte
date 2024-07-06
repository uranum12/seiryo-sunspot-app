<script lang="ts" context="module">
  export type FormInput = {
    files: string[]
    filename: string
    overwrite: boolean
  }
</script>

<script lang="ts">
  import { untrack } from "svelte"

  import Accordion from "@/components/accordion.svelte"
  import Alert from "@/components/alert.svelte"
  import ConfirmDialog from "@/components/confirm_dialog.svelte"

  type Props = {
    files: string[]
    onSubmit: (input: FormInput) => void
  }

  let { files, onSubmit }: Props = $props()

  let selected = $state<string[]>([])
  let filename = $state<string>("")
  let overwrite = $state<boolean>(false)

  let filtered = $state<string[]>(files.sort())
  let checked = $state<string[]>([])
  let filter = $state<string>("")

  const hidden = $derived(files.filter((file) => !filtered.includes(file)))

  $effect(() => {
    selected = untrack<string[]>(() => selected)
      .filter((file) => hidden.includes(file))
      .concat(checked)
  })

  let showConfirmOverwrite = $state<boolean>(false)

  const fileSelectInvalid = $derived(selected.length === 0)

  const submitDisabled = $derived(fileSelectInvalid || filename.trim() === "")

  const filterApply = () => {
    filtered = files.filter((file) =>
      file.replace(/^data\//, "").includes(filter)
    )
    checked = selected.filter((file) => filtered.includes(file))
  }

  const filterClear = () => {
    filter = ""
    filterApply()
  }

  const selectAll = () => {
    checked = filtered
  }

  const deselectAll = () => {
    checked = []
  }

  const submit = () => {
    onSubmit({ files: selected, filename, overwrite })
  }

  const onClickSubmit = () => {
    if (overwrite) {
      showConfirmOverwrite = true
    } else {
      submit()
    }
  }

  const confirmOverwrite = () => {
    submit()
  }
</script>

<section>
  <Accordion class="mb-1" summary="filter">
    <input bind:value={filter} class="mb-1" />
    <button onclick={filterApply}>apply</button>
    <button onclick={filterClear}>clear</button>
  </Accordion>

  {#if filtered.length === 0}
    <Alert type="warning">
      <p>no files matched</p>
    </Alert>
  {:else}
    <div class="mb-1">
      <button onclick={selectAll}>select all files</button>
      <button onclick={deselectAll}>deselect all files</button>
    </div>

    <div
      class="mb-1 max-h-96 overflow-y-auto rounded border border-gray-300 p-2"
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

  <input
    class="mb-1"
    placeholder="output file name"
    required
    bind:value={filename}
  />
  <label class="mb-1">
    <input type="checkbox" bind:checked={overwrite} />
    <span>Overwrite</span>
  </label>
  <button disabled={submitDisabled} onclick={onClickSubmit}>submit</button>
</section>

<ConfirmDialog bind:isOpen={showConfirmOverwrite} onConfirm={confirmOverwrite}>
  Are you sure you want me to overwrite file {filename}.parquet ?
</ConfirmDialog>
