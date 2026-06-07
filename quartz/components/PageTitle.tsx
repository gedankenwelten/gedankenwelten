import { pathToRoot } from "../util/path"
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { classNames } from "../util/lang"
import { i18n } from "../i18n"
// @ts-ignore
import script from "./scripts/pageTitle.inline"

// Wortmarken-Pool — je Stil zwei Bilder (dark/light) in quartz/static/:
//   wordmark-<stil>-dark.png · wordmark-<stil>-light.png
// Täglicher Wechsel (siehe pageTitle.inline.ts). Neuen Stil hinzufügen =
// 2 Bilder ablegen + Schlüssel hier ergänzen. Ziel: Pool durch 3 teilbar
// (passt gleichmäßig auf ~30 Tage).
const WORDMARK_STYLES = ["klee", "sumie"]

const PageTitle: QuartzComponent = ({ fileData, cfg, displayClass }: QuartzComponentProps) => {
  const title = cfg?.pageTitle ?? i18n(cfg.locale).propertyDefaults.title
  const baseDir = pathToRoot(fileData.slug!)
  return (
    <h2
      class={classNames(displayClass, "page-title")}
      data-wm-styles={WORDMARK_STYLES.join(",")}
    >
      <a href={baseDir} aria-label={title}>
        {WORDMARK_STYLES.flatMap((s, i) => [
          <img
            class={`page-title-mark wm-${s} wm-dark${i === 0 ? " wm-active" : ""}`}
            src={`/static/wordmark-${s}-dark.png`}
            alt=""
            aria-hidden="true"
          />,
          <img
            class={`page-title-mark wm-${s} wm-light${i === 0 ? " wm-active" : ""}`}
            src={`/static/wordmark-${s}-light.png`}
            alt=""
            aria-hidden="true"
          />,
        ])}
      </a>
    </h2>
  )
}

PageTitle.css = `
.page-title {
  font-size: 1.75rem;
  margin: 0;
  font-family: var(--titleFont);
}
.page-title a {
  display: inline-block;
  line-height: 0;
}
.page-title-mark {
  display: none;
  height: 2.8rem;
  width: auto;
  max-width: 100%;
  margin: 0;
  border-radius: 0;
}
/* Sumi-e trägt mehr Leerraum (ensō) — etwas größer skalieren für gleiches Gewicht */
.page-title-mark.wm-sumie {
  height: 3.5rem;
}
/* Stil-Achse: nur der aktive (per JS täglich gewählte) Stil hat wm-active.
   Theme-Achse: dark/light per CSS. Kombiniert = genau ein sichtbares Bild. */
:root:not([saved-theme="light"]) .page-title-mark.wm-active.wm-dark {
  display: block;
}
:root[saved-theme="light"] .page-title-mark.wm-active.wm-light {
  display: block;
}
@media (max-width: 800px) {
  .page-title-mark {
    height: 2.1rem;
  }
  .page-title-mark.wm-sumie {
    height: 2.7rem;
  }
}
`

PageTitle.afterDOMLoaded = script

export default (() => PageTitle) satisfies QuartzComponentConstructor
