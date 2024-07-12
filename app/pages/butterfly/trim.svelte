<script lang="ts">
  import { postTrim } from "@/api/butterfly/trim"
  import { getFiles } from "@/api/files"
  import Alert from "@/components/alert.svelte"
  import ConfirmDialog from "@/components/confirm_dialog.svelte"
  import DateSelect from "@/components/date_select.svelte"
  import { FetchError } from "@/utils/fetch"

  let inputName = $state<string>("")
  let outputName = $state<string>("")
  let overwrite = $state<boolean>(false)

  let latMin = $state<number>()
  let latMax = $state<number>()
  let dateStart = $state<string>()
  let dateEnd = $state<string>()

  let showConfirmOverwrite = $state<boolean>(false)

  const submitDisabled = $derived<boolean>(
    inputName.trim() === "" || outputName.trim() === ""
  )

  const getFilesTrim = () => {
    return getFiles({ path: "out/butterfly", glob: "*.parquet" })
  }

  let filesPromise = $state<ReturnType<typeof getFiles>>(getFilesTrim())
  let trimPromise = $state<ReturnType<typeof postTrim>>()

  const fetchFiles = () => {
    trimPromise = undefined
    filesPromise = getFilesTrim()
  }

  const submitTrim = () => {
    trimPromise = postTrim({
      inputName,
      outputName,
      overwrite,
      latMin,
      latMax,
      dateStart,
      dateEnd,
    })
  }

  const clickSubmit = () => {
    if (overwrite) {
      showConfirmOverwrite = true
    } else {
      submitTrim()
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
        <label>
          <input type="checkbox" bind:checked={overwrite} />
          <span>Overwrite</span>
        </label>
        <button disabled={submitDisabled} onclick={clickSubmit}>submit</button>
      </div>
    </section>

    <ConfirmDialog bind:isOpen={showConfirmOverwrite} onConfirm={submitTrim}>
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

{#if trimPromise}
  {#await trimPromise}
    <p>loading...</p>
  {:then output}
    <section>
      <Alert type="success">
        <p>file {output.outputData} generated</p>
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
