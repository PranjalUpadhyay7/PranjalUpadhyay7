#!/usr/bin/env python3
"""Render GIFs of the animated SVGs (frames are seeked, not recorded).

Needs google-chrome and ImageMagick `convert` on PATH. Run after build_assets.py:
    python3 tools/make_gifs.py
"""
import os
import subprocess
import tempfile

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
ASSETS = os.path.join(ROOT, "assets")


def frame(svg_text, w, h, t, out):
    """Screenshot svg_text with every animation paused at t seconds."""
    seek = f"<style>*{{animation-play-state:paused!important;animation-delay:-{t}s!important}}</style>"
    svg = svg_text.replace("</svg>", seek + "</svg>")
    html = f"<body style='margin:0;background:#0B1020'>{svg}"
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(html)
    subprocess.run(
        ["google-chrome", "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
         f"--screenshot={out}", f"--window-size={w},{h}", "file://" + f.name],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.unlink(f.name)


def gif(name, w, h, times, delays, resize, colors=64):
    text = open(os.path.join(ASSETS, f"{name}.svg"), encoding="utf-8").read()
    with tempfile.TemporaryDirectory() as d:
        files = []
        for i, t in enumerate(times):
            p = os.path.join(d, f"{i:03d}.png")
            frame(text, w, h, t, p)
            files += ["-delay", str(delays[i]), p]
        out = os.path.join(ASSETS, f"{name}.gif")
        subprocess.run(["convert", *files, "-resize", f"{resize}x", "-layers", "Optimize",
                        "-colors", str(colors), "-loop", "0", out], check=True)
    print(name, os.path.getsize(out) // 1024, "KB")


if __name__ == "__main__":
    # banner: trace draws over 3.2 s, then holds on the finished frame
    ts = [round(i * 0.2, 1) for i in range(17)] + [3.4]
    gif("banner", 1200, 340, ts, [20] * 16 + [20, 300], 900)
