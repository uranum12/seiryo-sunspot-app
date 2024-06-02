<script lang="ts">
import { onMount } from "svelte"

import Agg from "./pages/agg.svelte"

let page: string

const getPageName = () => {
  page = location.hash.replace("#", "")
}

onMount(getPageName)
</script>

<svelte:window on:hashchange={getPageName} />

<main>
  <a href="/#">home</a>
  <a href="/#agg">agg</a>
  <a href="/docs">api docs</a>

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
