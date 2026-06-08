import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { resolveRelative, slugTag, FullSlug } from "../util/path"
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
  Geistesblitz: { key: "geistesblitz", label: "Geistesblitz", color: "#facc15", inAlles: true },
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
  { key: "geistesblitz", label: "Geistesblitz" },
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

interface CloudTag {
  tag: string
  count: number
  url: string
  color: string
}

// Strukturelle Tags gehören nicht in die Wolke — sie sind redundant zu den
// Rubrik-Chips bzw. reine Metadaten und würden die Wolke dominieren.
const EXCLUDED_TAGS = new Set([
  "zeitgeist",
  "denker",
  "gedanke",
  "gedanken",
  "panorama",
  "denker-vita",
  "denkervita",
  "goodnews",
  "good-news",
  "gespräch",
  "meta",
  "index",
])
const isStructuralTag = (t: string) => EXCLUDED_TAGS.has(t) || t.startsWith("year-")
// Tags ab dieser Häufigkeit erscheinen in der Wolke
const CLOUD_MIN_COUNT = 3

function shortDate(d: Date): string {
  return d.toLocaleDateString("de-DE", { day: "2-digit", month: "2-digit", year: "numeric" })
}

const DesktopFeed: QuartzComponent = ({ allFiles, fileData, displayClass }: QuartzComponentProps) => {
  const entries: FeedEntry[] = []
  // Tag-Häufigkeit gesamt + pro Rubrik (für Farbe nach dominanter Rubrik)
  const tagTotal: Record<string, number> = {}
  const tagByCat: Record<string, Record<string, number>> = {}
  const catColor: Record<string, string> = {}
  Object.values(CATEGORIES).forEach((c) => (catColor[c.key] = c.color))

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

    // Tags dieser Note zählen (strukturelle übersprungen)
    for (const rawTag of page.frontmatter?.tags ?? []) {
      const tag = String(rawTag).toLowerCase()
      if (isStructuralTag(tag)) continue
      tagTotal[tag] = (tagTotal[tag] ?? 0) + 1
      ;(tagByCat[tag] ??= {})[cat.key] = (tagByCat[tag]?.[cat.key] ?? 0) + 1
    }
  }

  entries.sort((a, b) => b.ts - a.ts)

  // Tag-Wolke: ab Mindesthäufigkeit, alphabetisch, Farbe = dominante Rubrik
  const cloud: CloudTag[] = Object.entries(tagTotal)
    .filter(([, count]) => count >= CLOUD_MIN_COUNT)
    .map(([tag, count]) => {
      const domKey = Object.entries(tagByCat[tag]).sort((a, b) => b[1] - a[1])[0][0]
      return {
        tag,
        count,
        color: catColor[domKey] ?? "#a78bfa",
        url: resolveRelative(fileData.slug!, `tags/${slugTag(tag)}` as FullSlug),
      }
    })
    .sort((a, b) => a.tag.localeCompare(b.tag, "de"))

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
        <button class="df-chip df-chip-tags" data-tab="tags" type="button" aria-label="Tag-Wolke">
          <svg
            class="df-chip-icon"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            aria-hidden="true"
          >
            <path d="M9 5H2v7l6.29 6.29a2.4 2.4 0 0 0 3.42 0l4.58-4.58a2.4 2.4 0 0 0 0-3.42L10 4" />
            <circle cx="5.5" cy="8.5" r="1.5" fill="currentColor" stroke="none" />
          </svg>
          <span>Tags</span>
        </button>
      </nav>
      <div class="df-grid" />
      <div class="df-sentinel" aria-hidden="true" />
      <div class="df-cloud" hidden />
      <script
        type="application/json"
        id="desktop-feed-data"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(entries) }}
      />
      <script
        type="application/json"
        id="desktop-feed-tags"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(cloud) }}
      />
    </div>
  )
}

DesktopFeed.afterDOMLoaded = script
DesktopFeed.css = style

export default (() => DesktopFeed) satisfies QuartzComponentConstructor
