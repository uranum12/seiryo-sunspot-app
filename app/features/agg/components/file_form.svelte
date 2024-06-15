<script lang="ts" context="module">
  export type FormInput = {
    files: string[]
    filename: string
    overwrite: boolean
  }
</script>

<script lang="ts">
  import ConfirmDialog from "@/components/confirm_dialog.svelte"
  import Container from "@/components/container.svelte"

  import FilesSelector from "./files_selector.svelte"

  type Props = {
    files: string[]
    onSubmit: (input: FormInput) => void
  }

  let { files, onSubmit }: Props = $props()

  let selected = $state<string[]>([])
  let filename = $state<string>("")
  let overwrite = $state<boolean>(false)

  let showConfirmOverwrite = $state<boolean>(false)

  const submitDisabled = $derived<boolean>(
    selected.length === 0 || filename.trim() === ""
  )

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
