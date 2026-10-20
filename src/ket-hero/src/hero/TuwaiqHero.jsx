import { Suspense, useEffect, useLayoutEffect, useMemo, useRef, useState } from 'react'
import { Canvas, useFrame, useThree } from '@react-three/fiber'
import { useGLTF, useProgress, ContactShadows, Environment, Lightformer, Html } from '@react-three/drei'
import * as THREE from 'three'
import { HERO_CSS } from './heroStyles.js'

// GSAP is not bundled: the hero uses the page's own window.gsap / window.ScrollTrigger, so the
// hero pin and the page's pins live in ONE ScrollTrigger instance and are measured in order.
const gsap = window.gsap
const ScrollTrigger = window.ScrollTrigger
gsap.registerPlugin(ScrollTrigger)

export const MODEL_URL = new URL('models/tuwaiq-chair.glb', document.baseURI).href
export const PARTS = ['ChairBase', 'SeatCushion', 'SeatBack']

const { degToRad, lerp, clamp } = THREE.MathUtils
const FLOOR_Y = -0.907            // lowest vertex of the assembled model
const START_ROT_Y = degToRad(-40) // chair angle while the parts fly in
const END_ROT_Y = degToRad(28)    // final hero showcase angle

/*
 * Flight plan for each part.
 *  corner     — where it waits, as a fraction of the visible half-width/half-height
 *               ([landscape], [portrait]); the 4th corner is left for the scroll hint.
 *               On phones the cushions wait stacked above the frame's landing spot, so
 *               nothing overlaps once the frame is in place.
 *  pose       — the angle it shows while waiting in its corner (world euler, radians)
 *  axis/turns — the extra tumble it unwinds on the way in (whole turns, so the corner
 *               pose and the assembled pose are both exact)
 *  arc        — how far the flight path bows toward the camera / upward mid-flight
 *  stage      — cushions first fly to a staging point at this offset from their seat
 *               (finishing the tumble on the way), then move straight into place: the seat
 *               slides in from the front under the armrests, the backrest drops in from
 *               above between the uprights. Nothing passes through the frame.
 */
const FLIGHT = {
  ChairBase: {
    key: 'base', label: { ar: 'الهيكل', en: 'Frame' }, idx: '01',
    corner: { land: [-0.56, -0.34], port: [-0.3, -0.34] },
    pose: [0.18, degToRad(55), -0.06], axis: [0, 1, 0], turns: 1, arc: [0.35, 0.45, 0.3], scale: 0.62,
  },
  SeatCushion: {
    key: 'cushion', label: { ar: 'المقعد', en: 'Seat' }, idx: '02', stage: [0, 0.12, 1.9],
    corner: { land: [0.58, 0.38], port: [0.25, 0.4] },
    pose: [0.55, degToRad(-35), 0.32], axis: [1, 0.35, 0.2], turns: 1, arc: [-0.35, 0.32, 0.25], scale: 0.66,
  },
  SeatBack: {
    key: 'back', label: { ar: 'المسند', en: 'Backrest' }, idx: '03', stage: [0, 0.75, 0],
    corner: { land: [-0.5, 0.44], port: [-0.25, 0.72] },
    pose: [-0.35, degToRad(40), -0.22], axis: [0.15, 1, -0.25], turns: -1, arc: [0.4, 0.5, 0.3], scale: 0.72,
  },
}

const COPY = {
  ar: { eyebrow: 'ket · مجموعة ٢٠٢٦', title: 'كرسي طويق', sub: 'نقوش نجد والحجاز وعسير، تجتمع في قطعة واحدة.', cta: 'تسوّق الكرسي', hint: 'مرّر لتركيب الكرسي', parts: '٣ قطع · كرسي واحد', loading: 'جارٍ تحميل النموذج' },
  en: { eyebrow: 'ket · 2026 collection', title: 'Tuwaiq Chair', sub: 'The patterns of Najd, Hijaz and Asir, brought together in one piece.', cta: 'Shop the chair', hint: 'Scroll to assemble', parts: '3 parts · 1 chair', loading: 'Loading model' },
}

const popIn = gsap.parseEase('back.out(1.6)')
const reduceMotion = () => window.matchMedia('(prefers-reduced-motion: reduce)').matches

/* ------------------------------------------------------------------ */
/* Step 1 — hierarchy inspection + resting (assembled) transforms      */
/* ------------------------------------------------------------------ */
export function inspectHierarchy(scene) {
  const rows = []
  const rest = {}
  scene.traverse(o => {
    rows.push({ name: o.name || '(unnamed)', type: o.type, parent: o.parent?.name || '—', mesh: !!o.isMesh })
    if (PARTS.includes(o.name)) {
      rest[o.name] = { obj: o, position: o.position.clone(), quaternion: o.quaternion.clone(), rotation: o.rotation.clone(), scale: o.scale.clone() }
    }
    if (o.isMesh) { o.castShadow = true; o.receiveShadow = true }
  })
  console.groupCollapsed('%c[TuwaiqHero] GLB hierarchy', 'font-weight:600')
  console.table(rows)
  console.table(Object.fromEntries(Object.entries(rest).map(([k, r]) => [k, {
    position: r.position.toArray().map(n => +n.toFixed(4)).join(', '),
    rotation: [r.rotation.x, r.rotation.y, r.rotation.z].map(n => +n.toFixed(4)).join(', '),
    scale: r.scale.toArray().map(n => +n.toFixed(4)).join(', '),
  }])))
  console.groupEnd()
  const missing = PARTS.filter(p => !rest[p])
  if (missing.length) console.warn('[TuwaiqHero] Missing expected parts:', missing)
  window.__tuwaiqHero = { rows, rest: Object.fromEntries(Object.entries(rest).map(([k, r]) => [k, { position: r.position.toArray(), rotation: [r.rotation.x, r.rotation.y, r.rotation.z], scale: r.scale.toArray() }])) }
  return rest
}

/* ------------------------------------------------------------------ */
/* Camera + layout: a wide shot that shows all four corners, dollying  */
/* in to the close hero framing as the chair completes.                */
/* ------------------------------------------------------------------ */
function computeLayout(size, dir) {
  const aspect = size.width / size.height
  const portrait = aspect < 0.9
  const fov = portrait ? 38 : 30
  const t = Math.tan(degToRad(fov / 2))
  const shift = portrait ? 0 : Math.min(1.25, (aspect - 1) * 1.1) * (dir === 'rtl' ? 1 : -1)
  const close = { dist: Math.max((portrait ? 4.6 : 4.0) / (2 * t), (portrait ? 2.9 : 3.4) / (2 * t * aspect)), x: shift, y: 0.7, lookY: portrait ? -0.75 : -0.1 }
  const wide = { dist: Math.max((portrait ? 6.4 : 5.2) / (2 * t), (portrait ? 3.4 : 6.6) / (2 * t * aspect)), x: 0, y: 0.9, lookY: portrait ? 0.05 : 0 }
  const halfH = wide.dist * t, halfW = halfH * aspect
  const corners = {}
  for (const name of PARTS) {
    const [fx, fy] = FLIGHT[name].corner[portrait ? 'port' : 'land']
    const mx = dir === 'rtl' ? -fx : fx // mirror the layout for Arabic
    corners[name] = new THREE.Vector3(wide.x + mx * halfW, wide.lookY + fy * halfH, 0)
  }
  return { fov, portrait, wide, close, corners }
}

function CameraRig({ prog, layout }) {
  const { camera } = useThree()
  const look = useMemo(() => new THREE.Vector3(), [])
  useFrame(() => {
    const L = layout.current; if (!L) return
    const c = prog.current.cam
    if (camera.fov !== L.fov) { camera.fov = L.fov; camera.updateProjectionMatrix() }
    camera.position.set(lerp(L.wide.x, L.close.x, c), lerp(L.wide.y, L.close.y, c), lerp(L.wide.dist, L.close.dist, c))
    look.set(lerp(L.wide.x, L.close.x, c), lerp(L.wide.lookY, L.close.lookY, c), 0)
    camera.lookAt(look)
  })
  return null
}

/* ------------------------------------------------------------------ */
/* The chair                                                           */
/* ------------------------------------------------------------------ */
const _v = new THREE.Vector3(), _arc = new THREE.Vector3(), _q = new THREE.Quaternion(), _qc = new THREE.Quaternion()
const _qSpin = new THREE.Quaternion(), _qInv = new THREE.Quaternion(), _e = new THREE.Euler(), _axis = new THREE.Vector3()

function Chair({ prog, layout, labels, lang }) {
  const { scene } = useGLTF(MODEL_URL, false, true)
  const rest = useMemo(() => inspectHierarchy(scene), [scene])
  const group = useRef()
  const shadow = useRef()

  useEffect(() => { // parts pop into their corners once the model is ready
    if (reduceMotion()) { prog.current.intro = 1; return }
    gsap.fromTo(prog.current, { intro: 0 }, { intro: 1, duration: 1.8, ease: 'expo.out', delay: 0.15 })
  }, [prog])

  useFrame(state => {
    const p = prog.current, L = layout.current, g = group.current
    if (!L || !g) return
    const time = state.clock.elapsedTime
    g.rotation.y = lerp(START_ROT_Y, END_ROT_Y, p.turn)
    g.scale.setScalar(1 + 0.014 * (p.hitBase + p.hitCushion + p.hitBack)) // landing pulses
    g.updateMatrixWorld()
    g.getWorldQuaternion(_qInv).invert()

    PARTS.forEach((name, i) => {
      const r = rest[name]; if (!r) return
      const f = FLIGHT[name]
      const e = p[f.key]          // 0 = waiting in its corner, 1 = assembled
      const wait = 1 - e
      const intro = clamp(p.intro * 1.5 - i * 0.22, 0, 1)

      // position: corner (world) → group-local, plus idle float and a bowed flight path
      g.worldToLocal(_v.copy(L.corners[name]))
      _v.y += Math.sin(time * 0.9 + i * 2.1) * 0.06 * wait
      const bow = Math.sin(Math.PI * e)
      _arc.set(f.arc[0], f.arc[1], f.arc[2]).multiplyScalar(bow).applyQuaternion(_qInv)
      // cushions: corner → staging point (forward/up moves early, coming down late, so the
      // path stays clear of the arms) → straight into place
      let em = e
      if (f.stage) {
        const A = 0.62
        const ea = Math.min(e / A, 1), eb = Math.max((e - A) / (1 - A), 0)
        em = ea * ea * (3 - 2 * ea)
        const early = 1 - Math.pow(1 - ea, 3), late = ea * ea * ea
        const slide = eb < 0.5 ? 4 * eb * eb * eb : 1 - Math.pow(-2 * eb + 2, 3) / 2
        const [sx, sy, sz] = f.stage
        const tx = r.position.x + sx, ty = r.position.y + sy, tz = r.position.z + sz
        const goingUp = ty > _v.y
        r.obj.position.set(
          lerp(_v.x, tx, early),
          lerp(_v.y, ty, goingUp ? early : late),
          lerp(_v.z, tz, early))
        _arc.set(f.arc[0], f.arc[1], f.arc[2]).multiplyScalar(Math.sin(Math.PI * em)).applyQuaternion(_qInv)
        r.obj.position.add(_arc)
        r.obj.position.x -= sx * slide; r.obj.position.y -= sy * slide; r.obj.position.z -= sz * slide
      } else {
        r.obj.position.copy(_v).lerp(r.position, e).add(_arc)
      }

      // rotation: corner pose (with a gentle idle sway) → resting pose, plus an unwinding tumble
      _e.set(f.pose[0], f.pose[1] + Math.sin(time * 0.6 + i) * 0.35 * wait, f.pose[2])
      _qc.setFromEuler(_e).premultiply(_qInv)
      _q.slerpQuaternions(_qc, r.quaternion, em)
      _qSpin.setFromAxisAngle(_axis.set(...f.axis).normalize(), f.turns * Math.PI * 2 * (1 - em))
      r.obj.quaternion.copy(_q).multiply(_qSpin)

      // scale: smaller in the corner, full size once seated; intro pops it in
      const s = lerp(f.scale, 1, em) * (intro < 1 ? popIn(intro) : 1)
      r.obj.scale.copy(r.scale).multiplyScalar(Math.max(s, 0.0001))
    })

    const sm = shadow.current?.children?.[0]?.material
    if (sm) sm.opacity = 0.12 + 0.34 * p.base
    labels.current.forEach(el => { if (el) { el.style.opacity = Math.min(p.labels, p.intro); el.style.visibility = p.labels > 0.02 ? 'visible' : 'hidden' } })
  })

  return (
    <>
      <group ref={group}><primitive object={scene} /></group>
      {layout.current && PARTS.map((name, i) => {
        const c = layout.current.corners[name]
        return (
          <Html key={name} position={[c.x, c.y - (layout.current.portrait ? 0.62 : 0.78), 0]} center zIndexRange={[2, 0]} style={{ pointerEvents: 'none' }}>
            <div ref={el => (labels.current[i] = el)} className="kh-label" style={{ opacity: 0 }}>
              <span className="kh-label__idx">{FLIGHT[name].idx}</span>{FLIGHT[name].label[lang]}
            </div>
          </Html>
        )
      })}
      <ContactShadows ref={shadow} position={[0, FLOOR_Y + 0.002, 0]} opacity={0.12} scale={5} blur={2.6} far={1.6} resolution={512} color="#2a2420" />
    </>
  )
}

function Studio({ prog }) {
  const recv = useRef()
  useFrame(() => { if (recv.current) recv.current.opacity = 0.03 + 0.12 * prog.current.base })
  return (
    <>
      <ambientLight intensity={0.35} />
      {/* warm key */}
      <directionalLight position={[3.2, 4.5, 3.4]} intensity={2.4} color="#ffe0bd" castShadow
        shadow-mapSize={[2048, 2048]} shadow-bias={-0.0004} shadow-normalBias={0.02} shadow-radius={6}
        shadow-camera-left={-4} shadow-camera-right={4} shadow-camera-top={4} shadow-camera-bottom={-4} shadow-camera-near={0.5} shadow-camera-far={16} />
      {/* cool rim + fill */}
      <directionalLight position={[-3.5, 2.6, -3.2]} intensity={1.3} color="#c9d6ff" />
      <directionalLight position={[-3, 1.2, 2.5]} intensity={0.45} color="#e8eeff" />
      {/* soft ground shadow receiver */}
      <mesh rotation-x={-Math.PI / 2} position={[0, FLOOR_Y, 0]} receiveShadow>
        <planeGeometry args={[20, 20]} />
        <shadowMaterial ref={recv} transparent opacity={0.03} />
      </mesh>
      {/* local light-formers for soft reflections; nothing is fetched */}
      <Environment resolution={128}>
        <Lightformer form="rect" intensity={2.2} color="#fff3e6" position={[3, 4, 3]} scale={[4, 4, 1]} target={[0, 0, 0]} />
        <Lightformer form="rect" intensity={1.2} color="#dfe7ff" position={[-4, 2, -3]} scale={[5, 3, 1]} target={[0, 0, 0]} />
        <Lightformer form="ring" intensity={0.8} color="#ffffff" position={[0, 5, 0]} scale={3} target={[0, 0, 0]} />
      </Environment>
    </>
  )
}

// Recomputes the corner layout whenever the canvas resizes or the language flips.
function LayoutSync({ layout, dir, onChange }) {
  const { size } = useThree()
  useLayoutEffect(() => { layout.current = computeLayout(size, dir); onChange(n => n + 1) }, [size, dir, layout, onChange])
  return null
}

/* ------------------------------------------------------------------ */
/* DOM overlay                                                         */
/* ------------------------------------------------------------------ */
function Loader({ label }) {
  const { active, progress } = useProgress()
  const [gone, setGone] = useState(false)
  useEffect(() => { if (!active && progress >= 100) { const t = setTimeout(() => setGone(true), 500); return () => clearTimeout(t) } }, [active, progress])
  if (gone) return null
  return (
    <div className={`kh-loader${!active && progress >= 100 ? ' is-done' : ''}`} role="status" aria-live="polite">
      <span className="kh-spinner" aria-hidden="true" />
      <span className="kh-loader__txt">{label} <b dir="ltr">{Math.round(progress)}%</b></span>
    </div>
  )
}

function useLang() {
  const get = () => (document.documentElement.lang === 'en' ? 'en' : 'ar')
  const [lang, setLang] = useState(get)
  useEffect(() => {
    const mo = new MutationObserver(() => setLang(get()))
    mo.observe(document.documentElement, { attributes: true, attributeFilter: ['lang'] })
    return () => mo.disconnect()
  }, [])
  return lang
}

function hasWebGL() {
  try { const c = document.createElement('canvas'); return !!(c.getContext('webgl2') || c.getContext('webgl')) } catch { return false }
}

export default function TuwaiqHero({ fallbackHTML = '' }) {
  const lang = useLang()
  const dir = lang === 'ar' ? 'rtl' : 'ltr'
  const t = COPY[lang]
  const section = useRef()
  const ui = useRef()
  const hint = useRef()
  const labels = useRef([])
  const layout = useRef(null)
  const [, setLayoutTick] = useState(0)
  const prog = useRef({ intro: 0, labels: 1, base: 0, cushion: 0, back: 0, hitBase: 0, hitCushion: 0, hitBack: 0, turn: 0, cam: 0, ui: 0 })
  const [webgl] = useState(hasWebGL)

  useLayoutEffect(() => {
    const p = prog.current
    const applyUI = () => {
      if (ui.current) {
        ui.current.style.opacity = p.ui
        ui.current.style.transform = `translate3d(0, ${(1 - p.ui) * 28}px, 0)`
        ui.current.style.visibility = p.ui > 0.01 ? 'visible' : 'hidden'
      }
      if (hint.current) hint.current.style.opacity = p.labels
    }
    if (reduceMotion() || !webgl) {
      Object.assign(p, { intro: 1, labels: 0, base: 1, cushion: 1, back: 1, turn: 1, cam: 1, ui: 1 })
      applyUI()
      return
    }
    applyUI()
    const ctx = gsap.context(() => {
      const hit = (key, at) => tl.to(p, { [key]: 1, duration: 0.025, ease: 'power2.out' }, at).to(p, { [key]: 0, duration: 0.05, ease: 'power2.in' }, at + 0.025)
      // Normalised 0→1 timeline, scrubbed by scroll while the hero is pinned.
      const tl = gsap.timeline({
        defaults: { ease: 'none' },
        onUpdate: applyUI,
        scrollTrigger: {
          trigger: section.current, start: 'top top', end: '+=280%',
          pin: true, pinSpacing: true, scrub: 1.2, anticipatePin: 1, invalidateOnRefresh: true,
          refreshPriority: 10, // measure first, so pins further down (the story) include this pin's scroll length
        },
      })
      tl.to(p, { labels: 0, duration: 0.07, ease: 'power1.in' }, 0.03)
        .to(p, { turn: 1, duration: 0.92, ease: 'power1.inOut' }, 0.04)            // chair keeps turning toward its showcase angle
        .to(p, { base: 1, duration: 0.3, ease: 'power3.inOut' }, 0.06)            // 1. frame swoops in from its corner
        .to(p, { cushion: 1, duration: 0.3, ease: 'power3.inOut' }, 0.3)          // 2. seat tumbles in and drops onto the frame
        .to(p, { back: 1, duration: 0.3, ease: 'expo.inOut' }, 0.54)              // 3. backrest spins in, glides and snaps
        .to(p, { cam: 1, duration: 0.42, ease: 'power2.inOut' }, 0.52)            // camera dollies in to the hero framing
        .to(p, { ui: 1, duration: 0.1, ease: 'power2.out' }, 0.86)                // copy fades in as it locks together
        .to({}, { duration: 0.04 }, 0.96)                                          // short hold, then the pin releases
      hit('hitBase', 0.355); hit('hitCushion', 0.595); hit('hitBack', 0.835)
    }, section)
    // The pin adds scroll distance above everything else: re-measure the page's own triggers.
    ScrollTrigger.sort()
    ScrollTrigger.refresh()
    return () => ctx.revert()
  }, [webgl])

  const goShop = e => {
    e.preventDefault()
    const target = document.getElementById('product')
    if (target) window.scrollTo({ top: target.getBoundingClientRect().top + window.scrollY - 64, behavior: reduceMotion() ? 'auto' : 'smooth' })
  }

  return (
    <section ref={section} className="kh" aria-label={t.title} dir={dir} lang={lang}>
      <style>{HERO_CSS}</style>
      {webgl ? (
        <Canvas className="kh-canvas" shadows dpr={Math.min(window.devicePixelRatio || 1, 2)}
          gl={{ antialias: true, alpha: true, powerPreference: 'high-performance', toneMapping: THREE.ACESFilmicToneMapping, outputColorSpace: THREE.SRGBColorSpace }}
          camera={{ fov: 30, near: 0.1, far: 80, position: [0, 0.9, 12] }}>
          <LayoutSync layout={layout} dir={dir} onChange={setLayoutTick} />
          <CameraRig prog={prog} layout={layout} />
          <Studio prog={prog} />
          <Suspense fallback={null}><Chair prog={prog} layout={layout} labels={labels} lang={lang} /></Suspense>
        </Canvas>
      ) : (
        <div className="kh-fallback" dangerouslySetInnerHTML={{ __html: fallbackHTML }} />
      )}

      <div ref={hint} className="kh-hint" aria-hidden="true"><b>{t.parts}</b><span>{t.hint}</span><i /></div>

      <div ref={ui} className="kh-ui">
        <p className="kh-eyebrow">{t.eyebrow}</p>
        <h2 className="kh-title">{t.title}</h2>
        <p className="kh-sub">{t.sub}</p>
        <a className="kh-cta" href="#product" onClick={goShop}>{t.cta}<span aria-hidden="true">{lang === 'ar' ? '←' : '→'}</span></a>
      </div>

      {webgl && <Loader label={t.loading} />}
    </section>
  )
}

useGLTF.preload(MODEL_URL, false, true)
