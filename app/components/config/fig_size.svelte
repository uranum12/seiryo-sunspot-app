<script lang="ts">
  import { type InferOutput, safeParse } from "valibot"

  import { schemaFigSize } from "@/schemas/common"

  type FigSize = InferOutput<typeof schemaFigSize>

  type Props = {
    init: FigSize
    value: FigSize | undefined
  }

  let { init, value = $bindable() }: Props = $props()

  let width = $state<FigSize["width"] | undefined>(init.width)
  let height = $state<FigSize["height"] | undefined>(init.height)

  const figSize = $derived({ width, height })

  $effect(() => {
    const result = safeParse(schemaFigSize, figSize)
    value = result.success ? result.output : undefined
  })
</script>

<div class="space-y-1">
  <input
    type="number"
    step="0.1"
    placeholder="figure width"
    bind:value={width}
  />
  <input
    type="number"
    step="0.1"
    placeholder="figure height"
    bind:value={height}
  />
</div>
