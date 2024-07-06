<script lang="ts">
  import Accordion from "@/components/accordion.svelte"
  import Alert from "@/components/alert.svelte"
  import ConfirmDialog from "@/components/confirm_dialog.svelte"
  import { FetchError } from "@/utils/fetch"

  import { postAgg } from "./api/agg"
  import { getFilesAgg } from "./api/files"
  import DateSelect from "./components/date_select.svelte"
  import IntervalSelect from "./components/interval_select.svelte"

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

  let filesPromise = $state<ReturnType<typeof getFilesAgg>>(getFilesAgg())
  let aggPromise = $state<ReturnType<typeof postAgg>>()

  const fetchFiles = () => {
    aggPromise = undefined
    filesPromise = getFilesAgg()
  }

  const submitAgg = () => {
    aggPromise = postAgg({
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

  const clickSubmit = () => {
    if (overwrite) {
      showConfirmOverwrite = true
    } else {
      submitAgg()
    }
  }
</script>

<section>
  <button onclick={fetchFiles}>refresh files</button>
</section>

{#await filesPromise}
  <p>loading...</p>
{:then files}
  {#if files.length !== 0}
    <section class="space-y-1">
      <select required bind:value={inputName}>
        <option value="" selected disabled>select file</option>
        {#each files.sort() as file}
          <option value={file}>{file.replace(/^out\//, "")}</option>
        {/each}
      </select>
      <input placeholder="output file name" required bind:value={outputName} />
      <Accordion summary="advanced settings">
        <div class="space-y-1">
          <input
            type="number"
            placeholder="latitude min value"
            min="-90"
            max="90"
            bind:value={latMin}
          />
          <input
            type="number"
            placeholder="latitude max value"
            min="-90"
            max="90"
            bind:value={latMax}
          />
          <DateSelect bind:date={dateStart} />
          <DateSelect bind:date={dateEnd} />
          <IntervalSelect bind:interval={dateInterval} />
        </div>
      </Accordion>
      <label>
        <input type="checkbox" bind:checked={overwrite} />
        <span>Overwrite</span>
      </label>
      <button disabled={submitDisabled} onclick={clickSubmit}>submit</button>
    </section>

    <ConfirmDialog bind:isOpen={showConfirmOverwrite} onConfirm={submitAgg}>
      Are you sure you want me to overwrite file ?
    </ConfirmDialog>
  {:else}
    <section>
      <Alert type="warning">
        <p>no files</p>
      </Alert>
    </section>
  {/if}
{:catch e}
  <section>
    <Alert type="error">
      <p>{e.message}</p>
    </Alert>
  </section>
{/await}

{#if aggPromise}
  {#await aggPromise}
    <p>loading...</p>
  {:then output}
    <section>
      <Alert type="success">
        <p>file {output.outputData} generated</p>
        <p>file {output.outputImage} generated</p>
        <p>file {output.outputInfo} generated</p>
      </Alert>
    </section>
  {:catch e}
    <section>
      <Alert type="error">
        <p>{e instanceof FetchError ? e.detail : e.message}</p>
      </Alert>
    </section>
  {/await}
{/if}
