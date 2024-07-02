<script lang="ts" context="module">
  export type FormInput = {
    inputName: string
    outputName: string
    overwrite: boolean
    latMin?: number
    latMax?: number
    dateStart?: string
    dateEnd?: string
    dateInterval?: string
  }
</script>

<script lang="ts">
  import ConfirmDialog from "@/components/confirm_dialog.svelte"
  import Container from "@/components/container.svelte"
  import Accordion from "@/components/accordion.svelte"

  import DateSelect from "./date_select.svelte"
  import IntervalSelect from "./interval_select.svelte"

  type Props = {
    files: string[]
    onSubmit: (input: FormInput) => void
  }

  let { files, onSubmit }: Props = $props()

  let inputName = $state<string>("")
  let outputName = $state<string>("")
  let overwrite = $state<boolean>(false)

  let latMin = $state<number>()
  let latMax = $state<number>()
  let dateStart = $state<string>()
  let dateEnd = $state<string>()
  let dateInterval = $state<string>()

  let showConfirmOverwrite = $state<boolean>(false)

  const submitDisabled = $derived<boolean>(
    inputName.trim() === "" || outputName.trim() === ""
  )

  const submit = () => {
    onSubmit({
      inputName,
      outputName,
      overwrite,
      latMin,
      latMax,
      dateStart,
      dateEnd,
      dateInterval,
    })
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
    <select class="pure-input-1" bind:value={inputName}>
      <option value="" selected disabled>select file</option>
      {#each files.sort() as file}
        <option value={file}>{file.replace(/^out\//, "")}</option>
      {/each}
    </select>
    <input
      placeholder="output file name"
      class="pure-input-1"
      required
      bind:value={outputName}
    />
    <Accordion summary="advanced settings">
      <input
        type="number"
        class="pure-input-1"
        placeholder="latitude min value"
        min="-90"
        max="90"
        bind:value={latMin}
      />
      <input
        type="number"
        class="pure-input-1"
        placeholder="latitude max value"
        min="-90"
        max="90"
        bind:value={latMax}
      />
      <DateSelect bind:date={dateStart} />
      <DateSelect bind:date={dateEnd} />
      <IntervalSelect bind:interval={dateInterval} />
    </Accordion>
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
  Are you sure you want me to overwrite file ?
</ConfirmDialog>
