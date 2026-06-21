import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { classNames } from "../util/lang"
// @ts-ignore
import script from "./scripts/randomNote.inline"
import styles from "./styles/randomNote.scss"

// Rubriken, aus denen gewürfelt wird (oberster Ordner in content/).
// DenkerVita bewusst NICHT dabei — das sind zeitlose Profile, keine Themen-Notes;
// die schaut man sich separat an. Index-/Landing-Seiten fliegen ohnehin raus.
const RANDOM_CATEGORIES = new Set([
  "Zeitgeist",
  "Denker",
  "Panorama",
  "Gedanken",
  "Geistesblitz",
  "Kultur",
  "GoodNews",
])

const RandomNote: QuartzComponent = ({ allFiles, displayClass }: QuartzComponentProps) => {
  // Liste aller würfelbaren Notes als FullSlugs — identisch auf jeder Seite.
  // Zur Laufzeit relativ zur aktuellen Seite aufgelöst (wie im Graph).
  const slugs: string[] = []
  for (const page of allFiles) {
    const slug = page.slug
    if (!slug || !slug.includes("/")) continue
    const parts = slug.split("/")
    const last = parts[parts.length - 1].toLowerCase()
    if (last === "index" || last === "readme") continue
    if (!RANDOM_CATEGORIES.has(parts[0])) continue
    if (!page.frontmatter?.title) continue
    slugs.push(slug)
  }

  const label = "Zufalls-Note"

  return (
    <>
      <button class={classNames(displayClass, "randomnote")} aria-label={label} title={label}>
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="diceIcon"
          width="20px"
          height="20px"
          viewBox="0 0 24 24"
          aria-label={label}
        >
          <title>{label}</title>
          <rect
            x="3"
            y="3"
            width="18"
            height="18"
            rx="3.5"
            ry="3.5"
            fill="none"
            stroke="currentColor"
            stroke-width="1.7"
          />
          <circle cx="8" cy="8" r="1.5" />
          <circle cx="16" cy="8" r="1.5" />
          <circle cx="12" cy="12" r="1.5" />
          <circle cx="8" cy="16" r="1.5" />
          <circle cx="16" cy="16" r="1.5" />
        </svg>
      </button>
      <script
        type="application/json"
        id="random-note-data"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(slugs) }}
      />
    </>
  )
}

RandomNote.afterDOMLoaded = script
RandomNote.css = styles

export default (() => RandomNote) satisfies QuartzComponentConstructor
