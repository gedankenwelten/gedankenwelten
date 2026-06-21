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
  Kultur: { key: "kultur", label: "Kultur", color: "#0ea5a4", inAlles: true },
  GoodNews: { key: "goodnews", label: "GoodNews", color: "#22c55e", inAlles: true },
  // Spuren: lebende Spuren (Zeit-Dimension) — im "Alles"-Feed, floatet via aktualisiert hoch
  Spuren: { key: "spuren", label: "Spuren", color: "#fb7185", inAlles: true },
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
  { key: "kultur", label: "Kultur" },
  { key: "goodnews", label: "GoodNews" },
  { key: "spuren", label: "Spuren" },
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
  tier: number
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
  "spur",
  "spuren",
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

// aktualisiert: erlaubt DD.MM.YYYY *und* ISO — new Date() würde das deutsche
// Format als US-MM/DD lesen (10.06. → 6. Oktober), daher explizit parsen.
export function parseFmDate(v: unknown): Date | undefined {
  if (v instanceof Date) return isNaN(v.getTime()) ? undefined : v
  if (v == null) return undefined
  const s = String(v).trim()
  const de = s.match(/^(\d{1,2})\.(\d{1,2})\.(\d{4})$/)
  if (de) return new Date(Number(de[3]), Number(de[2]) - 1, Number(de[1]))
  const parsed = new Date(s)
  return isNaN(parsed.getTime()) ? undefined : parsed
}

// Tiered-Sortierung (gespiegelt von build_journal.py): neue Notes (≤7T) immer
// zuoberst — sie gehen nie unter —, dann manuelle Hand (aktualisiert:), dann der
// galilei-Forschungsstand (forschung_aktualisiert:), dann die News-Brücke
// (presseschau_aktualisiert:), dann alt/legacy. Angereicherte Notes floaten hoch,
// aber nie über neue oder manuell vertiefte. Forschung wiegt schwerer als News.
const FEED_WINDOW_DAYS = 7
export function computeTier(
  page: QuartzComponentProps["allFiles"][number],
  now: Date = new Date(),
): { tier: number; when: Date } {
  const fm = (page.frontmatter ?? {}) as Record<string, unknown>
  // created aus dem `date:`-Frontmatter (stabiles Erstellungsdatum) — NICHT aus
  // page.dates.created: Quartz füllt das aus der Datei-Geburtszeit, die unser
  // Sync-cp auf *heute* setzt → alte Notes würden sonst als Tier 0 (neu) gelten.
  const created = parseFmDate(fm.date) ?? parseFmDate(fm.created) ?? page.dates?.created ?? page.dates?.modified
  const akt = parseFmDate(fm.aktualisiert) ?? parseFmDate(fm.updated)
  const fakt = parseFmDate(fm.forschung_aktualisiert)
  const pakt = parseFmDate(fm.presseschau_aktualisiert)
  const cutoff7 = new Date(now.getTime() - FEED_WINDOW_DAYS * 86400000)
  const enrich = [fakt, pakt].filter(Boolean) as Date[]
  if (created && created.getTime() >= cutoff7.getTime()) return { tier: 0, when: created }
  if (akt && enrich.every((d) => akt.getTime() >= d.getTime())) return { tier: 1, when: akt }
  if (fakt && (!pakt || fakt.getTime() >= pakt.getTime())) return { tier: 2, when: fakt }
  if (pakt) return { tier: 3, when: pakt }
  if (akt) return { tier: 1, when: akt }
  if (fakt) return { tier: 2, when: fakt }
  return { tier: 4, when: created ?? new Date(0) }
}

// Rubrik-Banner als Fallback-Thumbnail, wenn die Note kein eigenes Body-Bild hat.
// Öffentlich liegt der Gedankenwelten/-Ordner im Root → Pfad OHNE Gedankenwelten/-Prefix.
const RUBRIK_BANNER = (key: string): string => `/assets/rubrik-banner/${key}.jpg`

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

    // Tiered: neu (≤7T) → manuell → Forschung → Presseschau → alt; Datum = Aktivität des Rangs.
    const { tier, when } = computeTier(page)
    const ts = when.getTime()

    entries.push({
      title,
      cat: cat.key,
      catLabel: cat.label,
      color: cat.color,
      inAlles: cat.inAlles,
      url: resolveRelative(fileData.slug!, slug),
      thumb: page.banner?.src ?? RUBRIK_BANNER(cat.key),
      date: ts > 0 ? shortDate(when) : "",
      ts,
      tier,
    })

    // Tags dieser Note zählen (strukturelle übersprungen)
    for (const rawTag of page.frontmatter?.tags ?? []) {
      const tag = String(rawTag).toLowerCase()
      if (isStructuralTag(tag)) continue
      tagTotal[tag] = (tagTotal[tag] ?? 0) + 1
      ;(tagByCat[tag] ??= {})[cat.key] = (tagByCat[tag]?.[cat.key] ?? 0) + 1
    }
  }

  entries.sort((a, b) => a.tier - b.tier || b.ts - a.ts)

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
