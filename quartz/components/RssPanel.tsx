import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { classNames } from "../util/lang"
import style from "./styles/rssPanel.scss"

// Feed-Panel für die rechte Startseiten-Spalte (ersetzt dort das TOC, das auf
// der Startseite nur die Journal-Überschriften zeigen würde). Statische Liste —
// die Feeds selbst erzeugt der ContentIndex-Emitter (feedFolders).
interface FeedDef {
  folder: string
  label: string
  color: string
  icon?: string // /assets/rubrik-<key>.png — Vipassana hat keins → Farbpunkt
}

const FEEDS: FeedDef[] = [
  { folder: "Zeitgeist", label: "Zeitgeist", color: "#a78bfa", icon: "zeitgeist" },
  { folder: "Denker", label: "Denker", color: "#6366f1", icon: "denker" },
  { folder: "Panorama", label: "Panorama", color: "#2dd4bf", icon: "panorama" },
  { folder: "Gedanken", label: "Gedanken", color: "#f59e0b", icon: "gedanken" },
  { folder: "Geistesblitz", label: "Geistesblitz", color: "#facc15", icon: "geistesblitz" },
  { folder: "Kultur", label: "Kultur", color: "#0ea5a4", icon: "kultur" },
  { folder: "GoodNews", label: "GoodNews", color: "#22c55e", icon: "goodnews" },
  { folder: "Spuren", label: "Spuren", color: "#fb7185", icon: "spuren" },
  { folder: "DenkerVita", label: "DenkerVita", color: "#d6a06a", icon: "denkervita" },
  { folder: "Vipassana", label: "Vipassana", color: "#8b5cf6" },
]

const RssIcon = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    width="14"
    height="14"
    fill="currentColor"
    aria-hidden="true"
  >
    <path d="M6.18 17.82a2.18 2.18 0 1 1-4.36 0 2.18 2.18 0 0 1 4.36 0zM2 8.73v3.27c5.52 0 10 4.48 10 10h3.27C15.27 14.7 9.3 8.73 2 8.73zM2 2v3.27c9.24 0 16.73 7.49 16.73 16.73H22C22 10.95 13.05 2 2 2z" />
  </svg>
)

const RssPanel: QuartzComponent = ({ displayClass }: QuartzComponentProps) => {
  return (
    <div class={classNames(displayClass, "rss-panel")}>
      <h3 class="rss-panel-title">
        <RssIcon /> Abonnieren
      </h3>
      <p class="rss-panel-desc">
        Neue Notes per RSS — ohne Algorithmus, direkt in deinen Feed-Reader.
      </p>
      <a class="rss-panel-main" href="/index.xml">
        <RssIcon /> Alle Notes
      </a>
      <ul class="rss-panel-list">
        {FEEDS.map((f) => (
          <li>
            <a href={`/${f.folder}/index.xml`} style={`--rubrik-color: ${f.color}`}>
              {f.icon ? (
                <img class="rss-panel-icon" src={`/assets/rubrik-${f.icon}.png`} alt="" />
              ) : (
                <span class="rss-panel-dot" />
              )}
              {f.label}
            </a>
          </li>
        ))}
      </ul>
      <a class="rss-panel-more" href="/Feeds">
        Was ist RSS? →
      </a>
    </div>
  )
}

RssPanel.css = style

export default (() => RssPanel) satisfies QuartzComponentConstructor
