"""Build the self-contained SVG artwork used by the GitHub profile README.

Animation philosophy (Emil Kowalski / animate skill):
  - Animate transform + opacity only (GPU path).
  - ease-out for entrances, ease-in-out for on-screen movement, never linear on UI.
  - Durations: signals 300-600ms per phase; decorative loops stay under 4s per beat.
  - Stagger group entrances 40-80ms apart.
  - prefers-reduced-motion: keep opacity fade, drop transform motion.
  - No scale(0) -- start from scale(0.93)+opacity:0.
  - Every animation earns its place: spatial story, state indication, or delight.
"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)

FONT = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
INK   = "#0b1118"
PANEL = "#111a22"
LINE  = "#2c3a43"
TEXT  = "#edf4ef"
MUTED = "#9baeb0"
GREEN = "#75e2b8"

# Easing tokens (from animate skill STANDARDS)
# ease-out:    cubic-bezier(0.23, 1, 0.32, 1)   strong ease-out for entrances
# ease-in-out: cubic-bezier(0.77, 0, 0.175, 1)  strong ease-in-out for on-screen movement


def save(name: str, body: str, width: int, height: int, title: str, description: str) -> None:
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" font-family="{FONT}">'
        f"<title>{title}</title><desc>{description}</desc>{body}</svg>"
    )
    (ASSETS / name).write_text(svg + "\n", encoding="utf-8")


# ---- HERO -----------------------------------------------------------------
# Signature animation: name reveals with staggered ease-out slide-in,
# a terminal cursor blinks after the name settles,
# workflow nodes materialise in sequence (spatial story).
# Purpose: delight + spatial story (marketing/profile tier — seen rarely).
# Tool: CSS animation (runs off main thread, predetermined motion).
hero_css = """
<style>
/* Cursor blink — signature animation, step timing is intentional */
@keyframes blink {
  0%, 49% { opacity: 1; }
  50%, 100% { opacity: 0; }
}
.cursor { animation: blink 1.1s step-start 0.9s infinite; }

/* Name reveal: ease-out baked into % splits (fast settle at 38%) */
/* Purpose: preventing jarring appearance. Properties: opacity + translateY. */
@keyframes reveal-name {
  0%   { opacity: 0; transform: translateY(18px); }
  38%  { opacity: 1; transform: translateY(0); }
  100% { opacity: 1; transform: translateY(0); }
}
.name-1  { opacity: 0; animation: reveal-name 0.55s cubic-bezier(0.23, 1, 0.32, 1) 0.15s forwards; }
.name-2  { opacity: 0; animation: reveal-name 0.55s cubic-bezier(0.23, 1, 0.32, 1) 0.28s forwards; }
.tagline { opacity: 0; animation: reveal-name 0.50s cubic-bezier(0.23, 1, 0.32, 1) 0.44s forwards; }

/* Node reveal: scale(0.93)+opacity:0 -> scale(1). Never scale(0). */
/* Stagger 80ms per node. */
@keyframes node-in {
  0%   { opacity: 0; transform: scale(0.93); }
  40%  { opacity: 1; transform: scale(1.02); }
  65%  { transform: scale(0.99); }
  100% { opacity: 1; transform: scale(1); }
}
.node-1 { opacity: 0; animation: node-in 0.42s cubic-bezier(0.23, 1, 0.32, 1) 0.70s forwards; }
.node-2 { opacity: 0; animation: node-in 0.42s cubic-bezier(0.23, 1, 0.32, 1) 0.78s forwards; }
.node-3 { opacity: 0; animation: node-in 0.42s cubic-bezier(0.23, 1, 0.32, 1) 0.86s forwards; }
.node-4 { opacity: 0; animation: node-in 0.42s cubic-bezier(0.23, 1, 0.32, 1) 0.94s forwards; }

/* Signal: ease-in-out baked as % splits (slow start, fast mid, slow arrival) */
/* Purpose: state indication — data in transit. Not linear. */
@keyframes pulse-h {
  0%   { opacity: 0; transform: translateX(0); }
  8%   { opacity: 1; transform: translateX(0); }
  30%  { transform: translateX(55px); }
  70%  { transform: translateX(165px); }
  92%  { opacity: 1; transform: translateX(218px); }
  100% { opacity: 0; transform: translateX(218px); }
}
@keyframes pulse-v {
  0%, 26% { opacity: 0; transform: translateY(0); }
  34%  { opacity: 1; transform: translateY(0); }
  58%  { transform: translateY(50px); }
  88%  { opacity: 1; transform: translateY(95px); }
  100% { opacity: 0; transform: translateY(95px); }
}
.signal-h { opacity: 0; animation: pulse-h 5s cubic-bezier(0.77, 0, 0.175, 1) 1.2s infinite; }
.signal-v { opacity: 0; animation: pulse-v 5s cubic-bezier(0.77, 0, 0.175, 1) 1.2s infinite; }

/* Diagram panel slides in from right */
@keyframes panel-in {
  0%   { opacity: 0; transform: translateX(16px); }
  42%  { opacity: 1; transform: translateX(-2px); }
  100% { opacity: 1; transform: translateX(0); }
}
.diagram-panel { opacity: 0; animation: panel-in 0.55s cubic-bezier(0.23, 1, 0.32, 1) 0.5s forwards; }

/* Reduced motion: keep opacity fades, drop all transforms */
@media (prefers-reduced-motion: reduce) {
  .signal-h, .signal-v, .cursor { display: none; }
  .name-1, .name-2, .tagline { animation: none; opacity: 1; }
  .node-1, .node-2, .node-3, .node-4 { animation: none; opacity: 1; }
  .diagram-panel { animation: none; opacity: 1; }
}
</style>
"""

hero = f"""
{hero_css}
<rect width="1000" height="430" rx="18" fill="{INK}"/>
<rect x="1" y="1" width="998" height="428" rx="17" fill="none" stroke="{LINE}"/>
<path d="M40 68 H960 M40 365 H960" stroke="{LINE}"/>
<path d="M532 68 V365" stroke="{LINE}"/>
<rect x="40" y="42" width="8" height="8" rx="2" fill="{GREEN}"/>
<text x="58" y="50" font-size="13" font-weight="700" fill="{GREEN}">CODE IT. SHIP IT. IMPROVE IT.</text>
<text x="960" y="50" font-size="12" fill="{MUTED}" text-anchor="end">GANDHINAGAR, INDIA  ·  CSE '27</text>

<text x="48" y="157" font-size="18" letter-spacing="3" fill="{GREEN}">SOFTWARE ENGINEER</text>
<g fill="{TEXT}" font-size="73" font-weight="800" letter-spacing="-3">
  <text class="name-1" x="43" y="246">SHREYASH</text>
  <text class="name-2" x="43" y="323">SHUKLA<tspan fill="{GREEN}">.</tspan></text>
</g>
<rect class="cursor" x="44" y="333" width="4" height="26" rx="2" fill="{GREEN}"/>
<text class="tagline" x="47" y="392" font-size="13" fill="{MUTED}">CLOUD SYSTEMS  /  FULL-STACK PRODUCTS  /  APPLIED AI</text>

<g class="diagram-panel">
  <rect x="555" y="91" width="405" height="250" rx="14" fill="{PANEL}" stroke="{LINE}"/>
  <text x="576" y="123" font-size="12" font-weight="700" fill="{GREEN}">SERVERLESS WORKFLOW</text>
  <text x="938" y="123" font-size="11" fill="{MUTED}" text-anchor="end">REQUEST / RESPONSE</text>
  <path d="M605 183 H901 M751 183 V278" fill="none" stroke="#49605f" stroke-width="2"/>
  <path d="M897 179 L903 183 L897 187 M747 273 L751 279 L755 273" fill="none" stroke="{GREEN}" stroke-width="2"/>
</g>
<circle class="signal-h" cx="635" cy="183" r="5" fill="{GREEN}"/>
<circle class="signal-v" cx="751" cy="183" r="5" fill="{GREEN}"/>
<g fill="{INK}" stroke="{GREEN}" stroke-width="2">
  <rect class="node-1" x="584" y="162" width="70" height="42" rx="9"/>
  <rect class="node-2" x="711" y="162" width="80" height="42" rx="9"/>
  <rect class="node-3" x="863" y="162" width="76" height="42" rx="9"/>
  <rect class="node-4" x="711" y="278" width="80" height="42" rx="9"/>
</g>
<g fill="{TEXT}" font-size="11" font-weight="700" text-anchor="middle">
  <text class="node-1" x="619" y="188">CLIENT</text>
  <text class="node-2" x="751" y="188">LAMBDA</text>
  <text class="node-3" x="901" y="188">RESULT</text>
  <text class="node-4" x="751" y="304">DATA</text>
</g>
<text x="576" y="332" font-size="11" fill="{MUTED}">TYPESCRIPT  /  AWS LAMBDA  /  DYNAMODB</text>
"""
save(
    "hero.svg",
    hero,
    1000,
    430,
    "Shreyash Shukla — Software Engineer",
    "Name reveals with staggered ease-out, cursor blinks, workflow nodes materialise in sequence.",
)


# ---- EXPERIENCE ------------------------------------------------------------
# Previously: 4 cards appeared atomically (jarring change, zero animation).
# Now: stagger-in from translateY(12px)+opacity:0, 70ms between cards.
# Purpose: preventing jarring change. Frequency: rare (profile visitors).
# Also: status dot pulses subtly to indicate "live / shipped" state.
experience_css = """
<style>
@keyframes card-enter {
  0%   { opacity: 0; transform: translateY(12px); }
  45%  { opacity: 1; transform: translateY(-1px); }
  100% { opacity: 1; transform: translateY(0); }
}
.ec1 { opacity: 0; animation: card-enter 0.4s cubic-bezier(0.23, 1, 0.32, 1) 0.10s forwards; }
.ec2 { opacity: 0; animation: card-enter 0.4s cubic-bezier(0.23, 1, 0.32, 1) 0.17s forwards; }
.ec3 { opacity: 0; animation: card-enter 0.4s cubic-bezier(0.23, 1, 0.32, 1) 0.24s forwards; }
.ec4 { opacity: 0; animation: card-enter 0.4s cubic-bezier(0.23, 1, 0.32, 1) 0.31s forwards; }
/* Status dot: state indication — "shipped" pulse. Subtle scale, ease-in-out. */
@keyframes dot-pulse {
  0%, 100% { transform: scale(1); opacity: 0.65; }
  50%       { transform: scale(1.4); opacity: 1; }
}
.dot { animation: dot-pulse 3.5s cubic-bezier(0.77, 0, 0.175, 1) infinite; }
@media (prefers-reduced-motion: reduce) {
  .ec1, .ec2, .ec3, .ec4 { animation: none; opacity: 1; }
  .dot { animation: none; opacity: 1; }
}
</style>
"""

experience = f"""
{experience_css}
<rect width="1000" height="296" rx="18" fill="{INK}"/>
<rect x="1" y="1" width="998" height="294" rx="17" fill="none" stroke="{LINE}"/>
<text x="42" y="51" font-size="13" font-weight="700" fill="{GREEN}">EXPERIENCE / QUICKO</text>
<text x="958" y="51" font-size="12" fill="{MUTED}" text-anchor="end">MAY–JUNE 2026  ·  AHMEDABAD</text>
<path d="M42 69 H958" stroke="{LINE}"/>
<text x="42" y="111" font-size="24" font-weight="700" fill="{TEXT}">Four tools shipped to production.</text>
<text x="42" y="135" font-size="12" fill="{MUTED}">Serverless APIs, data contracts, and infrastructure behind financial workflows.</text>
"""

tools = [
    ("01", "PAN", "Verification",       "ec1", 0.0),
    ("02", "PAN–Aadhaar", "Link Checker", "ec2", 0.22),
    ("03", "Tax Payment", "Checker",      "ec3", 0.44),
    ("04", "e-Verify", "ITR",             "ec4", 0.66),
]
for i, (number, first, second, cls, dot_delay) in enumerate(tools):
    x = 42 + 232 * i
    experience += f"""
<g class="{cls}">
  <rect x="{x}" y="164" width="218" height="92" rx="12" fill="{PANEL}" stroke="{LINE}"/>
  <text x="{x+17}" y="191" font-size="13" fill="{GREEN}">{number}</text>
  <text x="{x+17}" y="218" font-size="16" font-weight="700" fill="{TEXT}">{first}</text>
  <text x="{x+17}" y="239" font-size="15" fill="{MUTED}">{second}</text>
  <circle class="dot" cx="{x+191}" cy="185" r="4" fill="{GREEN}"
          style="transform-origin: {x+191}px 185px; animation-delay: {dot_delay:.2f}s;"/>
</g>
"""
save(
    "experience.svg",
    experience,
    1000,
    296,
    "Four financial tools shipped at Quicko",
    "PAN Verification, PAN–Aadhaar Link Checker, Tax Payment Checker, e-Verify ITR — cards stagger in.",
)


# ---- CARD HELPER ----------------------------------------------------------
# Each card title reveals with ease-out from translateY(8px)+opacity:0.
# Purpose: preventing jarring change on first impression (marketing tier).
def card(number: str, title: str, kind: str, stack: str, accent: str, diagram: str, motion: str, description: str) -> str:
    return f"""
<style>
{motion}
/* Card title reveal: ease-out entrance, 400ms. Marketing budget. */
@keyframes title-in {{
  0%   {{ opacity: 0; transform: translateY(8px); }}
  50%  {{ opacity: 1; transform: translateY(-1px); }}
  100% {{ opacity: 1; transform: translateY(0); }}
}}
.card-title {{ opacity: 0; animation: title-in 0.4s cubic-bezier(0.23, 1, 0.32, 1) 0.05s forwards; }}
.card-kind  {{ opacity: 0; animation: title-in 0.4s cubic-bezier(0.23, 1, 0.32, 1) 0.13s forwards; }}
@media (prefers-reduced-motion: reduce) {{
  .moving {{ display: none; }}
  .connector {{ animation: none; stroke-dashoffset: 0; opacity: 0.4; }}
  .card-title, .card-kind {{ animation: none; opacity: 1; }}
}}
</style>
<rect width="490" height="250" rx="15" fill="{INK}"/>
<rect x="1" y="1" width="488" height="248" rx="14" fill="none" stroke="{LINE}"/>
<rect x="23" y="28" width="5" height="18" rx="2.5" fill="{accent}"/>
<text x="39" y="41" font-size="11" font-weight="700" fill="{accent}">{number} / FEATURED PROJECT</text>
<text class="card-title" x="25" y="98" font-size="28" font-weight="800" fill="{TEXT}">{title}</text>
<text class="card-kind" x="25" y="125" font-size="12" fill="{MUTED}">{kind}</text>
<path d="M25 177 H465" stroke="{LINE}"/>
<text x="25" y="209" font-size="11" fill="{accent}">{stack}</text>
<text x="25" y="230" font-size="11" fill="{MUTED}">OPEN PROJECT ↗</text>
{diagram}
"""


# ---- FRAUDSHIELD -----------------------------------------------------------
# Signal traces graph edges with ease-in-out baked into % splits.
# Purpose: explanation — demonstrates the GNN traversal concept.
# Active node pulses: state indication of current computation target.
fraud_motion = """
@keyframes trace {
  0%   { opacity: 0; transform: translate(0, 0); }
  10%  { opacity: 1; transform: translate(0, 0); }
  22%  { transform: translate(20px, -16px); }
  33%  { transform: translate(55px, -44px); }
  50%  { transform: translate(90px, -18px); }
  66%  { transform: translate(124px, 8px); }
  78%  { transform: translate(100px, 36px); }
  88%  { opacity: 1; transform: translate(55px, 62px); }
  100% { opacity: 0; transform: translate(55px, 62px); }
}
@keyframes node-glow {
  0%, 100% { opacity: 0.35; }
  50%       { opacity: 1; }
}
.moving { opacity: 0; animation: trace 5.5s cubic-bezier(0.77, 0, 0.175, 1) 0.3s infinite; }
.node-active { animation: node-glow 5.5s cubic-bezier(0.77, 0, 0.175, 1) 0.3s infinite; }
"""
fraud_diagram = f"""
<path d="M294 126 L349 82 L418 134 L349 188 Z M294 126 L418 134 M349 82 V188"
      fill="none" stroke="#405a54" stroke-width="1.5"/>
<circle class="moving" cx="294" cy="126" r="5" fill="{GREEN}"/>
<g fill="{INK}" stroke="{GREEN}" stroke-width="2">
  <circle cx="294" cy="126" r="12"/>
  <circle cx="349" cy="82"  r="12"/>
  <circle cx="418" cy="134" r="12"/>
  <circle cx="349" cy="188" r="12"/>
</g>
<circle class="node-active" cx="349" cy="82"  r="4" fill="{GREEN}"/>
<circle class="node-active" cx="418" cy="134" r="4" fill="{GREEN}" style="animation-delay: -1.8s;"/>
<text x="300" y="63" font-size="11" font-weight="700" fill="{GREEN}">GRAPH + MODEL</text>
"""
save(
    "card-fraudshield.svg",
    card("01", "FraudShield", "Fraud detection across transactions",
         "FASTAPI  /  XGBOOST  /  GNN", GREEN, fraud_diagram, fraud_motion, "Fraud detection"),
    490, 250, "FraudShield project", "A graph-based fraud detection project and HackNUthon winner.",
)


# ---- TRUSTCHAIN ------------------------------------------------------------
# Connector line draws left-to-right, then checkmarks reveal one by one.
# Purpose: state indication — each verification layer passes in sequence.
# Check icons: scale(0.93)+opacity:0 entrance, 80ms stagger. ease-out.
trust_accent = "#f4c97e"
trust_motion = f"""
@keyframes check-reveal {{
  0%   {{ opacity: 0; transform: scale(0.93); }}
  45%  {{ opacity: 1; transform: scale(1.04); }}
  100% {{ opacity: 1; transform: scale(1); }}
}}
@keyframes line-draw {{
  0%   {{ stroke-dashoffset: 108; opacity: 0; }}
  15%  {{ opacity: 1; }}
  80%  {{ stroke-dashoffset: 0; }}
  100% {{ stroke-dashoffset: 0; opacity: 1; }}
}}
.v1        {{ opacity: 0; animation: check-reveal 0.35s cubic-bezier(0.23, 1, 0.32, 1) 0.20s forwards; }}
.v2        {{ opacity: 0; animation: check-reveal 0.35s cubic-bezier(0.23, 1, 0.32, 1) 0.38s forwards; }}
.v3        {{ opacity: 0; animation: check-reveal 0.35s cubic-bezier(0.23, 1, 0.32, 1) 0.56s forwards; }}
.connector {{ stroke-dasharray: 108; stroke-dashoffset: 108; opacity: 0;
  animation: line-draw 0.55s cubic-bezier(0.23, 1, 0.32, 1) 0.10s forwards; }}
"""
trust_diagram = f"""
<path class="connector" d="M310 127 H418" fill="none" stroke="{trust_accent}" stroke-width="1.5"/>
<g fill="{INK}" stroke="{trust_accent}" stroke-width="2">
  <rect x="288" y="105" width="44" height="44" rx="10"/>
  <rect x="342" y="105" width="44" height="44" rx="10"/>
  <rect x="396" y="105" width="44" height="44" rx="10"/>
</g>
<g class="v1" fill="none" stroke="{trust_accent}" stroke-width="3"
   stroke-linecap="round" stroke-linejoin="round"
   style="transform-origin: 310px 127px;">
  <path d="M300 127 l7 7 12 -15"/>
</g>
<g class="v2" fill="none" stroke="{trust_accent}" stroke-width="3"
   stroke-linecap="round" stroke-linejoin="round"
   style="transform-origin: 364px 127px;">
  <path d="M354 127 l7 7 12 -15"/>
</g>
<g class="v3" fill="none" stroke="{trust_accent}" stroke-width="3"
   stroke-linecap="round" stroke-linejoin="round"
   style="transform-origin: 418px 127px;">
  <path d="M408 127 l7 7 12 -15"/>
</g>
<text x="306" y="170" font-size="11" fill="{trust_accent}">VERIFY  /  ATTEST  /  TRUST</text>
"""
save(
    "card-trustchain.svg",
    card("02", "TrustChain", "Layered fraud prevention",
         "SOLIDITY  /  FASTAPI  /  VISION", trust_accent, trust_diagram, trust_motion,
         "Layered fraud prevention"),
    490, 250, "TrustChain project", "A layered verification project and Breach 2025 runner-up.",
)


# ---- DAGENT ----------------------------------------------------------------
# Task token routes through DAG nodes with ease-in-out movement per edge.
# Purpose: explanation — shows orchestration flow between agent steps.
# Active node 2 pulses: state indication of current task execution.
dag_accent = "#b9adff"
dag_motion = """
@keyframes route {
  0%   { opacity: 0; transform: translate(0, 0); }
  12%  { opacity: 1; transform: translate(0, 0); }
  25%  { transform: translate(25px, -18px); }
  40%  { transform: translate(61px, -42px); }
  57%  { transform: translate(96px, -18px); }
  75%  { transform: translate(131px, 0); opacity: 1; }
  90%  { opacity: 0.2; }
  100% { transform: translate(131px, 0); opacity: 0; }
}
@keyframes task-active {
  0%, 100% { transform: scale(1); opacity: 0.45; }
  50%       { transform: scale(1.18); opacity: 1; }
}
.moving      { opacity: 0; animation: route 5.5s cubic-bezier(0.77, 0, 0.175, 1) 0.4s infinite; }
.active-node { animation: task-active 5.5s cubic-bezier(0.77, 0, 0.175, 1) 0.4s infinite;
               transform-origin: 353px 86px; }
"""
dag_diagram = f"""
<path d="M292 128 L353 86 L423 128 L353 170 Z M353 86 V170"
      fill="none" stroke="#514b71" stroke-width="1.5"/>
<circle class="moving" cx="292" cy="128" r="5" fill="{dag_accent}"/>
<g fill="{INK}" stroke="{dag_accent}" stroke-width="2">
  <circle cx="292" cy="128" r="13"/>
  <circle cx="353" cy="86"  r="13"/>
  <circle cx="353" cy="170" r="13"/>
  <circle cx="423" cy="128" r="13"/>
</g>
<g fill="{dag_accent}" font-size="12" font-weight="700" text-anchor="middle">
  <text x="292" y="132">1</text>
  <text class="active-node" x="353" y="90">2</text>
  <text x="353" y="174">3</text>
  <text x="423" y="132">4</text>
</g>
"""
save(
    "card-dagent.svg",
    card("03", "DAGent", "Agent workflow orchestration",
         "NEXT.JS  /  TYPESCRIPT  /  MCP", dag_accent, dag_diagram, dag_motion,
         "Agent workflow orchestration"),
    490, 250, "DAGent project", "A directed workflow for coordinating AI agents and MCP tools.",
)


# ---- DRIVEMESH -------------------------------------------------------------
# Two replication packets travel from ENC node to storage nodes — offset timing.
# Purpose: explanation — shows redundant replication to multiple nodes.
# ease-in-out baked per % splits. Second dot starts at -2.5s offset (half cycle).
drive_accent = "#8fd0e8"
drive_motion = """
@keyframes replicate {
  0%, 16%  { opacity: 0; transform: translateX(0); }
  26%  { opacity: 1; transform: translateX(0); }
  55%  { transform: translateX(48px); }
  82%  { opacity: 1; transform: translateX(94px); }
  96%  { opacity: 0; transform: translateX(94px); }
  100% { opacity: 0; transform: translateX(94px); }
}
.moving        { opacity: 0; animation: replicate 5s cubic-bezier(0.77, 0, 0.175, 1) 0.3s infinite; }
.moving-offset { opacity: 0; animation: replicate 5s cubic-bezier(0.77, 0, 0.175, 1) -2.5s infinite; }
"""
drive_diagram = f"""
<path d="M319 90 H413 M319 159 H413" stroke="#4a6570" stroke-width="1.5"/>
<path d="M407 86 L413 90 L407 94 M407 155 L413 159 L407 163"
      fill="none" stroke="{drive_accent}" stroke-width="2"/>
<circle class="moving"        cx="318" cy="90"  r="4.5" fill="{drive_accent}"/>
<circle class="moving-offset" cx="318" cy="159" r="4.5" fill="{drive_accent}"/>
<g fill="{INK}" stroke="{drive_accent}" stroke-width="2">
  <rect x="278" y="105" width="49" height="39" rx="7"/>
  <rect x="412" y="72"  width="45" height="36" rx="7"/>
  <rect x="412" y="141" width="45" height="36" rx="7"/>
</g>
<g fill="{drive_accent}" font-size="11" text-anchor="middle">
  <text x="302" y="129">ENC</text>
  <text x="434" y="95">01</text>
  <text x="434" y="164">02</text>
</g>
"""
save(
    "card-drivemesh.svg",
    card("04", "DriveMesh", "Encrypted distributed storage",
         "PYTHON  /  FLASK  /  FERNET", drive_accent, drive_diagram, drive_motion,
         "Encrypted distributed storage"),
    490, 250, "DriveMesh project", "Encrypted data replicated across storage nodes.",
)

print("Built 6 self-contained SVG assets with choreographed animations.")
