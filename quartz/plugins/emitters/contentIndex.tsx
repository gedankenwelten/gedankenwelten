import { Root } from "hast"
import { GlobalConfiguration } from "../../cfg"
import { getDate } from "../../components/Date"
import { escapeHTML } from "../../util/escape"
import { FilePath, FullSlug, SimpleSlug, joinSegments, simplifySlug } from "../../util/path"
import { QuartzEmitterPlugin } from "../types"
import { toHtml } from "hast-util-to-html"
import { write } from "./helpers"
import { i18n } from "../../i18n"

export type ContentIndexMap = Map<FullSlug, ContentDetails>

// Was im ausgelieferten schlanken Index landet: alles außer dem Volltext. Graph und
// Explorer arbeiten damit; der Volltext geht in contentIndex.search.json und wird
// erst geholt, wenn die Suche geöffnet wird.
export type SlimContentDetails = Omit<ContentDetails, "content" | "richContent" | "description">

export type ContentDetails = {
  slug: FullSlug
  filePath: FilePath
  title: string
  links: SimpleSlug[]
  tags: string[]
  content: string
  richContent?: string
  date?: Date
  description?: string
}

interface Options {
  enableSiteMap: boolean
  enableRSS: boolean
  rssLimit?: number
  rssFullHtml: boolean
  rssSlug: string
  includeEmptyFiles: boolean
  // Rubrik-Ordner, deren Notes den Haupt-Feed bilden UND je einen eigenen
  // Feed unter <Ordner>/index.xml bekommen. Meta-Seiten (Startseite, Indizes,
  // Impressum, Quellen & Links …) bleiben so automatisch draußen.
  feedFolders?: string[]
}

const defaultOptions: Options = {
  enableSiteMap: true,
  enableRSS: true,
  rssLimit: 10,
  rssFullHtml: false,
  rssSlug: "index",
  includeEmptyFiles: true,
}

function generateSiteMap(cfg: GlobalConfiguration, idx: ContentIndexMap): string {
  const base = cfg.baseUrl ?? ""
  const createURLEntry = (slug: SimpleSlug, content: ContentDetails): string => `<url>
    <loc>https://${joinSegments(base, encodeURI(slug))}</loc>
    ${content.date && `<lastmod>${content.date.toISOString()}</lastmod>`}
  </url>`
  const urls = Array.from(idx)
    .map(([slug, content]) => createURLEntry(simplifySlug(slug), content))
    .join("")
  return `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">${urls}</urlset>`
}

function generateRSSFeed(
  cfg: GlobalConfiguration,
  idx: ContentIndexMap,
  limit?: number,
  channel?: { title: string; link: string; description: string },
): string {
  const base = cfg.baseUrl ?? ""

  const createURLEntry = (slug: SimpleSlug, content: ContentDetails): string => `<item>
    <title>${escapeHTML(content.title)}</title>
    <link>https://${joinSegments(base, encodeURI(slug))}</link>
    <guid>https://${joinSegments(base, encodeURI(slug))}</guid>
    <description><![CDATA[ ${content.richContent ?? content.description} ]]></description>
    <pubDate>${content.date?.toUTCString()}</pubDate>
  </item>`

  const items = Array.from(idx)
    .sort(([_, f1], [__, f2]) => {
      if (f1.date && f2.date) {
        return f2.date.getTime() - f1.date.getTime()
      } else if (f1.date && !f2.date) {
        return -1
      } else if (!f1.date && f2.date) {
        return 1
      }

      return f1.title.localeCompare(f2.title)
    })
    .map(([slug, content]) => createURLEntry(simplifySlug(slug), content))
    .slice(0, limit ?? idx.size)
    .join("")

  const title = channel?.title ?? cfg.pageTitle
  const link = channel?.link ?? `https://${base}`
  const description =
    channel?.description ??
    `${!!limit ? i18n(cfg.locale).pages.rss.lastFewNotes({ count: limit }) : i18n(cfg.locale).pages.rss.recentNotes} on ${cfg.pageTitle}`

  return `<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
    <channel>
      <title>${escapeHTML(title)}</title>
      <link>${link}</link>
      <description>${escapeHTML(description)}</description>
      <language>${cfg.locale}</language>
      <generator>Quartz -- quartz.jzhao.xyz</generator>
      ${items}
    </channel>
  </rss>`
}

export const ContentIndex: QuartzEmitterPlugin<Partial<Options>> = (opts) => {
  opts = { ...defaultOptions, ...opts }
  return {
    name: "ContentIndex",
    async *emit(ctx, content) {
      const cfg = ctx.cfg.configuration
      const linkIndex: ContentIndexMap = new Map()
      for (const [tree, file] of content) {
        const slug = file.data.slug!
        const date = getDate(ctx.cfg.configuration, file.data) ?? new Date()
        if (opts?.includeEmptyFiles || (file.data.text && file.data.text !== "")) {
          linkIndex.set(slug, {
            slug,
            filePath: file.data.relativePath!,
            title: file.data.frontmatter?.title!,
            links: file.data.links ?? [],
            tags: file.data.frontmatter?.tags ?? [],
            content: file.data.text ?? "",
            richContent: opts?.rssFullHtml
              ? escapeHTML(toHtml(tree as Root, { allowDangerousHtml: true }))
              : undefined,
            date: date,
            description: file.data.description ?? "",
          })
        }
      }

      if (opts?.enableSiteMap) {
        yield write({
          ctx,
          content: generateSiteMap(cfg, linkIndex),
          slug: "sitemap" as FullSlug,
          ext: ".xml",
        })
      }

      if (opts?.enableRSS) {
        // Ohne feedFolders: Original-Verhalten (alle Seiten). Mit feedFolders:
        // nur echte Rubrik-Notes — keine Startseite, keine Indizes, kein Impressum.
        const feedFolders = opts?.feedFolders
        const isNote = (slug: FullSlug) =>
          !feedFolders ||
          feedFolders.some((f) => slug.startsWith(`${f}/`) && !slug.endsWith("/index"))

        const mainIndex: ContentIndexMap = feedFolders
          ? new Map(Array.from(linkIndex).filter(([slug]) => isNote(slug)))
          : linkIndex

        yield write({
          ctx,
          content: generateRSSFeed(cfg, mainIndex, opts.rssLimit),
          slug: (opts?.rssSlug ?? "index") as FullSlug,
          ext: ".xml",
        })

        // Je Rubrik ein eigener Feed unter <Rubrik>/index.xml
        for (const folder of feedFolders ?? []) {
          const folderIndex: ContentIndexMap = new Map(
            Array.from(linkIndex).filter(
              ([slug]) => slug.startsWith(`${folder}/`) && !slug.endsWith("/index"),
            ),
          )
          if (folderIndex.size === 0) continue
          yield write({
            ctx,
            content: generateRSSFeed(cfg, folderIndex, opts.rssLimit, {
              title: `${cfg.pageTitle} — ${folder}`,
              link: `https://${cfg.baseUrl}/${folder}`,
              description: `Neue Notes aus der Rubrik ${folder} auf ${cfg.pageTitle}`,
            }),
            slug: joinSegments(folder, "index") as FullSlug,
            ext: ".xml",
          })
        }
      }

      // Zwei Indizes statt einem.
      //
      // Der Volltext ist das Schwergewicht — bei 750 Notes rund 12 MB — und wird
      // ausschließlich von der Suche gebraucht. Graph und Explorer brauchen nur
      // Titel, Links, Tags und Datum. Solange beides in einer Datei lag, zogen der
      // Explorer (Sidebar, also jede Seite) und die Suche (nav-Handler) den ganzen
      // Volltext bei jedem Seitenaufruf; das lazy thenable in renderPage.tsx lief
      // damit ins Leere. Getrennt gilt: schlanker Index sofort, Volltext erst wenn
      // jemand die Suche öffnet.
      //
      // Beide Dateien heißen absichtlich `contentIndex*` — so deckt ein einziges
      // `Disallow: /static/contentIndex` in der robots.txt beide ab.
      const slimIndex: Record<string, any> = {}
      const searchIndex: Record<string, any> = {}

      for (const [slug, details] of linkIndex) {
        // description und richContent trägt nur der RSS-Feed (oben schon emittiert),
        // content nur die Suche — alle drei raus aus dem schlanken Index.
        const { content, richContent, description, date, ...rest } = details
        const slim: Record<string, any> = { ...rest }
        if (date) {
          // Als Timestamp, nicht als ISO-String: der Explorer sortiert danach.
          slim.date = (date as Date).getTime()
        }
        slimIndex[slug] = slim
        searchIndex[slug] = { title: details.title, content, tags: details.tags }
      }

      yield write({
        ctx,
        content: JSON.stringify(slimIndex),
        slug: joinSegments("static", "contentIndex") as FullSlug,
        ext: ".json",
      })

      yield write({
        ctx,
        content: JSON.stringify(searchIndex),
        slug: joinSegments("static", "contentIndex.search") as FullSlug,
        ext: ".json",
      })
    },
    externalResources: (ctx) => {
      if (opts?.enableRSS) {
        return {
          additionalHead: [
            <link
              rel="alternate"
              type="application/rss+xml"
              title="RSS Feed"
              href={`https://${ctx.cfg.configuration.baseUrl}/index.xml`}
            />,
          ],
        }
      }
    },
  }
}
