<script lang="ts">
  import { type InferOutput, safeParse } from "valibot"

  import { schemaBar } from "@/schemas/common"

  type Bar = InferOutput<typeof schemaBar>

  type Props = {
    init: Bar
    labelHidden?: boolean
    value: Bar | undefined
  }

  let { init, labelHidden: hidden, value = $bindable() }: Props = $props()

  let label = $state<Bar["label"] | undefined>(init.label)
  let width = $state<Bar["width"] | undefined>(init.width)
  let color = $state<Bar["color"] | undefined>(init.color)

  const bar = $derived({
    label,
    width,
    color,
  })

  $effect(() => {
    const result = safeParse(schemaBar, bar)
    value = result.success ? result.output : undefined
  })
</script>

<div class="space-y-1">
  <input placeholder="line label" bind:value={label} {hidden} />
  <input placeholder="line width" type="number" bind:value={width} />
  <input placeholder="color" bind:value={color} />
</div>
