<script lang="ts">
  import { type InferOutput, safeParse } from "valibot"

  import { schemaAxis } from "@/schemas/common"

  type Axis = InferOutput<typeof schemaAxis>

  type Props = {
    init: Axis
    value: Axis | undefined
  }

  let { init, value = $bindable() }: Props = $props()

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
  <input placeholder="font family" bind:value={titleFontFamily} />
  <input placeholder="font size" type="number" bind:value={titleFontSize} />
  <h2>Ticks</h2>
  <input placeholder="font family" bind:value={ticksFontFamily} />
  <input placeholder="font size" type="number" bind:value={ticksFontSize} />
</div>
