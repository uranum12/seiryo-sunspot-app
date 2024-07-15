<script lang="ts">
  import { type InferOutput, safeParse } from "valibot"

  import { schemaLegend } from "@/schemas/common"

  type Legend = InferOutput<typeof schemaLegend>

  type Props = {
    init: Legend
    fonts: string[]
    positionHidden?: boolean
    value: Legend | undefined
  }

  let { init, fonts, value = $bindable() }: Props = $props()

  let fontFamily = $state<Legend["fontFamily"] | undefined>(init.fontFamily)
  let fontSize = $state<Legend["fontSize"] | undefined>(init.fontSize)

  const legend = $derived({ fontFamily, fontSize })

  $effect(() => {
    const result = safeParse(schemaLegend, legend)
    value = result.success ? result.output : undefined
  })
</script>

<div class="space-y-1">
  <select bind:value={fontFamily}>
    <option value="" disabled>select font family</option>
    {#each fonts.sort() as font}
      <option value={font}>{font}</option>
    {/each}
  </select>
  <input placeholder="font size" type="number" bind:value={fontSize} />
</div>
