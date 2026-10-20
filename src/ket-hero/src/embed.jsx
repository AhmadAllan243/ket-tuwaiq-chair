import { createRoot } from 'react-dom/client'
import TuwaiqHero from './hero/TuwaiqHero.jsx'

// Mounts into <div id="ket-hero"> at the top of the product page.
// Whatever static markup is already inside it (title + photo) stays as the
// no-JS / no-WebGL fallback and is replaced once React takes over.
const mount = document.getElementById('ket-hero')
if (mount) {
  const fallbackHTML = mount.querySelector('.kh-static-media')?.innerHTML || ''
  createRoot(mount).render(<TuwaiqHero fallbackHTML={fallbackHTML} />)
}
