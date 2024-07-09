<script lang="ts">
  import { getFiles } from "@/api/files"
  import { postAgg } from "@/api/sunspot_number/with_silso_agg"
  import Alert from "@/components/alert.svelte"
  import ConfirmDialog from "@/components/confirm_dialog.svelte"
  import { FetchError } from "@/utils/fetch"

  let seiryoPath = $state<string>("")
  let silsoPath = $state<string>("")
  let outputName = $state<string>("")
  let overwrite = $state<boolean>(false)

  let showConfirmOverwrite = $state<boolean>(false)

  const submitDisabled = $derived<boolean>(
    seiryoPath.trim() === "" ||
      silsoPath.trim() === "" ||
      outputName.trim() === ""
  )

  const getFilesSeiryo = () => {
    return getFiles({ path: "out/sunspot", glob: "*/monthly.parquet" })
  }

  const getFilesSilso = () => {
    return getFiles({ path: "data/silso", glob: "*.txt" })
  }

  let filesSeiryoPromise = $state<ReturnType<typeof getFiles>>(getFilesSeiryo())
  let filesSilsoPromise = $state<ReturnType<typeof getFiles>>(getFilesSilso())
  let aggPromise = $state<ReturnType<typeof postAgg>>()

  const fetchFiles = () => {
    aggPromise = undefined
    filesSeiryoPromise = getFilesSeiryo()
    filesSilsoPromise = getFilesSilso()
  }

  const submitAgg = () => {
    aggPromise = postAgg({
      seiryoPath,
      silsoPath,
      outputName,
      overwrite,
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

{#await Promise.all([filesSeiryoPromise, filesSilsoPromise])}
  <p>loading...</p>
{:then result}
  {@const [filesSeiryo, filesSilso] = result}
  {#if filesSeiryo.length === 0}
    <section>
      <Alert type="warning">
        <p>no files for seiryo</p>
      </Alert>
    </section>
  {:else if filesSilso.length === 0}
    <section>
      <Alert type="warning">
        <p>no files for SILSO</p>
      </Alert>
    </section>
  {:else}
    <section class="space-y-1">
      <select required bind:value={seiryoPath}>
        <option value="" selected disabled>select file for seiryo</option>
        {#each filesSeiryo.sort() as file}
          <option value={file}>{file}</option>
        {/each}
      </select>
      <select required bind:value={silsoPath}>
        <option value="" selected disabled>select file for SILSO</option>
        {#each filesSilso as file}
          <option value={file}>{file.replace(/^data\/silso\//, "")}</option>
        {/each}
      </select>
      <input placeholder="output file name" required bind:value={outputName} />
      <label>
        <input type="checkbox" bind:checked={overwrite} />
        <span>Overwrite</span>
      </label>
      <button disabled={submitDisabled} onclick={clickSubmit}>submit</button>
    </section>

    <ConfirmDialog bind:isOpen={showConfirmOverwrite} onConfirm={submitAgg}>
      Are you sure you want me to overwrite file ?
    </ConfirmDialog>
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
        <p>file {output.outputWithSilso} generated</p>
        <p>file {output.outputFactorR2} generated</p>
        <p>file {output.outputRatioDiff} generated</p>
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
