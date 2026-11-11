# Trace read

Run: the port world (`tests/judge_worlds.py` `port_two_traders()`), 4 rounds, policy `resident`, judge rulings
setting `wait`, owner allowance, live World Builder after the deploy line "live page matches cab821d2bbcd; backend:
cab821d2bbcd", 2026-11-11 UTC. Rounds 1 and 2 are the live run `hold-2` (share `qlKA3Wp9v3kp`, the same rounds that
begin `../wait-approve`); rounds 3 and 4 were played from its state by `play.py wait-reject --branch hold-2.json:2`,
sending the owner's "Reject R1" with round 3. Share `iKefhnd6zOkc`
(`https://brianmills.dev/world-builder/?run=iKefhnd6zOkc`).

Four run-log lines, `run-log.jsonl`, trace ids `world-builder-live/run/e951e418d2a8405e980262a192bd3821` (round 1),
`world-builder-live/run/7c531ab69e5d47b0af396a8cc37b116b` (round 2),
`world-builder-live/run/0642b5322a3044c7a25b09642184f8c1` (round 3) and
`world-builder-live/run/710da999002049b2a2fbd94f8180e22c` (round 4). Measured cost $0.000626 + $0.002075 + $0.001386
+ $0.001439 = $0.005526. `earlier-tries.jsonl` holds the first live `wait-hold` try (`hold-1`, traces
`3f0a9e768e454743b99db8a164541938` and `976554be2d49417b97efe4e01356975c`, $0.004268, share `O_IP_E3-HP_i`).

I read every round in the `/run` responses and the owner decision lines, and from the server's call log the judge
calls of rounds 3 and 4 and the round 4 resident calls in full.

## Findings

- **A4 case 2, reject side, holds live.** With round 3 the owner rejected R1: `{"ruling_id": "R1", "decision":
  "rejected", "installed": false}`, and Ines's held attempt was refused with "the ruling R1 (Accept a handover of
  coins from the named trader.) was rejected". Nothing was installed and no coins moved in rounds 3 and 4 (Ines 30,
  Rosa 0, Vik 40).
- **A later attempt of the same kind is refused naming the rejected ruling, judge not asked.** Round 4 Ines tried the
  handover again; status `refused_ruling`, event `r4-pending-ines`, ruling `{"id": "R1", "state": "rejected"}`. Her
  resident's belief shows she read why: "refused because its proposed rule was not approved". Round 4's one judge call
  was for Vik's question, not for Ines.
- **The judge answered Vik's questions without writing a rule** (rounds 3 and 4, `no_rule`): "Asking it changes nothing
  in the world; Rosa's answer is her choice." Right: a question is words.
- **The earlier try `hold-1`** withdrew Vik's round 1 ruling ("transfers Vik's coins on Rosa's move alone") and held a
  giver-side `hand-coins` rule for Ines in round 2: the held path worked there too.

## Round 1

- Vik (`vik`) tried "I approach Rosa at the customs desk, hold out my 40 coins, and ask her to sign the release for my
  crate without inspecting it.": `sign-release`, `precondition_failed`, r1-e00001. Ines and Rosa waited.
- Trace `world-builder-live/run/e951e418d2a8405e980262a192bd3821`: 1 interpreter, 3 resident calls.

## Round 2

- Ines (`ines`) tried "I hand Rosa 10 coins from my purse at the customs desk.": `unsupported_action`, r2-e00001; judge
  `confirmed`; R1 `accept-coin-handover` held; attempt `pending`.
- Vik (`vik`) tried "I declare my crate at the customs desk.": `declare-crate`, `accepted`, r2-e00002. Rosa waited.
- Trace `world-builder-live/run/7c531ab69e5d47b0af396a8cc37b116b`: 2 interpreter, 3 resident, 2 judge calls.

## Round 3

- Owner decision sent with this round: Reject R1; Ines's held attempt refused naming R1.
- Vik (`vik`) tried "I ask Rosa at the customs desk whether she can release my declared crate today without
  inspecting it.": `unsupported_action`, asks rosa, r3-e00001; judge `no_rule`.
- Ines and Rosa waited. Trace `world-builder-live/run/0642b5322a3044c7a25b09642184f8c1`: 1 interpreter, 3 resident,
  1 judge call.

## Round 4

- Ines (`ines`) tried "I hand Rosa 10 coins from my purse at the customs desk.": `refused_ruling` (R1 rejected),
  r4-pending-ines.
- Rosa (`rosa`) tried "I inspect Vik's crate at the customs desk.": `inspect-crate`, `accepted`, r4-e00001.
- Vik (`vik`) tried "I ask Rosa at the customs desk to inspect my declared crate.": `unsupported_action`, asks rosa,
  r4-e00002; judge `no_rule`.
- Trace `world-builder-live/run/710da999002049b2a2fbd94f8180e22c`: 3 interpreter, 3 resident, 1 judge call.
