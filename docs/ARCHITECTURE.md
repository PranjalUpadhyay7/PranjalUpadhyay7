# Architecture

- README.md: all substantive text; images are decoration with alt text.
- tools/build_assets.py: one function per asset family (banner, section, emblems, footer); `svg()` wraps title/desc/opaque background; `write()` asserts < 40 KB. System font stacks only, no scripts, no animation, no external references.
- assets/: generated output (committed so GitHub can serve it).
- Extend: add a section to SECTIONS or a call to emblem(); keep the viewBox and opaque background.
- Test: parse each SVG, render in a browser at 1200 and 400 px, POST README.md to GitHub's markdown API and compare tags.
