<script lang="ts" context="module">
  export type FormInput = {
    filename: string
    overwrite: boolean
  }
</script>

<script lang="ts">
  import ConfirmDialog from "@/components/confirm_dialog.svelte"
  import Container from "@/components/container.svelte"

  type Props = {
    files: string[]
    onSubmit: (input: FormInput) => void
  }

  let { files, onSubmit }: Props = $props()

  let filename = $state<string>("")
  let overwrite = $state<boolean>(false)

  let showConfirmOverwrite = $state<boolean>(false)

  const submitDisabled = $derived<boolean>(filename.trim() === "")

  const submit = () => {
    onSubmit({ filename, overwrite })
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
    <button
      class="pure-button"
      disabled={submitDisabled}
      onclick={onClickSubmit}
    >
      submit
    </button>
  </div>
</Container>

<ConfirmDialog bind:isOpen={showConfirmOverwrite} onConfirm={confirmOverwrite}>
  Are you sure you want me to overwrite file {filename}.parquet ?
</ConfirmDialog>
