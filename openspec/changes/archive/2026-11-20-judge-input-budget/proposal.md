# The judge's input is bounded and its unchanging part comes first

## Why

On run `s4-waltzman-4` each judge prompt was about 285,000 tokens (1,190,699 characters) and no part of it was read
from the provider's cache (world-substrate#473; VPS `llm_calls` row 24925). PR #478 grouped pass 1, which brought it to
77,659 characters, but two causes remained:

- The judge read every thing's current values in the world text (10,005 of its 28,015 characters on that world), and
  each failed check once per distinct value (46 entries for one move), so the prompt still grew with the world's
  bindings rather than with its moves and checks.
- The system message named the person trying (character 105) and held the step's instructions (character 6,919),
  ahead of the document, so no two judge calls shared a leading part and nothing was cached.

No requirement stated a size, and every judge test used the two-person port world, so the checks could not catch it.

Source: Brian, 2026-11-20: "ia pprove your recommendations" (decision 1: the judge reads only what concerns the
attempt; a requirement that the judge's input stays under 20,000 tokens for the largest saved world, tested on the
Waltzman run; the prompt ordered so caching works). Earlier: "i dont understand why we would be giving the judges
285,0000 tokens for these tiny simulations. this obviosuly wont scale" (2026-11-20).

## What changes

- Pass 1 as the judge reads it gives each failed check once, by its label, with how many bindings it stopped and at
  most three example values; moves drop the engine's bookkeeping fields.
- The world text lists every thing by id, label and kinds; current values come from pass 1 (the person trying and
  each person and thing named). The world text holds no revision number, so it is the same for every judge call while
  the installed rules stay the same.
- `prompts/judge_steps.yaml`: the system message names no person and holds no step branch; the person and the step's
  instructions are a last user message after the document.
- A new requirement with two scenarios: the judge's first prompt on the Waltzman world stays under 20,000 tokens, and
  the system message and world are the same leading text of every judge call.

Measured on `s4-waltzman-4` (country-a's attempt, today's code): 44,067 characters, about 10,500 tokens at 4.2
characters a token (call 24925: prompt tokens over characters).
