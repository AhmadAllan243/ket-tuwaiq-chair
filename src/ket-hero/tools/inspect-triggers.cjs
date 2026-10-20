// Lists every ScrollTrigger on the page (debug helper).
const { chromium } = require('playwright-core')
;(async () => {
  const b = await chromium.launch({ channel: 'chrome', args: ['--enable-unsafe-swiftshader', '--use-angle=swiftshader'] })
  const p = await (await b.newContext({ viewport: { width: 390, height: 664 }, isMobile: true, hasTouch: true })).newPage()
  if (process.argv[3] === 'nohero') await p.route('**/ket-hero.js', r => r.abort())
  p.on('pageerror', e => console.log('PAGEERROR', e.message))
  if (process.argv[4] === 'trace') await p.addInitScript(() => {
    const iv = setInterval(() => {
      if (!window.ScrollTrigger) return; clearInterval(iv)
      const k = ScrollTrigger.prototype.kill
      ScrollTrigger.prototype.kill = function (...a) { if (!this.vars.once) console.log('KILL ' + (this.trigger?.id || this.trigger?.className) + ' ' + new Error().stack.split('\n').slice(2, 7).join(' | ')); return k.apply(this, a) }
    }, 1)
  })
  const logs = []; p.on('console', m => logs.push(m.type() + ': ' + m.text().slice(0, 140)))
  await p.goto(process.argv[2] || 'http://localhost:5178/site-preview/index.html', { waitUntil: 'load' })
  await p.waitForTimeout(5000)
  console.log(JSON.stringify(await p.evaluate(() => ({
    cls: document.documentElement.className,
    all: ScrollTrigger.getAll().map(s => [s.trigger?.id || String(s.trigger?.className).slice(0, 20), Math.round(s.start), Math.round(s.end), !!s.pin]),
    gsap: window.gsap && window.gsap.version,
  })), null, 1))
  console.log(logs.filter(l => !l.includes('TuwaiqHero')).filter(l => l.includes('KILL')).slice(0, 6).join('\n'))
  await b.close()
})()
