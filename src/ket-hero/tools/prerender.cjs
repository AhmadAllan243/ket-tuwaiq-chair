// Renders the source page in headless Chrome (reduced motion, hero bundle blocked)
// and saves the resulting DOM, so the HTML reads fully even where JS never runs.
const { chromium } = require('playwright-core')
const fs = require('fs')
const [src, out] = process.argv.slice(2)
;(async () => {
  const b = await chromium.launch({ channel: 'chrome' })
  const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, reducedMotion: 'reduce' })).newPage()
  await p.route('**/ket-hero.js', r => r.abort())
  await p.goto(src, { waitUntil: 'networkidle' })
  await p.waitForTimeout(800)
  const html = await p.evaluate(() => {
    const r = document.documentElement
    r.removeAttribute('class'); r.removeAttribute('style')
    document.querySelector('#toast').className = 'toast'
    document.querySelectorAll('.gzv').forEach(e => e.remove()); document.body.classList.remove('kg-hi')   // the peeking gazelle is added at runtime
    return '<!doctype html>\n' + r.outerHTML
  })
  fs.writeFileSync(out, html); await b.close()
})()
