// Checks the customer moments deck: cards render, next/prev, filter chips, quick add, lightbox; no errors.
const { chromium } = require('playwright-core')
const [OUT, URL = 'http://localhost:5178/site-preview/index.html'] = process.argv.slice(2)
;(async () => {
  const b = await chromium.launch({ channel: 'chrome', args: ['--enable-unsafe-swiftshader', '--use-angle=swiftshader'] })
  const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true })).newPage()
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => m.type() === 'error' && errs.push(m.text()))
  await p.goto(URL, { waitUntil: 'networkidle' }); await p.waitForTimeout(1500)
  await p.evaluate(() => document.querySelector('#moments').scrollIntoView()); await p.waitForTimeout(1500)
  const st = () => p.evaluate(() => ({ cards: document.querySelectorAll('.mcard').length, active: [...document.querySelectorAll('.mcard')].findIndex(c => c.classList.contains('is-active')), count: document.querySelector('#momCount')?.textContent, chips: document.querySelectorAll('.mom__chip').length, cart: document.querySelector('#cartCount').textContent }))
  const a = await st()
  await p.click('#momNext'); await p.waitForTimeout(900); const b1 = await st()
  await p.screenshot({ path: `${OUT}/moments.png` })
  const add = await p.$('.mcard.is-active .mcard__add'); if (add) { await add.click(); await p.waitForTimeout(1500) }
  const c = await st()
  const media = await p.$('.mcard.is-active .mcard__media'); if (media) { await media.click(); await p.waitForTimeout(800) }
  const lb = await p.evaluate(() => document.querySelector('#lightbox').classList.contains('is-open'))
  console.log(JSON.stringify({ start: a, afterNext: b1, afterAdd: c, lightboxOpen: lb, errors: errs })); await b.close()
})()
