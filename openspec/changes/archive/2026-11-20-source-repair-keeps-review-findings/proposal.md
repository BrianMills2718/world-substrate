# Proposal: a source repair also passes on the review's rule findings

Plan size: small

## Why

In the s4-waltzman-4 build (2026-11-19, `evidence/declared-laws/s4-waltzman-4/`, issue #474) the independent
review rejected the first try's actor inputs (`ActorInputPrivacyError`) and, in the same reply, found that rules the
description asks for were missing. The build repaired the world definition from the privacy feedback alone
(`guidance = ""`), so the one rewrite never heard the missing-rule findings, and the second try was kept with them.
Brian, 2026-11-20: "go" (fix #474, then a fresh Waltzman run).

## What changes

- `review_rules` keeps the review's rule findings on the error it raises for a rejected source judgment.
- The source repair passes those findings, first, to the rules writer's one rewrite, and the retained rejected try
  records them.
