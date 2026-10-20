// Scoped to .kh so nothing leaks into the existing page's global CSS.
export const HERO_CSS = `
.kh{ position:relative; width:100%; height:100vh; height:100lvh; --kh-toolbar:0px; overflow:hidden; isolation:isolate;
  background:radial-gradient(120% 80% at 50% 38%, #ffffff 0%, #f6f5f3 46%, #e9e7e4 100%);
  font-family:var(--font, 'Inter Tight', 'IBM Plex Sans Arabic', system-ui, sans-serif); color:#000; }
.kh-canvas{ position:absolute!important; inset:0; width:100%!important; height:100%!important; z-index:0; }
.kh-fallback{ position:absolute; inset:0; display:grid; place-items:center; }
.kh-fallback img{ width:min(78vw, 560px); height:auto; mix-blend-mode:multiply; }

@supports (height:100lvh){ .kh{ --kh-toolbar:calc(100lvh - 100svh); } }  /* keep copy above Safari's toolbar */
.kh-ui{ position:absolute; z-index:2; inset-inline:clamp(16px, 4vw, 56px); bottom:calc(var(--kh-toolbar) + clamp(28px, 7vh, 72px));
  display:grid; gap:12px; justify-items:start; max-width:560px; opacity:0; visibility:hidden; will-change:opacity, transform; }
.kh-eyebrow{ margin:0; font-size:12px; font-weight:600; letter-spacing:.08em; text-transform:uppercase; color:#555; }
.kh[lang="ar"] .kh-eyebrow{ letter-spacing:0; font-size:13px; }
.kh-title{ margin:0; font-size:clamp(48px, 9vw, 128px); line-height:.9; font-weight:600; letter-spacing:-.035em; text-transform:uppercase; text-wrap:balance; }
.kh[lang="ar"] .kh-title{ font-weight:700; letter-spacing:0; line-height:1.1; }
.kh-sub{ margin:0; max-width:38ch; font-size:clamp(15px, 1.3vw, 18px); line-height:1.5; color:#333; }
.kh-cta{ margin-top:8px; display:inline-flex; align-items:center; gap:10px; height:52px; padding-inline:26px; border-radius:999px;
  background:#000; color:#fff; text-decoration:none; font-size:15px; font-weight:600; letter-spacing:.03em; text-transform:uppercase;
  transition:transform .4s cubic-bezier(.165,.84,.44,1), background-color .25s; }
.kh[lang="ar"] .kh-cta{ letter-spacing:0; font-size:16px; }
.kh-cta:hover{ background:#262626; transform:translateY(-2px); }
.kh-cta:focus-visible{ outline:2px solid #000; outline-offset:3px; }
.kh-cta span{ transition:transform .4s cubic-bezier(.165,.84,.44,1); }
.kh-cta:hover span{ transform:translateX(4px); }
.kh[dir="rtl"] .kh-cta:hover span{ transform:translateX(-4px); }

.kh-hint{ position:absolute; z-index:2; inset-inline-end:clamp(16px, 4vw, 56px); bottom:calc(var(--kh-toolbar) + clamp(24px, 6vh, 56px));
  display:flex; flex-direction:column; align-items:flex-end; gap:8px; font-size:12px; font-weight:500; color:#444; pointer-events:none; text-align:end; }
.kh-hint b{ font-size:clamp(20px, 2.2vw, 30px); font-weight:600; color:#000; text-transform:uppercase; letter-spacing:-.02em; line-height:1; }
.kh[lang="ar"] .kh-hint b{ letter-spacing:0; font-weight:700; }
.kh-hint i{ width:1px; height:36px; background:linear-gradient(#000, transparent); animation:kh-drip 1.8s cubic-bezier(.645,.045,.355,1) infinite; transform-origin:top; }
.kh-label{ display:inline-flex; align-items:center; gap:8px; white-space:nowrap; padding:6px 12px 6px 6px; border-radius:999px;
  background:rgba(255,255,255,.92); box-shadow:0 1px 0 rgba(0,0,0,.06); font:600 12px/1 var(--font, 'Inter Tight', system-ui, sans-serif); color:#000; text-transform:uppercase; letter-spacing:.06em; }
.kh[lang="ar"] .kh-label{ letter-spacing:0; font-size:13px; padding:6px 6px 6px 12px; }
.kh-label__idx{ display:grid; place-items:center; width:22px; height:22px; border-radius:50%; background:#000; color:#fff; font:600 10px/1 'Inter Tight', system-ui, sans-serif; letter-spacing:0; }
@keyframes kh-drip{ 0%{ transform:scaleY(0); opacity:1; } 60%{ transform:scaleY(1); opacity:1; } 100%{ transform:scaleY(1); opacity:0; } }

.kh-loader{ position:absolute; z-index:3; top:50%; left:50%; transform:translate(-50%,-50%); display:flex; align-items:center; gap:12px;
  padding:10px 16px 10px 12px; border-radius:999px; background:rgba(255,255,255,.9); font-size:13px; color:#333; pointer-events:none;
  transition:opacity .45s ease; }
.kh-loader.is-done{ opacity:0; }
.kh-loader b{ font-weight:600; font-variant-numeric:tabular-nums; }
.kh-spinner{ width:18px; height:18px; border-radius:50%; border:2px solid #dcdcdc; border-top-color:#000; animation:kh-spin .8s linear infinite; }
@keyframes kh-spin{ to{ transform:rotate(360deg); } }

@media (max-width:767px){
  .kh-ui{ bottom:calc(var(--kh-toolbar) + 24px + env(safe-area-inset-bottom, 0px)); }
  .kh-title{ font-size:clamp(44px, 13vw, 64px); }
}
@media (prefers-reduced-motion: reduce){
  .kh-hint{ display:none; }
  .kh-spinner, .kh-hint i{ animation:none; }
}
`
