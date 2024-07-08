<script lang="ts">
  import { getCheckFile } from "@/api/check/file"
  import { getFileCsv } from "@/api/file/csv"
  import { getFiles } from "@/api/files"
  import Accordion from "@/components/accordion.svelte"
  import Alert from "@/components/alert.svelte"
  import FileSelect from "@/components/file_select.svelte"
  import { FetchError } from "@/utils/fetch"

  let selected = $state<string[]>([])
  let inputs = $state<string[]>([])

  const getFilesCheck = () => {
    return getFiles({ path: "data", glob: "*.csv" })
  }

  const getCsv = (i: number) => {
    return getFileCsv({ input: inputs[i] })
  }

  let filesPromise = $state<ReturnType<typeof getFiles>>(getFilesCheck())
  let checkPromises = $state<ReturnType<typeof getCheckFile>[]>([])

  const submitDisabled = $derived(selected.length === 0)

  const fetchFiles = () => {
    checkPromises = []
    filesPromise = getFilesCheck()
  }

  const submitCheck = () => {
    inputs = selected
    checkPromises = inputs.map((input) => getCheckFile({ input }))
  }

  const correctHeader = ["date", "no", "lat", "lon", "num"]

  const calcErrorPos = (
    errors: Awaited<ReturnType<typeof getCheckFile>>,
    csv: Awaited<ReturnType<typeof getFileCsv>>
  ) => {
    const errPos: [number, number[]][] = []
    for (const e of errors) {
      if (e.type === "field") {
        errPos.push([e.line - 1, e.fields.map((i) => correctHeader.indexOf(i))])
      }
    }
    const result: [number, number][] = []
    for (const i of errPos) {
      for (const j of i[1]) {
        result.push([i[0], j])
      }
    }
    if (errors.filter((e) => e.type === "header").length) {
      result.push([0, 0], [0, 1], [0, 2], [0, 3], [0, 4])
    }
    for (let i = 0; i < csv.length; i++) {
      for (let j = 0; j < csv[i].length; j++) {
        if (csv[i][j] !== null && j > 4) {
          result.push([i, j])
        }
      }
    }
    return result
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
      <FileSelect {files} bind:selected />
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

{#if checkPromises.length}
  {#await Promise.all(checkPromises)}
    <p>loading...</p>
  {:then result}
    {@const errorIndex = result
      .map((e, i) => ({ e, i }))
      .filter((i) => i.e.length)
      .map((i) => i.i)}
    {#if errorIndex.length}
      {#each errorIndex as i}
        <section class="space-y-1">
          <p class="text-xl">Error in {inputs[i]}</p>
          {#each result[i] as error}
            <Alert type="error">
              {#if error.type === "header"}
                <p>
                  invalid header : <code>{JSON.stringify(error.header)}</code>
                </p>
              {:else if error.type === "row"}
                <p>
                  line : {error.line}, over items :
                  <code>{JSON.stringify(error.over)}</code>
                </p>
              {:else}
                <p>
                  line : {error.line}, fields :
                  <code>{JSON.stringify(error.fields)}</code>
                </p>
              {/if}
            </Alert>
          {/each}
          {#await getCsv(i) then csv}
            {@const errPos = calcErrorPos(result[i], csv)}
            {JSON.stringify(errPos)}
            <Accordion summary="csv file">
              <table>
                <tbody>
                  {#each csv as line, i}
                    <tr>
                      <td class="border-r-2">{i + 1}</td>
                      {#each line as item, j}
                        <td
                          class:bg-gray-200={item === null}
                          class:bg-red-200={errPos.some(
                            (pos) => pos[0] === i && pos[1] === j
                          )}
                        >
                          {item}
                        </td>
                      {/each}
                    </tr>
                  {/each}
                </tbody>
              </table>
            </Accordion>
          {:catch e}
            <Alert type="error">
              <p>{e instanceof FetchError ? e.detail : e.message}</p>
            </Alert>
          {/await}
        </section>
      {/each}
    {:else}
      <section>
        <Alert type="success">
          <p>No Error in all files</p>
        </Alert>
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
