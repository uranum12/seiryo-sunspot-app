<script lang="ts" context="module">
  export type FormInput = {
    filename: string
    configName: string
  }
</script>

<script lang="ts">
  import Container from "@/components/container.svelte"

  type Props = {
    files: string[]
    configs: string[]
    defaultConfig: string
    onSubmit: (input: FormInput) => void
  }

  let { files, configs, defaultConfig, onSubmit }: Props = $props()

  let filename = $state<string>("")
  let configName = $state<string>(defaultConfig)

  const submitDisabled = $derived<boolean>(filename.trim() === "")

  const submit = () => {
    onSubmit({ filename, configName })
  }
</script>

<Container>
  <select class="mb-1" required bind:value={filename}>
    <option value="" selected disabled>select file</option>
    {#each files.sort() as file}
      <option value={file}>{file.replace(/^out\//, "")}</option>
    {/each}
  </select>
  <select class="mb-1" bind:value={configName}>
    <option value={defaultConfig} selected>default</option>
    {#each configs.sort() as config}
      <option value={config}>{config.replace(/^config\//, "")}</option>
    {/each}
  </select>
  <button disabled={submitDisabled} onclick={submit}>preview</button>
</Container>
