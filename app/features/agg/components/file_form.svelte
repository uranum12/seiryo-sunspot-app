<script lang="ts" context="module">
  export type FormInput = {
    files: string[]
    filename: string
    overwrite: boolean
  }
</script>

<script lang="ts">
  import { createEventDispatcher } from "svelte"

  import ConfirmDialog from "@/components/confirm_dialog.svelte"
  import Container from "@/components/container.svelte"

  import FilesSelector from "./files_selector.svelte"

  export let files: string[]

  const dispatch = createEventDispatcher<{ submit: FormInput }>()

  let selected: string[] = []
  let filename = ""
  let overwrite = false

  let showConfirmOverwrite = false

  let submitDisabled: boolean
  $: submitDisabled = selected.length === 0 || filename.trim() === ""

  const dispatchSubmit = () => {
    dispatch("submit", { files: selected, filename, overwrite })
  }

  const onSubmit = () => {
    if (overwrite) {
      showConfirmOverwrite = true
    } else {
      dispatchSubmit()
    }
  }

  const confirmOverwrite = () => {
    dispatchSubmit()
  }
</script>

<Container>
  <div class="pure-form pure-form-stacked">
    <FilesSelector {files} bind:selected />
    <input
      placeholder="output file name"
      class="pure-input-1"
      required
      bind:value={filename}
    />
    <label class="pure-checkbox pure-u-1">
      <input type="checkbox" bind:checked={overwrite} />
      <span>Overwrite</span>
    </label>
    <button class="pure-button" disabled={submitDisabled} on:click={onSubmit}>
      submit
    </button>
  </div>
</Container>

<ConfirmDialog bind:isOpen={showConfirmOverwrite} onConfirm={confirmOverwrite}>
  Are you sure you want me to overwrite file {filename}.parquet ?
</ConfirmDialog>
