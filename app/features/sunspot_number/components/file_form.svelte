<script lang="ts" context="module">
  export type FormInput = {
    filename: string
    overwrite: boolean
  }
</script>

<script lang="ts">
  import { createEventDispatcher } from "svelte"

  import ConfirmDialog from "@/components/confirm_dialog.svelte"
  import Container from "@/components/container.svelte"

  export let files: string[]

  const dispatch = createEventDispatcher<{ submit: FormInput }>()

  let filename = ""
  let overwrite = false

  let showConfirmOverwrite = false

  let submitDisabled: boolean
  $: submitDisabled = filename.trim() === ""

  const dispatchSubmit = () => {
    dispatch("submit", { filename, overwrite })
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
    <select class="pure-input-1" bind:value={filename}>
      <option value="" selected disabled>select file</option>
      {#each files.sort() as file}
        <option value={file}>{file.replace(/^out\//, "")}</option>
      {/each}
    </select>
    <label class="pure-checkbox pure-input-1">
      <input type="checkbox" bind:checked={overwrite} />
      <span>Overwrite</span>
    </label>
    <button class="pure-button" disabled={submitDisabled} on:click={onSubmit}>
      submit
    </button>
  </div>
</Container>

<ConfirmDialog bind:isOpen={showConfirmOverwrite} on:ok={confirmOverwrite}>
  Are you sure you want me to overwrite file {filename}.parquet ?
</ConfirmDialog>
