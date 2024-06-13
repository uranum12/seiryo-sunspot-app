<script lang="ts" context="module">
  export type FormInput = {
    filename: string
  }
</script>

<script lang="ts">
  import { createEventDispatcher } from "svelte"

  import Container from "@/components/container.svelte"

  export let files: string[]

  const dispatch = createEventDispatcher<{ submit: FormInput }>()

  let filename = ""

  let submitDisabled: boolean
  $: submitDisabled = filename.trim() === ""

  const dispatchSubmit = () => {
    dispatch("submit", { filename })
  }

  const onSubmit = () => {
    dispatchSubmit()
  }
</script>

<Container>
  <div class="pure-form">
    <select class="pure-input-2-3" bind:value={filename}>
      <option value="" selected disabled>select file</option>
      {#each files.sort() as file}
        <option value={file}>{file.replace(/^out\//, "")}</option>
      {/each}
    </select>
    <button class="pure-button" disabled={submitDisabled} on:click={onSubmit}>
      preview
    </button>
  </div>
</Container>
