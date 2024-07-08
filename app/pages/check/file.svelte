<script lang="ts">
  import {
    type CheckFileError,
    getCheckFile,
    isErrorField,
    isErrorHeader,
    isErrorRow,
  } from "@/api/check/file"
  import { getFileCsv } from "@/api/file/csv"
  import { getFiles } from "@/api/files"
  import Accordion from "@/components/accordion.svelte"
  import Alert from "@/components/alert.svelte"
  import Filter from "@/components/filter.svelte"
  import { FetchError } from "@/utils/fetch"

  type ErrorPos = {
    row: number
    col: number[]
  }

  const correctHeader = ["date", "no", "lat", "lon", "num"]

  let filter = $state<string>("")
  let input = $state<string>("")

  const getFilesCheck = () => {
    return getFiles({ path: "data", glob: "*.csv" })
  }

  let filesPromise = $state<ReturnType<typeof getFiles>>(getFilesCheck())
  let checkPromise = $state<ReturnType<typeof getCheckFile>>()
  let csvPromise = $state<ReturnType<typeof getFileCsv>>()

  const submitDisabled = $derived(input.trim() === "")

  const filterFiles = (files: string[]): string[] => {
    return files
      .filter((file) => file.replace(/^data\//, "").includes(filter))
      .sort()
  }

  const calcErrorPos = (errors: CheckFileError[]): ErrorPos[] => {
    return errors.filter(isErrorField).map((e) => ({
      row: e.line - 1,
      col: e.fields.map((i) => correctHeader.indexOf(i) + 1),
    }))
  }

  const isItemError = (
    item: string | null,
    row: number,
    col: number,
    errors: CheckFileError[],
    errorPos: ErrorPos[]
  ) => {
    return (
      errorPos.some((e) => e.row === row && e.col.includes(col)) ||
      (errors.filter(isErrorHeader).length && !row && col) ||
      (item !== null && col > 5)
    )
  }

  const fetchFiles = () => {
    checkPromise = undefined
    csvPromise = undefined
    filesPromise = getFilesCheck()
  }

  const submitCheck = () => {
    checkPromise = getCheckFile({ input })
    csvPromise = getFileCsv({ input })
  }
</script>

<section>
  <button onclick={fetchFiles}>refresh files</button>
</section>

{#await filesPromise}
  <p>loading...</p>
{:then files}
  {@const filtered = filterFiles(files)}
  <section class="space-y-1">
    <Filter bind:filter />
    {#if filtered.length === 0}
      <Alert type="warning">
        <p>no files matched</p>
      </Alert>
    {:else}
      <select required bind:value={input}>
        <option value="" selected disabled>select file</option>
        {#each filtered as file}
          <option value={file}>{file.replace(/^data\//, "")}</option>
        {/each}
      </select>
      <button disabled={submitDisabled} onclick={submitCheck}>submit</button>
    {/if}
  </section>
{:catch e}
  <section>
    <Alert type="error">
      <p>{e.message}</p>
    </Alert>
  </section>
{/await}

{#if checkPromise && csvPromise}
  {#await Promise.all([checkPromise, csvPromise])}
    <p>loading...</p>
  {:then result}
    {@const [errors, data] = result}
    {#if errors.length === 0}
      <section>
        <Alert type="success">No Error found</Alert>
      </section>
    {:else}
      {@const errorPos = calcErrorPos(errors)}
      <section>
        <Accordion summary="csv file">
          <table>
            <tbody>
              {#each data as row, i}
                <tr>
                  {#each [`${i + 1}`].concat(row) as item, j}
                    <td
                      class="first:border-r-2"
                      class:bg-gray-200={item === null}
                      class:bg-red-200={isItemError(
                        item,
                        i,
                        j,
                        errors,
                        errorPos
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
      </section>
      <section class="space-y-1">
        {#each errors as error}
          <Alert type="error">
            {#if isErrorHeader(error)}
              <p>
                invalid header :
                <code>[{error.header.map((i) => `"${i}"`)}]</code>
              </p>
            {:else if isErrorRow(error)}
              <p>
                line : {error.line}, over items :
                <code>[{error.over.map((i) => `"${i}"`)}]</code>
              </p>
            {:else if isErrorField(error)}
              <p>
                line : {error.line}, fields :
                <code>[{error.fields.map((i) => `"${i}"`)}]</code>
              </p>
            {/if}
          </Alert>
        {/each}
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
