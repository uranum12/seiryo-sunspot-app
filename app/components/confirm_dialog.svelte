<script lang="ts">
  import type { Snippet } from "svelte"

  type Props = {
    onConfirm?: () => void
    onCancel?: () => void
    children: Snippet
    isOpen: boolean
  }

  let { onConfirm, onCancel, children, isOpen = $bindable() }: Props = $props()

  let dialog: HTMLDialogElement

  $effect(() => {
    if (dialog) {
      if (isOpen) {
        dialog.showModal()
      } else {
        dialog.close()
      }
    }
  })

  const handleConfirm = () => {
    isOpen = false
    if (onConfirm) {
      onConfirm()
    }
  }

  const handleCancel = () => {
    isOpen = false
    if (onCancel) {
      onCancel()
    }
  }
</script>

<dialog class="dialog" bind:this={dialog}>
  <p>
    {@render children()}
  </p>
  <p>
    <button class="pure-button" onclick={handleConfirm}>ok</button>
    <button class="pure-button" onclick={handleCancel}>cancel</button>
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
