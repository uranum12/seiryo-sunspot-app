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

<section>
  <select class="mb-1" required bind:value={inputName}>
    <option value="" selected disabled>select file</option>
    {#each files.sort() as file}
      <option value={file}>{file.replace(/^out\//, "")}</option>
    {/each}
  </select>
  <input
    class="mb-1"
    placeholder="output file name"
    required
    bind:value={outputName}
  />
  <Accordion class="mb-1" summary="advanced settings">
    <input
      type="number"
      class="mb-1"
      placeholder="latitude min value"
      min="-90"
      max="90"
      bind:value={latMin}
    />
    <input
      type="number"
      class="mb-1"
      placeholder="latitude max value"
      min="-90"
      max="90"
      bind:value={latMax}
    />
    <DateSelect class="mb-1" bind:date={dateStart} />
    <DateSelect class="mb-1" bind:date={dateEnd} />
    <IntervalSelect bind:interval={dateInterval} />
  </Accordion>
  <label class="mb-1">
    <input type="checkbox" bind:checked={overwrite} />
    <span>Overwrite</span>
  </label>
  <button disabled={submitDisabled} onclick={onClickSubmit}>submit</button>
</section>

<ConfirmDialog bind:isOpen={showConfirmOverwrite} onConfirm={confirmOverwrite}>
  Are you sure you want me to overwrite file ?
</ConfirmDialog>
