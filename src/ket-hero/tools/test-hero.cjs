const { chromium } = require('playwright-core')
const OUT = process.argv[2]
const URL = 'http://localhost:5178/site-preview/index.html'
const sleep = ms => new Promise(r => setTimeout(r, ms))
;(async () => {
  const b = await chromium.launch({ channel: 'chrome', args: ['--enable-unsafe-swiftshader', '--use-angle=swiftshader', '--ignore-gpu-blocklist'] })
  for (const [tag, vp, mobile] of [['m', { width: 390, height: 844 }, true], ['d', { width: 1440, height: 900 }, false]]) {
    const ctx = await b.newContext({ viewport: vp, isMobile: mobile, hasTouch: mobile })
    const p = await ctx.newPage(); const errs = [], logs = []
    p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); if (m.text().includes('TuwaiqHero')) logs.push(m.text()) })
    await p.goto(URL, { waitUntil: 'networkidle' })
    await p.waitForFunction(() => window.__tuwaiqHero, null, { timeout: 30000 })
    if (tag === 'm') console.log('HIERARCHY', JSON.stringify(await p.evaluate(() => window.__tuwaiqHero), null, 1))
    await sleep(1200)
    const vh = vp.height
    const pins = await p.evaluate(() => ScrollTrigger.getAll().map(s => [s.trigger?.className || s.trigger?.id, Math.round(s.start), Math.round(s.end), !!s.pin]).slice(0, 3))
    console.log(tag, 'triggers', JSON.stringify(pins))
    for (const f of [0, 0.12, 0.24, 0.38, 0.5, 0.62, 0.74, 0.86, 1.0]) {
      await p.evaluate(y => window.scrollTo(0, y), (128 + f * vh * 2.8)); await sleep(2200)
      await p.screenshot({ path: `${OUT}/h-${tag}-${String(Math.round(f * 100)).padStart(3, '0')}.png` })
    }
    // past the pin: the product section should follow right after
    await p.evaluate(y => window.scrollTo(0, y), vh * 2.8 + vh * 0.8); await sleep(1500)
    await p.screenshot({ path: `${OUT}/h-${tag}-after.png` })
    const after = await p.evaluate(() => [document.querySelector('#pTitle').getBoundingClientRect().top, document.documentElement.scrollWidth])
    // reverse scrub back to top
    await p.evaluate(() => window.scrollTo(0, innerHeight * 0.6)); await sleep(2500)
    await p.screenshot({ path: `${OUT}/h-${tag}-reverse.png` })
    console.log(tag, 'after-pin product title top', Math.round(after[0]), 'scrollW', after[1], 'errors', JSON.stringify(errs))
    await ctx.close()
  }
  await b.close()
})()
