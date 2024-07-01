<script lang="ts">
  import Agg from "@/features/agg/agg.svelte"
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

<header>
  <div class="pure-menu pure-menu-horizontal">
    <a href="/#" class="pure-menu-heading pure-menu-link">home</a>
    <ul class="pure-menu-list">
      <li class="pure-menu-item">
        <a href="/#agg" class="pure-menu-link">agg</a>
      </li>
      <li class="pure-menu-item">
        <a href="/docs" class="pure-menu-link">api docs</a>
      </li>
    </ul>
  </div>
</header>

<main>
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
  {:else}
    <div class="container">
      <h2>Error: Not Found!</h2>
    </div>
  {/if}
</main>

<style>
  header {
    height: fit-content;
  }
  main {
    padding-left: 2rem;
    padding-right: 2rem;
  }
</style>
