# User manual

This repo is a GitHub profile README. Preview: open README.md on GitHub (assets are referenced by relative path, so they only render with the assets/ folder).
Change colours: edit the palette dict `P` in tools/build_assets.py, then `python3 tools/build_assets.py` (Python 3, no dependencies). Edit card text in the CARDS list. Commit the regenerated assets/
Troubleshooting: an image missing on GitHub usually means invalid XML; check with `python3 -c "import xml.dom.minidom as m;m.parse('assets/x.svg')"`.
GIFs: after build_assets.py run `python3 tools/make_gifs.py` (needs google-chrome and ImageMagick `convert`). It rewrites assets/banner.gif and assets/dialogue.gif.
Stats: assets/github-stats.svg is refreshed daily by .github/workflows/update-stats.yml. Run it once by hand after merging: Actions tab, update-stats, Run workflow. Local test: `GITHUB_TOKEN=<token> python3 tools/update_stats.py`.
