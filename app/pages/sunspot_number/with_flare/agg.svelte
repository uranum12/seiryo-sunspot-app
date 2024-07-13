<script lang="ts">
  import { getFiles } from "@/api/files"
  import { postAgg } from "@/api/sunspot_number/with_flare_agg"
  import Alert from "@/components/alert.svelte"
  import ConfirmDialog from "@/components/confirm_dialog.svelte"
  import FileSelect from "@/components/file_select.svelte"
  import { FetchError } from "@/utils/fetch"

  let seiryoPath = $state<string>("")
  let flareFilesNorth = $state<string[]>([])
  let flareFilesSouth = $state<string[]>([])
  let flareFilesTotal = $state<string[]>([])
  let outputName = $state<string>("")
  let overwrite = $state<boolean>(false)

  let tabNumber = $state<number>(0)

  let showConfirmOverwrite = $state<boolean>(false)

  const submitDisabled = $derived(
    seiryoPath.trim() === "" ||
      outputName.trim() === "" ||
      (flareFilesNorth.length === 0 &&
        flareFilesSouth.length === 0 &&
        flareFilesTotal.length === 0)
  )

  const getFilesSeiryo = () => {
    return getFiles({ path: "out/sunspot", glob: "*/monthly.parquet" })
  }

  const getFilesFlare = () => {
    return getFiles({ path: "data/flare", glob: "*.txt" })
  }

  let filesSeiryoPromise = $state<ReturnType<typeof getFiles>>(getFilesSeiryo())
  let filesFlarePromise = $state<ReturnType<typeof getFiles>>(getFilesFlare())
  let aggPromise = $state<ReturnType<typeof postAgg>>()

  const fetchFiles = () => {
    aggPromise = undefined
    filesSeiryoPromise = getFilesSeiryo()
    filesFlarePromise = getFilesFlare()
  }

  const submitAgg = () => {
    aggPromise = postAgg({
      seiryoPath,
      flareFilesNorth,
      flareFilesSouth,
      flareFilesTotal,
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

{#await Promise.all([filesSeiryoPromise, filesFlarePromise])}
  <p>loading...</p>
{:then result}
  {@const [filesSeiryo, filesFlare] = result}
  {#if filesSeiryo.length === 0}
    <section>
      <Alert type="warning">
        <p>no files for seiryo</p>
      </Alert>
    </section>
  {:else if filesFlare.length === 0}
    <section>
      <Alert type="warning">
        <p>no files for Flare Index</p>
      </Alert>
    </section>
  {:else}
    <section class="space-y-1">
      <div>
        <div class="flex gap-x-2 px-2">
          {#each ["North", "South", "Total"] as title, i}
            <button
              class="rounded-b-none border-2 border-b-0 border-gray-300"
              class:!border-blue-300={tabNumber === i}
              onclick={() => (tabNumber = i)}
            >
              {title}
            </button>
          {/each}
        </div>
        <div class="rounded border border-gray-300 p-2">
          <div class:hidden={tabNumber !== 0}>
            <FileSelect files={filesFlare} bind:selected={flareFilesNorth} />
          </div>
          <div class:hidden={tabNumber !== 1}>
            <FileSelect files={filesFlare} bind:selected={flareFilesSouth} />
          </div>
          <div class:hidden={tabNumber !== 2}>
            <FileSelect files={filesFlare} bind:selected={flareFilesTotal} />
          </div>
        </div>
      </div>
      <select required bind:value={seiryoPath}>
        <option value="" selected disabled>select file for seiryo</option>
        {#each filesSeiryo.sort() as file}
          <option value={file}>{file}</option>
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
        <p>file {output.outputWithFlare} generated</p>
        <p>file {output.outputFactors} generated</p>
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
