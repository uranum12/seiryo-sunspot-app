<script lang="ts">
  import { toDate } from "date-fns"

  import { getFinder } from "@/api/check/finder"
  import { getFileCsv } from "@/api/file/csv"
  import Accordion from "@/components/accordion.svelte"
  import Alert from "@/components/alert.svelte"
  import DateSelect from "@/components/date_select.svelte"
  import { fromDate } from "@/utils/date"
  import { FetchError } from "@/utils/fetch"

  let date = $state<string>()

  let finderPromise = $state<ReturnType<typeof getFinder>>()

  const submitFinder = () => {
    if (date) {
      finderPromise = getFinder(fromDate(toDate(date)))
    }
  }
</script>

<section class="space-y-1">
  <DateSelect bind:date required />
  <button onclick={submitFinder}>submit</button>
</section>

{#if finderPromise}
  {#await finderPromise}
    <p>loading...</p>
  {:then result}
    {#if result.length === 0}
      <section>
        <Alert type="warning">
          <p>No matching data exist</p>
        </Alert>
      </section>
    {:else}
      {#each result as file}
        <section class="space-y-1">
          <p class="text-xl">{file.path}</p>
          <Alert type="success">
            <p>lines : <code>{JSON.stringify(file.lines)}</code></p>
          </Alert>
          {#await getFileCsv({ input: file.path }) then csv}
            <Accordion summary="csv file">
              <table>
                <tbody>
                  {#each csv as line, i}
                    <tr class:bg-red-200={file.lines.includes(i + 1)}>
                      <td>{i + 1}</td>
                      {#each line as item}
                        <td>{item}</td>
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
    {/if}
  {:catch e}
    <section>
      <Alert type="error">
        <p>{e.message}</p>
      </Alert>
    </section>
  {/await}
{/if}
