// Checks the animated numbers and stars: start values, final values, no errors; plus a static (reduced-motion) pass.
const { chromium } = require('playwright-core')
const OUT = process.argv[2]
const read = p => p.evaluate(() => ({
  sold: document.querySelector('#soldPill').textContent, rate: document.querySelector('#ratingVal').textContent,
  count: document.querySelector('#ratingCount').textContent, off: document.querySelector('#priceOff').textContent,
  stock: document.querySelector('#stockText').textContent, score: document.querySelector('#revScore').textContent,
  based: document.querySelector('#revBased').textContent,
  bars: [...document.querySelectorAll('#revBars .cnt')].map(e => e.textContent).join(','),
  starOpacity: [...document.querySelectorAll('[data-stars="hero"] .star')].map(e => (+getComputedStyle(e).opacity).toFixed(2)).join(','),
}))
;(async () => {
  const b = await chromium.launch({ channel: 'chrome', args: ['--enable-unsafe-swiftshader', '--use-angle=swiftshader'] })
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true })
  const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => m.type() === 'error' && errs.push(m.text()))
  await p.goto('http://localhost:5178/site-preview/index.html', { waitUntil: 'networkidle' }); await p.waitForTimeout(2000)
  console.log('before scroll', JSON.stringify(await read(p)))
  const y = await p.evaluate(() => document.querySelector('#soldPill').getBoundingClientRect().top + scrollY - 200)
  await p.evaluate(y => scrollTo(0, y), y)
  for (const [i, ms] of [[1, 250], [2, 350], [3, 500], [4, 1600]].entries()) { await p.waitForTimeout(ms[1]); await p.screenshot({ path: `${OUT}/cnt-${ms[0]}.png`, clip: { x: 0, y: 160, width: 390, height: 520 } }) }
  console.log('after scroll ', JSON.stringify(await read(p)))
  await p.evaluate(() => document.querySelector('#revScore').scrollIntoView({ block: 'center' })); await p.waitForTimeout(2600)
  console.log('reviews      ', JSON.stringify(await read(p)))
  await p.click('#langBtn'); await p.waitForTimeout(600)
  console.log('english      ', JSON.stringify(await read(p)), 'errors', JSON.stringify(errs))
  await ctx.close()
  const q = await (await b.newContext({ viewport: { width: 390, height: 844 }, reducedMotion: 'reduce' })).newPage()
  await q.goto('http://localhost:5178/site-preview/index.html', { waitUntil: 'networkidle' }); await q.waitForTimeout(800)
  console.log('reduced motion', JSON.stringify(await read(q)))
  await b.close()
})()
