# Architecture

- README.md: banner, stat strip, one short paragraph, linked cards, collapsed measurement notes. Every image has full alt text; links are real text.
- tools/build_assets.py: generator. Families: banner, section bars, stats strip, CARDS (project cards built from the EMBLEMS drawings plus chip rows), experience cards, skills chip map, footer. `svg()` wraps title/desc/opaque background; `write()` asserts < 40 KB; `chips()` flows rounded chips with wrapping. Running it clears assets/ first.
- assets/: generated output, committed so GitHub can serve it.
- Extend: add a tuple to CARDS (slug, emblem file, title, status, tagline, chips, alt) and an <img> in README.md.
- Test: parse every SVG, render in headless Chrome at 720 px and phone width, POST README.md to GitHub's markdown API and compare element counts.
