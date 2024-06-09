<script lang="ts">
  import { onMount } from "svelte"

  import Agg from "@/pages/agg.svelte"

  let page: string

  const getPageName = () => {
    page = location.hash.replace("#", "")
  }

  onMount(getPageName)
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
    <div class="container">
      <h1>hello world!</h1>
    </div>
  {:else if page === "agg"}
    <Agg />
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
