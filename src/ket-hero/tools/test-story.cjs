// Captures the story section at several scroll points (phone + desktop) and reports errors.
const { chromium } = require('playwright-core')
const OUT = process.argv[2]
;(async () => {
  const b = await chromium.launch({ channel: 'chrome', args: ['--enable-unsafe-swiftshader', '--use-angle=swiftshader'] })
  for (const [tag, vp, mobile] of [['m', { width: 390, height: 844 }, true], ['d', { width: 1440, height: 900 }, false]]) {
    const p = await (await b.newContext({ viewport: vp, isMobile: mobile, hasTouch: mobile, deviceScaleFactor: mobile ? 2 : 1 })).newPage()
    const errs = []; p.on('pageerror', e => errs.push(e.message))
    await p.goto('http://localhost:5178/site-preview/index.html', { waitUntil: 'networkidle' }); await p.waitForTimeout(1500)
    const st = await p.evaluate(() => { const s = ScrollTrigger.getAll().find(s => s.pin && s.trigger.id === 'storyStage'); return [s.start, s.end] })
    await p.evaluate(y => scrollTo(0, y), st[0] - vp.height * 0.4); await p.waitForTimeout(1800)
    await p.screenshot({ path: `${OUT}/st-${tag}-0.png` })
    for (const f of [0.15, 0.35, 0.55, 0.75, 1.0]) {
      await p.evaluate(y => scrollTo(0, y), st[0] + f * (st[1] - st[0])); await p.waitForTimeout(1800)
      await p.screenshot({ path: `${OUT}/st-${tag}-${Math.round(f * 100)}.png` })
    }
    console.log(tag, 'story pin', st.map(Math.round), 'errors', JSON.stringify(errs))
  }
  await b.close()
})()
