import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { classNames } from "../util/lang"
// @ts-ignore
import script from "./scripts/feedShare.inline"
import style from "./styles/feedShare.scss"

// Interaktive Feed-Liste für die /Feeds-Seite: Jeder Feed bekommt einen
// Teilen-Button (natives Share-Sheet, mobil) und einen Kopieren-Button —
// statt nackter XML-Links, die im Browser nur Rohtext zeigen.
interface FeedDef {
  folder: string
  label: string
  desc: string
  color: string
  icon?: string
}

const FEEDS: FeedDef[] = [
  { folder: "Zeitgeist", label: "Zeitgeist", desc: "Interviews & Vorträge zum Geist der Zeit", color: "#a78bfa", icon: "zeitgeist" },
  { folder: "Denker", label: "Denker", desc: "Tiefenanalysen einzelner Denkerinnen und Denker", color: "#6366f1", icon: "denker" },
  { folder: "DenkerVita", label: "DenkerVita", desc: "Biografie-Profile", color: "#d6a06a", icon: "denkervita" },
  { folder: "Geistesblitz", label: "Geistesblitz", desc: "Wissen & Schöpferkraft", color: "#facc15", icon: "geistesblitz" },
  { folder: "Kultur", label: "Kultur", desc: "Land und Leute von innen", color: "#0ea5a4", icon: "kultur" },
  { folder: "Gedanken", label: "Gedanken", desc: "persönliche Reflexionen", color: "#f59e0b", icon: "gedanken" },
  { folder: "Panorama", label: "Panorama", desc: "thematische Synthesen", color: "#2dd4bf", icon: "panorama" },
  { folder: "Spuren", label: "Spuren", desc: "lebende investigative Thesen", color: "#fb7185", icon: "spuren" },
  { folder: "GoodNews", label: "GoodNews", desc: "das Heilsame", color: "#22c55e", icon: "goodnews" },
  { folder: "Vipassana", label: "Vipassana", desc: "Meditation & Praxis", color: "#8b5cf6" },
]

const BASE = "https://gedankenwelten.org"

const ShareIcon = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    width="15"
    height="15"
    fill="none"
    stroke="currentColor"
    stroke-width="1.7"
    stroke-linecap="round"
    stroke-linejoin="round"
    aria-hidden="true"
  >
    <path d="M12 3v12" />
    <path d="M8 7l4-4 4 4" />
    <path d="M5 12v7a1.5 1.5 0 0 0 1.5 1.5h11A1.5 1.5 0 0 0 19 19v-7" />
  </svg>
)

const CopyIcon = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    width="15"
    height="15"
    fill="none"
    stroke="currentColor"
    stroke-width="1.7"
    stroke-linecap="round"
    stroke-linejoin="round"
    aria-hidden="true"
  >
    <rect x="9" y="9" width="11" height="11" rx="2" />
    <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" />
  </svg>
)

const FeedRow = ({ url, label, desc, color, icon }: { url: string; label: string; desc: string; color?: string; icon?: string }) => (
  <li class="feed-share-row" style={color ? `--rubrik-color: ${color}` : undefined}>
    {icon ? (
      <img class="feed-share-icon" src={`/assets/rubrik-${icon}.png`} alt="" loading="lazy" />
    ) : (
      <span class="feed-share-dot" />
    )}
    <div class="feed-share-text">
      <span class="feed-share-label">{label}</span>
      <span class="feed-share-desc">{desc}</span>
    </div>
    <div class="feed-share-actions">
      <button class="feed-share-btn" type="button" data-url={url} data-label={label} title="Teilen">
        <ShareIcon />
      </button>
      <button class="feed-copy-btn" type="button" data-url={url} title="Feed-URL kopieren">
        <CopyIcon />
        <span class="feed-copy-tip" aria-hidden="true">
          kopiert ✓
        </span>
      </button>
    </div>
  </li>
)

const FeedShare: QuartzComponent = ({ displayClass }: QuartzComponentProps) => {
  return (
    <div class={classNames(displayClass, "feed-share")}>
      <p>
        Die Gedankenwelten lassen sich abonnieren — ganz klassisch per RSS. Kein Algorithmus
        entscheidet, was du siehst; dein Feed-Reader (<a href="https://netnewswire.com/">NetNewsWire</a>,{" "}
        <a href="https://feedly.com/">Feedly</a>, <a href="https://www.inoreader.com/">Inoreader</a> …)
        holt einfach ab, was neu gedacht wurde.
      </p>
      <p class="feed-share-hint">
        <em>Teilen</em> öffnet das Share-Sheet deines Geräts — darüber landet der Feed direkt in
        deiner Reader-App. <em>Kopieren</em> legt die Feed-URL in die Zwischenablage.
      </p>
      <h2>Haupt-Feed</h2>
      <ul class="feed-share-list feed-share-main">
        <FeedRow
          url={`${BASE}/index.xml`}
          label="Alle Notes"
          desc="der Haupt-Feed, quer durch alle Rubriken"
          color="#f59e0b"
        />
      </ul>
      <h2>Rubrik-Feeds</h2>
      <p class="feed-share-hint">Wer nur einem Teil folgen möchte:</p>
      <ul class="feed-share-list">
        {FEEDS.map((f) => (
          <FeedRow url={`${BASE}/${f.folder}/index.xml`} label={f.label} desc={f.desc} color={f.color} icon={f.icon} />
        ))}
      </ul>
      <p class="feed-share-hint">
        Jeder Feed enthält die jeweils 30 zuletzt bearbeiteten Notes, sortiert nach dem Datum der
        letzten <em>inhaltlichen</em> Änderung — derselben Logik, die auch das Journal auf der
        Startseite speist.
      </p>
    </div>
  )
}

FeedShare.afterDOMLoaded = script
FeedShare.css = style

export default (() => FeedShare) satisfies QuartzComponentConstructor
