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

const INITIAL = 21
const BATCH = 21

function escapeHtml(s: string): string {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
}

let observer: IntersectionObserver | undefined

function setupDesktopFeed() {
  const feed = document.querySelector<HTMLElement>(".desktop-feed")
  if (!feed) return

  const dataEl = document.getElementById("desktop-feed-data")
  const grid = feed.querySelector<HTMLElement>(".df-grid")
  const sentinel = feed.querySelector<HTMLElement>(".df-sentinel")
  if (!dataEl || !grid || !sentinel) return

  let all: FeedEntry[] = []
  try {
    all = JSON.parse(dataEl.textContent || "[]")
  } catch {
    return
  }

  let activeTab = "alles"
  let shown = INITIAL

  const filtered = (): FeedEntry[] =>
    activeTab === "alles" ? all.filter((e) => e.inAlles) : all.filter((e) => e.cat === activeTab)

  function cardHtml(e: FeedEntry): string {
    const src = e.thumb || `/assets/rubrik-${e.cat}.png`
    return `
      <a class="df-card" href="${e.url}">
        <div class="df-thumb"><img src="${src}" loading="lazy" alt=""></div>
        <div class="df-title">${escapeHtml(e.title)}</div>
        <div class="df-meta">
          <span class="df-cat">
            <img class="df-cat-icon" src="/assets/rubrik-${e.cat}.png" alt="">
            ${escapeHtml(e.catLabel)}
          </span>
          <span class="df-date">${escapeHtml(e.date)}</span>
        </div>
      </a>`
  }

  function render() {
    const items = filtered()
    grid!.innerHTML = items.slice(0, shown).map(cardHtml).join("")
  }

  function loadMore() {
    if (filtered().length > shown) {
      shown += BATCH
      render()
    }
  }

  feed.querySelectorAll<HTMLButtonElement>(".df-chip").forEach((chip) => {
    chip.addEventListener("click", () => {
      const key = chip.dataset.tab
      if (!key || key === activeTab) return
      activeTab = key
      shown = INITIAL
      feed.querySelectorAll(".df-chip").forEach((c) => c.classList.remove("active"))
      chip.classList.add("active")
      render()
    })
  })

  observer?.disconnect()
  observer = new IntersectionObserver(
    (entries) => {
      if (entries.some((en) => en.isIntersecting)) loadMore()
    },
    { rootMargin: "600px" },
  )
  observer.observe(sentinel)

  render()
}

document.addEventListener("nav", () => {
  setupDesktopFeed()
})
