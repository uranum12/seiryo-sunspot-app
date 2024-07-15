<script lang="ts">
  import { type InferOutput, safeParse } from "valibot"

  import { schemaIndex } from "@/schemas/butterfly"

  type Index = InferOutput<typeof schemaIndex>

  type Props = {
    init: Index
    value: Index | undefined
  }

  let { init, value = $bindable() }: Props = $props()

  let yearInterval = $state<Index["yearInterval"] | undefined>(
    init.yearInterval
  )
  let latInterval = $state<Index["latInterval"] | undefined>(init.latInterval)

  const index = $derived({ yearInterval, latInterval })

  $effect(() => {
    const result = safeParse(schemaIndex, index)
    value = result.success ? result.output : undefined
  })
</script>

<div class="space-y-1">
  <input type="number" placeholder="years" bind:value={yearInterval} />
  <input type="number" placeholder="latitude" bind:value={latInterval} />
</div>
