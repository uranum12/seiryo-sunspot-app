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

  let page = $state<string>("")

  const getPageName = () => {
    page = location.hash.replace("#", "")
  }

  $effect(getPageName)
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
  {#if page === ""}
    <h1>hello world!</h1>
  {:else if page === "agg"}
    <Agg />
  {:else if page === "sunspot_number/agg"}
    <SunspotNumberAgg />
  {:else if page === "sunspot_number/whole_disk"}
    <SunspotNumberWholeDisk />
  {:else if page === "sunspot_number/hemispheric"}
    <SunspotNumberHemispheric />
  {:else if page === "observations/agg"}
    <ObservationsAgg />
  {:else if page === "observations/monthly"}
    <ObservationsMonthly />
  {:else if page === "observations/calendar"}
    <ObservationsCalendar />
  {:else if page === "butterfly/agg"}
    <ButterflyAgg />
  {:else if page === "butterfly/draw"}
    <ButterflyDraw />
  {:else}
    <div class="container">
      <h2>Error: Not Found!</h2>
    </div>
  {/if}
</main>
