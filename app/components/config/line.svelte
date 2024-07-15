<script lang="ts">
  import { type InferOutput, safeParse } from "valibot"

  import lineList from "@/constants/line_list.json"
  import markerList from "@/constants/marker_list.json"
  import { schemaLine } from "@/schemas/common"

  type Line = InferOutput<typeof schemaLine>

  type Props = {
    init: Line
    labelHidden?: boolean
    value: Line | undefined
  }

  let { init, labelHidden: hidden, value = $bindable() }: Props = $props()

  let label = $state<Line["label"] | undefined>(init.label)
  let style = $state<Line["style"] | undefined>(init.style)
  let width = $state<Line["width"] | undefined>(init.width)
  let color = $state<Line["color"] | undefined>(init.color)
  let marker = $state<Line["marker"]["marker"] | undefined>(init.marker.marker)
  let size = $state<Line["marker"]["size"] | undefined>(init.marker.size)

  const line = $derived({
    label,
    style,
    width,
    color,
    marker: { marker, size },
  })

  $effect(() => {
    const result = safeParse(schemaLine, line)
    value = result.success ? result.output : undefined
  })
</script>

<div class="space-y-1">
  <input placeholder="line label" bind:value={label} {hidden} />
  <select bind:value={style}>
    <option value="" disabled>select line style</option>
    {#each lineList as line}
      <option value={line.style}>{line.description}</option>
    {/each}
  </select>
  <input placeholder="line width" type="number" bind:value={width} />
  <input placeholder="color" bind:value={color} />
  <select bind:value={marker}>
    <option value="" disabled>select marker style</option>
    {#each markerList as marker}
      <option value={marker.style}>{marker.description}</option>
    {/each}
  </select>
  <input placeholder="marker size" type="number" bind:value={size} />
</div>
