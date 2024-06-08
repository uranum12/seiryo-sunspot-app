<script lang="ts">
  import { createEventDispatcher } from "svelte"

  export let isOpen = false

  let dialog: HTMLDialogElement

  $: if (dialog) {
    if (isOpen) {
      dialog.showModal()
    } else {
      dialog.close()
    }
  }

  const dispatch = createEventDispatcher()

  const handleOk = () => {
    dispatch("ok")
    isOpen = false
  }

  const handleCancel = () => {
    dispatch("cancel")
    isOpen = false
  }
</script>

<dialog class="dialog" bind:this={dialog}>
  <p>
    <slot />
  </p>
  <p>
    <button class="pure-button" on:click={handleOk}>ok</button>
    <button class="pure-button" on:click={handleCancel}>cancel</button>
  </p>
</dialog>

<style>
  .dialog {
    border: 1px solid;
    border-radius: 4px;
    padding: 0 1rem;
    border-color: orange;
  }
</style>
