<script lang="ts">
  import { type InferOutput, safeParse } from "valibot"

  import { schemaCmap } from "@/schemas/butterfly"

  type Cmap = InferOutput<typeof schemaCmap>

  type Props = {
    init: Cmap
    value: Cmap | undefined
  }

  let { init, value = $bindable() }: Props = $props()

  let cmap = $state<Cmap>(init)

  $effect(() => {
    const result = safeParse(schemaCmap, cmap)
    value = result.success ? result.output : undefined
  })
</script>

<div class="space-y-1 rounded border border-gray-300 p-2">
  {#each cmap as c, index}
    <div class="flex items-center">
      <span class="w-8 text-lg">{`${index + 1}.`}</span>
      <div class="flex w-full gap-x-2">
        <div
          class="w-full rounded border border-gray-300"
          style:background-color="rgb({c.red}, {c.green}, {c.blue})"
        ></div>
        <input
          type="number"
          min="0"
          max="255"
          placeholder="Red"
          bind:value={cmap[index].red}
        />
        <input
          type="number"
          min="0"
          max="255"
          placeholder="Green"
          bind:value={cmap[index].green}
        />
        <input
          type="number"
          min="0"
          max="255"
          placeholder="Blue"
          bind:value={cmap[index].blue}
        />
      </div>
    </div>
  {/each}
  <button onclick={() => (cmap = [...cmap, { red: 0, green: 0, blue: 0 }])}
    >append item</button
  >
  <button onclick={() => (cmap = cmap.slice(0, -1))}>remove last item</button>
</div>
