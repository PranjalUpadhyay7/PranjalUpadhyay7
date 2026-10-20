# User manual

This repo is a GitHub profile README. Preview: open README.md on GitHub (assets are referenced by relative path, so they only render with the assets/ folder).
Change colours: edit the palette dict `P` in tools/build_assets.py, then `python3 tools/build_assets.py` (Python 3, no dependencies). Edit card text in the CARDS list. Commit the regenerated assets/
Troubleshooting: an image missing on GitHub usually means invalid XML; check with `python3 -c "import xml.dom.minidom as m;m.parse('assets/x.svg')"`.
