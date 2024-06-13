<script lang="ts" context="module">
  export type FormInput = {
    format: string
    dpi: number
    overwrite: boolean
  }
</script>

<script lang="ts">
  import { createEventDispatcher } from "svelte"

  import ConfirmDialog from "@/components/confirm_dialog.svelte"
  import Container from "@/components/container.svelte"

  export let filename: string

  const dispatch = createEventDispatcher<{ submit: FormInput }>()

  let format = ""
  let dpi = 300
  let overwrite = false

  let showConfirmOverwrite = false

  let submitDisabled: boolean
  $: submitDisabled = format === ""

  const dispatchSubmit = () => {
    dispatch("submit", { format, dpi, overwrite })
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
    <select class="pure-input-1" bind:value={format}>
      <option value="" selected disabled>select file format</option>
      <option>png</option>
      <option>pdf</option>
      <option>eps</option>
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
  Are you sure you want me to overwrite file {filename}.{format} ?
</ConfirmDialog>
