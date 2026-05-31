import { PageLayout, SharedLayout } from "./quartz/cfg"
import * as Component from "./quartz/components"

// components shared across all pages
export const sharedPageComponents: SharedLayout = {
  head: Component.Head(),
  header: [],
  afterBody: [],
  footer: Component.Footer({
    logo: "/static/gedankenwelten-logo.svg",
    links: {
      Impressum: "/Impressum",
      Graph: "/graph",
      GitHub: "https://github.com/gedankenwelten/gedankenwelten",
    },
  }),
}

// components for pages that display a single page (e.g. a single note)
export const defaultContentPageLayout: PageLayout = {
  beforeBody: [
    Component.ConditionalRender({
      component: Component.Breadcrumbs(),
      condition: (page) => page.fileData.slug !== "index",
    }),
    Component.ArticleTitle(),
    Component.ContentMeta(),
    Component.TagList(),
    // Graph NUR auf der dedizierten /graph-Ansicht rendern. Auf normalen Notes
    // startete der Graph sonst eine dauerhafte PIXI/WebGL-Render-Schleife und lud
    // den 7,4-MB-contentIndex eager — das ließ iOS-Safari den Tab abschießen.
    Component.ConditionalRender({
      component: Component.Graph({
        localGraph: { depth: -1, showTags: true },
        globalGraph: { showTags: true },
      }),
      condition: (page) => page.fileData.slug === "graph",
    }),
  ],
  left: [
    Component.PageTitle(),
    Component.MobileOnly(Component.Spacer()),
    Component.Flex({
      components: [
        {
          Component: Component.Search(),
          grow: true,
        },
        { Component: Component.Darkmode() },
        { Component: Component.ReaderMode() },
      ],
    }),
    Component.Explorer({
      sortFn: (a, b) => {
        if (a.isFolder && !b.isFolder) return -1
        if (!a.isFolder && b.isFolder) return 1
        const aDate = a.data?.date ? new Date(a.data.date).getTime() : 0
        const bDate = b.data?.date ? new Date(b.data.date).getTime() : 0
        if (aDate !== bDate) return bDate - aDate
        return a.displayName.localeCompare(b.displayName, undefined, { numeric: true, sensitivity: "base" })
      },
    }),
  ],
  right: [
    Component.DesktopOnly(Component.TableOfContents()),
    Component.Backlinks(),
  ],
}

// components for pages that display lists of pages  (e.g. tags or folders)
export const defaultListPageLayout: PageLayout = {
  beforeBody: [Component.Breadcrumbs(), Component.ArticleTitle(), Component.ContentMeta()],
  left: [
    Component.PageTitle(),
    Component.MobileOnly(Component.Spacer()),
    Component.Flex({
      components: [
        {
          Component: Component.Search(),
          grow: true,
        },
        { Component: Component.Darkmode() },
      ],
    }),
    Component.Explorer({
      sortFn: (a, b) => {
        if (a.isFolder && !b.isFolder) return -1
        if (!a.isFolder && b.isFolder) return 1
        const aDate = a.data?.date ? new Date(a.data.date).getTime() : 0
        const bDate = b.data?.date ? new Date(b.data.date).getTime() : 0
        if (aDate !== bDate) return bDate - aDate
        return a.displayName.localeCompare(b.displayName, undefined, { numeric: true, sensitivity: "base" })
      },
    }),
  ],
  right: [],
}
