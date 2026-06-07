import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { resolveRelative } from "../util/path"
import { classNames } from "../util/lang"
// @ts-ignore
import script from "./scripts/desktopFeed.inline"
import style from "./styles/desktopFeed.scss"

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

// Reihenfolge der Chips (Profile ganz rechts)
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
}

function shortDate(d: Date): string {
  return d.toLocaleDateString("de-DE", { day: "2-digit", month: "2-digit", year: "numeric" })
}

const DesktopFeed: QuartzComponent = ({ allFiles, fileData, displayClass }: QuartzComponentProps) => {
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
    const fmDate = page.frontmatter?.aktualisiert as string | undefined
    let when: Date | undefined
    if (fmDate) {
      const parsed = new Date(fmDate)
      if (!isNaN(parsed.getTime())) when = parsed
    }
    if (!when) when = page.dates?.created ?? page.dates?.modified
    const ts = when ? when.getTime() : 0

    entries.push({
      title,
      cat: cat.key,
      catLabel: cat.label,
      color: cat.color,
      inAlles: cat.inAlles,
      url: resolveRelative(fileData.slug!, slug),
      thumb: page.banner?.src ?? null,
      date: when ? shortDate(when) : "",
      ts,
    })
  }

  entries.sort((a, b) => b.ts - a.ts)

  return (
    <div class={classNames(displayClass, "desktop-feed")}>
      <nav class="df-chips" aria-label="Rubriken">
        {TABS.map((t, i) => (
          <button class={`df-chip${i === 0 ? " active" : ""}`} data-tab={t.key} type="button">
            {t.key === "alles" ? (
              <svg
                class="df-chip-icon"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                aria-hidden="true"
              >
                <rect x="3" y="3" width="7" height="7" rx="1.5" />
                <rect x="14" y="3" width="7" height="7" rx="1.5" />
                <rect x="3" y="14" width="7" height="7" rx="1.5" />
                <rect x="14" y="14" width="7" height="7" rx="1.5" />
              </svg>
            ) : (
              <img class="df-chip-icon" src={`/assets/rubrik-${t.key}.png`} alt="" />
            )}
            <span>{t.label}</span>
          </button>
        ))}
      </nav>
      <div class="df-grid" />
      <div class="df-sentinel" aria-hidden="true" />
      <script
        type="application/json"
        id="desktop-feed-data"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(entries) }}
      />
    </div>
  )
}

DesktopFeed.afterDOMLoaded = script
DesktopFeed.css = style

export default (() => DesktopFeed) satisfies QuartzComponentConstructor
