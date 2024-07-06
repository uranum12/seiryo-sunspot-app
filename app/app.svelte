<script lang="ts">
  import Agg from "@/features/agg/agg.svelte"
  import ButterflyAgg from "@/features/butterfly/agg.svelte"
  import ButterflyDraw from "@/features/butterfly/draw.svelte"
  import ObservationsAgg from "@/features/observations/agg.svelte"
  import ObservationsCalendar from "@/features/observations/calendar.svelte"
  import ObservationsMonthly from "@/features/observations/monthly.svelte"
  import SunspotNumberAgg from "@/features/sunspot_number/agg.svelte"
  import SunspotNumberHemispheric from "@/features/sunspot_number/hemispheric.svelte"
  import SunspotNumberWholeDisk from "@/features/sunspot_number/whole_disk.svelte"
  import { type Page, searchPage, searchPath } from "@/utils/pages"

  let currentPath = $state<string[]>([""])

  const getPageName = () => {
    currentPath = location.hash.replace("#/", "").split("/")
  }

  $effect(getPageName)

  const pages: Page[] = [
    { path: "", name: "Home", page: Agg },
    { path: "agg", name: "Agg", page: Agg },
    {
      path: "sunspot_number",
      name: "Sunspot Number",
      children: [
        { path: "agg", name: "Agg", page: SunspotNumberAgg },
        {
          path: "whole_disk",
          name: "Whole Disk",
          page: SunspotNumberWholeDisk,
        },
        {
          path: "hemispheric",
          name: "Hemispheric",
          page: SunspotNumberHemispheric,
        },
      ],
    },
    {
      path: "observations",
      name: "Observations",
      children: [
        { path: "agg", name: "Agg", page: ObservationsAgg },
        { path: "monthly", name: "Monthly", page: ObservationsMonthly },
        { path: "calendar", name: "Calendar", page: ObservationsCalendar },
      ],
    },
    {
      path: "butterfly",
      name: "Butterfly Diagram",
      children: [
        { path: "agg", name: "Agg", page: ButterflyAgg },
        { path: "draw", name: "Draw", page: ButterflyDraw },
      ],
    },
  ]

  const page = $derived(searchPage(currentPath, pages))
  const paths = $derived(searchPath(currentPath, pages))
</script>

<svelte:window on:hashchange={getPageName} />

<header class="mb-4 px-8">
  <nav class="space-y-1">
    {#each paths as navs}
      <div class="flex space-x-2 overflow-x-auto">
        {#each navs as nav}
          <a
            href={nav.path}
            class="block border-b-4 border-gray-300 px-4 py-2 hover:bg-gray-200 focus:bg-gray-200 focus:outline-none"
            class:!border-blue-300={nav.selected}
          >
            {nav.name}
          </a>
        {/each}
      </div>
    {/each}
  </nav>
</header>

<main class="px-8">
  {#if page}
    <svelte:component this={page} />
  {:else}
    <section>
      <h2>Error: Not Found!</h2>
    </section>
  {/if}
</main>
