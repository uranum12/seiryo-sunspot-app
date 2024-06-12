<script lang="ts">
  import Alert from "@/components/alert.svelte"
  import Container from "@/components/container.svelte"
  import { FetchError } from "@/utils/fetch"

  import { postAgg } from "./api/agg"
  import { getFiles } from "./api/files"
  import FileForm, { type FormInput } from "./components/file_form.svelte"

  let filesPromise: Promise<string[]> = getFiles()
  let aggPromise: Promise<string> | undefined

  const fetchFiles = () => {
    aggPromise = undefined
    filesPromise = getFiles()
  }

  const submitAgg = (e: CustomEvent<FormInput>) => {
    aggPromise = postAgg({ ...e.detail })
  }
</script>

{#await filesPromise}
  <p>loading...</p>
{:then files}
  {#if files.length !== 0}
    <Container>
      <button class="pure-button" on:click={fetchFiles}>refresh files</button>
    </Container>
    <FileForm {files} on:submit={submitAgg} />
  {:else}
    <Container>
      <button class="pure-button" on:click={fetchFiles}
        >retry fetch files</button
      >
    </Container>
    <Container>
      <Alert severity="warning">
        <p>no files</p>
      </Alert>
    </Container>
  {/if}
{:catch e}
  <Container>
    <button class="pure-button" on:click={fetchFiles}>retry fetch files</button>
  </Container>
  <Container>
    <Alert severity="error">
      <p>{e.message}</p>
    </Alert>
  </Container>
{/await}

{#if aggPromise}
  {#await aggPromise}
    <p>loading...</p>
  {:then output}
    <Container>
      <Alert severity="success">
        <p>file {output} generated</p>
      </Alert>
    </Container>
  {:catch e}
    <Container>
      <Alert severity="error">
        <p>{e instanceof FetchError ? e.detail : e.message}</p>
      </Alert>
    </Container>
  {/await}
{/if}
