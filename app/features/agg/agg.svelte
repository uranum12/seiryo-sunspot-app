<script lang="ts">
  import { onMount } from "svelte"

  import Alert from "@/components/alert.svelte"
  import Container from "@/components/container.svelte"
  import { FetchError } from "@/utils/fetch"

  import { postAgg } from "./api/agg"
  import { getFiles } from "./api/files"
  import FileForm, { type FormInput } from "./components/file_form.svelte"

  let filesPromise: ReturnType<typeof getFiles>
  let aggPromise: ReturnType<typeof postAgg> | undefined

  const fetchFiles = () => {
    aggPromise = undefined
    filesPromise = getFiles()
  }

  const submitAgg = (e: CustomEvent<FormInput>) => {
    aggPromise = postAgg(e.detail)
  }

  onMount(fetchFiles)
</script>

<Container>
  <button class="pure-button" on:click={fetchFiles}>refresh files</button>
</Container>

{#if filesPromise}
  {#await filesPromise}
    <p>loading...</p>
  {:then files}
    {#if files.length !== 0}
      <FileForm {files} on:submit={submitAgg} />
    {:else}
      <Container>
        <Alert severity="warning">
          <p>no files</p>
        </Alert>
      </Container>
    {/if}
  {:catch e}
    <Container>
      <Alert severity="error">
        <p>{e.message}</p>
      </Alert>
    </Container>
  {/await}
{/if}

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
