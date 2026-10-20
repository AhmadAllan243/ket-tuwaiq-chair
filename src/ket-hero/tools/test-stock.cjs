// Captures the stock bar + count-down over time (count text, bar width as % of track, bar colour).
const { chromium } = require('playwright-core')
;(async () => {
  const b = await chromium.launch({ channel: 'chrome', args: ['--enable-unsafe-swiftshader', '--use-angle=swiftshader'] })
  const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true })).newPage()
  const errs = []; p.on('pageerror', e => errs.push(e.message))
  await p.goto('http://localhost:5178/site-preview/index.html', { waitUntil: 'networkidle' }); await p.waitForTimeout(1500)
  const y = await p.evaluate(() => document.querySelector('#stockText').getBoundingClientRect().top + scrollY - 420)
  await p.evaluate(y => scrollTo(0, y), y)
  const out = []
  for (const ms of [60, 250, 400, 600, 1400]) {
    await p.waitForTimeout(ms)
    out.push(await p.evaluate(() => {
      const bar = document.querySelector('#stockBar'), tr = bar.parentElement
      return [document.querySelector('#stockText').textContent, Math.round(bar.getBoundingClientRect().width / tr.getBoundingClientRect().width * 100) + '%', getComputedStyle(bar).backgroundColor]
    }))
    await p.screenshot({ path: `${process.argv[2]}/stock-${out.length}.png`, clip: { x: 0, y: 380, width: 390, height: 120 } })
  }
  console.log(JSON.stringify(out), 'errors', JSON.stringify(errs)); await b.close()
})()
