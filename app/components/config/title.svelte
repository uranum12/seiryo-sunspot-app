<script lang="ts">
  import { type InferOutput, safeParse } from "valibot"

  import { schemaTitle } from "@/schemas/common"

  type Title = InferOutput<typeof schemaTitle>

  type Props = {
    init: Title
    fonts: string[]
    positionHidden?: boolean
    value: Title | undefined
  }

  let {
    init,
    fonts,
    positionHidden: hidden,
    value = $bindable(),
  }: Props = $props()

  let text = $state<Title["text"] | undefined>(init.text)
  let fontFamily = $state<Title["fontFamily"] | undefined>(init.fontFamily)
  let fontSize = $state<Title["fontSize"] | undefined>(init.fontSize)
  let position = $state<Title["position"] | undefined>(init.position)

  const title = $derived({ text, fontFamily, fontSize, position })

  $effect(() => {
    const result = safeParse(schemaTitle, title)
    value = result.success ? result.output : undefined
  })
</script>

<div class="space-y-1">
  <input placeholder="text" bind:value={text} />
  <select bind:value={fontFamily}>
    <option value="" disabled>select font family</option>
    {#each fonts.sort() as font}
      <option value={font}>{font}</option>
    {/each}
  </select>
  <input placeholder="font size" type="number" bind:value={fontSize} />
  <input
    placeholder="title position"
    type="number"
    step="0.01"
    bind:value={position}
    {hidden}
  />
</div>
