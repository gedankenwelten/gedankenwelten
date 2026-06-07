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
  const tagsEl = document.getElementById("desktop-feed-tags")
  const grid = feed.querySelector<HTMLElement>(".df-grid")
  const sentinel = feed.querySelector<HTMLElement>(".df-sentinel")
  const cloud = feed.querySelector<HTMLElement>(".df-cloud")
  if (!dataEl || !grid || !sentinel || !cloud) return

  let all: FeedEntry[] = []
  try {
    all = JSON.parse(dataEl.textContent || "[]")
  } catch {
    return
  }

  let cloudTags: CloudTag[] = []
  try {
    cloudTags = JSON.parse(tagsEl?.textContent || "[]")
  } catch {
    cloudTags = []
  }

  let activeTab = "alles"
  let shown = INITIAL
  let cloudRendered = false

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

  function renderCloud() {
    if (cloudRendered || cloudTags.length === 0) return
    const counts = cloudTags.map((t) => t.count)
    const lmin = Math.log(Math.min(...counts))
    const lmax = Math.log(Math.max(...counts))
    const span = lmax - lmin
    const MIN_REM = 0.85
    const MAX_REM = 2.45
    cloud!.innerHTML = cloudTags
      .map((t) => {
        const f = span > 0 ? (Math.log(t.count) - lmin) / span : 1
        const size = (MIN_REM + (MAX_REM - MIN_REM) * f).toFixed(2)
        const op = (0.62 + 0.38 * f).toFixed(2) // seltener = etwas blasser
        return `<a class="df-cloud-tag" href="${t.url}" style="font-size:${size}rem;color:${t.color};opacity:${op}" title="${t.count} Notes">${escapeHtml(t.tag)}</a>`
      })
      .join("")
    cloudRendered = true
  }

  function showCloud(on: boolean) {
    if (on) renderCloud()
    cloud!.hidden = !on
    grid!.hidden = on
    sentinel!.hidden = on
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
      feed.querySelectorAll(".df-chip").forEach((c) => c.classList.remove("active"))
      chip.classList.add("active")
      if (key === "tags") {
        showCloud(true)
        return
      }
      showCloud(false)
      shown = INITIAL
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
