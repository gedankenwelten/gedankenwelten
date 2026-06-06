import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { classNames } from "../util/lang"
import { htmlToJsx } from "../util/jsx"

// Rendert das von HeroLayout hochgezogene Banner-Bild (fileData.banner) prominent
// zwischen Lesezeit und Tags. Das 🎨-Easteregg (Maler-/Stil-Detail) wird direkt
// unter dem Bild gerendert. Ohne Banner rendert die Komponente nichts.
const Banner: QuartzComponent = ({ fileData, displayClass }: QuartzComponentProps) => {
  const banner = fileData.banner
  if (!banner?.src) {
    return null
  }
  return (
    <figure class={classNames(displayClass, "note-banner")}>
      <img src={banner.src} alt={banner.alt} loading="eager" />
      {banner.palette ? (
        <figcaption class="banner-palette">
          {htmlToJsx(fileData.filePath!, banner.palette)}
        </figcaption>
      ) : null}
    </figure>
  )
}

Banner.css = `
.note-banner {
  margin: 1rem 0 1.5rem 0;
}
.note-banner img {
  display: block;
  width: 100%;
  height: auto;
  border-radius: 8px;
}
.banner-palette {
  margin: 0.35rem 0 0 0;
}
.banner-palette > summary {
  list-style: none;
  cursor: pointer;
  width: fit-content;
  margin-left: auto;
  padding: 0.1rem 0.35rem;
  font-size: 0.95rem;
  line-height: 1;
  opacity: 0.5;
  transition: opacity 0.15s ease;
  user-select: none;
}
.banner-palette > summary::-webkit-details-marker {
  display: none;
}
.banner-palette > summary:hover,
.banner-palette[open] > summary {
  opacity: 1;
}
.banner-palette[open] > summary ~ * {
  font-size: 0.85rem;
  line-height: 1.55;
  color: var(--darkgray);
}
.banner-palette p {
  margin: 0.5rem 0;
}
@media (max-width: 800px) {
  .note-banner {
    margin: 0.75rem 0 1rem 0;
  }
}
`

export default (() => Banner) satisfies QuartzComponentConstructor
