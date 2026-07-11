// Teilen/Kopieren für die /Feeds-Seite. Teilen nutzt das native Share-Sheet
// (navigator.share) — wo es das nicht gibt (Desktop-Firefox etc.), wird der
// Teilen-Button ausgeblendet und Kopieren bleibt der Weg.
function setupFeedShare() {
  const root = document.querySelector(".feed-share")
  if (!root) return

  const canShare = typeof navigator.share === "function"
  for (const btn of root.querySelectorAll<HTMLButtonElement>(".feed-share-btn")) {
    if (!canShare) {
      btn.hidden = true
      continue
    }
    const onShare = async () => {
      const url = btn.dataset.url
      if (!url) return
      try {
        await navigator.share({
          title: `Gedankenwelten — ${btn.dataset.label ?? "RSS-Feed"}`,
          url,
        })
      } catch {
        // Abbruch des Share-Sheets ist kein Fehler
      }
    }
    btn.addEventListener("click", onShare)
    window.addCleanup?.(() => btn.removeEventListener("click", onShare))
  }

  for (const btn of root.querySelectorAll<HTMLButtonElement>(".feed-copy-btn")) {
    const onCopy = async () => {
      const url = btn.dataset.url
      if (!url) return
      try {
        await navigator.clipboard.writeText(url)
      } catch {
        // Fallback für alte Browser
        const ta = document.createElement("textarea")
        ta.value = url
        document.body.appendChild(ta)
        ta.select()
        document.execCommand("copy")
        ta.remove()
      }
      btn.classList.add("copied")
      setTimeout(() => btn.classList.remove("copied"), 1600)
    }
    btn.addEventListener("click", onCopy)
    window.addCleanup?.(() => btn.removeEventListener("click", onCopy))
  }
}

document.addEventListener("nav", setupFeedShare)
