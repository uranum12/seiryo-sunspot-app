<script lang="ts">
  import { postImageColor } from "@/api/butterfly/image_color"
  import { getFiles } from "@/api/files"
  import Alert from "@/components/alert.svelte"
  import ConfirmDialog from "@/components/confirm_dialog.svelte"
  import { FetchError } from "@/utils/fetch"

  const defaultColors = "config/butterfly/color_map.json"

  let inputName = $state<string>("")
  let colorsName = $state<string>(defaultColors)
  let outputName = $state<string>("")
  let overwrite = $state<boolean>(false)

  let showConfirmOverwrite = $state<boolean>(false)

  const submitDisabled = $derived<boolean>(
    inputName.trim() === "" || outputName.trim() === ""
  )

  const getFilesImage = () => {
    return getFiles({ path: "out/butterfly", glob: "*.npz" })
  }

  const getFilesColors = () => {
    return getFiles({ path: "config/butterfly/color_map", glob: "*.json" })
  }

  let filesPromise = $state<ReturnType<typeof getFiles>>(getFilesImage())
  let colorsPromise = $state<ReturnType<typeof getFiles>>(getFilesColors())
  let imagePromise = $state<ReturnType<typeof postImageColor>>()

  const fetchFiles = () => {
    imagePromise = undefined
    filesPromise = getFilesImage()
    colorsPromise = getFilesColors()
  }

  const submitImage = () => {
    imagePromise = postImageColor({
      inputName,
      colorsName,
      outputName,
      overwrite,
    })
  }

  const clickSubmit = () => {
    if (overwrite) {
      showConfirmOverwrite = true
    } else {
      submitImage()
    }
  }
</script>

<section>
  <button onclick={fetchFiles}>refresh files</button>
</section>

{#await Promise.all([filesPromise, colorsPromise])}
  <p>loading...</p>
{:then result}
  {@const [files, colors] = result}
  {#if files.length === 0}
    <section>
      <Alert type="warning">
        <p>no files</p>
      </Alert>
    </section>
  {:else}
    <section class="space-y-1">
      <select required bind:value={inputName}>
        <option value="" selected disabled>select file</option>
        {#each files.sort() as file}
          <option value={file}>{file.replace(/^out\//, "")}</option>
        {/each}
      </select>
      <select required bind:value={colorsName}>
        <option value={defaultColors} selected>default</option>
        {#each colors as color}
          <option value={color}>{color.replace(/^config\//, "")}</option>
        {/each}
      </select>
      <input placeholder="output file name" required bind:value={outputName} />
      <label>
        <input type="checkbox" bind:checked={overwrite} />
        <span>Overwrite</span>
      </label>
      <button disabled={submitDisabled} onclick={clickSubmit}>submit</button>
    </section>

    <ConfirmDialog bind:isOpen={showConfirmOverwrite} onConfirm={submitImage}>
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

{#if imagePromise}
  {#await imagePromise}
    <p>loading...</p>
  {:then output}
    <section>
      <Alert type="success">
        <p>file {output.outputInfo} generated</p>
        <p>file {output.outputImage} generated</p>
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
