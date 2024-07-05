<script lang="ts">
  import type { Component } from "svelte"

  import Agg from "@/features/agg/agg.svelte"
  import ButterflyAgg from "@/features/butterfly/agg.svelte"
  import ButterflyDraw from "@/features/butterfly/draw.svelte"
  import ObservationsAgg from "@/features/observations/agg.svelte"
  import ObservationsCalendar from "@/features/observations/calendar.svelte"
  import ObservationsMonthly from "@/features/observations/monthly.svelte"
  import SunspotNumberAgg from "@/features/sunspot_number/agg.svelte"
  import SunspotNumberHemispheric from "@/features/sunspot_number/hemispheric.svelte"
  import SunspotNumberWholeDisk from "@/features/sunspot_number/whole_disk.svelte"

  let currentPath = $state<string[]>([""])

  const getPageName = () => {
    currentPath = location.hash.replace("#/", "").split("/")
  }

  $effect(getPageName)

  type Page = {
    path: string
    page?: Component
    children?: Page[]
  }

  const searchPage = (path: string[], pages: Page[]): Component | undefined => {
    if (path.length < 1) {
      return undefined
    }
    for (let page of pages) {
      if (page.path === path[0]) {
        if (path.length === 1) {
          return page.page
        }
        return page.children && searchPage(path.slice(1), page.children)
      }
    }
    return undefined
  }

  const pages: Page[] = [
    { path: "", page: Agg },
    { path: "agg", page: Agg },
    {
      path: "sunspot_number",

      children: [
        { path: "agg", page: SunspotNumberAgg },
        {
          path: "whole_disk",

          page: SunspotNumberWholeDisk,
        },
        {
          path: "hemispheric",

          page: SunspotNumberHemispheric,
        },
      ],
    },
    {
      path: "observations",

      children: [
        { path: "agg", page: ObservationsAgg },
        { path: "monthly", page: ObservationsMonthly },
        { path: "calendar", page: ObservationsCalendar },
      ],
    },
    {
      path: "butterfly",

      children: [
        { path: "agg", page: ButterflyAgg },
        { path: "draw", page: ButterflyDraw },
      ],
    },
  ]

  const page = $derived(searchPage(currentPath, pages))
</script>

<svelte:window on:hashchange={getPageName} />

<header class="mb-4 px-8">
  <ul class="flex">
    <li class="">
      <a
        href="/#"
        class="block px-4 py-2 border-blue-300 hover:bg-gray-200 focus:bg-gray-200 focus:outline-none"
        >home</a
      >
    </li>
    <li class="">
      <a
        href="/#agg"
        class="block px-4 py-2 hover:bg-gray-200 focus:bg-gray-200 focus:outline-none"
        >agg</a
      >
    </li>
    <li class="">
      <a
        href="/docs"
        class="block px-4 py-2 hover:bg-gray-200 focus:bg-gray-200 focus:outline-none"
        >api docs</a
      >
    </li>
  </ul>
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
