import { QuartzConfig } from "./quartz/cfg"
import * as Plugin from "./quartz/plugins"

/**
 * Quartz 4 Configuration
 *
 * See https://quartz.jzhao.xyz/configuration for more information.
 */
const config: QuartzConfig = {
  configuration: {
    pageTitle: "Gedankenwelten",
    pageTitleSuffix: " · Gedankenwelten",
    enableSPA: true,
    enablePopovers: true,
    analytics: {
      provider: "umami",
      host: "https://analytics.gedankenwelten.org",
      websiteId: "a4a71367-eeb4-42a6-b570-ef915b848718",
    },
    locale: "de-DE",
    baseUrl: "gedankenwelten.org",
    ignorePatterns: ["private", "templates", ".obsidian", "Transkripte"],
    defaultDateType: "modified",
    theme: {
      fontOrigin: "googleFonts",
      cdnCaching: true,
      typography: {
        header: "Inter",
        body: "Inter",
        code: "JetBrains Mono",
      },
      colors: {
        lightMode: {
          light: "#fafafa",
          lightgray: "#e4e4e7",
          gray: "#a1a1aa",
          darkgray: "#3f3f46",
          dark: "#18181b",
          secondary: "#6d28d9",
          tertiary: "#8b5cf6",
          highlight: "rgba(109, 40, 217, 0.08)",
          textHighlight: "#c4b5fd88",
        },
        darkMode: {
          light: "#09090b",
          lightgray: "#27272a",
          gray: "#52525b",
          darkgray: "#d4d4d8",
          dark: "#fafafa",
          secondary: "#a78bfa",
          tertiary: "#8b5cf6",
          highlight: "rgba(167, 139, 250, 0.12)",
          textHighlight: "#c4b5fd44",
        },
      },
    },
  },
  plugins: {
    transformers: [
      Plugin.FrontMatter(),
      Plugin.CreatedModifiedDate({
        priority: ["frontmatter", "git", "filesystem"],
      }),
      Plugin.SyntaxHighlighting({
        theme: {
          light: "github-light",
          dark: "github-dark",
        },
        keepBackground: false,
      }),
      Plugin.ObsidianFlavoredMarkdown({ enableInHtmlEmbed: false }),
      Plugin.GitHubFlavoredMarkdown(),
      Plugin.TableOfContents(),
      Plugin.CrawlLinks({ markdownLinkResolution: "shortest", openLinksInNewTab: true }),
      Plugin.HeroLayout(),
      Plugin.Description(),
      Plugin.Latex({ renderEngine: "katex" }),
    ],
    filters: [Plugin.RemoveDrafts()],
    emitters: [
      Plugin.AliasRedirects(),
      Plugin.ComponentResources(),
      Plugin.ContentPage(),
      Plugin.FolderPage(),
      Plugin.TagPage(),
      Plugin.ContentIndex({
        enableSiteMap: true,
        enableRSS: true,
      }),
      Plugin.Assets(),
      Plugin.Static(),
      Plugin.Favicon(),
      Plugin.NotFoundPage(),
      // Comment out CustomOgImages to speed up build time
      Plugin.CustomOgImages(),
    ],
  },
}

export default config
