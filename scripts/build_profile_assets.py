"""Build the self-contained SVG artwork used by the GitHub profile README."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)

FONT = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
INK = "#0b1118"
PANEL = "#111a22"
LINE = "#2c3a43"
TEXT = "#edf4ef"
MUTED = "#9baeb0"
GREEN = "#75e2b8"


def save(name: str, body: str, width: int, height: int, title: str, description: str) -> None:
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" font-family="{FONT}">'
        f"<title>{title}</title><desc>{description}</desc>{body}</svg>"
    )
    (ASSETS / name).write_text(svg + "\n", encoding="utf-8")


hero_css = """
<style>
@keyframes send {
  0% { opacity: 0; transform: translateX(0); }
  9% { opacity: 1; }
  88% { opacity: 1; }
  100% { opacity: 0; transform: translateX(218px); }
}
@keyframes store {
  0%, 28% { opacity: 0; transform: translateY(0); }
  36%, 82% { opacity: 1; }
  100% { opacity: 0; transform: translateY(95px); }
}
.signal-h { opacity: 0; animation: send 6s linear infinite; }
.signal-v { opacity: 0; animation: store 6s linear infinite; }
@media (prefers-reduced-motion: reduce) {
  .signal-h, .signal-v { display: none; }
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
  <text x="43" y="246">SHREYASH</text>
  <text x="43" y="323">SHUKLA<tspan fill="{GREEN}">.</tspan></text>
</g>
<text x="47" y="392" font-size="13" fill="{MUTED}">CLOUD SYSTEMS  /  FULL-STACK PRODUCTS  /  APPLIED AI</text>

<rect x="555" y="91" width="405" height="250" rx="14" fill="{PANEL}" stroke="{LINE}"/>
<text x="576" y="123" font-size="12" font-weight="700" fill="{GREEN}">SERVERLESS WORKFLOW</text>
<text x="938" y="123" font-size="11" fill="{MUTED}" text-anchor="end">REQUEST / RESPONSE</text>
<path d="M605 183 H901 M751 183 V278" fill="none" stroke="#49605f" stroke-width="2"/>
<path d="M897 179 L903 183 L897 187 M747 273 L751 279 L755 273" fill="none" stroke="{GREEN}" stroke-width="2"/>
<circle class="signal-h" cx="635" cy="183" r="5" fill="{GREEN}"/>
<circle class="signal-v" cx="751" cy="183" r="5" fill="{GREEN}"/>

<g fill="{INK}" stroke="{GREEN}" stroke-width="2">
  <rect x="584" y="162" width="70" height="42" rx="9"/>
  <rect x="711" y="162" width="80" height="42" rx="9"/>
  <rect x="863" y="162" width="76" height="42" rx="9"/>
  <rect x="711" y="278" width="80" height="42" rx="9"/>
</g>
<g fill="{TEXT}" font-size="11" font-weight="700" text-anchor="middle">
  <text x="619" y="188">CLIENT</text>
  <text x="751" y="188">LAMBDA</text>
  <text x="901" y="188">RESULT</text>
  <text x="751" y="304">DATA</text>
</g>
<text x="576" y="332" font-size="11" fill="{MUTED}">TYPESCRIPT  /  AWS LAMBDA  /  DYNAMODB</text>
"""
save(
    "hero.svg",
    hero,
    1000,
    430,
    "Shreyash Shukla — Software Engineer",
    "A self-contained engineering-themed banner with a restrained animated system flow.",
)


experience = f"""
<rect width="1000" height="296" rx="18" fill="{INK}"/>
<rect x="1" y="1" width="998" height="294" rx="17" fill="none" stroke="{LINE}"/>
<text x="42" y="51" font-size="13" font-weight="700" fill="{GREEN}">EXPERIENCE / QUICKO</text>
<text x="958" y="51" font-size="12" fill="{MUTED}" text-anchor="end">MAY–JUNE 2026  ·  AHMEDABAD</text>
<path d="M42 69 H958" stroke="{LINE}"/>
<text x="42" y="111" font-size="24" font-weight="700" fill="{TEXT}">Four tools shipped to production.</text>
<text x="42" y="135" font-size="12" fill="{MUTED}">Serverless APIs, data contracts, and infrastructure behind financial workflows.</text>
"""

tools = [
    ("01", "PAN", "Verification"),
    ("02", "PAN–Aadhaar", "Link Checker"),
    ("03", "Tax Payment", "Checker"),
    ("04", "e-Verify", "ITR"),
]
for i, (number, first, second) in enumerate(tools):
    x = 42 + 232 * i
    experience += f"""
<rect x="{x}" y="164" width="218" height="92" rx="12" fill="{PANEL}" stroke="{LINE}"/>
<text x="{x+17}" y="191" font-size="13" fill="{GREEN}">{number}</text>
<text x="{x+17}" y="218" font-size="16" font-weight="700" fill="{TEXT}">{first}</text>
<text x="{x+17}" y="239" font-size="15" fill="{MUTED}">{second}</text>
<circle cx="{x+191}" cy="185" r="4" fill="{GREEN}"/>
"""
save(
    "experience.svg",
    experience,
    1000,
    296,
    "Four financial tools shipped at Quicko",
    "PAN Verification, PAN–Aadhaar Link Checker, Tax Payment Checker, and e-Verify ITR.",
)


def card(number: str, title: str, kind: str, stack: str, accent: str, diagram: str, motion: str, description: str) -> str:
    return f"""
<style>
{motion}
@media (prefers-reduced-motion: reduce) {{
  .moving {{ display: none; }}
  .verify {{ animation: none; opacity: .88; }}
}}
</style>
<rect width="490" height="250" rx="15" fill="{INK}"/>
<rect x="1" y="1" width="488" height="248" rx="14" fill="none" stroke="{LINE}"/>
<rect x="23" y="28" width="5" height="18" rx="2.5" fill="{accent}"/>
<text x="39" y="41" font-size="11" font-weight="700" fill="{accent}">{number} / FEATURED PROJECT</text>
<text x="25" y="98" font-size="28" font-weight="800" fill="{TEXT}">{title}</text>
<text x="25" y="125" font-size="12" fill="{MUTED}">{kind}</text>
<path d="M25 177 H465" stroke="{LINE}"/>
<text x="25" y="209" font-size="11" fill="{accent}">{stack}</text>
<text x="25" y="230" font-size="11" fill="{MUTED}">OPEN PROJECT ↗</text>
{diagram}
"""


fraud_motion = """
@keyframes trace {
  0% { opacity: 0; transform: translate(0,0); }
  10% { opacity: 1; }
  33% { transform: translate(55px,-44px); }
  66% { transform: translate(124px,8px); }
  88% { opacity: 1; }
  100% { opacity: 0; transform: translate(55px,62px); }
}
.moving { opacity: 0; animation: trace 6s linear infinite; }
"""
fraud_diagram = f"""
<path d="M294 126 L349 82 L418 134 L349 188 Z M294 126 L418 134 M349 82 V188"
      fill="none" stroke="#405a54" stroke-width="2"/>
<circle class="moving" cx="294" cy="126" r="5" fill="{GREEN}"/>
<g fill="{INK}" stroke="{GREEN}" stroke-width="2">
  <circle cx="294" cy="126" r="12"/><circle cx="349" cy="82" r="12"/>
  <circle cx="418" cy="134" r="12"/><circle cx="349" cy="188" r="12"/>
</g>
<circle cx="349" cy="82" r="4" fill="{GREEN}"/>
<circle cx="418" cy="134" r="4" fill="{GREEN}"/>
<text x="300" y="63" font-size="11" font-weight="700" fill="{GREEN}">GRAPH + MODEL</text>
"""
save(
    "card-fraudshield.svg",
    card("01", "FraudShield", "Fraud detection across transactions", "FASTAPI  /  XGBOOST  /  GNN", GREEN, fraud_diagram, fraud_motion, "Fraud detection"),
    490, 250, "FraudShield project", "A graph-based fraud detection project and HackNUthon winner.",
)


trust_accent = "#f4c97e"
trust_motion = """
@keyframes verifyOne { 0%, 8% { opacity: .25; } 18%, 70% { opacity: 1; } 90%, 100% { opacity: .25; } }
@keyframes verifyTwo { 0%, 27% { opacity: .25; } 37%, 70% { opacity: 1; } 90%, 100% { opacity: .25; } }
@keyframes verifyThree { 0%, 46% { opacity: .25; } 56%, 70% { opacity: 1; } 90%, 100% { opacity: .25; } }
.v1 { animation: verifyOne 6s linear infinite; }
.v2 { animation: verifyTwo 6s linear infinite; }
.v3 { animation: verifyThree 6s linear infinite; }
"""
trust_diagram = f"""
<path d="M310 127 H418" fill="none" stroke="#665843" stroke-width="2"/>
<g fill="{INK}" stroke="{trust_accent}" stroke-width="2">
  <rect x="288" y="105" width="44" height="44" rx="10"/>
  <rect x="342" y="105" width="44" height="44" rx="10"/>
  <rect x="396" y="105" width="44" height="44" rx="10"/>
</g>
<g class="verify v1" fill="none" stroke="{trust_accent}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M300 127 l7 7 12 -15"/></g>
<g class="verify v2" fill="none" stroke="{trust_accent}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M354 127 l7 7 12 -15"/></g>
<g class="verify v3" fill="none" stroke="{trust_accent}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M408 127 l7 7 12 -15"/></g>
<text x="318" y="170" font-size="11" fill="{trust_accent}">VERIFY  /  ATTEST  /  TRUST</text>
"""
save(
    "card-trustchain.svg",
    card("02", "TrustChain", "Layered fraud prevention", "SOLIDITY  /  FASTAPI  /  VISION", trust_accent, trust_diagram, trust_motion, "Layered fraud prevention"),
    490, 250, "TrustChain project", "A layered verification project and Breach 2025 runner-up.",
)


dag_accent = "#b9adff"
dag_motion = """
@keyframes route {
  0% { opacity: 0; transform: translate(0,0); }
  12% { opacity: 1; }
  40% { transform: translate(61px,-42px); }
  75% { transform: translate(131px,0); opacity: 1; }
  100% { transform: translate(131px,0); opacity: 0; }
}
.moving { opacity: 0; animation: route 5.5s linear infinite; }
"""
dag_diagram = f"""
<path d="M292 128 L353 86 L423 128 L353 170 Z M353 86 V170"
      fill="none" stroke="#514b71" stroke-width="2"/>
<circle class="moving" cx="292" cy="128" r="5" fill="{dag_accent}"/>
<g fill="{INK}" stroke="{dag_accent}" stroke-width="2">
  <circle cx="292" cy="128" r="13"/><circle cx="353" cy="86" r="13"/>
  <circle cx="353" cy="170" r="13"/><circle cx="423" cy="128" r="13"/>
</g>
<g fill="{dag_accent}" font-size="12" font-weight="700" text-anchor="middle">
  <text x="292" y="132">1</text><text x="353" y="90">2</text>
  <text x="353" y="174">3</text><text x="423" y="132">4</text>
</g>
"""
save(
    "card-dagent.svg",
    card("03", "DAGent", "Agent workflow orchestration", "NEXT.JS  /  TYPESCRIPT  /  MCP", dag_accent, dag_diagram, dag_motion, "Agent workflow orchestration"),
    490, 250, "DAGent project", "A directed workflow for coordinating AI agents and MCP tools.",
)


drive_accent = "#8fd0e8"
drive_motion = """
@keyframes replicate {
  0%, 18% { opacity: 0; transform: translateX(0); }
  30% { opacity: 1; }
  80% { opacity: 1; }
  100% { opacity: 0; transform: translateX(95px); }
}
.moving { opacity: 0; animation: replicate 5.5s linear infinite; }
"""
drive_diagram = f"""
<path d="M319 90 H413 M319 159 H413" stroke="#4a6570" stroke-width="2"/>
<path d="M407 86 L413 90 L407 94 M407 155 L413 159 L407 163"
      fill="none" stroke="{drive_accent}" stroke-width="2"/>
<circle class="moving" cx="318" cy="90" r="4.5" fill="{drive_accent}"/>
<circle class="moving" cx="318" cy="159" r="4.5" fill="{drive_accent}" style="animation-delay: -2.75s"/>
<g fill="{INK}" stroke="{drive_accent}" stroke-width="2">
  <rect x="278" y="105" width="49" height="39" rx="7"/>
  <rect x="412" y="72" width="45" height="36" rx="7"/>
  <rect x="412" y="141" width="45" height="36" rx="7"/>
</g>
<g fill="{drive_accent}" font-size="11" text-anchor="middle">
  <text x="302" y="129">ENC</text><text x="434" y="95">01</text><text x="434" y="164">02</text>
</g>
"""
save(
    "card-drivemesh.svg",
    card("04", "DriveMesh", "Encrypted distributed storage", "PYTHON  /  FLASK  /  FERNET", drive_accent, drive_diagram, drive_motion, "Encrypted distributed storage"),
    490, 250, "DriveMesh project", "Encrypted data replicated across storage nodes.",
)

print("Built 6 self-contained SVG assets.")
