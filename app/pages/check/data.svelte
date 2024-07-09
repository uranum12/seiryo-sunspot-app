<script lang="ts">
  import {
    getCheckDataGroupNumber,
    getCheckDataLatInterval,
    getCheckDataLatRange,
    getCheckDataLonInterval,
    getCheckDataLonRange,
  } from "@/api/check/data"
  import { getFiles } from "@/api/files"
  import Alert from "@/components/alert.svelte"
  import { FetchError } from "@/utils/fetch"
  import {
    zipGroupNumber,
    zipLatInterval,
    zipLatRange,
    zipLonInterval,
    zipLonRange,
  } from "@/utils/zip_array"

  let input = $state<string>("")
  let latThreshold = $state<number>(50)
  let lonMinThreshold = $state<number>(-180)
  let lonMaxThreshold = $state<number>(180)
  let latInterval = $state<number>(15)
  let lonInterval = $state<number>(30)

  const getFilesCheck = () => {
    return getFiles({ path: "out", glob: "*.parquet" })
  }

  let filesPromise = $state<ReturnType<typeof getFiles>>(getFilesCheck())
  let groupNumberPromise = $state<ReturnType<typeof getCheckDataGroupNumber>>()
  let latRangePromise = $state<ReturnType<typeof getCheckDataLatRange>>()
  let lonRangePromise = $state<ReturnType<typeof getCheckDataLonRange>>()
  let latIntervalPromise = $state<ReturnType<typeof getCheckDataLatInterval>>()
  let lonIntervalPromise = $state<ReturnType<typeof getCheckDataLonInterval>>()

  const checkPromisesAll = $derived(
    groupNumberPromise &&
      latRangePromise &&
      lonRangePromise &&
      latIntervalPromise &&
      lonIntervalPromise
      ? Promise.all([
          groupNumberPromise,
          latRangePromise,
          lonRangePromise,
          latIntervalPromise,
          lonIntervalPromise,
        ])
      : undefined
  )

  const submitDisabled = $derived(input.trim() === "")

  const fetchFiles = () => {
    groupNumberPromise = undefined
    latRangePromise = undefined
    lonRangePromise = undefined
    latIntervalPromise = undefined
    lonIntervalPromise = undefined
    filesPromise = getFilesCheck()
  }

  const submitCheck = () => {
    groupNumberPromise = getCheckDataGroupNumber({ input })
    latRangePromise = getCheckDataLatRange({
      input,
      threshold: latThreshold,
    })
    lonRangePromise = getCheckDataLonRange({
      input,
      minThreshold: lonMinThreshold,
      maxThreshold: lonMaxThreshold,
    })
    latIntervalPromise = getCheckDataLatInterval({
      input,
      interval: latInterval,
    })
    lonIntervalPromise = getCheckDataLonInterval({
      input,
      interval: lonInterval,
    })
  }
</script>

<section>
  <button onclick={fetchFiles}>refresh files</button>
</section>

{#await filesPromise}
  <p>loading...</p>
{:then files}
  {#if files.length !== 0}
    <section class="space-y-1">
      <select required bind:value={input}>
        <option value="" selected disabled>select file</option>
        {#each files as file}
          <option value={file}>{file.replace(/^data\//, "")}</option>
        {/each}
      </select>
      <button disabled={submitDisabled} onclick={submitCheck}>submit</button>
    </section>
  {:else}
    <section>
      <Alert type="warning">
        <p>no files</p>
      </Alert>
    </section>
  {/if}
{:catch e}
  <section>
    <Alert type="error">
      <p>{e.message}</p>
    </Alert>
  </section>
{/await}

{#snippet showError(name, headers, data)}
  {#if data.length === 0}
    <section>
      <Alert type="success">
        <p>No Error in {name}</p>
      </Alert>
    </section>
  {:else}
    <section class="space-y-1">
      <Alert type="error">
        <p>Error in {name}</p>
      </Alert>
      <table>
        <thead>
          <tr>
            {#each headers as header}
              <th>{header}</th>
            {/each}
          </tr>
        </thead>
        <tbody>
          {#each data as row}
            <tr>
              {#each row as item}
                {#if Array.isArray(item)}
                  <td><code>{JSON.stringify(item)}</code></td>
                {:else}
                  <td>{item}</td>
                {/if}
              {/each}
            </tr>
          {/each}
        </tbody>
      </table>
    </section>
  {/if}
{/snippet}

{#if checkPromisesAll}
  {#await checkPromisesAll}
    <p>loading...</p>
  {:then result}
    {@const [
      groupNumberData,
      latRangeData,
      lonRangeData,
      latIntervalData,
      lonIntervalData,
    ] = result}
    {@render showError(
      "group number",
      ["date", "original", "expected"],
      zipGroupNumber(groupNumberData)
    )}
    {@render showError(
      "latitude range",
      ["date", "no", "lat_min", "lat_max"],
      zipLatRange(latRangeData)
    )}
    {@render showError(
      "longitude range",
      ["date", "no", "lon_min", "lon_max"],
      zipLonRange(lonRangeData)
    )}
    {@render showError(
      "latitude interval",
      ["date", "no", "lat_min", "lat_max", "interval"],
      zipLatInterval(latIntervalData)
    )}
    {@render showError(
      "longitude interval",
      ["date", "no", "lon_min", "lon_max", "interval"],
      zipLonInterval(lonIntervalData)
    )}
  {:catch e}
    <section>
      <Alert type="error">
        <p>{e instanceof FetchError ? e.detail : e.message}</p>
      </Alert>
    </section>
  {/await}
{/if}
