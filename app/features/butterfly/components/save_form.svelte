<script lang="ts" context="module">
  export type FormInput = {
    format: string
    dpi: number
    overwrite: boolean
  }
</script>

<script lang="ts">
  import formatList from "@/constants/format_list.json"
  import ConfirmDialog from "@/components/confirm_dialog.svelte"
  import Container from "@/components/container.svelte"

  type Props = {
    filename: string
    onSubmit: (input: FormInput) => void
  }

  let { filename, onSubmit }: Props = $props()

  let format = $state<string>("")
  let dpi = $state<number>(300)
  let overwrite = $state<boolean>(false)

  let showConfirmOverwrite = $state<boolean>(false)

  const submitDisabled = $derived(format === "" || dpi === null)

  const submit = () => {
    onSubmit({ format, dpi, overwrite })
  }

  const onClickSubmit = () => {
    if (overwrite) {
      showConfirmOverwrite = true
    } else {
      submit()
    }
  }
</script>

<Container>
  <select class="mb-1" required bind:value={format}>
    <option value="" selected disabled>select file format</option>
    {#each formatList as format}
      <option value={format.format}>
        {format.description} ({format.format})
      </option>
    {/each}
  </select>
  <input type="number" class="mb-1" placeholder="dpi" bind:value={dpi} />
  <label class="mb-1">
    <input type="checkbox" bind:checked={overwrite} />
    <span>Overwrite</span>
  </label>
  <button disabled={submitDisabled} onclick={onClickSubmit}>submit</button>
</Container>

<ConfirmDialog bind:isOpen={showConfirmOverwrite} onConfirm={submit}>
  Are you sure you want me to overwrite file {filename}.{format} ?
</ConfirmDialog>
