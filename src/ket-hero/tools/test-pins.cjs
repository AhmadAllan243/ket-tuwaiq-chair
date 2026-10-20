// Checks that pins further down never start inside the hero's pin, incl. after a
// mobile-toolbar style viewport resize, and screenshots the seat landing.
const { chromium, webkit } = require('playwright-core')
const OUT = process.argv[2], URL = process.argv[3] || 'http://localhost:5178/site-preview/index.html'
;(async () => {
  const engines = [['chrome', () => chromium.launch({ channel: 'chrome', args: ['--enable-unsafe-swiftshader', '--use-angle=swiftshader'] })]]
  try { require('fs').accessSync(require('path').join(require('os').homedir(), 'Library/Caches/ms-playwright')); engines.push(['webkit', () => webkit.launch()]) } catch {}
  for (const [tag, launch] of engines) {
    let b; try { b = await launch() } catch (e) { console.log(tag, 'unavailable:', e.message.split('\n')[0]); continue }
    const ctx = await b.newContext({ viewport: { width: 390, height: 664 }, isMobile: tag === 'chrome', hasTouch: true, deviceScaleFactor: 1 })
    const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message))
    await p.goto(URL, { waitUntil: 'networkidle' })
    await p.waitForFunction(() => window.__tuwaiqHero, null, { timeout: 60000 }).catch(() => errs.push('model not loaded'))
    await p.waitForTimeout(1500)
    const pins = () => p.evaluate(() => ScrollTrigger.getAll().filter(s => s.pin).map(s => ({ id: (s.trigger.id || s.trigger.className).slice(0, 16), start: Math.round(s.start), end: Math.round(s.end) })))
    const a = await pins()
    await p.setViewportSize({ width: 390, height: 760 }); await p.waitForTimeout(1200)   // toolbar collapses
    const b2 = await pins()
    const ok = s => s.length >= 2 && s[1].start >= s[0].end
    console.log(tag, 'pins', JSON.stringify(a), ok(a) ? 'OK' : 'OVERLAP', '| after resize', JSON.stringify(b2), ok(b2) ? 'OK' : 'OVERLAP', 'errors', JSON.stringify(errs))
    // seat landing frames
    const h = a[0]; for (const f of [0.38, 0.46, 0.52, 0.58]) {
      await p.evaluate(y => scrollTo(0, y), h.start + f * (h.end - h.start)); await p.waitForTimeout(2200)
      await p.screenshot({ path: `${OUT}/seat-${tag}-${Math.round(f * 100)}.png` })
    }
    // just past the hero: the story section must not be pinned yet
    await p.evaluate(y => scrollTo(0, y), a[0].end + 40); await p.waitForTimeout(1500)
    const storyTop = await p.evaluate(() => Math.round(document.querySelector('#story').getBoundingClientRect().top))
    console.log(tag, 'story section top just after hero:', storyTop, storyTop > 0 ? 'OK (below)' : 'PINNED TOO EARLY')
    await b.close()
  }
})()
