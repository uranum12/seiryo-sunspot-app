import fs from "node:fs"
import esbuild from "esbuild"
import sveltePlugin from "esbuild-svelte"
import sveltePreprocess from "svelte-preprocess"

if (!fs.existsSync("dist")) {
  fs.mkdirSync("dist")
}

esbuild
  .build({
    entryPoints: ["app/main.ts"],
    mainFields: ["svelte", "browser", "module", "main"],
    conditions: ["svelte", "browser"],
    outdir: "dist",
    bundle: true,
    minify: true,
    plugins: [
      sveltePlugin({
        preprocess: sveltePreprocess(),
      }),
    ],
    logLevel: "info",
  })
  .catch((err) => {
    console.error(err)
    process.exit(1)
  })

fs.cpSync("app/static", "dist", { recursive: true })
