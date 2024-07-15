<script lang="ts">
  import { type InferOutput, safeParse } from "valibot"

  import { schemaAxis } from "@/schemas/common"

  type Axis = InferOutput<typeof schemaAxis>

  type Props = {
    init: Axis
    fonts: string[]
    value: Axis | undefined
  }

  let { init, fonts, value = $bindable() }: Props = $props()

  let titleText = $state(init.title.text)
  let titleFontFamily = $state(init.title.fontFamily)
  let titleFontSize = $state(init.title.fontSize)

  let ticksFontFamily = $state(init.ticks.fontFamily)
  let ticksFontSize = $state(init.ticks.fontSize)

  const axis = $derived({
    title: {
      text: titleText,
      fontFamily: titleFontFamily,
      fontSize: titleFontSize,
      position: init.title.position,
    },
    ticks: {
      fontFamily: ticksFontFamily,
      fontSize: ticksFontSize,
    },
  })

  $effect(() => {
    const result = safeParse(schemaAxis, axis)
    value = result.success ? result.output : undefined
  })
</script>

<div class="space-y-1">
  <h2>Title</h2>
  <input placeholder="text" bind:value={titleText} />
  <select bind:value={titleFontFamily}>
    <option value="" disabled>select font family</option>
    {#each fonts.sort() as font}
      <option value={font}>{font}</option>
    {/each}
  </select>
  <input placeholder="font size" type="number" bind:value={titleFontSize} />
  <h2>Ticks</h2>
  <select bind:value={ticksFontFamily}>
    <option value="" disabled>select font family</option>
    {#each fonts.sort() as font}
      <option value={font}>{font}</option>
    {/each}
  </select>
  <input placeholder="font size" type="number" bind:value={ticksFontSize} />
</div>
