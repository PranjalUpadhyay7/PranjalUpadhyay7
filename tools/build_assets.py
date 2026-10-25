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


REDUCE = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"


def svg(w, h, title, desc, body, rx=0, css=""):
    style = f"<style>{css}{REDUCE}</style>\n" if css else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">\n'
        f"<title>{escape(title)}</title>\n<desc>{escape(desc)}</desc>\n{style}"
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
    L = sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)) + 2
    body = (
        grid(1200, 340)
        + f'<polyline class="trace" points="{path}" fill="none" stroke="{P["teal"]}" stroke-width="2.5" opacity="0.55"/>'
        + f'<circle class="dot" cx="{ex:.1f}" cy="{ey:.1f}" r="6" fill="{P["amber"]}"/>'
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
            css=f".trace{{stroke-dasharray:{L:.0f};animation:draw 3.2s ease-out both}}@keyframes draw{{from{{stroke-dashoffset:{L:.0f}}}to{{stroke-dashoffset:0}}}}"
                ".dot{transform-box:fill-box;transform-origin:center;animation:pop 3.2s both,pulse 2s 3.2s infinite ease-in-out}"
                "@keyframes pop{0%,90%{opacity:0;transform:scale(.2)}100%{opacity:1;transform:scale(1)}}@keyframes pulse{50%{transform:scale(1.7);opacity:.6}}",
        ),
    )


SECTIONS = ["QUEST LOG", "ACHIEVEMENTS", "TRAINING GROUNDS", "INVENTORY", "CONTACT"]


def section(i, label):
    body = (
        f'<rect width="720" height="36" fill="{P["panel"]}"/>'
        f'<rect width="6" height="36" fill="{P["teal"]}"/>'
        f'<text x="24" y="24.5" font-family="{SANS}" font-size="17" font-weight="700" letter-spacing="5" fill="{P["text"]}">{label}</text>'
        f'<text x="696" y="23.5" text-anchor="end" font-family="{MONO}" font-size="14" fill="{P["amber"]}">{i:02d}</text>'
    )
    slug = label.lower().replace(" ", "-")
    write(
        f"section-{slug}.svg",
        svg(720, 36, f"Section: {label.title()}", f"Header bar for the {label.title()} section.", body),
    )


EMBLEMS = {}


def emblem(name, title, desc, inner):
    """Emblem drawings are only embedded in cards (see card()); no standalone files."""
    EMBLEMS[name] = inner


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
    emblem("project-7.svg", "OpenVINS in Python", "A camera pose frustum moving along an estimated trajectory.",
           f'<polyline points="26,118 52,96 74,104 100,70 134,52" {stroke(T, 4)} stroke-dasharray="2 8"/>'
           f'<path d="M96 86 L124 78 L116 106 Z" {stroke(A)}/>'
           f'<circle cx="26" cy="118" r="5" fill="{M}"/>')
    pts = [(40, 112), (62, 128), (84, 118), (110, 132), (128, 108), (52, 96)]
    emblem("project-8.svg", "DROID-SLAM on OAK-D Pro", "A camera observing a sparse point map.",
           "".join(f'<circle cx="{x}" cy="{y}" r="4" fill="{M}"/>' for x, y in pts)
           + f'<rect x="62" y="30" width="36" height="26" rx="5" {stroke(A, 4, P["panel"])}/>'
           + f'<circle cx="80" cy="43" r="7" {stroke(T, 3)}/>'
           + "".join(f'<path d="M80 56 L{x} {y}" {stroke(T, 1.5)} opacity="0.5"/>' for x, y in pts[::2]))

def chip_w(text, size=16):
    return int(len(text) * size * 0.6 + 26)


def chips(items, x0, y0, x_max, size=16, color=None, row_h=38, ch=30):
    """Flow rounded chips left to right, wrapping at x_max. Returns (svg, bottom_y)."""
    out, x, y = [], x0, y0
    for t in items:
        w = chip_w(t, size)
        if x + w > x_max and x > x0:
            x, y = x0, y + row_h
        out.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{ch}" rx="{ch / 2}" fill="{P["base"]}" stroke="{color or P["line"]}" stroke-width="1.5"/>'
            f'<text x="{x + 13}" y="{y + ch * 0.5 + size * 0.35:.1f}" font-family="{MONO}" font-size="{size}" fill="{P["text"]}">{escape(t)}</text>'
        )
        x += w + 10
    return "".join(out), y + ch


CARDS = [
    ("ap-copilot", "project-1.svg", "AP-Copilot", "QUEST COMPLETE · PUBLIC REPO",
     "The LLM can propose. It can never write.",
     ["31/60 → 59/60 tasks", "0 unsafe writes", "480 tests", "219/219 mutants killed"],
     "AP-Copilot, public repo. A safety-critical LLM agent that configures ArduPilot/Pixhawk parameters from plain-language requests; the model has no write tool, and deterministic validation plus a human-approval gate decide. Hybrid RAG with BM25, embeddings and RRF. On a 60-task benchmark the full system passed 59/60 for gpt-oss-20b versus 31/60 with retrieval and validation removed; no model produced an unsafe write on the full system. 480 tests, 219/219 mutants killed in the validation layer."),
    ("federated", "project-2.svg", "Federated Mood Prediction", "QUEST COMPLETE · PUBLIC REPO",
     "Mood screening where every participant is a client",
     ["TabM 69.95%", "within 2% of centralized", "LSTM 68.28%"],
     "Federated Mood Prediction for Early Depression Screening. Flower pipeline predicting 5-class mood from smartphone behavioural signals, DiversityOne dataset, non-IID clients. TabM 69.95%, LSTM 68.28%, within 2% of centralized."),
    ("novalearn", "project-3.svg", "NovaLearn", "SUBMITTED · AMAZON NOVA HACKATHON 2025",
     "A study session in, a 24-second animation out",
     ["24 s animation in ~4 min", "Chrome extension"],
     "NovaLearn. Planner plus executor multi-agent study companion on four Amazon Nova models through an AWS Bedrock layer; a 4-scene parallel pipeline produces a 24 second animation in about 4 minutes; shipped as a Chrome extension."),
    ("dytox", "project-4.svg", "DyTox Modification", "QUEST COMPLETE · PUBLIC REPO",
     "One extension helped. One cost 3.2 points. Both shown.",
     ["forgetting 18.7 → 14.8%", "DCPE cost 3.2–3.3 pts"],
     "Two extensions to the DyTox continual-learning transformer on CIFAR-100. The Task-Aware Encoder cut forgetting from 18.7% to 14.8%. Dynamic Contextual Positional Embeddings cost 3.2 to 3.3 points, which I report."),
    ("liquid-nn", "project-5.svg", "Liquid NN Controller", "IN PROGRESS · PAPER IN PREPARATION",
     "A controller that keeps adapting without blocking",
     ["~340x lower latency", "~19% lower tracking error"],
     "Liquid neural network adaptive controller with online parameter updates on a background thread; about 340x lower control-loop latency and about 19% lower tracking error than a DNN plus ODE-solver baseline. Journal paper in preparation."),
    ("nidar", "project-6.svg", "Applied Robotics: NIDAR 2.0", "BOSS FIGHT · SWARM IN SIMULATION",
     "8 drones, 1 disaster zone. Simulated, not flown yet.",
     ["VIO 7.5 → 3.7–4.0 ms", "4.5 FPS YOLO on Jetson Nano", "GNSS-denied, 50–80 m flights"],
     "NIDAR 2.0, team lead of 6. Building an 8-drone disaster-search swarm; validated in simulation with 2 recon and 4 delivery drones over 10 hectares; the full mission is the planned target. OpenVINS backend update 7.5 ms to 3.7 to 4.0 ms; LEAF-YOLO-s at 4.5 to 4.6 FPS on a Jetson Nano; GNSS-denied navigation flight-validated at 50 to 80 m."),
    ("openvins-python", "project-7.svg", "OpenVINS in Python", "QUEST COMPLETE · BS THESIS · PUBLIC REPOS",
     "Rebuilt a VIO estimator, then taught it to spot hovering",
     ["Python port of OpenVINS MSCKF", "hovering-aware FIFO/LIFO mode", "BS thesis, Apr 2026"],
     "A Python port of the OpenVINS MSCKF visual-inertial estimator, plus a hovering-aware extension that implements the motion-classification algorithm of Kottas, Wu and Roumeliotis (IROS 2014), for which no reference code was published. It is the implementation behind my BS thesis at IISER Bhopal (April 2026). Validated on a Jetson Orin Nano UAV against the KAIST VIO benchmark and a custom hovering flight dataset."),
    ("droid-slam", "project-8.svg", "DROID-SLAM on OAK-D", "SIDE QUEST · PUBLIC REPO",
     "Deep visual SLAM, live from an OAK-D camera",
     ["fork of DROID-SLAM", "live OAK-D demo"],
     "My fork of DROID-SLAM (Teed and Deng) that adds a real-time demo driven by a live OAK-D camera stream."),
]


def card(slug, emb, title, status, tagline, items, alt):
    """One slim quest row: emblem, status/title/tagline on the left, two metric chips stacked right."""
    h = 58
    body = (
        f'<rect x="2" y="2" width="716" height="{h - 4}" rx="10" fill="{P["panel"]}" stroke="{P["line"]}" stroke-width="2"/>'
        f'<g transform="translate(10,2) scale(0.34)"><g class="float" style="animation-delay:{(len(slug) % 5) * 0.4:.1f}s">{EMBLEMS[emb]}</g></g>'
        f'<text class="{"blink" if status.startswith(("IN PROGRESS", "BOSS")) else ""}" x="80" y="17" font-family="{SANS}" font-size="9.5" letter-spacing="1.8" fill="{P["amber"]}" font-weight="600">{escape(status)}</text>'
        f'<text x="80" y="35" font-family="{SANS}" font-size="17" font-weight="700" fill="{P["text"]}">{escape(title)}</text>'
        f'<text x="80" y="50" font-family="{SANS}" font-size="12" fill="{P["muted"]}">{escape(tagline)}</text>'
    )
    for n, t in enumerate(items[:2]):
        w = len(t) * 11.5 * 0.6 + 20
        y = 5 + n * 25
        body += (f'<rect x="{708 - w:.0f}" y="{y}" width="{w:.0f}" height="22" rx="11" fill="{P["base"]}" stroke="{P["line"]}" stroke-width="1.5"/>'
                 f'<text x="{708 - w + 10:.0f}" y="{y + 15}" font-family="{MONO}" font-size="11.5" fill="{P["text"]}">{escape(t)}</text>')
    css = ".float{animation:float 3.4s ease-in-out infinite}@keyframes float{50%{transform:translateY(-6px)}}.blink{animation:blink 1.6s ease-in-out infinite}@keyframes blink{50%{opacity:.35}}"
    write(f"card-{slug}.svg", svg(720, h, title, alt, body, css=css))


def experience():
    cards = [
        ("experience-tcs", "TCS Research & Innovation", "Research Intern, AI and Robotics", "12 MAY – 31 AUG 2025",
         "Soft-gripper simulation, RGB-D 6-DoF grasping, PPO policy. Simulation only.", P["teal"],
         "TCS Research and Innovation, Research Intern in AI and Robotics, 12 May to 31 Aug 2025. Robotic Mobile Manipulation Platform for Retail and Warehouses: PyBullet platform with 4 warehouse scenarios and 20 object categories, RGB-D 6-DoF grasp pose prediction in clutter, PPO policy trained over a 48-hour simulation run, 15 to 30 s per-object pick cycles. Simulation only."),
        ("experience-moon", "MOON Lab, IISER Bhopal", "Undergraduate researcher, 2 years", "ADVISOR: DR. P. B. SUJIT",
         "Perception, state estimation, GNSS-denied navigation, drone hardware.", P["amber"],
         "MOON Lab, IISER Bhopal, undergraduate researcher for two years, advised by Dr. P. B. Sujit. Perception, state estimation, adaptive control and GNSS-denied navigation; algorithms deployed on Jetson edge devices and drones; Python implementation of OpenVINS."),
    ]
    for slug, org, role, tag, line, c, alt in cards:
        body = (
            f'<rect x="2" y="2" width="716" height="76" rx="12" fill="{P["panel"]}" stroke="{P["line"]}" stroke-width="2"/>'
            f'<rect x="2" y="2" width="7" height="76" rx="3" fill="{c}"/>'
            f'<text x="26" y="30" font-family="{SANS}" font-size="20" font-weight="700" fill="{P["text"]}">{escape(org)}</text>'
            f'<text x="26" y="51" font-family="{SANS}" font-size="14.5" fill="{P["muted"]}">{escape(role)}</text>'
            f'<text x="26" y="69" font-family="{SANS}" font-size="12.5" fill="{P["muted"]}" opacity="0.85">{escape(line)}</text>'
            f'<text x="696" y="28" text-anchor="end" font-family="{SANS}" font-size="12" letter-spacing="2.5" fill="{P["amber"]}" font-weight="600">{escape(tag)}</text>'
        )
        write(f"{slug}.svg", svg(720, 80, f"{org}, {role}", alt, body))


SKILLS = [
    ("ML & DEEP LEARNING", P["teal"], ["PyTorch", "TabM", "LSTM", "Transformers", "Continual learning", "Federated learning", "RL (PPO)", "Object detection"]),
    ("ROBOTICS", P["amber"], ["VIO: OpenVINS, MSCKF, EKF", "Visual SLAM", "GNSS-denied navigation", "PyBullet", "Adaptive control", "ROS 2", "Drone + edge hardware"]),
    ("GENAI & NLP", P["teal"], ["LangGraph", "Hybrid RAG", "Agent guardrails", "AWS Bedrock", "Whisper"]),
    ("LANGUAGES", P["muted"], ["Python", "C++", "TypeScript", "Rust"]),
    ("DEPLOYMENT", P["muted"], ["FastAPI", "TensorRT FP16", "Jetson Nano / Orin Nano", "ArduPilot", "pytest + mutmut"]),
]


def skills():
    body, y = "", 4
    for label, color, items in SKILLS:
        body += f'<text x="4" y="{y + 18}" font-family="{SANS}" font-size="10.5" letter-spacing="2" font-weight="700" fill="{color}">{escape(label)}</text>'
        c, bottom = chips(items, 158, y, 716, 12.5, color, row_h=29, ch=24)
        body += c
        y = bottom + 10
    alt = "Skills. " + " ".join(f"{l.title()}: {', '.join(i)}." for l, _, i in SKILLS)
    write("skills.svg", svg(720, y, "Skills", alt, body))


ACHIEVEMENTS = [
    (True, "ZERO UNSAFE WRITES", "60 tasks, 5 models"),
    (True, "100% MUTANTS KILLED", "219/219, validation layer"),
    (True, "HONEST REPORTER", "DCPE cost 3.2 pts, shown"),
    (True, "2X FASTER", "7.5 → 3.7–4.0 ms, ATE 0.98"),
    (True, "LIGHT ON A NANO", "LEAF-YOLO-s, 4.5 FPS"),
    (True, "OFF THE GRID", "GNSS-denied, 50–80 m flights"),
    (False, "FULL SWARM FLIGHT", "planned target: 8 drones"),
    (False, "PAPER PUBLISHED", "liquid-NN paper in prep"),
    (False, "FIRST ML ROLE", "full-time, India: you?"),
]


def achievements():
    w, h, g = 232, 58, 8
    body = ""
    for i, (on, title, sub) in enumerate(ACHIEVEMENTS):
        x, y = (i % 3) * (w + g), (i // 3) * (h + g)
        c = (P["teal"], P["amber"])[(i // 3) % 2] if on else P["muted"]
        dash = "" if on else ' stroke-dasharray="6 5"'
        d = f'style="animation-delay:{i * 0.3:.1f}s"'
        glyph = (
            f'<g class="glow" {d}><circle cx="{x + 28}" cy="{y + 29}" r="14" {stroke(c, 3)}/><path d="M{x + 21} {y + 29} L{x + 26} {y + 34} L{x + 35} {y + 24}" {stroke(c, 3)}/></g>'
            if on else
            f'<g class="lock" {d}><rect x="{x + 18}" y="{y + 28}" width="20" height="15" rx="3" {stroke(c, 3)}/><path d="M{x + 22} {y + 28} V{y + 22} a6 6 0 0 1 12 0 V{y + 28}" {stroke(c, 3)}/></g>'
        )
        body += (
            f'<rect x="{x + 1}" y="{y + 1}" width="{w - 2}" height="{h - 2}" rx="12" fill="{P["panel"]}" stroke="{P["line"] if on else c}" stroke-width="2"{dash}{"" if on else ' class="march"'}/>'
            + glyph
            + f'<text x="{x + 54}" y="{y + 32}" font-family="{SANS}" font-size="13" font-weight="700" letter-spacing="0.5" fill="{P["text"] if on else P["muted"]}">{escape(title)}</text>'
            + f'<text x="{x + 54}" y="{y + 48}" font-family="{SANS}" font-size="11.5" fill="{P["muted"]}">{escape(sub)}</text>'
            + f'<text x="{x + w - 12}" y="{y + 15}" text-anchor="end" font-family="{SANS}" font-size="9" letter-spacing="1.5" fill="{c}">{"UNLOCKED" if on else "LOCKED"}</text>'
        )
    alt = ("Achievements. Unlocked: " + "; ".join(f"{t.title()} ({s})" for o, t, s in ACHIEVEMENTS if o)
           + ". Locked, planned or in progress: " + "; ".join(f"{t.title()} ({s})" for o, t, s in ACHIEVEMENTS if not o) + ".")
    css = (".glow{animation:glow 2.4s ease-in-out infinite}@keyframes glow{50%{opacity:.4}}"
           ".lock{transform-box:fill-box;transform-origin:50% 100%;animation:wob 3.6s ease-in-out infinite}"
           "@keyframes wob{0%,78%,100%{transform:rotate(0)}82%{transform:rotate(-9deg)}88%{transform:rotate(9deg)}94%{transform:rotate(-4deg)}}"
           ".march{animation:march 1.8s linear infinite}@keyframes march{to{stroke-dashoffset:-22}}")
    write("achievements.svg", svg(720, 3 * h + 2 * g, "Achievements", alt, body, css=css))

JOURNEY = [
    ("LAUNCH · IISER BHOPAL", "BS-MS, Computer Science + Data Science", "graduating May 2027"),
    ("FIRST REPS", "Learned to think fast in contests", "645 problems · CodeChef max 1644"),
    ("FIRST RESEARCH", "Made a transformer forget less", "forgetting 18.7% → 14.8%"),
    ("TCS RESEARCH · 2025", "Taught a robot gripper to pick, in simulation", "PPO policy · 20 object categories"),
    ("MOON LAB", "Flew drones where GPS can't reach", "VIO update 2x faster · flights at 50–80 m"),
    ("THESIS · APR 2026", "Rebuilt OpenVINS in Python, made it hover-aware", "both repos open source"),
    ("AP-COPILOT · 2026", "Built an LLM that can't write to the drone", "60 tasks · 0 unsafe writes"),
    ("NEXT WAYPOINT", "Your team.", "full-time ML Engineer · India"),
]


def journey():
    """A quadcopter flies a mission route and lights one waypoint per chapter.

    Straight legs + linear keyframes keep the drone, the drawn trail and the
    captions in sync. Without animation (reduced motion) everything shows.
    """
    T, start, leg, dwell, fade = 19.2, 0.5, 0.95, 1.1, 18.4
    top, row = 82, 49
    pts = [(52 if k % 2 == 0 else 92, top + k * row) for k in range(len(JOURNEY))]
    seg = [math.dist(pts[k], pts[k + 1]) for k in range(len(pts) - 1)]
    cum = [0.0]
    for s_ in seg:
        cum.append(cum[-1] + s_)
    frac = [c / cum[-1] for c in cum]
    arrive = [start + k * (leg + dwell) for k in range(len(pts))]
    pc = lambda t: f"{t / T * 100:.2f}%"

    drone_kf = [f"0%{{transform:translate({pts[0][0]}px,{pts[0][1]}px);opacity:0}}"]
    trail_kf = ["0%{stroke-dashoffset:1}"]
    for k, (x, y) in enumerate(pts):
        a = arrive[k]
        d = min(a + dwell, fade) if k < len(pts) - 1 else fade
        drone_kf += [f"{pc(a)}{{transform:translate({x}px,{y}px);opacity:1}}", f"{pc(d)}{{transform:translate({x}px,{y}px);opacity:1}}"]
        trail_kf += [f"{pc(a)}{{stroke-dashoffset:{1 - frac[k]:.4f}}}", f"{pc(d)}{{stroke-dashoffset:{1 - frac[k]:.4f}}}"]
    drone_kf.append(f"100%{{transform:translate({pts[-1][0]}px,{pts[-1][1]}px);opacity:0}}")
    trail_kf.append(f"{pc(fade)}{{stroke-dashoffset:0;opacity:1}}")
    trail_kf.append("100%{stroke-dashoffset:0;opacity:0}")

    css = (f".drone{{transform:translate({pts[-1][0]}px,{pts[-1][1]}px);animation:fly {T}s linear infinite}}"
           f"@keyframes fly{{{''.join(drone_kf)}}}"
           f".trail{{stroke-dasharray:1;animation:trail {T}s linear infinite}}@keyframes trail{{{''.join(trail_kf)}}}"
           ".pulse{transform-box:fill-box;transform-origin:center;animation:pulse 1.6s ease-out infinite}"
           "@keyframes pulse{from{transform:scale(1);opacity:.9}to{transform:scale(2.6);opacity:0}}"
           ".spin{animation:spin .25s linear infinite}@keyframes spin{50%{opacity:.35}}")

    body = (f'<rect x="2" y="2" width="716" height="{top + (len(pts) - 1) * row + 36}" rx="14" fill="{P["panel"]}" stroke="{P["line"]}" stroke-width="2"/>'
            f'<text x="28" y="36" font-family="{SANS}" font-size="13" letter-spacing="4" font-weight="700" fill="{P["amber"]}">FLIGHT LOG</text>'
            f'<text x="692" y="36" text-anchor="end" font-family="{MONO}" font-size="13" fill="{P["muted"]}">{len(pts)} WAYPOINTS · 1 PILOT</text>'
            f'<line x1="28" y1="50" x2="692" y2="50" stroke="{P["line"]}" stroke-width="1.5"/>')
    route = " ".join(f"{x},{y}" for x, y in pts)
    body += (f'<polyline points="{route}" fill="none" stroke="{P["line"]}" stroke-width="2.5" stroke-dasharray="4 7"/>'
             f'<polyline class="trail" pathLength="1" points="{route}" fill="none" stroke="{P["teal"]}" stroke-width="3" stroke-linejoin="round"/>')
    for k, ((x, y), (tag, title, metric)) in enumerate(zip(pts, JOURNEY)):
        last = k == len(pts) - 1
        c = P["amber"] if last else P["teal"]
        a = arrive[k]
        css += (f".w{k}{{animation:w{k} {T}s linear infinite}}"
                f"@keyframes w{k}{{0%,{pc(max(a - 0.05, 0))}{{opacity:0;transform:translateX(-10px)}}"
                f"{pc(a + 0.45)},{pc(fade)}{{opacity:1;transform:translateX(0)}}100%{{opacity:0}}}}")
        body += f'<circle cx="{x}" cy="{y}" r="9" fill="{P["base"]}" stroke="{P["line"]}" stroke-width="2.5"/>'
        body += f'<g class="w{k}"><circle cx="{x}" cy="{y}" r="9" fill="{c}"/>'
        if last:
            body += f'<circle class="pulse" cx="{x}" cy="{y}" r="9" fill="none" stroke="{c}" stroke-width="2.5"/>'
        body += (f'<text x="136" y="{y + 1}" font-family="{SANS}" font-size="20" font-weight="700" fill="{P["text"]}">{escape(title)}</text>'
                 f'<text x="136" y="{y + 22}"><tspan font-family="{SANS}" font-size="11" letter-spacing="2" font-weight="700" fill="{P["amber"]}">{k + 1:02d} · {escape(tag)}</tspan>'
                 f'<tspan dx="12" font-family="{MONO}" font-size="14" fill="{c}">{escape(metric)}</tspan></text></g>')
    rotors = "".join(f'<circle class="spin" cx="{sx * 9}" cy="{sy * 9}" r="6" fill="none" stroke="{P["text"]}" stroke-width="2"/>'
                     for sx in (-1, 1) for sy in (-1, 1))
    body += (f'<g class="drone"><path d="M-9 -9 L9 9 M9 -9 L-9 9" stroke="{P["muted"]}" stroke-width="3" stroke-linecap="round"/>'
             f'{rotors}<rect x="-5" y="-5" width="10" height="10" rx="2" fill="{P["amber"]}"/></g>')
    h = top + (len(pts) - 1) * row + 40
    alt = "Flight log of my journey, animated as a drone flying a mission route. " + " ".join(
        f"{k + 1}. {t.title()}: {ti} ({m})." for k, (t, ti, m) in enumerate(JOURNEY))
    write("journey.svg", svg(720, h, "Flight log", alt, body, css=css))


def hud():
    n_on = sum(1 for o, _, _ in ACHIEVEMENTS if o)
    cells = [
        ("PLAYER 1", "PRANJAL"),
        ("CLASS", "ML ENGINEER"),
        ("GUILD", "IISER BHOPAL"),
        ("QUESTS", str(len(CARDS))),
        ("UNLOCKED", f"{n_on}/{len(ACHIEVEMENTS)}"),
        ("STATUS", "OPEN TO WORK"),
    ]
    ws = [max(len(l) * 7.5, len(v) * 9.2) + 28 + (16 if l == "STATUS" else 0) for l, v in cells]
    extra = (716 - sum(ws)) / len(cells)
    ws = [w + extra for w in ws]
    body = f'<rect x="2" y="2" width="716" height="66" rx="12" fill="{P["panel"]}" stroke="{P["line"]}" stroke-width="2"/>'
    x = 2
    for (l, v), w in zip(cells, ws):
        col = P["amber"] if l == "STATUS" else P["teal"]
        body += (
            f'<text x="{x + 16:.0f}" y="28" font-family="{SANS}" font-size="10.5" letter-spacing="2.5" fill="{P["muted"]}">{l}</text>'
            f'<text x="{x + 16:.0f}" y="52" font-family="{MONO}" font-size="15" font-weight="700" fill="{col}">{escape(v)}</text>'
        )
        if l == "STATUS":
            body += f'<rect class="cur" x="{x + 16 + len(v) * 9.2 + 4:.0f}" y="40" width="9" height="15" fill="{col}"/>'
        x += w
        if l != "STATUS":
            body += f'<line x1="{x:.0f}" y1="14" x2="{x:.0f}" y2="56" stroke="{P["line"]}" stroke-width="1.5"/>'
    css = ".cur{animation:cur 1.1s steps(1) infinite}@keyframes cur{50%{opacity:0}}"
    write("hud.svg", svg(720, 70, "Player card",
          f"Player 1: Pranjal. Class: ML engineer. Guild: IISER Bhopal. Quests: {len(CARDS)}. Achievements unlocked: {n_on} of {len(ACHIEVEMENTS)}. Status: open to work.", body, css=css))


CODING = [("CODECHEF", "1644", "max rating, 3 star"), ("CODESTUDIO", "1741", "max rating"), ("CODEFORCES", "1128", "max rating")]


def coding():
    w, gap = 226, 6
    body = (f'<rect x="2" y="2" width="716" height="134" rx="14" fill="{P["panel"]}" stroke="{P["line"]}" stroke-width="2"/>'
            f'<text x="24" y="26" font-family="{SANS}" font-size="11.5" letter-spacing="3" font-weight="700" fill="{P["amber"]}">COMPETITIVE PROGRAMMING · MAX RATINGS · CODOLIO</text>')
    for i, (name, val, sub) in enumerate(CODING):
        x = 18 + i * (w + gap)
        c = P["teal"] if i % 2 == 0 else P["amber"]
        label = f"{name} · 3 STAR" if "3 star" in sub else name
        body += (f'<rect x="{x}" y="38" width="{w - 14}" height="56" rx="10" fill="{P["base"]}" stroke="{P["line"]}" stroke-width="1.5"/>'
                 f'<text x="{x + (w - 14) / 2}" y="55" text-anchor="middle" font-family="{SANS}" font-size="10.5" letter-spacing="2.2" fill="{P["muted"]}">{label}</text>'
                 f'<text x="{x + (w - 14) / 2}" y="85" text-anchor="middle" font-family="{MONO}" font-size="28" font-weight="700" fill="{c}">{val}</text>')
    c, _ = chips(["645 questions solved", "42 contests", "28-day max streak"], 18, 104, 700, 12.5, ch=24)
    alt = ("Competitive programming on Codolio. Max ratings: CodeChef 1644 (3 star), CodeStudio 1741, CodeForces 1128. "
           "645 questions solved, 42 contests attended, longest streak 28 days.")
    write("coding.svg", svg(720, 138, "Competitive programming", alt, body + c))


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
    for f in os.listdir(OUT):  # only generated SVGs; keep GIFs, the demo and github-stats.svg
        if f.endswith(".svg") and f != "github-stats.svg":
            os.remove(os.path.join(OUT, f))
    banner()
    for i, s in enumerate(SECTIONS, 1):
        section(i, s)
    emblems()
    for c in CARDS:
        card(*c)
    experience()
    skills()
    achievements()
    coding()
    journey()
    hud()
    footer()
    print("wrote", len(os.listdir(OUT)), "files to", os.path.normpath(OUT))
