// Captures the hero at fine progress steps on a phone viewport (seat + backrest flights).
const { chromium } = require('playwright-core')
const [OUT, from = '0.28', to = '0.88', step = '0.04'] = process.argv.slice(2)
;(async () => {
  const b = await chromium.launch({ channel: 'chrome', args: ['--enable-unsafe-swiftshader', '--use-angle=swiftshader'] })
  const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true })).newPage()
  await p.goto('http://localhost:5178/site-preview/index.html', { waitUntil: 'networkidle' })
  await p.waitForFunction(() => window.__tuwaiqHero, null, { timeout: 60000 }); await p.waitForTimeout(1200)
  const h = await p.evaluate(() => { const s = ScrollTrigger.getAll().find(s => s.pin && s.trigger.classList.contains('kh')); return [s.start, s.end] })
  for (let f = +from; f <= +to + 1e-6; f += +step) {
    await p.evaluate(y => scrollTo(0, y), h[0] + f * (h[1] - h[0])); await p.waitForTimeout(2000)
    await p.screenshot({ path: `${OUT}/fl-${String(Math.round(f * 100)).padStart(3, '0')}.png` })
  }
  await b.close()
})()
