// Screenshots the shipping accordion (mascot) and the footer bottom on a phone.
const { chromium } = require('playwright-core')
const OUT = process.argv[2]
;(async () => {
  const b = await chromium.launch({ channel: 'chrome', args: ['--enable-unsafe-swiftshader', '--use-angle=swiftshader'] })
  const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true })).newPage()
  const errs = []; p.on('pageerror', e => errs.push(e.message))
  await p.goto('http://localhost:5178/site-preview/index.html', { waitUntil: 'networkidle' }); await p.waitForTimeout(1500)
  await p.evaluate(() => document.querySelector('#accb1').scrollIntoView({ block: 'center' })); await p.waitForTimeout(800)
  await p.click('#accb1'); await p.waitForTimeout(1200)
  const r = await p.evaluate(() => { const e = document.querySelector('.acc__ship').getBoundingClientRect(); return { y: e.top, h: e.height } })
  await p.screenshot({ path: `${OUT}/ship.png`, clip: { x: 0, y: Math.max(0, r.y - 80), width: 390, height: r.h + 160 } })
  await p.evaluate(() => scrollTo(0, document.documentElement.scrollHeight)); await p.waitForTimeout(1500)
  await p.screenshot({ path: `${OUT}/footer.png` })
  console.log('errors', JSON.stringify(errs)); await b.close()
})()
