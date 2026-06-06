import { normalizeRelativeURLs } from "../../util/path"
import { fetchCanonical } from "./util"

const domParser = new DOMParser()

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

const BATCH = 20

function escapeHtml(s: string): string {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
}

let observer: IntersectionObserver | undefined
let resizeBound = false

// Tabs kleben direkt unter dem (sticky) Header — Offset = Header-Höhe
function updateTabsOffset() {
  const sidebar = document.querySelector<HTMLElement>(".left.sidebar")
  const h = sidebar ? Math.round(sidebar.getBoundingClientRect().height) : 0
  document.documentElement.style.setProperty("--mf-tabs-top", h + "px")
}

function setupMobileFeed() {
  const feed = document.querySelector<HTMLElement>(".mobile-feed")
  if (!feed) return

  const dataEl = document.getElementById("mobile-feed-data")
  const list = feed.querySelector<HTMLElement>(".mf-list")
  const moreBtn = feed.querySelector<HTMLButtonElement>(".mf-more")
  const sentinel = feed.querySelector<HTMLElement>(".mf-sentinel")
  if (!dataEl || !list || !moreBtn || !sentinel) return

  let all: FeedEntry[] = []
  try {
    all = JSON.parse(dataEl.textContent || "[]")
  } catch {
    return
  }

  let activeTab = "alles"
  let shown = BATCH

  const filtered = (): FeedEntry[] =>
    activeTab === "alles" ? all.filter((e) => e.inAlles) : all.filter((e) => e.cat === activeTab)

  function cardHtml(e: FeedEntry): string {
    // Banner-Thumbnail, sonst das Rubrik-Bild als Fallback
    const src = e.thumb || `/assets/rubrik-${e.cat}.png`
    const thumb = `<div class="gn-thumb"><img src="${src}" loading="lazy" alt=""></div>`
    return `
      <div class="gn-body">
        <div class="gn-cat"><span class="gn-dot" style="background:${e.color}"></span>${escapeHtml(
          e.catLabel,
        )}</div>
        <div class="gn-title">${escapeHtml(e.title)}</div>
        <div class="gn-date">${escapeHtml(e.date)}</div>
      </div>
      ${thumb}`
  }

  function render() {
    const items = filtered()
    const slice = items.slice(0, shown)
    list!.innerHTML = slice
      .map(
        (e) =>
          `<a class="gn-card" href="${e.url}" data-desc="${escapeHtml(e.desc)}" data-title="${escapeHtml(
            e.title,
          )}" data-cat="${escapeHtml(e.catLabel)}" data-color="${e.color}">${cardHtml(e)}</a>`,
      )
      .join("")
    const hasMore = items.length > shown
    moreBtn!.hidden = !hasMore
  }

  function loadMore() {
    if (filtered().length > shown) {
      shown += BATCH
      render()
    }
  }

  // Tab-Wechsel
  feed.querySelectorAll<HTMLButtonElement>(".mf-tab").forEach((tab) => {
    tab.addEventListener("click", () => {
      const key = tab.dataset.tab
      if (!key || key === activeTab) return
      activeTab = key
      shown = BATCH
      feed.querySelectorAll(".mf-tab").forEach((t) => t.classList.remove("active"))
      tab.classList.add("active")
      feed.scrollIntoView({ block: "start" })
      render()
    })
  })

  moreBtn.addEventListener("click", loadMore)

  // Auto-Nachladen beim Runterscrollen
  observer?.disconnect()
  observer = new IntersectionObserver(
    (entries) => {
      if (entries.some((en) => en.isIntersecting)) loadMore()
    },
    { rootMargin: "400px" },
  )
  observer.observe(sentinel)

  updateTabsOffset()
  setTimeout(updateTabsOffset, 200) // nach Layout-/Font-Settle nachmessen
  if (!resizeBound) {
    window.addEventListener("resize", updateTabsOffset)
    resizeBound = true
  }

  setupSheets(feed, list)
  render()
}

// --- Bottom-Sheets (Intro-Footer + Lang-Druck-Vorschau) ---
function setupSheets(feed: HTMLElement, list: HTMLElement) {
  const introSheet = feed.querySelector<HTMLElement>("#mf-intro-sheet")
  const descSheet = feed.querySelector<HTMLElement>("#mf-desc-sheet")
  const noteSheet = feed.querySelector<HTMLElement>("#mf-note-sheet")
  const introBar = feed.querySelector<HTMLButtonElement>(".mf-introbar")

  const openSheet = (sheet: HTMLElement | null) => {
    if (!sheet) return
    sheet.hidden = false
    document.body.classList.add("mf-sheet-open")
    requestAnimationFrame(() => sheet.classList.add("open"))
  }
  const closeSheet = (sheet: HTMLElement | null) => {
    if (!sheet) return
    sheet.classList.remove("open")
    document.body.classList.remove("mf-sheet-open")
    setTimeout(() => {
      sheet.hidden = true
    }, 280)
  }

  introBar?.addEventListener("click", () => openSheet(introSheet))

  for (const sheet of [introSheet, descSheet, noteSheet]) {
    sheet?.querySelectorAll<HTMLElement>("[data-close]").forEach((el) => {
      el.addEventListener("click", () => closeSheet(sheet))
    })
  }
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      closeSheet(introSheet)
      closeSheet(descSheet)
      closeSheet(noteSheet)
    }
  })

  // Note in einem Sheet öffnen (statt wegzunavigieren) — Inhalt via Fetch laden
  async function openNote(url: string, _title: string) {
    if (!noteSheet) return
    const content = noteSheet.querySelector<HTMLElement>(".mf-note-content")!
    const full = noteSheet.querySelector<HTMLAnchorElement>(".mf-note-full")
    if (full) full.href = url
    content.innerHTML = `<p class="mf-note-loading">Lädt …</p>`
    openSheet(noteSheet)
    content.scrollTop = 0
    try {
      const target = new URL(url, location.href)
      target.hash = ""
      target.search = ""
      const res = await fetchCanonical(target)
      const html = domParser.parseFromString(await res.text(), "text/html")
      normalizeRelativeURLs(html, target)
      const elts = [...html.getElementsByClassName("popover-hint")]
      if (elts.length === 0) {
        content.innerHTML = `<p>Konnte die Note nicht laden.</p>`
        return
      }
      content.replaceChildren(...elts)
      content.querySelectorAll(".breadcrumb-container").forEach((e) => e.remove())
      content.scrollTop = 0
    } catch {
      content.innerHTML = `<p>Konnte die Note nicht laden.</p>`
    }
  }

  // Beschreibungs-Sheet mit Card-Daten füllen
  function openDesc(card: HTMLElement) {
    if (!descSheet) return
    const cat = card.dataset.cat || ""
    const color = card.dataset.color || "var(--secondary)"
    const title = card.dataset.title || ""
    const desc = card.dataset.desc || "Keine Beschreibung vorhanden."
    const url = card.getAttribute("href") || "#"
    const catEl = descSheet.querySelector<HTMLElement>(".mf-desc-cat")
    if (catEl) catEl.innerHTML = `<span class="gn-dot" style="background:${color}"></span>${cat}`
    descSheet.querySelector<HTMLElement>(".mf-desc-title")!.textContent = title
    descSheet.querySelector<HTMLElement>(".mf-desc-text")!.textContent = desc
    descSheet.querySelector<HTMLAnchorElement>(".mf-desc-open")!.href = url
    openSheet(descSheet)
  }

  // Lang-Druck auf eine Card (Touch) — öffnet die Vorschau statt zu navigieren
  let lpTimer: number | undefined
  let lpFired = false
  let sx = 0
  let sy = 0

  list.addEventListener(
    "touchstart",
    (e) => {
      const card = (e.target as HTMLElement).closest<HTMLElement>(".gn-card")
      if (!card) return
      lpFired = false
      const t = e.touches[0]
      sx = t.clientX
      sy = t.clientY
      lpTimer = window.setTimeout(() => {
        lpFired = true
        if (navigator.vibrate) navigator.vibrate(8)
        openDesc(card)
      }, 450)
    },
    { passive: true },
  )
  list.addEventListener(
    "touchmove",
    (e) => {
      if (lpTimer === undefined) return
      const t = e.touches[0]
      if (Math.abs(t.clientX - sx) > 10 || Math.abs(t.clientY - sy) > 10) {
        clearTimeout(lpTimer)
        lpTimer = undefined
      }
    },
    { passive: true },
  )
  list.addEventListener("touchend", () => {
    if (lpTimer !== undefined) {
      clearTimeout(lpTimer)
      lpTimer = undefined
    }
  })
  // Card-Tap fängt den Klick in der Capture-Phase ab (vor dem SPA-Router):
  // statt wegzunavigieren öffnet sich das Note-Sheet. Hat der Lang-Druck
  // bereits das Beschreibungs-Sheet geöffnet, wird der Klick nur geschluckt.
  list.addEventListener(
    "click",
    (e) => {
      const card = (e.target as HTMLElement).closest<HTMLElement>(".gn-card")
      if (!card) return
      e.preventDefault()
      e.stopPropagation()
      if (lpFired) {
        lpFired = false
        return
      }
      openNote(card.getAttribute("href") || "#", card.dataset.title || "")
    },
    true,
  )
  // iOS-Kontextmenü beim Halten unterdrücken
  list.addEventListener("contextmenu", (e) => {
    if ((e.target as HTMLElement).closest(".gn-card")) e.preventDefault()
  })
}

document.addEventListener("nav", () => {
  setupMobileFeed()
})
