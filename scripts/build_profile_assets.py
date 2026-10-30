"""Build the self-contained SVG artwork used by the GitHub profile README.

Animation philosophy (Emil Kowalski / animate skill):
  - GPU-only: transform + opacity. stroke-dashoffset for line-drawing.
  - ease-out  cubic-bezier(0.23, 1, 0.32, 1)  — entrances.
  - ease-in-out cubic-bezier(0.77, 0, 0.175, 1) — on-screen movement.
  - linear — ONLY for constant streams (marquee, data flow, progress).
  - Stagger group entrances 60-80 ms apart.
  - prefers-reduced-motion: keep opacity, drop transform + movement.
  - Never scale(0). Use scale(0.93) + opacity:0.
  - Every animation earns its place: spatial story, state, or delight.

Key visual upgrades:
  - Dot-grid background pattern (visible at a glance, premium feel).
  - Hero scan bar: one-shot sweep plays on load (signature animation).
  - Flowing dashes on connection lines (stroke-dashoffset, linear stream).
  - Diagrams rebuilt with richer visual geometry.
  - Experience: timeline stagger with animated "shipped" status pulse.
"""

from pathlib import Path

ROOT   = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)

FONT  = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
INK   = "#080e15"      # slightly deeper than before
PANEL = "#0d1520"
LINE  = "#1e2d3d"      # cooler blue-grey border
TEXT  = "#dce8f0"
MUTED = "#5a7282"
GREEN = "#5ecba1"      # slightly less saturated — not neon

# ------------------------------------------------------------------
# Easing tokens
# ease-out:    cubic-bezier(0.23, 1, 0.32, 1)
# ease-in-out: cubic-bezier(0.77, 0, 0.175, 1)
# ------------------------------------------------------------------


def save(name: str, body: str, w: int, h: int, title: str, desc: str) -> None:
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="{w}" height="{h}" font-family="{FONT}">'
        f"<title>{title}</title><desc>{desc}</desc>{body}</svg>"
    )
    (ASSETS / name).write_text(svg + "\n", encoding="utf-8")


# ══════════════════════════════════════════════════════════════════
#  HERO
#  Signature: scan bar sweeps once on load, text reveals in its wake.
#  Diagram: flowing dashes on connection lines (constant data stream).
# ══════════════════════════════════════════════════════════════════

hero_css = """
<style>
/* ── DOT GRID subtle breathe (very subtle scale on the whole bg) ──
   Rejected as too distracting. Dot grid is purely static — CSS pattern. */

/* ── SCAN BAR ─────────────────────────────────────────────────────
   One-shot. Plays once with forwards (does not repeat).
   A soft horizontal light band sweeps top-to-bottom of the left panel.
   Purpose: delight / first impression (profile tier, seen once per visit).
   Easing: ease-out — fast start, decelerates. Feels like a scan completing.
   Duration: 1.35s marketing tier. */
@keyframes scan {
  0%   { transform: translateY(-120px); opacity: 0; }
  7%   { opacity: 1; }
  88%  { opacity: 0.9; }
  100% { transform: translateY(370px); opacity: 0; }
}
.scan-bar { animation: scan 1.35s cubic-bezier(0.23,1,0.32,1) 0.2s forwards; }

/* ── TEXT REVEAL ───────────────────────────────────────────────────
   Each line appears just after the scan bar has passed it.
   translateY(6px) → 0, opacity 0→1. ease-out. Never ease-in. */
@keyframes reveal {
  0%   { opacity: 0; transform: translateY(6px); }
  100% { opacity: 1; transform: translateY(0); }
}
.rl  { opacity:0; animation: reveal 0.32s cubic-bezier(0.23,1,0.32,1) 0.32s forwards; }
.rn1 { opacity:0; animation: reveal 0.32s cubic-bezier(0.23,1,0.32,1) 0.58s forwards; }
.rn2 { opacity:0; animation: reveal 0.32s cubic-bezier(0.23,1,0.32,1) 0.72s forwards; }
.rt  { opacity:0; animation: reveal 0.32s cubic-bezier(0.23,1,0.32,1) 0.90s forwards; }

/* ── CURSOR ────────────────────────────────────────────────────────
   step-start is intentional — cursors in terminals blink with no
   easing. Appears after name has settled. */
@keyframes blink {
  0%, 48% { opacity: 1; }
  50%, 100% { opacity: 0; }
}
.cur { opacity:0; animation: blink 1.05s step-start 1.05s infinite; }

/* ── DIAGRAM SLIDE-IN ──────────────────────────────────────────────
   Right panel slides from translateX(16px). ease-out. 500ms. */
@keyframes din {
  0%   { opacity:0; transform: translateX(16px); }
  45%  { opacity:1; transform: translateX(-1px); }
  100% { opacity:1; transform: translateX(0); }
}
.diag { opacity:0; animation: din 0.5s cubic-bezier(0.23,1,0.32,1) 0.25s forwards; }

/* ── NODE POP ─────────────────────────────────────────────────────
   scale(0.93)+opacity:0. Never scale(0). 80ms stagger. ease-out. */
@keyframes npop {
  0%   { opacity:0; transform: scale(0.93); }
  50%  { opacity:1; transform: scale(1.03); }
  75%  { transform: scale(0.99); }
  100% { opacity:1; transform: scale(1); }
}
.n1 { opacity:0; animation: npop 0.38s cubic-bezier(0.23,1,0.32,1) 0.78s forwards; }
.n2 { opacity:0; animation: npop 0.38s cubic-bezier(0.23,1,0.32,1) 0.86s forwards; }
.n3 { opacity:0; animation: npop 0.38s cubic-bezier(0.23,1,0.32,1) 0.94s forwards; }
.n4 { opacity:0; animation: npop 0.38s cubic-bezier(0.23,1,0.32,1) 1.02s forwards; }

/* ── DATA FLOW ─────────────────────────────────────────────────────
   stroke-dashoffset constant stream — linear is CORRECT here.
   This is the "constant motion / marquee" case from the easing table.
   A continuous data stream has no acceleration — it flows uniformly. */
@keyframes fh { from { stroke-dashoffset: 44; } to { stroke-dashoffset: -256; } }
@keyframes fv { from { stroke-dashoffset: 44; } to { stroke-dashoffset: -140; } }
.fh { animation: fh 2.1s linear 1.4s infinite; }
.fv { animation: fv 2.1s linear 1.4s infinite; }

/* ── REDUCED MOTION ────────────────────────────────────────────────
   Keep opacity fades (they aid comprehension). Drop all movement. */
@media (prefers-reduced-motion: reduce) {
  .scan-bar, .cur { display: none; }
  .rl,.rn1,.rn2,.rt { animation: none; opacity: 1; }
  .diag { animation: none; opacity: 1; }
  .n1,.n2,.n3,.n4 { animation: none; opacity: 1; }
  .fh,.fv { display: none; }
}
</style>
"""

# dot-grid background (24px spacing, very subtle)
DOT_GRID = f"""
<defs>
  <pattern id="dots" x="0" y="0" width="24" height="24" patternUnits="userSpaceOnUse">
    <circle cx="0.5" cy="0.5" r="0.8" fill="{LINE}" opacity="0.55"/>
  </pattern>
  <!-- Scan bar gradient: horizontal band with soft falloff -->
  <linearGradient id="scan-g" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%"   stop-color="{GREEN}" stop-opacity="0"/>
    <stop offset="35%"  stop-color="{GREEN}" stop-opacity="0.06"/>
    <stop offset="50%"  stop-color="{GREEN}" stop-opacity="0.20"/>
    <stop offset="65%"  stop-color="{GREEN}" stop-opacity="0.06"/>
    <stop offset="100%" stop-color="{GREEN}" stop-opacity="0"/>
  </linearGradient>
  <!-- Flow dashes gradient for connection lines -->
  <linearGradient id="flow-g" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%"   stop-color="{GREEN}" stop-opacity="0.4"/>
    <stop offset="50%"  stop-color="{GREEN}" stop-opacity="0.9"/>
    <stop offset="100%" stop-color="{GREEN}" stop-opacity="0.4"/>
  </linearGradient>
</defs>
"""

hero = f"""
{hero_css}
{DOT_GRID}

<!-- Base layer -->
<rect width="1000" height="430" rx="18" fill="{INK}"/>
<rect width="1000" height="430" rx="18" fill="url(#dots)"/>
<rect x="1" y="1" width="998" height="428" rx="17" fill="none" stroke="{LINE}" stroke-width="1.5"/>

<!-- Layout dividers -->
<path d="M40 68 H960 M40 365 H960" stroke="{LINE}" stroke-width="1"/>
<path d="M532 68 V365" stroke="{LINE}" stroke-width="1"/>

<!-- Header bar -->
<rect x="40" y="39" width="8" height="8" rx="2" fill="{GREEN}"/>
<text x="58" y="49" font-size="12" font-weight="700" fill="{GREEN}" letter-spacing="1">CODE IT. SHIP IT. IMPROVE IT.</text>
<text x="960" y="49" font-size="11" fill="{MUTED}" text-anchor="end">GANDHINAGAR, INDIA  ·  CSE '27</text>

<!-- SCAN BAR (left panel only, clipped) -->
<clipPath id="left-clip">
  <rect x="40" y="68" width="490" height="297"/>
</clipPath>
<rect class="scan-bar" clip-path="url(#left-clip)"
      x="40" y="68" width="490" height="130"
      fill="url(#scan-g)" opacity="0"/>

<!-- LEFT: text reveals -->
<text class="rl" x="48" y="152" font-size="11" font-weight="700"
      fill="{GREEN}" letter-spacing="4">SOFTWARE ENGINEER</text>

<g fill="{TEXT}" font-size="78" font-weight="800" letter-spacing="-3.5">
  <text class="rn1" x="40" y="252">SHREYASH</text>
  <text class="rn2" x="40" y="335">SHUKLA<tspan fill="{GREEN}">.</tspan></text>
</g>

<!-- cursor: appears after name settles -->
<rect class="cur" x="41" y="345" width="5" height="28" rx="2" fill="{GREEN}"/>

<text class="rt" x="47" y="390" font-size="12" fill="{MUTED}" letter-spacing="0.5">
  CLOUD SYSTEMS  ·  FULL-STACK  ·  APPLIED AI
</text>

<!-- RIGHT: diagram -->
<g class="diag">
  <rect x="553" y="89" width="409" height="254" rx="14" fill="{PANEL}" stroke="{LINE}" stroke-width="1.5"/>

  <!-- Diagram header -->
  <text x="574" y="118" font-size="10" font-weight="700" fill="{GREEN}" letter-spacing="2">SERVERLESS WORKFLOW</text>
  <text x="940" y="118" font-size="10" fill="{MUTED}" text-anchor="end" letter-spacing="1">REQUEST / RESPONSE</text>
  <path d="M574 126 H940" stroke="{LINE}" stroke-width="1"/>

  <!-- Connection paths (dim baseline) -->
  <path d="M607 185 H899 M751 185 V280" fill="none" stroke="{LINE}" stroke-width="2"/>

  <!-- Arrows -->
  <path d="M895 181 L901 185 L895 189 M747 275 L751 281 L755 275"
        fill="none" stroke="{GREEN}" stroke-width="1.8"/>

  <!-- Flowing data streams (stroke-dashoffset, linear = correct for constant flow) -->
  <path class="fh" d="M607 185 H899" fill="none" stroke="{GREEN}" stroke-width="2"
        stroke-dasharray="22 22" stroke-dashoffset="44" opacity="0.7"/>
  <path class="fv" d="M751 185 V280" fill="none" stroke="{GREEN}" stroke-width="2"
        stroke-dasharray="22 22" stroke-dashoffset="44" opacity="0.7"/>

  <text x="574" y="328" font-size="10" fill="{MUTED}" letter-spacing="1">TYPESCRIPT  /  AWS LAMBDA  /  DYNAMODB</text>
</g>

<!-- Nodes (reveal with stagger) -->
<g fill="{INK}" stroke="{GREEN}" stroke-width="1.8">
  <rect class="n1" x="584" y="163" width="68" height="40" rx="9"/>
  <rect class="n2" x="711" y="163" width="80" height="40" rx="9"/>
  <rect class="n3" x="862" y="163" width="76" height="40" rx="9"/>
  <rect class="n4" x="711" y="278" width="80" height="40" rx="9"/>
</g>
<g fill="{TEXT}" font-size="10" font-weight="700" text-anchor="middle" letter-spacing="0.5">
  <text class="n1" x="618" y="188">CLIENT</text>
  <text class="n2" x="751" y="188">LAMBDA</text>
  <text class="n3" x="900" y="188">RESULT</text>
  <text class="n4" x="751" y="303">DATA</text>
</g>
"""

save("hero.svg", hero, 1000, 430,
     "Shreyash Shukla — Software Engineer",
     "Scan bar sweeps once on load, text reveals in its wake, architecture shows flowing data streams.")


# ══════════════════════════════════════════════════════════════════
#  EXPERIENCE
#  4 tool cards stagger in. Animated connector line drawn between them.
#  Status dots pulse to indicate "shipped" state.
# ══════════════════════════════════════════════════════════════════

exp_css = """
<style>
/* Card stagger entrance — translateY(14px) + opacity:0 → settled.
   ease-out baked at 45% keyframe. 70ms stagger between cards. */
@keyframes ce {
  0%   { opacity:0; transform: translateY(14px); }
  45%  { opacity:1; transform: translateY(-1px); }
  100% { opacity:1; transform: translateY(0); }
}
.ec1 { opacity:0; animation: ce 0.38s cubic-bezier(0.23,1,0.32,1) 0.08s forwards; }
.ec2 { opacity:0; animation: ce 0.38s cubic-bezier(0.23,1,0.32,1) 0.15s forwards; }
.ec3 { opacity:0; animation: ce 0.38s cubic-bezier(0.23,1,0.32,1) 0.22s forwards; }
.ec4 { opacity:0; animation: ce 0.38s cubic-bezier(0.23,1,0.32,1) 0.29s forwards; }

/* Status dot: scale pulse — state indication ("shipped/live").
   ease-in-out for on-screen movement. 3.4s loop. Subtle (1→1.5). */
@keyframes dp {
  0%, 100% { transform: scale(1); opacity: 0.55; }
  50%       { transform: scale(1.5); opacity: 1; }
}
.dp { animation: dp 3.4s cubic-bezier(0.77,0,0.175,1) infinite; }

/* Connector line drawing between cards */
@keyframes ld {
  0%   { stroke-dashoffset: 696; opacity: 0; }
  10%  { opacity: 0.5; }
  100% { stroke-dashoffset: 0; opacity: 0.5; }
}
.conn { stroke-dasharray: 696; stroke-dashoffset: 696; opacity: 0;
        animation: ld 0.7s cubic-bezier(0.23,1,0.32,1) 0.08s forwards; }

@media (prefers-reduced-motion: reduce) {
  .ec1,.ec2,.ec3,.ec4 { animation: none; opacity: 1; }
  .dp { animation: none; opacity: 0.8; }
  .conn { animation: none; stroke-dashoffset: 0; opacity: 0.4; }
}
</style>
"""

experience = f"""
{exp_css}
<defs>
  <pattern id="edots" x="0" y="0" width="24" height="24" patternUnits="userSpaceOnUse">
    <circle cx="0.5" cy="0.5" r="0.8" fill="{LINE}" opacity="0.5"/>
  </pattern>
</defs>

<rect width="1000" height="296" rx="18" fill="{INK}"/>
<rect width="1000" height="296" rx="18" fill="url(#edots)"/>
<rect x="1" y="1" width="998" height="294" rx="17" fill="none" stroke="{LINE}" stroke-width="1.5"/>

<text x="42" y="47" font-size="10" font-weight="700" fill="{GREEN}" letter-spacing="2">EXPERIENCE / QUICKO</text>
<text x="958" y="47" font-size="10" fill="{MUTED}" text-anchor="end" letter-spacing="1">MAY–JUNE 2026  ·  AHMEDABAD</text>
<path d="M42 58 H958" stroke="{LINE}" stroke-width="1"/>

<text x="42" y="98" font-size="22" font-weight="700" fill="{TEXT}">Four tools shipped to production.</text>
<text x="42" y="119" font-size="11" fill="{MUTED}">Serverless APIs · data contracts · AWS infrastructure · financial workflows.</text>

<!-- Connector line drawn between card top edges -->
<path class="conn" d="M151 164 H260 M393 164 H502 M625 164 H734" fill="none" stroke="{GREEN}" stroke-width="1"/>
"""

tools_exp = [
    ("01", "PAN",         "Verification",  "ec1", 0.00),
    ("02", "PAN-Aadhaar", "Link Checker",  "ec2", 0.22),
    ("03", "Tax Payment", "Checker",       "ec3", 0.44),
    ("04", "e-Verify",    "ITR",           "ec4", 0.66),
]
for i, (num, first, second, cls, dd) in enumerate(tools_exp):
    x = 42 + 232 * i
    experience += f"""
<g class="{cls}">
  <rect x="{x}" y="148" width="210" height="110" rx="12" fill="{PANEL}" stroke="{LINE}" stroke-width="1.5"/>
  <text x="{x+14}" y="172" font-size="10" fill="{GREEN}" font-weight="700" letter-spacing="1">{num}</text>
  <text x="{x+14}" y="200" font-size="16" font-weight="700" fill="{TEXT}">{first}</text>
  <text x="{x+14}" y="222" font-size="13" fill="{MUTED}">{second}</text>
  <circle class="dp" cx="{x+186}" cy="166" r="3.5" fill="{GREEN}"
          style="transform-origin:{x+186}px 166px; animation-delay:{dd:.2f}s;"/>
</g>
"""

save("experience.svg", experience, 1000, 296,
     "Four financial tools shipped at Quicko",
     "Cards stagger in with ease-out. Connector line draws between them. Status dots pulse.")


# ══════════════════════════════════════════════════════════════════
#  CARD HELPER
# ══════════════════════════════════════════════════════════════════

def card(num, title, kind, stack, accent, diagram_css, diagram_svg, desc):
    return f"""
<style>
{diagram_css}
/* Title + subtitle: staggered ease-out reveal */
@keyframes ti {{
  0%   {{ opacity:0; transform: translateY(7px); }}
  100% {{ opacity:1; transform: translateY(0); }}
}}
.ct {{ opacity:0; animation: ti 0.38s cubic-bezier(0.23,1,0.32,1) 0.06s forwards; }}
.ck {{ opacity:0; animation: ti 0.38s cubic-bezier(0.23,1,0.32,1) 0.14s forwards; }}
@media (prefers-reduced-motion: reduce) {{
  .moving,.flow {{ display: none; }}
  .ldr {{ animation: none; stroke-dashoffset: 0; opacity: 0.4; }}
  .ct,.ck {{ animation: none; opacity: 1; }}
}}
</style>

<defs>
  <pattern id="cdots" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
    <circle cx="0.5" cy="0.5" r="0.7" fill="{LINE}" opacity="0.5"/>
  </pattern>
</defs>

<rect width="490" height="250" rx="15" fill="{INK}"/>
<rect width="490" height="250" rx="15" fill="url(#cdots)"/>
<rect x="1" y="1" width="488" height="248" rx="14" fill="none" stroke="{LINE}" stroke-width="1.5"/>

<!-- accent bar -->
<rect x="22" y="26" width="4" height="20" rx="2" fill="{accent}"/>
<text x="36" y="40" font-size="9" font-weight="700" fill="{accent}" letter-spacing="2">{num} / FEATURED PROJECT</text>

<text class="ct" x="22" y="95" font-size="26" font-weight="800" fill="{TEXT}">{title}</text>
<text class="ck" x="22" y="118" font-size="11" fill="{MUTED}">{kind}</text>
<path d="M22 172 H468" stroke="{LINE}" stroke-width="1"/>
<text x="22" y="203" font-size="10" fill="{accent}" letter-spacing="1">{stack}</text>
<text x="22" y="224" font-size="10" fill="{MUTED}">OPEN PROJECT ↗</text>
{diagram_svg}
"""


# ══════════════════════════════════════════════════════════════════
#  FRAUDSHIELD
#  Graph traversal: signal traces edges with eased movement per segment.
#  Active nodes: pulsing glow (state indication of current computation).
#  Flow: eased movement along graph edges (ease-in-out per segment).
# ══════════════════════════════════════════════════════════════════

fraud_css = """
/* Graph traversal: ease-in-out baked per edge via keyframe % splits.
   Each edge pair of keyframes approximates ease-in-out acceleration.
   Purpose: explanation — demonstrates GNN traversal concept. */
@keyframes trace {
  0%   { opacity:0; transform: translate(0,0); }
  9%   { opacity:1; transform: translate(0,0); }
  /* Edge 1: origin→top-node  (ease-in-out split) */
  20%  { transform: translate(22px,-18px); }
  33%  { transform: translate(55px,-44px); }
  /* Edge 2: top-node→right-node */
  48%  { transform: translate(90px,-22px); }
  62%  { transform: translate(124px,8px); }
  /* Edge 3: right-node→bottom-node */
  76%  { transform: translate(100px,36px); }
  88%  { opacity:1; transform: translate(55px,62px); }
  100% { opacity:0; transform: translate(55px,62px); }
}
/* Node glow: synced with traversal — lights up when signal arrives */
@keyframes ng1 { 0%,12%{opacity:.3}  18%,40%{opacity:1} 50%,100%{opacity:.3} }
@keyframes ng2 { 0%,40%{opacity:.3}  46%,70%{opacity:1} 78%,100%{opacity:.3} }
@keyframes ng3 { 0%,72%{opacity:.3}  78%,96%{opacity:1} 100%{opacity:.3} }
.moving { opacity:0; animation: trace 5.2s cubic-bezier(0.77,0,0.175,1) 0.3s infinite; }
.ng1 { animation: ng1 5.2s cubic-bezier(0.77,0,0.175,1) 0.3s infinite; }
.ng2 { animation: ng2 5.2s cubic-bezier(0.77,0,0.175,1) 0.3s infinite; }
.ng3 { animation: ng3 5.2s cubic-bezier(0.77,0,0.175,1) 0.3s infinite; }
"""

fraud_svg = f"""
<text x="282" y="62" font-size="9" font-weight="700" fill="{GREEN}" letter-spacing="2">GRAPH + MODEL</text>
<path d="M294 126 L349 82 L418 134 L349 188 Z M294 126 L418 134 M349 82 V188"
      fill="none" stroke="{LINE}" stroke-width="2"/>
<!-- Traversal signal -->
<circle class="moving" cx="294" cy="126" r="5" fill="{GREEN}"/>
<!-- Node rings -->
<g fill="{INK}" stroke="{GREEN}" stroke-width="2">
  <circle cx="294" cy="126" r="13"/><circle cx="349" cy="82" r="13"/>
  <circle cx="418" cy="134" r="13"/><circle cx="349" cy="188" r="13"/>
</g>
<!-- Active indicators (glow dots synced with signal) -->
<circle class="ng1" cx="349" cy="82"  r="4" fill="{GREEN}" opacity="0.3"/>
<circle class="ng2" cx="418" cy="134" r="4" fill="{GREEN}" opacity="0.3"/>
<circle class="ng3" cx="349" cy="188" r="4" fill="{GREEN}" opacity="0.3"/>
"""

save("card-fraudshield.svg",
     card("01", "FraudShield", "Graph-based fraud detection",
          "FASTAPI  ·  XGBOOST  ·  GNN", GREEN, fraud_css, fraud_svg, "Fraud detection"),
     490, 250, "FraudShield project",
     "Graph traversal signal traces edges. Nodes glow when the signal arrives.")


# ══════════════════════════════════════════════════════════════════
#  TRUSTCHAIN
#  Connector line draws left-to-right (stroke-dashoffset, ease-out).
#  Checkmarks reveal sequentially with scale(0.93) → scale(1).
#  Purpose: state indication — pipeline stages completing in order.
# ══════════════════════════════════════════════════════════════════

trust_accent = "#d4a84b"  # warm gold, not neon

trust_css = f"""
/* Connector line draw: ease-out (information appears, completes quickly).
   stroke-dashoffset 0 → full. One-shot with forwards. */
@keyframes ld {{
  0%   {{ stroke-dashoffset: 108; opacity:0; }}
  12%  {{ opacity:0.5; }}
  100% {{ stroke-dashoffset: 0; opacity:0.5; }}
}}
/* Checkmark reveal: scale(0.93)+opacity:0 → scale(1). ease-out. 80ms stagger. */
@keyframes cr {{
  0%   {{ opacity:0; transform: scale(0.93); }}
  50%  {{ opacity:1; transform: scale(1.05); }}
  100% {{ opacity:1; transform: scale(1); }}
}}
.ldr {{ stroke-dasharray:108; stroke-dashoffset:108; opacity:0;
  animation: ld 0.55s cubic-bezier(0.23,1,0.32,1) 0.10s forwards; }}
.v1 {{ opacity:0; animation: cr 0.32s cubic-bezier(0.23,1,0.32,1) 0.20s forwards; }}
.v2 {{ opacity:0; animation: cr 0.32s cubic-bezier(0.23,1,0.32,1) 0.38s forwards; }}
.v3 {{ opacity:0; animation: cr 0.32s cubic-bezier(0.23,1,0.32,1) 0.56s forwards; }}
"""

trust_svg = f"""
<text x="280" y="170" font-size="9" fill="{trust_accent}" font-weight="700" letter-spacing="2">VERIFY  ·  ATTEST  ·  TRUST</text>
<path class="ldr" d="M310 127 H418" fill="none" stroke="{trust_accent}" stroke-width="2"/>
<g fill="{INK}" stroke="{trust_accent}" stroke-width="2">
  <rect x="288" y="105" width="44" height="44" rx="10"/>
  <rect x="342" y="105" width="44" height="44" rx="10"/>
  <rect x="396" y="105" width="44" height="44" rx="10"/>
</g>
<g class="v1" fill="none" stroke="{trust_accent}" stroke-width="3"
   stroke-linecap="round" stroke-linejoin="round" style="transform-origin:310px 127px;">
  <path d="M299 127 l7 7 12-15"/>
</g>
<g class="v2" fill="none" stroke="{trust_accent}" stroke-width="3"
   stroke-linecap="round" stroke-linejoin="round" style="transform-origin:364px 127px;">
  <path d="M353 127 l7 7 12-15"/>
</g>
<g class="v3" fill="none" stroke="{trust_accent}" stroke-width="3"
   stroke-linecap="round" stroke-linejoin="round" style="transform-origin:418px 127px;">
  <path d="M407 127 l7 7 12-15"/>
</g>
"""

save("card-trustchain.svg",
     card("02", "TrustChain", "Layered fraud prevention",
          "SOLIDITY  ·  FASTAPI  ·  VISION", trust_accent, trust_css, trust_svg, "Fraud prevention"),
     490, 250, "TrustChain project",
     "Connector line draws, then checkmarks reveal sequentially.")


# ══════════════════════════════════════════════════════════════════
#  DAGENT
#  Token traverses DAG with ease-in-out per edge (waypoints).
#  Active node 2 pulses while token is in transit — state indication.
# ══════════════════════════════════════════════════════════════════

dag_accent = "#8b7cf6"  # muted purple, not neon

dag_css = """
@keyframes route {
  0%   { opacity:0; transform: translate(0,0); }
  11%  { opacity:1; transform: translate(0,0); }
  /* Edge 1 → node 2 (ease-in-out) */
  24%  { transform: translate(24px,-18px); }
  40%  { transform: translate(61px,-42px); }
  /* Edge 2 → node 4 (ease-in-out) */
  56%  { transform: translate(95px,-18px); }
  72%  { transform: translate(131px,0); opacity:1; }
  90%  { opacity:0.2; }
  100% { transform: translate(131px,0); opacity:0; }
}
@keyframes ta {
  0%,100% { transform: scale(1); opacity:0.4; }
  50%      { transform: scale(1.2); opacity:1; }
}
.moving      { opacity:0; animation: route 5.2s cubic-bezier(0.77,0,0.175,1) 0.4s infinite; }
.active-node { animation: ta 5.2s cubic-bezier(0.77,0,0.175,1) 0.4s infinite;
               transform-origin: 353px 86px; }
"""

dag_svg = f"""
<path d="M292 128 L353 86 L423 128 L353 170 Z M353 86 V170"
      fill="none" stroke="{LINE}" stroke-width="2"/>
<circle class="moving" cx="292" cy="128" r="5" fill="{dag_accent}"/>
<g fill="{INK}" stroke="{dag_accent}" stroke-width="2">
  <circle cx="292" cy="128" r="13"/>
  <circle cx="353" cy="86"  r="13"/>
  <circle cx="353" cy="170" r="13"/>
  <circle cx="423" cy="128" r="13"/>
</g>
<g fill="{dag_accent}" font-size="11" font-weight="700" text-anchor="middle">
  <text x="292" y="132">1</text>
  <text class="active-node" x="353" y="90">2</text>
  <text x="353" y="174">3</text>
  <text x="423" y="132">4</text>
</g>
"""

save("card-dagent.svg",
     card("03", "DAGent", "Agent workflow orchestration",
          "NEXT.JS  ·  TYPESCRIPT  ·  MCP", dag_accent, dag_css, dag_svg, "DAG orchestration"),
     490, 250, "DAGent project",
     "Token routes through DAG nodes with eased movement. Active node pulses.")


# ══════════════════════════════════════════════════════════════════
#  DRIVEMESH
#  Flowing dashes on both replication paths (stroke-dashoffset, linear).
#  Linear = CORRECT: constant data stream, uniform flow rate.
#  Two separate dash offsets on each path create independent streams.
# ══════════════════════════════════════════════════════════════════

drive_accent = "#4fa3c7"  # calm blue, not neon

drive_css = """
/* Constant replication stream — linear is correct (marquee/data flow case). */
@keyframes rh1 { from { stroke-dashoffset: 44; } to { stroke-dashoffset: -94; } }
@keyframes rh2 { from { stroke-dashoffset: 44; } to { stroke-dashoffset: -94; } }
.flow1 { animation: rh1 2s linear 0.3s infinite; }
.flow2 { animation: rh2 2s linear -1.0s infinite; }
/* ENC box: subtle beat indicating active encryption */
@keyframes enc-pulse {
  0%,100% { opacity: 0.7; }
  50%      { opacity: 1; }
}
.enc { animation: enc-pulse 2s cubic-bezier(0.77,0,0.175,1) infinite; }
"""

drive_svg = f"""
<path d="M319 90 H413 M319 159 H413" stroke="{LINE}" stroke-width="2"/>
<path d="M407 86 L413 90 L407 94 M407 155 L413 159 L407 163"
      fill="none" stroke="{drive_accent}" stroke-width="2"/>
<!-- Flowing dashes on both paths -->
<path class="flow1" d="M319 90 H413" fill="none" stroke="{drive_accent}" stroke-width="2"
      stroke-dasharray="18 26" stroke-dashoffset="44" opacity="0.8"/>
<path class="flow2" d="M319 159 H413" fill="none" stroke="{drive_accent}" stroke-width="2"
      stroke-dasharray="18 26" stroke-dashoffset="44" opacity="0.8"/>
<!-- Nodes -->
<g fill="{INK}" stroke="{drive_accent}" stroke-width="2">
  <rect class="enc" x="278" y="105" width="49" height="39" rx="7"/>
  <rect x="412" y="72"  width="45" height="36" rx="7"/>
  <rect x="412" y="141" width="45" height="36" rx="7"/>
</g>
<g fill="{drive_accent}" font-size="10" font-weight="700" text-anchor="middle" letter-spacing="0.5">
  <text x="302" y="129">ENC</text>
  <text x="434" y="95">N1</text>
  <text x="434" y="164">N2</text>
</g>
"""

save("card-drivemesh.svg",
     card("04", "DriveMesh", "Encrypted distributed storage",
          "PYTHON  ·  FLASK  ·  FERNET", drive_accent, drive_css, drive_svg, "Distributed storage"),
     490, 250, "DriveMesh project",
     "Flowing dashes stream from ENC to storage nodes — constant replication.")


print("Built 6 SVG assets — visual redesign complete.")
print("Key changes: dot-grid bg, scan-bar hero, stroke-dashoffset data flows, node glow sync.")
