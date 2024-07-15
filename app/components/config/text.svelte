<script lang="ts">
  import { type InferOutput, safeParse } from "valibot"

  import { schemaText } from "@/schemas/common"

  type Text = InferOutput<typeof schemaText>

  type Props = {
    init: Text
    fonts: string[]
    value: Text | undefined
  }

  let { init, fonts, value = $bindable() }: Props = $props()

  let x = $state<Text["x"]>(init.x)
  let y = $state<Text["y"]>(init.y)
  let mathFontFamily = $state<Text["mathFontFamily"] | undefined>(
    init.mathFontFamily
  )
  let fontFamily = $state<Text["fontFamily"] | undefined>(init.fontFamily)
  let fontSize = $state<Text["fontSize"] | undefined>(init.fontSize)

  const text = $derived({ x, y, mathFontFamily, fontFamily, fontSize })

  $effect(() => {
    const result = safeParse(schemaText, text)
    value = result.success ? result.output : undefined
  })
</script>

<div class="space-y-1">
  <input type="number" step="0.1" placeholder="x position" bind:value={x} />
  <input type="number" step="0.1" placeholder="y position" bind:value={y} />
  <input placeholder="math font family" bind:value={mathFontFamily} />
  <select bind:value={fontFamily}>
    <option value="" disabled>select font family</option>
    {#each fonts.sort() as font}
      <option value={font}>{font}</option>
    {/each}
  </select>
  <input placeholder="font size" type="number" bind:value={fontSize} />
</div>
