import { getFullSlug, resolveRelative, FullSlug } from "../../util/path"

// Mobil verhält sich der Würfel exakt wie ein Tap auf eine Feed-Card:
// dasselbe Note-Sheet (window.gwOpenNote, vom MobileFeed bereitgestellt),
// nur mit einem zufällig gewürfelten Link. Auf Desktop einfach die Note öffnen.
// Im offenen Shuffle-Sheet sitzt mittig ein Würfel zum Weitershuffeln.
const isMobile = () => window.matchMedia("(max-width: 800px)").matches

// Zuletzt gewürfelte Note — beim Weitershuffeln nicht direkt wiederholen.
let lastShuffled: string | null = null

function pickRandomSlug(): FullSlug | null {
  const dataEl = document.getElementById("random-note-data")
  if (!dataEl) return null
  let slugs: string[] = []
  try {
    slugs = JSON.parse(dataEl.textContent || "[]")
  } catch {
    return null
  }
  if (slugs.length === 0) return null
  // Aktuelle Seite und die zuletzt gewürfelte Note möglichst nicht erneut ziehen.
  const here = getFullSlug(window)
  let pool = slugs.filter((s) => s !== here && s !== lastShuffled)
  if (pool.length === 0) pool = slugs
  const choice = pool[Math.floor(Math.random() * pool.length)]
  lastShuffled = choice
  return choice as FullSlug
}

type OpenNote = (url: string, title: string, opts?: { shuffle?: boolean }) => void

function roll() {
  const slug = pickRandomSlug()
  if (!slug) return
  const rel = resolveRelative(getFullSlug(window), slug)
  // Sheet-Pfad nur wenn das Sheet im AKTUELLEN DOM existiert (= Startseite).
  // Sonst hält window.gwOpenNote nach SPA-Navigation eine veraltete Closure auf
  // ein längst entferntes Sheet-Element — dann passiert nichts. Auf Note-Seiten
  // gibt es kein Sheet, also normal zur Note navigieren.
  const sheetLive = document.getElementById("mf-note-sheet")
  const openNote = (window as any).gwOpenNote as OpenNote | undefined
  if (isMobile() && sheetLive && typeof openNote === "function") {
    openNote(rel, "", { shuffle: true })
  } else {
    window.spaNavigate(new URL(rel, window.location.toString()))
  }
}

function setupRandomNote() {
  const btn = document.querySelector<HTMLButtonElement>(".randomnote")
  if (btn) {
    btn.removeEventListener("click", roll)
    btn.addEventListener("click", roll)
  }
  // Weiter-Würfel im offenen Sheet (vom MobileFeed gerendert)
  const shuffleBtn = document.querySelector<HTMLButtonElement>(".mf-note-shuffle")
  if (shuffleBtn) {
    shuffleBtn.removeEventListener("click", roll)
    shuffleBtn.addEventListener("click", roll)
  }
}

document.addEventListener("nav", () => {
  setupRandomNote()
})
