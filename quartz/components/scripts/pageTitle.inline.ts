// Wählt täglich eine Wortmarke aus dem Pool (Klee, Sumi-e, …).
// Deterministisch pro Kalendertag → stabil über Reloads, wechselt um Mitternacht.
// Tag-des-Monats modulo Pool-Größe; Tag 31 fällt auf Slot 0 zurück ("gerundet").
// Generisch: der Pool kommt aus data-wm-styles, das Theme (dark/light) macht CSS.
function pickWordmark() {
  const title = document.querySelector<HTMLElement>(".page-title")
  if (!title) return
  const styles = (title.getAttribute("data-wm-styles") || "").split(",").filter(Boolean)
  if (styles.length === 0) return
  const idx = (new Date().getDate() - 1) % styles.length
  const active = styles[idx]
  title.querySelectorAll(".page-title-mark").forEach((img) => img.classList.remove("wm-active"))
  title.querySelectorAll(".wm-" + active).forEach((img) => img.classList.add("wm-active"))
}

document.addEventListener("nav", pickWordmark)
