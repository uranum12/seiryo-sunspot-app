<script lang="ts">
  import {
    getCheckDataGroupNumber,
    getCheckDataLatRange,
    getCheckDataLonRange,
    getCheckDataLatInterval,
    getCheckDataLonInterval,
  } from "@/api/check/data"
  import { getFiles } from "@/api/files"
  import Alert from "@/components/alert.svelte"
  import { FetchError } from "@/utils/fetch"

  type GroupNumber = [string, number[], number[]]

  function zipGroupNumber(
    res: Awaited<ReturnType<typeof getCheckDataGroupNumber>>
  ): GroupNumber[] {
    const len = res.date.length
    const result: GroupNumber[] = []
    for (let i = 0; i < len; i++) {
      result.push([res.date[i], res.original[i], res.expected[i]])
    }
    return result
  }

  type Range = [string, number, number, number]

  function zipLatRange(
    res: Awaited<ReturnType<typeof getCheckDataLatRange>>
  ): Range[] {
    const len = res.date.length
    const result: Range[] = []
    for (let i = 0; i < len; i++) {
      result.push([res.date[i], res.no[i], res.latMin[i], res.latMax[i]])
    }
    return result
  }

  function zipLonRange(
    res: Awaited<ReturnType<typeof getCheckDataLonRange>>
  ): Range[] {
    const len = res.date.length
    const result: Range[] = []
    for (let i = 0; i < len; i++) {
      result.push([res.date[i], res.no[i], res.lonMin[i], res.lonMax[i]])
    }
    return result
  }

  type Interval = [string, number, number, number, number]

  function zipLatInterval(
    res: Awaited<ReturnType<typeof getCheckDataLatInterval>>
  ): Interval[] {
    const len = res.date.length
    const result: Interval[] = []
    for (let i = 0; i < len; i++) {
      result.push([
        res.date[i],
        res.no[i],
        res.latMin[i],
        res.latMax[i],
        res.interval[i],
      ])
    }
    return result
  }

  function zipLonInterval(
    res: Awaited<ReturnType<typeof getCheckDataLonInterval>>
  ): Interval[] {
    const len = res.date.length
    const result: Interval[] = []
    for (let i = 0; i < len; i++) {
      result.push([
        res.date[i],
        res.no[i],
        res.lonMin[i],
        res.lonMax[i],
        res.interval[i],
      ])
    }
    return result
  }

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
  <section class="space-y-1">
    <select required bind:value={input}>
      <option value="" selected disabled>select file</option>
      {#each files as file}
        <option value={file}>{file.replace(/^data\//, "")}</option>
      {/each}
    </select>
    <button disabled={submitDisabled} onclick={submitCheck}>submit</button>
  </section>
{:catch e}
  <section>
    <Alert type="error">
      <p>{e.message}</p>
    </Alert>
  </section>
{/await}

{#snippet table(headers, data)}
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
            <td>{item}</td>
          {/each}
        </tr>
      {/each}
    </tbody>
  </table>
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
    {#if groupNumberData.date.length === 0}
      <section>
        <Alert type="success">
          <p>No Error in group number</p>
        </Alert>
      </section>
    {:else}
      <section class="space-y-1">
        <Alert type="error">
          <p>Error in group number</p>
        </Alert>
        {@render table(
          ["date", "original", "expected"],
          zipGroupNumber(groupNumberData)
        )}
      </section>
    {/if}
    {#if latRangeData.date.length === 0}
      <section>
        <Alert type="success">
          <p>No Error in latitude range</p>
        </Alert>
      </section>
    {:else}
      <section class="space-y-1">
        <Alert type="error">
          <p>Error in latitude range</p>
        </Alert>
        {@render table(
          ["date", "no", "lat_min", "lat_max"],
          zipLatRange(latRangeData)
        )}
      </section>
    {/if}
    {#if lonRangeData.date.length === 0}
      <section>
        <Alert type="success">
          <p>No Error in longitude range</p>
        </Alert>
      </section>
    {:else}
      <section class="space-y-1">
        <Alert type="error">
          <p>Error in longitude range</p>
        </Alert>
        {@render table(
          ["date", "no", "lon_min", "lon_max"],
          zipLonRange(lonRangeData)
        )}
      </section>
    {/if}
    {#if latIntervalData.date.length === 0}
      <section>
        <Alert type="success">
          <p>No Error in latitude interval</p>
        </Alert>
      </section>
    {:else}
      <section class="space-y-1">
        <Alert type="error">
          <p>Error in latitude interval</p>
        </Alert>
        {@render table(
          ["date", "no", "lat_min", "lat_max", "interval"],
          zipLatInterval(latIntervalData)
        )}
      </section>
    {/if}
    {#if lonIntervalData.date.length === 0}
      <section>
        <Alert type="success">
          <p>No Error in longitude interval</p>
        </Alert>
      </section>
    {:else}
      <section class="space-y-1">
        <Alert type="error">
          <p>Error in longitude interval</p>
        </Alert>
        {@render table(
          ["date", "no", "lon_min", "lon_max", "interval"],
          zipLonInterval(lonIntervalData)
        )}
      </section>
    {/if}
  {:catch e}
    <section>
      <Alert type="error">
        <p>{e instanceof FetchError ? e.detail : e.message}</p>
      </Alert>
    </section>
  {/await}
{/if}
