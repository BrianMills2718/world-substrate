# Trace read

Run: the port world (`tests/judge_worlds.py` `port_two_traders()`), 4 rounds, policy `resident`, judge rulings
setting `wait` (a confirmed ruling is held until the owner answers), owner allowance, live World Builder after the
deploy line "live page matches cab821d2bbcd; backend: cab821d2bbcd", 2026-11-11 UTC. Rounds 1 and 2 are the live
run `hold-2` (`play.py wait-hold`, share `qlKA3Wp9v3kp`); rounds 3 and 4 were played from its state by
`play.py wait-approve --branch hold-2.json:2`, sending the owner's "Approve R1" with round 3. Share `F_ND9bo29lvp`
(`https://brianmills.dev/world-builder/?run=F_ND9bo29lvp`). The same rounds 1 and 2 begin `../wait-reject`.

Four run-log lines, `run-log.jsonl`, trace ids `world-builder-live/run/e951e418d2a8405e980262a192bd3821` (round 1),
`world-builder-live/run/7c531ab69e5d47b0af396a8cc37b116b` (round 2),
`world-builder-live/run/63f090835708477e806c45e58214c8e4` (round 3) and
`world-builder-live/run/fdd44d0e55a247b99f5060642f16f08c` (round 4). Measured cost $0.000626 + $0.002075 + $0.000989
+ $0.000938 = $0.004628.

I read every round in the `/run` responses (attempt, interpretation, status, event id, values, the ruling and its
attempts list, the owner decision lines), and from the server's call log the two judge calls of round 2 and all
resident and interpreter calls of rounds 3 and 4 in full.

## Findings

- **A4 case 2 holds live: held, then approved, then the queued attempt goes on.** Round 2 the judge confirmed a rule
  for Ines's handover and, under `wait`, R1 `accept-coin-handover` was held: Ines's attempt is `pending` and her coins
  did not move. With round 3 the owner approved R1: the decision lines read `{"ruling_id": "R1", "decision":
  "approved", "installed": true}` and Ines's held attempt `routed` to Rosa. Rosa, who now saw the move, took it
  (r3-e00002): Ines 30 to 20, Rosa 0 to 10.
- **The approved rule let Ines take Vik's coins without any offer from him (round 4, r4-e00001).** The judge wrote the
  receiver's move: "Accept a handover of coins from the named trader", checks only that the named trader has the
  coins and is at the same place. Nothing in the world records an offer, so once installed the move is listed to
  every person for every trader: Ines's round 4 page listed "accept-coin-handover: recipient vik, amount 10 [effects:
  vik ... subtract 10; ines ... add 10]". Her resident wrote "accepting Vik's offered coins is the available action";
  Vik had offered nothing. Vik 40 to 30, Ines 20 to 30. The review (call 2 of round 2) had confirmed the rule saying
  "Rosa is the actor, so the transfer correctly depends on her choice"; it did not consider the giver's choice.
  In the other live tries the review withdrew this same shape three times for exactly that reason (see
  `../install-default` and `../wait-reject`). Recorded as open question Q96; the owner's Approve is today the only
  guard in `wait` mode, and in `create` mode nothing guards it.
- **Ines's own round 3 try failed on the receiver rule** (r3-e00001, `precondition_failed`): she read "I hand Rosa 10
  coins" as `accept-coin-handover` naming Rosa as the trader, and Rosa is an officer with 0 coins. The interpreter
  matched the giver's words to the receiver's move.

## Round 1

- Vik (`vik`) tried "I approach Rosa at the customs desk, hold out my 40 coins, and ask her to sign the release for my
  crate without inspecting it.": `sign-release`, `precondition_failed`, r1-e00001. Ines and Rosa waited.
- Trace `world-builder-live/run/e951e418d2a8405e980262a192bd3821`: 1 interpreter, 3 resident calls.

## Round 2

- Ines (`ines`) tried "I hand Rosa 10 coins from my purse at the customs desk.": `unsupported_action`, r2-e00001;
  judge `confirmed`, whose choice `rosa`, R1 held, attempt `pending`. The judge's propose call returned the rule and
  test move `rosa accept-coin-handover recipient ines amount 10`; the test run moved 10 coins, review `confirm`.
- Vik (`vik`) tried "I declare my crate at the customs desk.": `declare-crate`, `accepted`, r2-e00002.
- Rosa waited. Trace `world-builder-live/run/7c531ab69e5d47b0af396a8cc37b116b`: 2 interpreter, 3 resident, 2 judge calls.

## Round 3

- Owner decision sent with this round: Approve R1; R1 installed; Ines's queued attempt routed to Rosa.
- Ines (`ines`) tried "I hand Rosa 10 coins from my purse at the customs desk.": `accept-coin-handover` recipient rosa,
  `precondition_failed`, r3-e00001.
- Rosa (`rosa`) tried "I accept 10 coins from Ines at the customs desk.": `accept-coin-handover` recipient ines,
  `accepted`, r3-e00002 (Ines 20, Rosa 10).
- Vik waited. Trace `world-builder-live/run/63f090835708477e806c45e58214c8e4`: 2 interpreter, 3 resident calls, no judge.

## Round 4

- Ines (`ines`) tried "I accept 10 coins from Vik at the customs desk.": `accept-coin-handover` recipient vik,
  `accepted`, r4-e00001 (Vik 40 to 30, Ines 20 to 30). Decided by R1, judge not asked.
- Rosa and Vik waited (Vik: "accepting Ines's coins would not address the inspection requirement").
- Trace `world-builder-live/run/fdd44d0e55a247b99f5060642f16f08c`: 1 interpreter, 3 resident calls.
