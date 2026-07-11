import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { classNames } from "../util/lang"
import styles from "./styles/rssLink.scss"

// RSS-Icon in der Header-Leiste — führt zur /Feeds-Seite (Haupt-Feed + Rubrik-Feeds).
// Gleicher Stil wie Darkmode (Mond), ReaderMode (Buch) und RandomNote (Würfel).
const RssLink: QuartzComponent = ({ displayClass }: QuartzComponentProps) => {
  const label = "RSS-Feeds"
  return (
    <a href="/Feeds" class={classNames(displayClass, "rsslink")} aria-label={label} title={label}>
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="rssIcon"
        width="20px"
        height="20px"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="1.7"
        stroke-linecap="round"
        aria-label={label}
      >
        <title>{label}</title>
        <path d="M4 11a9 9 0 0 1 9 9" />
        <path d="M4 4a16 16 0 0 1 16 16" />
        <circle cx="5" cy="19" r="1.5" fill="currentColor" stroke="none" />
      </svg>
    </a>
  )
}

RssLink.css = styles

export default (() => RssLink) satisfies QuartzComponentConstructor
