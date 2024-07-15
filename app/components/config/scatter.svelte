<script lang="ts">
  import { type InferOutput, safeParse } from "valibot"

  import markerList from "@/constants/marker_list.json"
  import { schemaScatter } from "@/schemas/common"

  type Scatter = InferOutput<typeof schemaScatter>

  type Props = {
    init: Scatter
    labelHidden?: boolean
    value: Scatter | undefined
  }

  let { init, labelHidden: hidden, value = $bindable() }: Props = $props()

  let label = $state<Scatter["label"] | undefined>(init.label)
  let color = $state<Scatter["color"] | undefined>(init.color)
  let edgeColor = $state<Scatter["edgeColor"] | undefined>(init.edgeColor)
  let marker = $state<Scatter["marker"]["marker"] | undefined>(
    init.marker.marker
  )
  let size = $state<Scatter["marker"]["size"] | undefined>(init.marker.size)

  const scatter = $derived({
    label,
    color,
    edgeColor,
    marker: { marker, size },
  })

  $effect(() => {
    const result = safeParse(schemaScatter, scatter)
    value = result.success ? result.output : undefined
  })
</script>

<div class="space-y-1">
  <input placeholder="scatter label" bind:value={label} {hidden} />
  <input placeholder="color" bind:value={color} />
  <input placeholder="edge color" bind:value={edgeColor} />
  <select bind:value={marker}>
    <option value="" disabled>select marker style</option>
    {#each markerList as marker}
      <option value={marker.style}>{marker.description}</option>
    {/each}
  </select>
  <input placeholder="marker size" type="number" bind:value={size} />
</div>
