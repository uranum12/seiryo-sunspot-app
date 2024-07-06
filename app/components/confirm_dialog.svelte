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

<dialog class="rounded border border-yellow-400 px-4 py-3" bind:this={dialog}>
  <p>
    {@render children()}
  </p>
  <p class="pt-2">
    <button onclick={handleConfirm}>ok</button>
    <button onclick={handleCancel}>cancel</button>
  </p>
</dialog>
