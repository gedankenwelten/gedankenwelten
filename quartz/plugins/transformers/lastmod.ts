import fs from "fs"
import { Repository } from "@napi-rs/simple-git"
import { QuartzTransformerPlugin } from "../types"
import path from "path"
import { styleText } from "util"
import { execSync } from "child_process"

// Git-Erstellungsdatum (erster Commit, der die Datei hinzufügt) je repo-relativem
// Pfad. @napi-rs/simple-git bietet nur das *letzte* Änderungsdatum — für ein
// stabiles "created" (immun gegen Checkout-Zeit & spätere Banner-/Link-Commits)
// lesen wir die Add-Historie einmal pro Build via `git log --diff-filter=A`.
const gitCreatedCache = new Map<string, Map<string, number>>()

function getGitCreatedMap(workdir: string): Map<string, number> {
  const cached = gitCreatedCache.get(workdir)
  if (cached) return cached

  const map = new Map<string, number>()
  try {
    const out = execSync(
      "git -c core.quotepath=false log --diff-filter=A --name-only --format=@%cs",
      { cwd: workdir, encoding: "utf8", maxBuffer: 256 * 1024 * 1024 },
    )
    let cur = 0
    for (const raw of out.split("\n")) {
      const line = raw.trim()
      if (!line) continue
      if (line.startsWith("@")) {
        const d = new Date(line.slice(1) + "T00:00:00")
        cur = isNaN(d.getTime()) ? 0 : d.getTime()
      } else if (cur) {
        // log läuft neueste→älteste: überschreiben lässt das ÄLTESTE Add gewinnen
        map.set(line, cur)
      }
    }
  } catch {
    // kein Git / Fehler — Map bleibt leer, Fallback greift
  }

  gitCreatedCache.set(workdir, map)
  return map
}

export interface Options {
  priority: ("frontmatter" | "git" | "filesystem")[]
}

const defaultOptions: Options = {
  priority: ["frontmatter", "git", "filesystem"],
}

// YYYY-MM-DD
const iso8601DateOnlyRegex = /^\d{4}-\d{2}-\d{2}$/
const germanDateRegex = /^(\d{2})\.(\d{2})\.(\d{4})$/ // DD.MM.YYYY

function coerceDate(fp: string, d: any): Date {
  // bare year: YAML parses `date: 2016` as the number 2016, which `new Date()`
  // would read as 2016 milliseconds after epoch (-> 01.01.1970). Treat 4-digit
  // integers (and "2016" strings) as January 1st of that year. Filesystem
  // timestamps live in the ~1e12 range, so they are never caught here.
  if (typeof d === "number" && Number.isInteger(d) && d >= 1000 && d <= 9999) {
    d = `${d}-01-01T00:00:00`
  }
  if (typeof d === "string" && /^\d{4}$/.test(d)) {
    d = `${d}-01-01T00:00:00`
  }

  // check ISO8601 date-only format
  // we treat this one as local midnight as the normal
  // js date ctor treats YYYY-MM-DD as UTC midnight
  if (typeof d === "string" && iso8601DateOnlyRegex.test(d)) {
    d = `${d}T00:00:00`
  }

  // convert German DD.MM.YYYY -> ISO before parsing
  if (typeof d === "string") {
    const gm = d.match(germanDateRegex)
    if (gm) d = gm[3] + "-" + gm[2] + "-" + gm[1] + "T00:00:00"
  }

  const dt = new Date(d)
  const invalidDate = isNaN(dt.getTime()) || dt.getTime() === 0
  if (invalidDate && d !== undefined) {
    console.log(
      styleText(
        "yellow",
        `\nWarning: found invalid date "${d}" in \`${fp}\`. Supported formats: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date#date_time_string_format`,
      ),
    )
  }

  return invalidDate ? new Date() : dt
}

type MaybeDate = undefined | string | number
export const CreatedModifiedDate: QuartzTransformerPlugin<Partial<Options>> = (userOpts) => {
  const opts = { ...defaultOptions, ...userOpts }
  return {
    name: "CreatedModifiedDate",
    markdownPlugins(ctx) {
      return [
        () => {
          let repo: Repository | undefined = undefined
          let repositoryWorkdir: string
          if (opts.priority.includes("git")) {
            try {
              repo = Repository.discover(ctx.argv.directory)
              repositoryWorkdir = repo.workdir() ?? ctx.argv.directory
            } catch (e) {
              console.log(
                styleText(
                  "yellow",
                  `\nWarning: couldn't find git repository for ${ctx.argv.directory}`,
                ),
              )
            }
          }

          return async (_tree, file) => {
            let created: MaybeDate = undefined
            let modified: MaybeDate = undefined
            let published: MaybeDate = undefined

            const fp = file.data.relativePath!
            const fullFp = file.data.filePath!
            for (const source of opts.priority) {
              if (source === "filesystem") {
                const st = await fs.promises.stat(fullFp)
                created ||= st.birthtimeMs
                modified ||= st.mtimeMs
              } else if (source === "frontmatter" && file.data.frontmatter) {
                created ||= file.data.frontmatter.created as MaybeDate
                modified ||= file.data.frontmatter.modified as MaybeDate
                published ||= file.data.frontmatter.published as MaybeDate
              } else if (source === "git" && repo) {
                try {
                  const relativePath = path.relative(repositoryWorkdir, fullFp)
                  modified ||= await repo.getFileLatestModifiedDateAsync(relativePath)
                  // created aus Git-Add-Historie (statt Checkout-Zeit des Filesystems)
                  const gitCreated = getGitCreatedMap(repositoryWorkdir).get(relativePath)
                  if (gitCreated) created ||= gitCreated
                } catch {
                  console.log(
                    styleText(
                      "yellow",
                      `\nWarning: ${file.data.filePath!} isn't yet tracked by git, dates will be inaccurate`,
                    ),
                  )
                }
              }
            }

            file.data.dates = {
              created: coerceDate(fp, created),
              modified: coerceDate(fp, modified),
              published: coerceDate(fp, published),
            }
          }
        },
      ]
    },
  }
}

declare module "vfile" {
  interface DataMap {
    dates: {
      created: Date
      modified: Date
      published: Date
    }
  }
}
