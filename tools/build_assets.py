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


SECTIONS = ["SELECTED WORK", "EXPERIENCE", "SKILLS", "CONTACT"]


def section(i, label):
    body = (
        f'<rect width="720" height="44" fill="{P["panel"]}"/>'
        f'<rect width="6" height="44" fill="{P["teal"]}"/>'
        f'<text x="24" y="29" font-family="{SANS}" font-size="19" font-weight="700" letter-spacing="5" fill="{P["text"]}">{label}</text>'
        f'<text x="696" y="28" text-anchor="end" font-family="{MONO}" font-size="15" fill="{P["amber"]}">{i:02d}</text>'
    )
    slug = label.lower().replace(" ", "-")
    write(
        f"section-{slug}.svg",
        svg(720, 44, f"Section: {label.title()}", f"Header bar for the {label.title()} section.", body),
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


def chips(items, x0, y0, x_max, size=16, color=None, row_h=38):
    """Flow rounded chips left to right, wrapping at x_max. Returns (svg, bottom_y)."""
    out, x, y = [], x0, y0
    for t in items:
        w = chip_w(t, size)
        if x + w > x_max and x > x0:
            x, y = x0, y + row_h
        out.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="30" rx="15" fill="{P["base"]}" stroke="{color or P["line"]}" stroke-width="1.5"/>'
            f'<text x="{x + 13}" y="{y + 20}" font-family="{MONO}" font-size="{size}" fill="{P["text"]}">{escape(t)}</text>'
        )
        x += w + 10
    return "".join(out), y + 30


def stats():
    tiles = [
        ("0", "unsafe writes in the", "60-task agent benchmark"),
        ("2x", "faster VIO update at", "accuracy parity"),
        ("~340x", "lower control-loop", "latency, liquid NN"),
        ("-3.9 pp", "forgetting from my", "DyTox extension"),
    ]
    body, w = "", 167
    for i, (n, l1, l2) in enumerate(tiles):
        x = i * (w + 16) + 2
        c = P["teal"] if i % 2 == 0 else P["amber"]
        body += (
            f'<rect x="{x}" y="2" width="{w}" height="116" rx="12" fill="{P["panel"]}" stroke="{P["line"]}" stroke-width="2"/>'
            f'<rect x="{x}" y="2" width="{w}" height="5" rx="2" fill="{c}"/>'
            f'<text x="{x + w / 2}" y="60" text-anchor="middle" font-family="{MONO}" font-size="{40 if len(n) < 6 else 30}" font-weight="700" fill="{c}">{escape(n)}</text>'
            f'<text x="{x + w / 2}" y="87" text-anchor="middle" font-family="{SANS}" font-size="12.5" fill="{P["muted"]}">{escape(l1)}</text>'
            f'<text x="{x + w / 2}" y="105" text-anchor="middle" font-family="{SANS}" font-size="12.5" fill="{P["muted"]}">{escape(l2)}</text>'
        )
    write("stats.svg", svg(720, 120, "Key results",
          "0 unsafe writes on the 60-task AP-Copilot benchmark; 2x faster OpenVINS update at accuracy parity; about 340x lower control-loop latency for the liquid neural network controller; 3.9 percentage points less forgetting from the DyTox Task-Aware Encoder.", body))


CARDS = [
    ("ap-copilot", "project-1.svg", "AP-Copilot", "PUBLIC REPO",
     "LLM agent that configures ArduPilot, guarded by validators",
     ["31/60 → 59/60 tasks", "0 unsafe writes", "480 tests", "219/219 mutants killed"],
     "AP-Copilot, public repo. A safety-critical LLM agent that configures ArduPilot/Pixhawk parameters from plain-language requests; the model has no write tool, and deterministic validation plus a human-approval gate decide. Hybrid RAG with BM25, embeddings and RRF. On a 60-task benchmark the full system passed 59/60 for gpt-oss-20b versus 31/60 with retrieval and validation removed; no model produced an unsafe write on the full system. 480 tests, 219/219 mutants killed in the validation layer."),
    ("federated", "project-2.svg", "Federated Mood Prediction", "PUBLIC REPO",
     "Federated mood screening from phone signals, 8 countries",
     ["TabM 69.95%", "LSTM 68.28%", "within 2% of centralized"],
     "Federated Mood Prediction for Early Depression Screening. Flower pipeline predicting 5-class mood from smartphone behavioural signals, DiversityOne dataset, non-IID clients. TabM 69.95%, LSTM 68.28%, within 2% of centralized."),
    ("novalearn", "project-3.svg", "NovaLearn", "AMAZON NOVA HACKATHON 2025",
     "Multi-agent study companion on 4 Amazon Nova models",
     ["24 s animation in ~4 min", "Chrome extension"],
     "NovaLearn. Planner plus executor multi-agent study companion on four Amazon Nova models through an AWS Bedrock layer; a 4-scene parallel pipeline produces a 24 second animation in about 4 minutes; shipped as a Chrome extension."),
    ("dytox", "project-4.svg", "DyTox Modification", "PUBLIC REPO",
     "Continual-learning transformer: one win, one failure",
     ["forgetting 18.7 → 14.8%", "DCPE cost 3.2–3.3 pts"],
     "Two extensions to the DyTox continual-learning transformer on CIFAR-100. The Task-Aware Encoder cut forgetting from 18.7% to 14.8%. Dynamic Contextual Positional Embeddings cost 3.2 to 3.3 points, which I report."),
    ("liquid-nn", "project-5.svg", "Liquid NN Controller", "PAPER IN PREPARATION",
     "Liquid-NN adaptive controller with online updates",
     ["~340x lower latency", "~19% lower tracking error"],
     "Liquid neural network adaptive controller with online parameter updates on a background thread; about 340x lower control-loop latency and about 19% lower tracking error than a DNN plus ODE-solver baseline. Journal paper in preparation."),
    ("nidar", "project-6.svg", "Applied Robotics: NIDAR 2.0", "SWARM IN SIMULATION · BENCHMARK PUBLIC",
     "8-drone disaster-search swarm. Team lead, 6 members.",
     ["VIO 7.5 → 3.7–4.0 ms", "4.5 FPS YOLO on Jetson Nano", "GNSS-denied, 50–80 m flights"],
     "NIDAR 2.0, team lead of 6. Building an 8-drone disaster-search swarm; validated in simulation with 2 recon and 4 delivery drones over 10 hectares; the full mission is the planned target. OpenVINS backend update 7.5 ms to 3.7 to 4.0 ms; LEAF-YOLO-s at 4.5 to 4.6 FPS on a Jetson Nano; GNSS-denied navigation flight-validated at 50 to 80 m."),
    ("openvins-python", "project-7.svg", "OpenVINS in Python", "PUBLIC REPOS · BS THESIS",
     "Python MSCKF port plus a hovering-aware extension",
     ["Python port of OpenVINS MSCKF", "hovering-aware FIFO/LIFO mode", "BS thesis, Apr 2026"],
     "A Python port of the OpenVINS MSCKF visual-inertial estimator, plus a hovering-aware extension that implements the motion-classification algorithm of Kottas, Wu and Roumeliotis (IROS 2014), for which no reference code was published. It is the implementation behind my BS thesis at IISER Bhopal (April 2026). Validated on a Jetson Orin Nano UAV against the KAIST VIO benchmark and a custom hovering flight dataset."),
    ("droid-slam", "project-8.svg", "DROID-SLAM on OAK-D", "PUBLIC REPO",
     "Real-time visual SLAM from a live OAK-D camera",
     ["fork of DROID-SLAM", "live OAK-D demo"],
     "My fork of DROID-SLAM (Teed and Deng) that adds a real-time demo driven by a live OAK-D camera stream."),
]


def card(slug, emb, title, status, tagline, items, alt):
    chip_svg, bottom = chips(items, 172, 118, 700, 15)
    h = bottom + 22
    body = (
        f'<rect x="2" y="2" width="716" height="{h - 4}" rx="14" fill="{P["panel"]}" stroke="{P["line"]}" stroke-width="2"/>'
        f'<g transform="translate(22,{(h - 120) / 2:.0f}) scale(0.75)">{EMBLEMS[emb]}</g>'
        f'<text x="172" y="38" font-family="{SANS}" font-size="12" letter-spacing="2.5" fill="{P["amber"]}" font-weight="600">{escape(status)}</text>'
        f'<text x="172" y="72" font-family="{SANS}" font-size="28" font-weight="700" fill="{P["text"]}">{escape(title)}</text>'
        f'<text x="172" y="98" font-family="{SANS}" font-size="17" fill="{P["muted"]}">{escape(tagline)}</text>'
        + chip_svg
    )
    write(f"card-{slug}.svg", svg(720, h, title, alt, body))


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
            f'<rect x="2" y="2" width="716" height="106" rx="14" fill="{P["panel"]}" stroke="{P["line"]}" stroke-width="2"/>'
            f'<rect x="2" y="2" width="8" height="106" rx="3" fill="{c}"/>'
            f'<text x="30" y="40" font-family="{SANS}" font-size="24" font-weight="700" fill="{P["text"]}">{escape(org)}</text>'
            f'<text x="30" y="66" font-family="{SANS}" font-size="17" fill="{P["muted"]}">{escape(role)}</text>'
            f'<text x="30" y="92" font-family="{SANS}" font-size="15" fill="{P["muted"]}" opacity="0.85">{escape(line)}</text>'
            f'<text x="696" y="34" text-anchor="end" font-family="{SANS}" font-size="12" letter-spacing="2.5" fill="{P["amber"]}" font-weight="600">{escape(tag)}</text>'
        )
        write(f"{slug}.svg", svg(720, 110, f"{org}, {role}", alt, body))


SKILLS = [
    ("ML & DEEP LEARNING", P["teal"], ["PyTorch", "TabM", "LSTM", "Transformers", "Continual learning", "Federated learning", "RL (PPO)", "Object detection"]),
    ("ROBOTICS", P["amber"], ["VIO: OpenVINS, MSCKF, EKF", "Visual SLAM", "GNSS-denied navigation", "PyBullet", "Adaptive control", "ROS 2", "Drone + edge hardware"]),
    ("GENAI & NLP", P["teal"], ["LangGraph", "Hybrid RAG", "Agent guardrails", "AWS Bedrock", "Whisper"]),
    ("LANGUAGES", P["muted"], ["Python", "C++", "TypeScript", "Rust"]),
    ("DEPLOYMENT", P["muted"], ["FastAPI", "TensorRT FP16", "Jetson Nano / Orin Nano", "ArduPilot", "pytest + mutmut"]),
]


def skills():
    body, y = "", 8
    for label, color, items in SKILLS:
        body += f'<text x="4" y="{y + 12}" font-family="{SANS}" font-size="12" letter-spacing="3" font-weight="700" fill="{color}">{escape(label)}</text>'
        c, bottom = chips(items, 2, y + 22, 716, 15, color)
        body += c
        y = bottom + 20
    alt = "Skills. " + " ".join(f"{l.title()}: {', '.join(i)}." for l, _, i in SKILLS)
    write("skills.svg", svg(720, y, "Skills", alt, body))



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
    for f in os.listdir(OUT):
        os.remove(os.path.join(OUT, f))
    banner()
    for i, s in enumerate(SECTIONS, 1):
        section(i, s)
    emblems()
    for c in CARDS:
        card(*c)
    stats()
    experience()
    skills()
    footer()
    print("wrote", len(os.listdir(OUT)), "files to", os.path.normpath(OUT))
