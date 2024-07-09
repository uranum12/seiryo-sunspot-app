<script lang="ts">
  import Agg from "@/pages/agg/agg.svelte"
  import ButterflyAgg from "@/pages/butterfly/agg.svelte"
  import ButterflyDraw from "@/pages/butterfly/draw.svelte"
  import CheckData from "@/pages/check/data.svelte"
  import CheckFile from "@/pages/check/file.svelte"
  import CheckFinder from "@/pages/check/finder.svelte"
  import ObservationsAgg from "@/pages/observations/agg.svelte"
  import ObservationsCalendar from "@/pages/observations/calendar.svelte"
  import ObservationsMonthly from "@/pages/observations/monthly.svelte"
  import SunspotNumberAgg from "@/pages/sunspot_number/agg.svelte"
  import SunspotNumberHemispheric from "@/pages/sunspot_number/hemispheric.svelte"
  import SunspotNumberWholeDisk from "@/pages/sunspot_number/whole_disk.svelte"
  import SunspotNumberWithSilsoAgg from "@/pages/sunspot_number/with_silso/agg.svelte"
  import SunspotNumberWithSilsoDiff from "@/pages/sunspot_number/with_silso/diff.svelte"
  import SunspotNumberWithSilsoRatio from "@/pages/sunspot_number/with_silso/ratio.svelte"
  import SunspotNumberWithSilsoRatioDiff1 from "@/pages/sunspot_number/with_silso/ratio_diff_1.svelte"
  import SunspotNumberWithSilsoScatter from "@/pages/sunspot_number/with_silso/scatter.svelte"
  import SunspotNumberWithSilsoDraw from "@/pages/sunspot_number/with_silso/with_silso.svelte"
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
      path: "check",
      name: "Check",
      children: [
        { path: "file", name: "File", page: CheckFile },
        { path: "data", name: "Data", page: CheckData },
        { path: "finder", name: "Finder", page: CheckFinder },
      ],
    },
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
        {
          path: "with_silso",
          name: "With SILSO",
          children: [
            {
              path: "agg",
              name: "Agg",
              page: SunspotNumberWithSilsoAgg,
            },
            {
              path: "with_silso",
              name: "With SILSO",
              page: SunspotNumberWithSilsoDraw,
            },
            {
              path: "scatter",
              name: "Scatter",
              page: SunspotNumberWithSilsoScatter,
            },
            {
              path: "ratio",
              name: "Ratio",
              page: SunspotNumberWithSilsoRatio,
            },
            {
              path: "diff",
              name: "Diff",
              page: SunspotNumberWithSilsoDiff,
            },
            {
              path: "ratio_diff_1",
              name: "Ratio and Difference 1",
              page: SunspotNumberWithSilsoRatioDiff1,
            },
          ],
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
            class="block whitespace-nowrap border-b-4 border-gray-300 px-4 py-2 hover:bg-gray-200 focus:bg-gray-200 focus:outline-none"
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
