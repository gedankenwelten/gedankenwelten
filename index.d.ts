declare module "*.scss" {
  const content: string
  export = content
}

// dom custom event
interface CustomEventMap {
  prenav: CustomEvent<{}>
  nav: CustomEvent<{ url: FullSlug }>
  themechange: CustomEvent<{ theme: "light" | "dark" }>
  readermodechange: CustomEvent<{ mode: "on" | "off" }>
}

// Schlanker Index — Titel, Links, Tags, Datum. Graph und Explorer brauchen nur das,
// und der Explorer sitzt auf jeder Seite in der Sidebar. Ohne Volltext.
type ContentIndex = Record<FullSlug, SlimContentDetails>
declare const fetchData: Promise<ContentIndex>

// Volltext-Index — nur für die Suche, eigene Datei, wird erst geholt, wenn jemand
// die Suche tatsächlich öffnet. Siehe renderPage.tsx und search.inline.ts.
type SearchIndexEntry = Pick<ContentDetails, "title" | "content" | "tags">
type SearchIndex = Record<FullSlug, SearchIndexEntry>
declare const fetchSearchData: Promise<SearchIndex>
