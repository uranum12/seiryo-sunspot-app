<script lang="ts">
  import { type InferOutput, safeParse } from "valibot"

  import { schemaImage } from "@/schemas/common"

  type Image = InferOutput<typeof schemaImage>

  type Props = {
    init: Image
    value: Image | undefined
  }

  let { init, value = $bindable() }: Props = $props()

  let cmap = $state<Image["cmap"] | undefined>(init.cmap)
  let aspect = $state<Image["aspect"] | undefined>(init.aspect)

  const image = $derived({ cmap, aspect })

  $effect(() => {
    const result = safeParse(schemaImage, image)
    value = result.success ? result.output : undefined
  })
</script>

<div class="space-y-1">
  <input placeholder="color map" bind:value={cmap} />
  <input placeholder="aspect" type="number" step="0.01" bind:value={aspect} />
</div>
