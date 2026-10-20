# Progress

## Done (2026-10-20, branch readme-refresh)
- tools/build_assets.py -> 17 SVGs in assets/ (banner, 6 section bars, 3 principle + 6 project emblems, footer), each < 4 KB, rendered in headless Chrome at 1200 and 400 px.
- README.md rebuilt (phase 1). GitHub markdown API keeps all HTML used; relative images resolve; links 200 (LinkedIn answers 999 to bots).

## Open conflicts (owner decides)
- AP-Copilot tests: fact sheet 239; repo today 434 passed / 16 skipped. Number left out of README.
- AP-Copilot 20/30 -> 30/30: repo attributes it to RAG-indexer fix, BM25+RRF retrieval, prompt v1.3.0, a recursion fix and an approval-message bug fix (docs/decisions.md 2026-09-30), not to "adding embeddings". README states the numbers without that causal claim.
- Federated "within 2%": ambiguous (relative vs points). Repo not available locally.

## Next
- Phase 2 READMEs in Federated_Learning and dytox_modification (not started; repos are not on this machine).
