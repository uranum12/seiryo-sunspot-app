<script lang="ts" context="module">
  export type FormInput = {
    filename: string
  }
</script>

<script lang="ts">
  import Container from "@/components/container.svelte"

  type Props = {
    files: string[]
    onSubmit: (input: FormInput) => void
  }

  let { files, onSubmit }: Props = $props()

  let filename = $state<string>("")

  const submitDisabled = $derived<boolean>(filename.trim() === "")

  const submit = () => {
    onSubmit({ filename })
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
    <button class="pure-button" disabled={submitDisabled} onclick={submit}>
      preview
    </button>
  </div>
</Container>
