// iPhone-resolution (3x) frames of the hero for checking model detail.
const { chromium } = require('playwright-core')
const [OUT, ...fs] = process.argv.slice(2)
;(async () => {
  const b = await chromium.launch({ channel: 'chrome', args: ['--enable-unsafe-swiftshader', '--use-angle=swiftshader'] })
  const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 3, isMobile: true, hasTouch: true })).newPage()
  await p.goto('http://localhost:5178/site-preview/index.html', { waitUntil: 'networkidle' })
  await p.waitForFunction(() => window.__tuwaiqHero, null, { timeout: 60000 }); await p.waitForTimeout(1200)
  const h = await p.evaluate(() => { const s = ScrollTrigger.getAll().find(s => s.pin && s.trigger.classList.contains('kh')); return [s.start, s.end] })
  for (const f of fs.map(Number)) {
    await p.evaluate(y => scrollTo(0, y), h[0] + f * (h[1] - h[0])); await p.waitForTimeout(2500)
    await p.screenshot({ path: `${OUT}/q-${Math.round(f * 100)}.png` })
  }
  await b.close()
})()
