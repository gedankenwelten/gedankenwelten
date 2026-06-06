import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { classNames } from "../util/lang"

// Rendert das von HeroLayout hochgezogene Banner-Bild (fileData.banner) prominent
// zwischen Lesezeit und Tags. Ohne Banner rendert die Komponente nichts.
const Banner: QuartzComponent = ({ fileData, displayClass }: QuartzComponentProps) => {
  const banner = fileData.banner
  if (!banner?.src) {
    return null
  }
  return (
    <figure class={classNames(displayClass, "note-banner")}>
      <img src={banner.src} alt={banner.alt} loading="eager" />
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
@media (max-width: 800px) {
  .note-banner {
    margin: 0.75rem 0 1rem 0;
  }
}
`

export default (() => Banner) satisfies QuartzComponentConstructor
