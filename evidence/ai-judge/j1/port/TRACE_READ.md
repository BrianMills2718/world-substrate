# Trace read

Run: the port world (`tests/judge_worlds.py` `port()`, the AI judge plan's canonical example), 3 rounds, policy
`resident` (open attempts on), owner allowance, posted by `post_port.py` to a local World Builder service running
the J1 branch (`feat/judge-j1`), 2026-11-10. One run-log line, `run-log.jsonl`; its one llm_client trace id is
`world-builder-live/run/0b8584250e124b2bbfa58d7494e98a32` (resident and interpreter calls share it). Measured cost:
`cost_usd` 0.002049 in the run-log line. `reaction_limit` is null (no cap, J0). Vik's and Rosa's briefs are in the
request. `pass-two.json` holds pass 2 of the coin rule on the world as it stood at Vik's offer (`pass_two.py`, free).

I read every round's request, each person's belief, expectation, reasoning, wanted and did move, status, event id,
and every pass 1 record in full.

## Findings

- **Pass 1 is recorded with every unmatched attempt (3 of 3).** Each `unsupported_action` row carries
  `consequence.pass_one`: the moves of the person acting and of each person the attempt names, every check with its
  value, and the values of everyone and everything named. Vik's offer (r2-e00004) names `rosa`, `customs-desk` and
  `crate`; pass 1 lists Vik's moves and Rosa's, and gives Vik's purse (40 coins), Rosa's (0), the crate's cargo
  (inspected, declared, not released) and the desk.
- **A person's moves appear only on their own page.** At Vik's offer, Rosa's page shows `sign-release` available
  (the crate is inspected: true; the release is not signed yet: false) and `inspect-crate` blocked ("the crate is
  not inspected yet", actual true); Vik's page shows only his own `declare-crate`, blocked (already declared). So
  the A2 line "sign release: blocked, inspected is false" did not arise in this run: Rosa had inspected the crate in
  round 1 (r1-e00001) before Vik offered coins. The J2 port run needs the offer before any inspection.
- **The interpreter's `names` work on live replies.** All three unmatched readings list only ids in the world and
  leave out the speaker: Vik's offer `[rosa, customs-desk, crate]` with `asks: rosa`; Rosa's refusal `[vik, crate]`;
  Vik's "I take my released crate ... and leave the port" `[crate, customs-desk]`. A place named in the words
  (`customs-desk`) is included; pass 1 gives its values and no moves (it is not a person).
- **Pass 2 of the coin rule on this run's state (pass-two.json).** The rule passes the rules check; test-run from
  revision 2 with Vik handing Rosa 40 coins, it moves Rosa's coins 0 to 40 and Vik's 40 to 0, with no blocker and a
  chain of length 0, stopped as settled. The real run's world was not touched (pass 2 runs on a copy).
- **The request reached the person asked.** Rosa's round 3 belief says "Vik has offered me 40 coins, but I have
  not accepted them", and she refuses in her own words; the existing request routing (#326) did that. No judge is
  asked in J1: every unmatched attempt changes nothing.
- **Something to carry into J2.** Rosa signed the release in round 2 (r2-e00005) for her own stated reason ("The
  crate is declared and inspected"), in the same round as Vik's offer; Vik's round 3 belief reads it as "Rosa
  signed the release after I offered to pay her". That is Vik's belief, not a recorded cause: the engine records
  r2-e00005's cause as Rosa's own move.

## Round 1

- Rosa (`rosa`) tried `inspect-crate` on the crate: accepted, r1-e00001 ("My role is to sign releases, so I should check
  this undeclared cargo first.").
- Vik (`vik`) tried `declare-crate` on the crate: accepted, r1-e00003 (retried once at revision 1 after Rosa committed
  first). His belief already names the goal from his brief: release today without inspection, willing to pay.

## Round 2

- Vik (`vik`) tried "I offer Rosa 40 coins at the customs desk and ask her to release my crate.": no rule covers it,
  recorded `unsupported_action`, r2-e00004, nearest kind `sign-release`, `asks: rosa`, names
  `[rosa, customs-desk, crate]`; pass 1 recorded (Vik: `declare-crate` blocked; Rosa: `sign-release` available,
  `inspect-crate` blocked).
- Rosa (`rosa`) tried `sign-release` on the crate: accepted, r2-e00005 ("The crate is declared and inspected, so I can
  sign its inspection release.").

## Round 3

- Rosa (`rosa`) tried "At the customs desk, I tell Vik, 'I refuse your 40 coins. Your crate has already been released.'":
  `unsupported_action`, r3-e00006, names `[vik, crate]`; pass 1 recorded (Rosa: `inspect-crate` and
  `sign-release` blocked; Vik: `declare-crate` blocked).
- Vik (`vik`) tried "I take my released crate from the customs desk and leave the port.": `unsupported_action`, r3-e00007,
  names `[crate, customs-desk]`; pass 1 recorded (Vik: `declare-crate` blocked).
