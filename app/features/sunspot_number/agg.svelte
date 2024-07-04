<script lang="ts">
  import Alert from "@/components/alert.svelte"
  import { FetchError } from "@/utils/fetch"

  import { postAgg } from "./api/agg"
  import { getFilesAgg } from "./api/files"
  import FileForm, { type FormInput } from "./components/file_form.svelte"

  let filesPromise = $state<ReturnType<typeof getFilesAgg>>(getFilesAgg())
  let aggPromise = $state<ReturnType<typeof postAgg> | undefined>(undefined)

  const fetchFiles = () => {
    aggPromise = undefined
    filesPromise = getFilesAgg()
  }

  const submitAgg = (input: FormInput) => {
    aggPromise = postAgg(input)
  }
</script>

<section>
  <button onclick={fetchFiles}>refresh files</button>
</section>

{#await filesPromise}
  <p>loading...</p>
{:then files}
  {#if files.length !== 0}
    <FileForm {files} onSubmit={submitAgg} />
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
        <p>file {output.outputRaw} generated</p>
        <p>file {output.outputDaily} generated</p>
        <p>file {output.outputMonthly} generated</p>
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
