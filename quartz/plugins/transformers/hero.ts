import { QuartzTransformerPlugin } from "../types"
import { Root, Element, ElementContent } from "hast"
import path from "path"

export interface BannerData {
  src: string
  alt: string
  width?: string | number
}

function textContent(node: ElementContent): string {
  if (node.type === "text") return node.value
  if (node.type === "element") return (node.children ?? []).map(textContent).join("")
  return ""
}

function normalize(s: string): string {
  return s.replace(/\s+/g, " ").trim()
}

/**
 * HeroLayout — räumt den Kopf jeder Note auf, damit Quartz' ArticleTitle die
 * einzige Überschrift bleibt und das Banner-Bild prominent zwischen Lesezeit
 * und Tags rendern kann (siehe Banner-Komponente + quartz.layout.ts).
 *
 * 1. Entfernt die führende `# H1`, wenn sie den Frontmatter-Titel dupliziert
 *    (Pipeline-Konvention: jede Note startet mit `# <title>`).
 * 2. Zieht das erste Banner-Bild aus dem Body und legt es als `fileData.banner`
 *    ab — die Banner-Komponente rendert es dann an der gewünschten Stelle.
 *
 * Läuft als htmlPlugin NACH CrawlLinks, damit die Bild-`src` bereits relativ
 * zur Seite aufgelöst ist.
 */
export const HeroLayout: QuartzTransformerPlugin = () => ({
  name: "HeroLayout",
  htmlPlugins() {
    return [
      () => (tree: Root, file) => {
        const title = (file.data.frontmatter?.title as string | undefined) ?? ""
        const children = tree.children

        // 1) führende, titel-gleiche H1 entfernen
        const firstElIdx = children.findIndex((c) => c.type === "element")
        if (firstElIdx !== -1) {
          const el = children[firstElIdx] as Element
          if (el.tagName === "h1") {
            const sameAsTitle = title && normalize(textContent(el)) === normalize(title)
            if (sameAsTitle) {
              children.splice(firstElIdx, 1)
            }
          }
        }

        // 2) erstes Banner-Bild hochziehen. Führende Überschriften überspringen —
        //    manche Notes haben eine Body-H1, die nicht dem Frontmatter-Titel
        //    entspricht (und daher oben nicht entfernt wurde); das Banner steht
        //    dann direkt dahinter.
        for (let i = 0; i < children.length; i++) {
          const node = children[i]
          if (node.type !== "element") continue
          const el = node as Element
          if (/^h[1-6]$/.test(el.tagName)) continue // führende Überschrift überspringen

          let img: Element | undefined
          if (el.tagName === "img") {
            img = el
          } else if (el.tagName === "p") {
            const inner = (el.children ?? []).filter(
              (c) => c.type === "element",
            ) as Element[]
            if (inner.length === 1 && inner[0].tagName === "img") {
              img = inner[0]
            }
          }

          if (img) {
            const props = img.properties ?? {}
            const src = props.src
            if (typeof src === "string" && src.length > 0) {
              // src ist nach CrawlLinks seiten-relativ (z.B. ../assets/x.png).
              // In einen absoluten Root-Pfad (/assets/x.png) umrechnen, damit das
              // Bild auch von der Startseite (MobileFeed) aus geladen werden kann.
              let abs = src
              if (!/^https?:\/\//.test(src) && !src.startsWith("/")) {
                const slug = (file.data.slug as string) ?? ""
                const dir = path.posix.dirname(slug)
                abs = path.posix.normalize(path.posix.join("/", dir, src))
              }
              file.data.banner = {
                src: abs,
                alt: typeof props.alt === "string" ? props.alt : "",
                width: props.width as string | number | undefined,
              }
              children.splice(i, 1)
            }
          }
          // nur das erste inhaltliche Element kommt als Banner in Frage
          break
        }
      },
    ]
  },
})

declare module "vfile" {
  interface DataMap {
    banner?: BannerData
  }
}
