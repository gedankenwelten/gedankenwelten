import { pathToRoot } from "../util/path"
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { classNames } from "../util/lang"
import { i18n } from "../i18n"

const PageTitle: QuartzComponent = ({ fileData, cfg, displayClass }: QuartzComponentProps) => {
  const title = cfg?.pageTitle ?? i18n(cfg.locale).propertyDefaults.title
  const baseDir = pathToRoot(fileData.slug!)
  return (
    <h2 class={classNames(displayClass, "page-title")}>
      <a href={baseDir} aria-label={title}>
        <img class="page-title-mark page-title-mark-dark" src="/static/wordmark-dark.png" alt={title} />
        <img
          class="page-title-mark page-title-mark-light"
          src="/static/wordmark-light.png"
          alt=""
          aria-hidden="true"
        />
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
  display: block;
  width: 15rem;
  max-width: 100%;
  height: auto;
  margin: 0;
  border-radius: 0;
}
/* Theme-Switch: dunkles Wortmark per Default, helles im Lightmode */
.page-title-mark-light {
  display: none;
}
:root[saved-theme="light"] .page-title-mark-dark {
  display: none;
}
:root[saved-theme="light"] .page-title-mark-light {
  display: block;
}
@media (max-width: 800px) {
  .page-title-mark {
    width: 11rem;
  }
}
`

export default (() => PageTitle) satisfies QuartzComponentConstructor
