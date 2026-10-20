#!/usr/bin/env python3
"""Generate the decorative SVGs in assets/. Standard library only.

Run from the repo root:  python3 tools/build_assets.py
Change the palette below and re-run; every file picks it up.
All substantive text lives in README.md, never in these images.
"""
import math
import os
from xml.sax.saxutils import escape

P = {
    "base": "#0B1020",
    "panel": "#111832",
    "line": "#26345E",
    "text": "#E6EDF7",
    "muted": "#8FA0C0",
    "teal": "#2DD4BF",
    "amber": "#F5B544",
}
SANS = "'Segoe UI', Helvetica, Arial, sans-serif"
SERIF = "Georgia, 'Times New Roman', serif"
MONO = "ui-monospace, 'SFMono-Regular', Consolas, 'Liberation Mono', monospace"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")


def svg(w, h, title, desc, body, rx=0):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">\n'
        f"<title>{escape(title)}</title>\n<desc>{escape(desc)}</desc>\n"
        f'<rect width="{w}" height="{h}" rx="{rx}" fill="{P["base"]}"/>\n{body}\n</svg>\n'
    )


def write(name, content):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    size = len(content.encode())
    assert size < 40_000, f"{name} is {size} bytes"


def grid(w, h, step=40, opacity=0.35):
    lines = [f'<line x1="{x}" y1="0" x2="{x}" y2="{h}"/>' for x in range(0, w + 1, step)]
    lines += [f'<line x1="0" y1="{y}" x2="{w}" y2="{y}"/>' for y in range(0, h + 1, step)]
    return f'<g stroke="{P["line"]}" stroke-width="1" opacity="{opacity}">' + "".join(lines) + "</g>"


def loss_curve(x0, x1, y_top, y_bot, n=90):
    """Deterministic decaying curve with small ripples, like a training-loss trace."""
    pts = []
    for i in range(n):
        t = i / (n - 1)
        v = math.exp(-4.2 * t) + 0.05 * math.sin(26 * t) * (1 - t) + 0.02
        pts.append((x0 + t * (x1 - x0), y_top + (y_bot - y_top) * (1 - v / 1.07)))
    return pts


def banner():
    pts = loss_curve(950, 1160, 40, 310, 60)
    path = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    ex, ey = pts[-1]
    body = (
        grid(1200, 340)
        + f'<polyline points="{path}" fill="none" stroke="{P["teal"]}" stroke-width="2.5" opacity="0.55"/>'
        + f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="6" fill="{P["amber"]}"/>'
        + f'<rect x="64" y="64" width="44" height="4" fill="{P["amber"]}"/>'
        + f'<text x="64" y="112" font-family="{SANS}" font-size="20" letter-spacing="3" fill="{P["teal"]}" font-weight="600">'
        "MACHINE LEARNING ENGINEER · IISER BHOPAL · EXP. MAY 2027</text>"
        + f'<text x="62" y="205" font-family="{SANS}" font-size="74" font-weight="700" letter-spacing="3" fill="{P["text"]}">'
        "PRANJAL UPADHYAY</text>"
        + f'<text x="64" y="264" font-family="{SERIF}" font-size="25" font-style="italic" fill="{P["muted"]}">'
        "Machine learning systems that are measured, guarded and deployed on real hardware.</text>"
        + f'<rect x="1" y="1" width="1198" height="338" fill="none" stroke="{P["line"]}" stroke-width="2"/>'
    )
    write(
        "banner.svg",
        svg(
            1200, 340,
            "Pranjal Upadhyay, Machine Learning Engineer",
            "Banner: name, role line, and tagline over a faint grid with a decaying loss-curve trace.",
            body,
        ),
    )


SECTIONS = ["ABOUT", "SELECTED WORK", "EXPERIENCE", "SKILLS", "CONTACT"]


def section(i, label):
    body = (
        f'<rect x="0" y="0" width="1200" height="48" fill="{P["panel"]}"/>'
        f'<rect x="0" y="0" width="6" height="48" fill="{P["teal"]}"/>'
        f'<text x="28" y="31" font-family="{SANS}" font-size="18" font-weight="700" letter-spacing="5" fill="{P["text"]}">{label}</text>'
        f'<line x1="{60 + 15 * len(label) + 40}" y1="24" x2="1130" y2="24" stroke="{P["line"]}" stroke-width="2"/>'
        f'<text x="1172" y="30" text-anchor="end" font-family="{MONO}" font-size="15" fill="{P["amber"]}">{i:02d}</text>'
    )
    slug = label.lower().replace(" ", "-")
    write(
        f"section-{slug}.svg",
        svg(1200, 48, f"Section: {label.title()}", f"Header bar for the {label.title()} section.", body),
    )


def emblem(name, title, desc, inner):
    frame = (
        f'<rect x="3" y="3" width="154" height="154" rx="14" fill="{P["panel"]}" stroke="{P["line"]}" stroke-width="2"/>'
    )
    write(name, svg(160, 160, title, desc, frame + inner, rx=14))


T, A, M = P["teal"], P["amber"], P["muted"]


def stroke(color=T, w=4, fill="none"):
    return f'fill="{fill}" stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"'


def emblems():
    # projects
    emblem("project-1.svg", "AP-Copilot", "A shield with an approval gate inside.",
           f'<path d="M80 26 L124 42 V82 C124 108 104 124 80 134 C56 124 36 108 36 82 V42 Z" {stroke(T)}/>'
           f'<path d="M62 70 V96 M98 70 V96 M62 84 H98" {stroke(A, 5)}/>')
    nodes = [(80, 80)] + [(80 + 50 * math.cos(math.radians(a)), 80 + 50 * math.sin(math.radians(a))) for a in range(-90, 270, 72)]
    lines = "".join(f'<line x1="80" y1="80" x2="{x:.1f}" y2="{y:.1f}" {stroke(M, 2.5)}/>' for x, y in nodes[1:])
    dots = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9" {stroke(T, 4, P["panel"])}/>' for x, y in nodes[1:])
    emblem("project-2.svg", "Federated mood prediction", "A hub connected to five client nodes.",
           lines + dots + f'<circle cx="80" cy="80" r="13" fill="{A}"/>')
    emblem("project-3.svg", "NovaLearn", "Two linked agents followed by three parallel workers.",
           f'<rect x="22" y="58" width="38" height="44" rx="6" {stroke(T)}/><rect x="76" y="58" width="38" height="44" rx="6" {stroke(A)}/>'
           f'<path d="M60 80 H76" {stroke(M, 3)}/>'
           f'<path d="M114 80 H126 M126 50 V110" {stroke(M, 3)}/>'
           f'<circle cx="138" cy="50" r="6" {stroke(T, 3)}/><circle cx="138" cy="80" r="6" {stroke(T, 3)}/><circle cx="138" cy="110" r="6" {stroke(T, 3)}/>'
           f'<path d="M126 50 H132 M126 80 H132 M126 110 H132" {stroke(M, 3)}/>')
    layers = ""
    for k, (dy, c) in enumerate([(0, M), (22, T), (44, A)]):
        y = 56 + dy
        layers += f'<path d="M80 {y - 22} L132 {y} L80 {y + 22} L28 {y} Z" {stroke(c, 4, P["panel"])}/>'
    emblem("project-4.svg", "DyTox modification", "Three stacked transformer layers in isometric view.",
           layers)
    pts = []
    for i in range(61):
        t = i / 60
        pts.append(f"{24 + 112 * t:.1f},{80 - 44 * math.sin(t * 6 * math.pi) * math.exp(-1.4 * t):.1f}")
    emblem("project-5.svg", "Liquid neural network controller", "A decaying waveform over a baseline axis.",
           f'<path d="M24 80 H136" {stroke(M, 2)} stroke-dasharray="4 6"/>'
           f'<polyline points="{" ".join(pts)}" {stroke(T, 4)}/>'
           f'<circle cx="136" cy="80" r="6" fill="{A}"/>')
    arms = "".join(f'<path d="M80 80 L{80 + 40 * sx} {80 + 40 * sy}" {stroke(M, 4)}/>' for sx in (-1, 1) for sy in (-1, 1))
    rotors = "".join(f'<circle cx="{80 + 40 * sx}" cy="{80 + 40 * sy}" r="17" {stroke(T, 3.5)}/>' for sx in (-1, 1) for sy in (-1, 1))
    emblem("project-6.svg", "Applied robotics, NIDAR 2.0", "Top-down outline of a quadcopter.",
           arms + rotors + f'<rect x="68" y="68" width="24" height="24" rx="5" {stroke(A, 4, P["panel"])}/>')


def footer():
    body = (
        f'<line x1="0" y1="1" x2="1200" y2="1" stroke="{P["line"]}" stroke-width="2"/>'
        f'<rect x="64" y="22" width="44" height="4" fill="{P["amber"]}"/>'
        f'<text x="124" y="30" font-family="{SANS}" font-size="14" letter-spacing="4" fill="{P["muted"]}">PRANJAL UPADHYAY · BHOPAL, INDIA</text>'
        f'<polyline points="900,36 940,36 952,18 968,44 984,26 1000,36 1136,36" fill="none" stroke="{P["teal"]}" stroke-width="2" opacity="0.6"/>'
    )
    write("footer.svg", svg(1200, 56, "Closing bar", "Slim closing bar with a small signal trace.", body))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    banner()
    for i, s in enumerate(SECTIONS, 1):
        section(i, s)
    emblems()
    footer()
    print("wrote", len(os.listdir(OUT)), "files to", os.path.normpath(OUT))
