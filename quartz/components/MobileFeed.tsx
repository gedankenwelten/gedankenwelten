import fs from "fs"
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { FullSlug, resolveRelative } from "../util/path"
import { QuartzPluginData } from "../plugins/vfile"
import { classNames } from "../util/lang"
// @ts-ignore
import script from "./scripts/mobileFeed.inline"
import style from "./styles/mobileFeed.scss"

interface Category {
  key: string
  label: string
  color: string
  inAlles: boolean
}

// Rubrik-Definitionen — Schlüssel = oberster Ordner in content/
const CATEGORIES: Record<string, Category> = {
  Zeitgeist: { key: "zeitgeist", label: "Zeitgeist", color: "#a78bfa", inAlles: true },
  Denker: { key: "denker", label: "Denker", color: "#6366f1", inAlles: true },
  Panorama: { key: "panorama", label: "Panorama", color: "#2dd4bf", inAlles: true },
  Gedanken: { key: "gedanken", label: "Gedanken", color: "#f59e0b", inAlles: true },
  GoodNews: { key: "goodnews", label: "GoodNews", color: "#22c55e", inAlles: true },
  // DenkerVita: eigener Tab, aber NICHT im "Alles"-Feed (zeitlose Profile)
  DenkerVita: { key: "denkervita", label: "DenkerVita", color: "#d6a06a", inAlles: false },
}

// Reihenfolge der Tabs (Profile ganz rechts)
const TABS = [
  { key: "alles", label: "Alles" },
  { key: "zeitgeist", label: "Zeitgeist" },
  { key: "denker", label: "Denker" },
  { key: "panorama", label: "Panorama" },
  { key: "gedanken", label: "Gedanken" },
  { key: "goodnews", label: "GoodNews" },
  { key: "denkervita", label: "DenkerVita" },
]

interface FeedEntry {
  title: string
  cat: string
  catLabel: string
  color: string
  inAlles: boolean
  url: string
  thumb: string | null
  date: string
  ts: number
  desc: string
}

function shortDate(d: Date): string {
  return d.toLocaleDateString("de-DE", { day: "2-digit", month: "2-digit", year: "numeric" })
}

const MobileFeed: QuartzComponent = ({ allFiles, fileData, displayClass }: QuartzComponentProps) => {
  const entries: FeedEntry[] = []

  for (const page of allFiles) {
    const slug = page.slug
    if (!slug || !slug.includes("/")) continue // Ordner-/Index-Seiten überspringen
    const parts = slug.split("/")
    const top = parts[0]
    const last = parts[parts.length - 1].toLowerCase()
    if (last === "index" || last === "readme") continue // Rubrik-Landingpages raus
    const cat = CATEGORIES[top]
    if (!cat) continue
    const title = page.frontmatter?.title
    if (!title) continue

    // Datum: aktualisiert (Frontmatter) bevorzugt, sonst Erstellungsdatum.
    // Bewusst NICHT git-modified (defaultDateType) — sonst steigen alte Notes
    // hoch, nur weil sie kürzlich ein Banner-/Cross-Link-Commit hatten.
    const fmDate = page.frontmatter?.aktualisiert as string | undefined
    let when: Date | undefined
    if (fmDate) {
      const parsed = new Date(fmDate)
      if (!isNaN(parsed.getTime())) when = parsed
    }
    if (!when) when = page.dates?.created ?? page.dates?.modified
    const ts = when ? when.getTime() : 0

    const banner = page.banner
    const desc = (page.description ?? (page.frontmatter?.description as string) ?? "").trim()

    entries.push({
      title,
      cat: cat.key,
      catLabel: cat.label,
      color: cat.color,
      inAlles: cat.inAlles,
      url: resolveRelative(fileData.slug!, slug),
      thumb: banner?.src ?? null,
      date: when ? shortDate(when) : "",
      ts,
      desc: desc.length > 200 ? desc.slice(0, 197) + "…" : desc,
    })
  }

  entries.sort((a, b) => b.ts - a.ts)

  // Intro-Text aus index.md ziehen (alles vor dem Journal) — für den Footer-Sheet.
  // Direkt aus der Quelldatei lesen (am Build), damit die Original-Absätze erhalten
  // bleiben — fileData.text normalisiert Zeilenumbrüche weg.
  let introParas: string[] = []
  try {
    const raw = fs.readFileSync(fileData.filePath!, "utf8")
    const body = raw.replace(/^---\n[\s\S]*?\n---\n/, "") // Frontmatter weg
    const beforeJournal = body.split(/<!--\s*JOURNAL:START|##\s+Was zuletzt gedacht/)[0]
    const noHeading = beforeJournal.replace(/^#\s+.*$/m, "") // "# Gedankenwelten" weg
    introParas = noHeading
      .split(/\n\s*\n/)
      .map((s) => s.replace(/\s+/g, " ").trim())
      .filter((s) => s && s !== "---")
  } catch {
    introParas = []
  }

  return (
    <div class={classNames(displayClass, "mobile-feed")}>
      <nav class="mf-tabs" aria-label="Rubriken">
        {TABS.map((t, i) => (
          <button class={`mf-tab${i === 0 ? " active" : ""}`} data-tab={t.key} type="button">
            {t.label}
          </button>
        ))}
      </nav>
      <div class="mf-list" />
      <button class="mf-more" type="button" hidden>
        Mehr anzeigen
      </button>
      <div class="mf-sentinel" aria-hidden="true" />
      <script
        type="application/json"
        id="mobile-feed-data"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(entries) }}
      />

      {/* Footer-Leiste — Tap öffnet den Intro-Sheet */}
      <button class="mf-introbar" type="button" aria-haspopup="dialog">
        Gedankenwelten
      </button>

      {/* Intro-Sheet (statisch) */}
      <div class="mf-sheet" id="mf-intro-sheet" role="dialog" aria-modal="true" hidden>
        <div class="mf-sheet-backdrop" data-close />
        <div class="mf-sheet-panel">
          <div class="mf-sheet-handle" data-close />
          <div class="mf-sheet-scroll">
            <h2 class="mf-sheet-title">Gedankenwelten</h2>
            {introParas.map((p) => (
              <p>{p}</p>
            ))}
          </div>
        </div>
      </div>

      {/* Beschreibungs-Sheet (dynamisch, per Lang-Druck) */}
      <div class="mf-sheet" id="mf-desc-sheet" role="dialog" aria-modal="true" hidden>
        <div class="mf-sheet-backdrop" data-close />
        <div class="mf-sheet-panel">
          <div class="mf-sheet-handle" data-close />
          <div class="mf-sheet-scroll">
            <div class="mf-desc-cat" />
            <h2 class="mf-desc-title" />
            <p class="mf-desc-text" />
            <a class="mf-desc-open" href="#">
              Note öffnen →
            </a>
          </div>
        </div>
      </div>

      {/* Note-Sheet (hoch, unter der Suche) — zeigt die Note ohne wegzunavigieren */}
      <div class="mf-sheet mf-sheet-tall" id="mf-note-sheet" role="dialog" aria-modal="true" hidden>
        <div class="mf-sheet-backdrop" data-close />
        <div class="mf-sheet-panel">
          <div class="mf-note-bar">
            <button class="mf-note-close" type="button" data-close aria-label="Schließen">
              ✕
            </button>
            <a class="mf-note-full" href="#">
              ganze Seite ↗
            </a>
          </div>
          <div class="mf-note-content" />
        </div>
      </div>
    </div>
  )
}

MobileFeed.afterDOMLoaded = script
MobileFeed.css = style

export default (() => MobileFeed) satisfies QuartzComponentConstructor
