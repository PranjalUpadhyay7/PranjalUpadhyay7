# Mistakes

## M-001 Duplicate SVG attribute (2026-10-20)
What: three emblems had `fill=` twice (a helper already emitted fill="none"), so the XML was invalid and the images did not render.
Root cause: composing attribute strings from helpers without checking the result.
Fix: helper takes a fill parameter. Rule: parse every generated SVG with an XML parser and render it, never trust it unseen.

## M-002 Banner trace crossed the text (2026-10-20)
What: the loss-curve ran through the name and tagline. Caught by looking at the render.
Rule: position decorative traces in a region the text does not occupy, then view the render.

## M-003 zsh expands `====WORD` (2026-10-20)
What: `echo ====DYTOX` aborted a command chain. Rule: quote echo separators.
