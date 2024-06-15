<script lang="ts">
  import Alert from "@/components/alert.svelte"
  import Container from "@/components/container.svelte"
  import { FetchError } from "@/utils/fetch"

  import { postAgg } from "./api/agg"
  import { getFiles } from "./api/files"
  import FileForm, { type FormInput } from "./components/file_form.svelte"

  let filesPromise = $state<ReturnType<typeof getFiles>>(getFiles())
  let aggPromise = $state<ReturnType<typeof postAgg> | undefined>(undefined)

  const fetchFiles = () => {
    aggPromise = undefined
    filesPromise = getFiles()
  }

  const submitAgg = (input: FormInput) => {
    aggPromise = postAgg(input)
  }
</script>

<Container>
  <button class="pure-button" onclick={fetchFiles}>refresh files</button>
</Container>

{#await filesPromise}
  <p>loading...</p>
{:then files}
  {#if files.length !== 0}
    <FileForm {files} onSubmit={submitAgg} />
  {:else}
    <Container>
      <Alert type="warning">
        <p>no files</p>
      </Alert>
    </Container>
  {/if}
{:catch e}
  <Container>
    <Alert type="error">
      <p>{e.message}</p>
    </Alert>
  </Container>
{/await}

{#if aggPromise}
  {#await aggPromise}
    <p>loading...</p>
  {:then output}
    <Container>
      <Alert type="success">
        <p>file {output} generated</p>
      </Alert>
    </Container>
  {:catch e}
    <Container>
      <Alert type="error">
        <p>{e instanceof FetchError ? e.detail : e.message}</p>
      </Alert>
    </Container>
  {/await}
{/if}
