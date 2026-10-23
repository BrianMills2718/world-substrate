# Trace read: c4-run21

C4 live run: "a pencil logistics and supply network" typed on the live page with the owner allowance,
2026-10-23 ~03:57Z, at live commit 9bfa8d3. Share link `NVZGnhM87Yj1` (28 rounds shown; the page sent 29 /run).
31 server rows, all status 200, $0.0117 (the build only; rounds cost $0). How it was read: every round's eight
actors (move wanted, move done, event id) and every world event, from the run-log rows dumped round by round,
plus the Engine changes of round 10 opened in full.

## Findings

**Verdict: PASS C4.** Built as things: 10 entities, 7 actions (harvest-logs, cut-wood-slats, prepare-graphite,
assemble-pencils, deliver-pencils, place-pencil-order, sell-pencil), no people briefs. It ran 29 rounds. All
eight actors act by round 6, and every round from 6 to 29 has 8 different moves. It is a real chain: in round 10
r10-e00011 moves logs forest->mara, r10-e00013 logs->slats at noah, r10-e00007 graphite mine->gia, r10-e00005
graphite+slats->pencils at eli, r10-e00015 pencil eli->lee, r10-e00009 pencil lee->ava. Readout 13 of 13
claims match the trace (c1r/c2check.py).

These moves are made by the scripted mover ("chose the allowed move it had done least recently"), not AI
people. That is how a things world runs; it is not presented as AI.

Weaknesses (not fixed here):
- Selling never reduces `orders_waiting` (2 -> 87 over 29 rounds): the sell rule does not touch orders.
- Lee always sells to ava; ben orders every round and is never served.

## Build and readout traces

- `/generate-world` 2026-10-23T03:58:23Z $0.0097: `world-builder-live/kind/922bbce9bab9458d9ce87af672fffc65`, `world-builder-live/world/e2ba2ca09cab4557aa5dce8ec36cdd72`
- `/readout` 2026-10-23T03:59:32Z $0.0020: `world-builder-live/readout/5ed97edd18be4e4397374a37e4a7caeb`

## Round 1

Trace `world-builder-live/run/3956ec03053b40bcac87fc124c61b3b2`, $0.0000.

Read: Customers ava and ben place orders (r1-e00001/03); the other six have no allowed move yet (stock is empty). Rules: forest-regrowth r1-e00004 and mine-renewal r1-e00005 add raw goods; customer-demand r1-e00006 adds an order.

- ava: accepted r1-e00001 did=place-pencil-order
- ben: accepted r1-e00003 did=place-pencil-order

World events: r1-e00001, r1-e00002, r1-e00003, r1-e00004, r1-e00005, r1-e00006

## Round 2

Trace `world-builder-live/run/5aee8c4e30cd4c70bdb401eb677bc7d8`, $0.0000.

Read: Gia prepares graphite (r2-e00005) and mara harvests logs (r2-e00007) from the renewed stock; eli, lee, noah, sam still have nothing allowed.

- ava: accepted r2-e00001 did=place-pencil-order
- ben: accepted r2-e00003 did=place-pencil-order
- gia: accepted r2-e00005 did=prepare-graphite
- mara: accepted r2-e00007 did=harvest-logs

World events: r2-e00001, r2-e00002, r2-e00003, r2-e00004, r2-e00005, r2-e00006, r2-e00007, r2-e00008, r2-e00009, r2-e00010

## Round 3

Trace `world-builder-live/run/df7d1be8267a4474b51152257e29f7db`, $0.0000.

Read: Noah cuts slats from mara's logs (r3-e00009); the chain reaches the sawmill.

- ava: accepted r3-e00001 did=place-pencil-order
- ben: accepted r3-e00003 did=place-pencil-order
- gia: accepted r3-e00005 did=prepare-graphite
- mara: accepted r3-e00007 did=harvest-logs
- noah: accepted r3-e00009 did=cut-wood-slats

World events: r3-e00001, r3-e00002, r3-e00003, r3-e00004, r3-e00005, r3-e00006, r3-e00007, r3-e00008, r3-e00009, r3-e00010, r3-e00011, r3-e00012

## Round 4

Trace `world-builder-live/run/bec05b1691204817abc388eb6efd0972`, $0.0000.

Read: Eli assembles pencils from gia's graphite and noah's slats (r4-e00005).

- ava: accepted r4-e00001 did=place-pencil-order
- ben: accepted r4-e00003 did=place-pencil-order
- eli: accepted r4-e00005 did=assemble-pencils
- gia: accepted r4-e00007 did=prepare-graphite
- mara: accepted r4-e00009 did=harvest-logs
- noah: accepted r4-e00011 did=cut-wood-slats

World events: r4-e00001, r4-e00002, r4-e00003, r4-e00004, r4-e00005, r4-e00006, r4-e00007, r4-e00008, r4-e00009, r4-e00010, r4-e00011, r4-e00012, r4-e00013, r4-e00014

## Round 5

Trace `world-builder-live/run/387e893fbab04fe1b04d98216121f8da`, $0.0000.

Read: Sam delivers eli's pencils to lee (r5-e00013); only lee still waits.

- ava: accepted r5-e00001 did=place-pencil-order
- ben: accepted r5-e00003 did=place-pencil-order
- eli: accepted r5-e00005 did=assemble-pencils
- gia: accepted r5-e00007 did=prepare-graphite
- mara: accepted r5-e00009 did=harvest-logs
- noah: accepted r5-e00011 did=cut-wood-slats
- sam: accepted r5-e00013 did=deliver-pencils

World events: r5-e00001, r5-e00002, r5-e00003, r5-e00004, r5-e00005, r5-e00006, r5-e00007, r5-e00008, r5-e00009, r5-e00010, r5-e00011, r5-e00012, r5-e00013, r5-e00014, r5-e00015, r5-e00016

## Round 6

Trace `world-builder-live/run/a8e409afffc546c0a34f3090cffdcc6f`, $0.0000.

Read: Lee sells a pencil to ava (r6-e00009): all eight act, eight different moves. From here every round is the full chain once.

- ava: accepted r6-e00001 did=place-pencil-order
- ben: accepted r6-e00003 did=place-pencil-order
- eli: accepted r6-e00005 did=assemble-pencils
- gia: accepted r6-e00007 did=prepare-graphite
- lee: accepted r6-e00009 did=sell-pencil
- mara: accepted r6-e00011 did=harvest-logs
- noah: accepted r6-e00013 did=cut-wood-slats
- sam: accepted r6-e00015 did=deliver-pencils

World events: r6-e00001, r6-e00002, r6-e00003, r6-e00004, r6-e00005, r6-e00006, r6-e00007, r6-e00008, r6-e00009, r6-e00010, r6-e00011, r6-e00012, r6-e00013, r6-e00014, r6-e00015, r6-e00016, r6-e00017, r6-e00018

## Round 7

Trace `world-builder-live/run/af2647aadd4f4729b2c44b926b85bcff`, $0.0000.

Read: Same full chain as round 6, every move changing stock (e.g. r7-e00005 assemble moves graphite and slats into pencils, r7-e00015 deliver moves a pencil from eli to lee, r7-e00009 lee sells to ava). Orders waiting keep rising by 3 (r7-e00018): selling never reduces them, and ben is never sold to.

- ava: accepted r7-e00001 did=place-pencil-order
- ben: accepted r7-e00003 did=place-pencil-order
- eli: accepted r7-e00005 did=assemble-pencils
- gia: accepted r7-e00007 did=prepare-graphite
- lee: accepted r7-e00009 did=sell-pencil
- mara: accepted r7-e00011 did=harvest-logs
- noah: accepted r7-e00013 did=cut-wood-slats
- sam: accepted r7-e00015 did=deliver-pencils

World events: r7-e00001, r7-e00002, r7-e00003, r7-e00004, r7-e00005, r7-e00006, r7-e00007, r7-e00008, r7-e00009, r7-e00010, r7-e00011, r7-e00012, r7-e00013, r7-e00014, r7-e00015, r7-e00016, r7-e00017, r7-e00018

## Round 8

Trace `world-builder-live/run/d0aa0c695b734678b6bf03a59f671a13`, $0.0000.

Read: Same full chain as round 6, every move changing stock (e.g. r8-e00005 assemble moves graphite and slats into pencils, r8-e00015 deliver moves a pencil from eli to lee, r8-e00009 lee sells to ava). Orders waiting keep rising by 3 (r8-e00018): selling never reduces them, and ben is never sold to.

- ava: accepted r8-e00001 did=place-pencil-order
- ben: accepted r8-e00003 did=place-pencil-order
- eli: accepted r8-e00005 did=assemble-pencils
- gia: accepted r8-e00007 did=prepare-graphite
- lee: accepted r8-e00009 did=sell-pencil
- mara: accepted r8-e00011 did=harvest-logs
- noah: accepted r8-e00013 did=cut-wood-slats
- sam: accepted r8-e00015 did=deliver-pencils

World events: r8-e00001, r8-e00002, r8-e00003, r8-e00004, r8-e00005, r8-e00006, r8-e00007, r8-e00008, r8-e00009, r8-e00010, r8-e00011, r8-e00012, r8-e00013, r8-e00014, r8-e00015, r8-e00016, r8-e00017, r8-e00018

## Round 9

Trace `world-builder-live/run/ceec329bf7614790adea246a48471c0e`, $0.0000.

Read: Same full chain as round 6, every move changing stock (e.g. r9-e00005 assemble moves graphite and slats into pencils, r9-e00015 deliver moves a pencil from eli to lee, r9-e00009 lee sells to ava). Orders waiting keep rising by 3 (r9-e00018): selling never reduces them, and ben is never sold to.

- ava: accepted r9-e00001 did=place-pencil-order
- ben: accepted r9-e00003 did=place-pencil-order
- eli: accepted r9-e00005 did=assemble-pencils
- gia: accepted r9-e00007 did=prepare-graphite
- lee: accepted r9-e00009 did=sell-pencil
- mara: accepted r9-e00011 did=harvest-logs
- noah: accepted r9-e00013 did=cut-wood-slats
- sam: accepted r9-e00015 did=deliver-pencils

World events: r9-e00001, r9-e00002, r9-e00003, r9-e00004, r9-e00005, r9-e00006, r9-e00007, r9-e00008, r9-e00009, r9-e00010, r9-e00011, r9-e00012, r9-e00013, r9-e00014, r9-e00015, r9-e00016, r9-e00017, r9-e00018

## Round 10

Trace `world-builder-live/run/4ce38492b15547a08ef3c68a3508b4c0`, $0.0000.

Read: Same full chain as round 6, every move changing stock (e.g. r10-e00005 assemble moves graphite and slats into pencils, r10-e00015 deliver moves a pencil from eli to lee, r10-e00009 lee sells to ava). Orders waiting keep rising by 3 (r10-e00018): selling never reduces them, and ben is never sold to.

- ava: accepted r10-e00001 did=place-pencil-order
- ben: accepted r10-e00003 did=place-pencil-order
- eli: accepted r10-e00005 did=assemble-pencils
- gia: accepted r10-e00007 did=prepare-graphite
- lee: accepted r10-e00009 did=sell-pencil
- mara: accepted r10-e00011 did=harvest-logs
- noah: accepted r10-e00013 did=cut-wood-slats
- sam: accepted r10-e00015 did=deliver-pencils

World events: r10-e00001, r10-e00002, r10-e00003, r10-e00004, r10-e00005, r10-e00006, r10-e00007, r10-e00008, r10-e00009, r10-e00010, r10-e00011, r10-e00012, r10-e00013, r10-e00014, r10-e00015, r10-e00016, r10-e00017, r10-e00018

## Round 11

Trace `world-builder-live/run/e50cdc068c5a447699fb830593fce44e`, $0.0000.

Read: Same full chain as round 6, every move changing stock (e.g. r11-e00005 assemble moves graphite and slats into pencils, r11-e00015 deliver moves a pencil from eli to lee, r11-e00009 lee sells to ava). Orders waiting keep rising by 3 (r11-e00018): selling never reduces them, and ben is never sold to.

- ava: accepted r11-e00001 did=place-pencil-order
- ben: accepted r11-e00003 did=place-pencil-order
- eli: accepted r11-e00005 did=assemble-pencils
- gia: accepted r11-e00007 did=prepare-graphite
- lee: accepted r11-e00009 did=sell-pencil
- mara: accepted r11-e00011 did=harvest-logs
- noah: accepted r11-e00013 did=cut-wood-slats
- sam: accepted r11-e00015 did=deliver-pencils

World events: r11-e00001, r11-e00002, r11-e00003, r11-e00004, r11-e00005, r11-e00006, r11-e00007, r11-e00008, r11-e00009, r11-e00010, r11-e00011, r11-e00012, r11-e00013, r11-e00014, r11-e00015, r11-e00016, r11-e00017, r11-e00018

## Round 12

Trace `world-builder-live/run/8550d679427b4894bfea769b79f92967`, $0.0000.

Read: Same full chain as round 6, every move changing stock (e.g. r12-e00005 assemble moves graphite and slats into pencils, r12-e00015 deliver moves a pencil from eli to lee, r12-e00009 lee sells to ava). Orders waiting keep rising by 3 (r12-e00018): selling never reduces them, and ben is never sold to.

- ava: accepted r12-e00001 did=place-pencil-order
- ben: accepted r12-e00003 did=place-pencil-order
- eli: accepted r12-e00005 did=assemble-pencils
- gia: accepted r12-e00007 did=prepare-graphite
- lee: accepted r12-e00009 did=sell-pencil
- mara: accepted r12-e00011 did=harvest-logs
- noah: accepted r12-e00013 did=cut-wood-slats
- sam: accepted r12-e00015 did=deliver-pencils

World events: r12-e00001, r12-e00002, r12-e00003, r12-e00004, r12-e00005, r12-e00006, r12-e00007, r12-e00008, r12-e00009, r12-e00010, r12-e00011, r12-e00012, r12-e00013, r12-e00014, r12-e00015, r12-e00016, r12-e00017, r12-e00018

## Round 13

Trace `world-builder-live/run/3d58f7bb0347439e9168b2e06edab2f8`, $0.0000.

Read: Same full chain as round 6, every move changing stock (e.g. r13-e00005 assemble moves graphite and slats into pencils, r13-e00015 deliver moves a pencil from eli to lee, r13-e00009 lee sells to ava). Orders waiting keep rising by 3 (r13-e00018): selling never reduces them, and ben is never sold to.

- ava: accepted r13-e00001 did=place-pencil-order
- ben: accepted r13-e00003 did=place-pencil-order
- eli: accepted r13-e00005 did=assemble-pencils
- gia: accepted r13-e00007 did=prepare-graphite
- lee: accepted r13-e00009 did=sell-pencil
- mara: accepted r13-e00011 did=harvest-logs
- noah: accepted r13-e00013 did=cut-wood-slats
- sam: accepted r13-e00015 did=deliver-pencils

World events: r13-e00001, r13-e00002, r13-e00003, r13-e00004, r13-e00005, r13-e00006, r13-e00007, r13-e00008, r13-e00009, r13-e00010, r13-e00011, r13-e00012, r13-e00013, r13-e00014, r13-e00015, r13-e00016, r13-e00017, r13-e00018

## Round 14

Trace `world-builder-live/run/11aa27c7b2454bfdb0fe3ced77dfb49f`, $0.0000.

Read: Same full chain as round 6, every move changing stock (e.g. r14-e00005 assemble moves graphite and slats into pencils, r14-e00015 deliver moves a pencil from eli to lee, r14-e00009 lee sells to ava). Orders waiting keep rising by 3 (r14-e00018): selling never reduces them, and ben is never sold to.

- ava: accepted r14-e00001 did=place-pencil-order
- ben: accepted r14-e00003 did=place-pencil-order
- eli: accepted r14-e00005 did=assemble-pencils
- gia: accepted r14-e00007 did=prepare-graphite
- lee: accepted r14-e00009 did=sell-pencil
- mara: accepted r14-e00011 did=harvest-logs
- noah: accepted r14-e00013 did=cut-wood-slats
- sam: accepted r14-e00015 did=deliver-pencils

World events: r14-e00001, r14-e00002, r14-e00003, r14-e00004, r14-e00005, r14-e00006, r14-e00007, r14-e00008, r14-e00009, r14-e00010, r14-e00011, r14-e00012, r14-e00013, r14-e00014, r14-e00015, r14-e00016, r14-e00017, r14-e00018

## Round 15

Trace `world-builder-live/run/e330b6da22e349168a4f27c939c35e74`, $0.0000.

Read: Same full chain as round 6, every move changing stock (e.g. r15-e00005 assemble moves graphite and slats into pencils, r15-e00015 deliver moves a pencil from eli to lee, r15-e00009 lee sells to ava). Orders waiting keep rising by 3 (r15-e00018): selling never reduces them, and ben is never sold to.

- ava: accepted r15-e00001 did=place-pencil-order
- ben: accepted r15-e00003 did=place-pencil-order
- eli: accepted r15-e00005 did=assemble-pencils
- gia: accepted r15-e00007 did=prepare-graphite
- lee: accepted r15-e00009 did=sell-pencil
- mara: accepted r15-e00011 did=harvest-logs
- noah: accepted r15-e00013 did=cut-wood-slats
- sam: accepted r15-e00015 did=deliver-pencils

World events: r15-e00001, r15-e00002, r15-e00003, r15-e00004, r15-e00005, r15-e00006, r15-e00007, r15-e00008, r15-e00009, r15-e00010, r15-e00011, r15-e00012, r15-e00013, r15-e00014, r15-e00015, r15-e00016, r15-e00017, r15-e00018

## Round 16

Trace `world-builder-live/run/261f0d77b6e54159a0de596c1896fcd7`, $0.0000.

Read: Same full chain as round 6, every move changing stock (e.g. r16-e00005 assemble moves graphite and slats into pencils, r16-e00015 deliver moves a pencil from eli to lee, r16-e00009 lee sells to ava). Orders waiting keep rising by 3 (r16-e00018): selling never reduces them, and ben is never sold to.

- ava: accepted r16-e00001 did=place-pencil-order
- ben: accepted r16-e00003 did=place-pencil-order
- eli: accepted r16-e00005 did=assemble-pencils
- gia: accepted r16-e00007 did=prepare-graphite
- lee: accepted r16-e00009 did=sell-pencil
- mara: accepted r16-e00011 did=harvest-logs
- noah: accepted r16-e00013 did=cut-wood-slats
- sam: accepted r16-e00015 did=deliver-pencils

World events: r16-e00001, r16-e00002, r16-e00003, r16-e00004, r16-e00005, r16-e00006, r16-e00007, r16-e00008, r16-e00009, r16-e00010, r16-e00011, r16-e00012, r16-e00013, r16-e00014, r16-e00015, r16-e00016, r16-e00017, r16-e00018

## Round 17

Trace `world-builder-live/run/8d1c55ef0ec643129959370eace95bdb`, $0.0000.

Read: Same full chain as round 6, every move changing stock (e.g. r17-e00005 assemble moves graphite and slats into pencils, r17-e00015 deliver moves a pencil from eli to lee, r17-e00009 lee sells to ava). Orders waiting keep rising by 3 (r17-e00018): selling never reduces them, and ben is never sold to.

- ava: accepted r17-e00001 did=place-pencil-order
- ben: accepted r17-e00003 did=place-pencil-order
- eli: accepted r17-e00005 did=assemble-pencils
- gia: accepted r17-e00007 did=prepare-graphite
- lee: accepted r17-e00009 did=sell-pencil
- mara: accepted r17-e00011 did=harvest-logs
- noah: accepted r17-e00013 did=cut-wood-slats
- sam: accepted r17-e00015 did=deliver-pencils

World events: r17-e00001, r17-e00002, r17-e00003, r17-e00004, r17-e00005, r17-e00006, r17-e00007, r17-e00008, r17-e00009, r17-e00010, r17-e00011, r17-e00012, r17-e00013, r17-e00014, r17-e00015, r17-e00016, r17-e00017, r17-e00018

## Round 18

Trace `world-builder-live/run/9d6f68f745984f9e9d0c0521e8d94e99`, $0.0000.

Read: Same full chain as round 6, every move changing stock (e.g. r18-e00005 assemble moves graphite and slats into pencils, r18-e00015 deliver moves a pencil from eli to lee, r18-e00009 lee sells to ava). Orders waiting keep rising by 3 (r18-e00018): selling never reduces them, and ben is never sold to.

- ava: accepted r18-e00001 did=place-pencil-order
- ben: accepted r18-e00003 did=place-pencil-order
- eli: accepted r18-e00005 did=assemble-pencils
- gia: accepted r18-e00007 did=prepare-graphite
- lee: accepted r18-e00009 did=sell-pencil
- mara: accepted r18-e00011 did=harvest-logs
- noah: accepted r18-e00013 did=cut-wood-slats
- sam: accepted r18-e00015 did=deliver-pencils

World events: r18-e00001, r18-e00002, r18-e00003, r18-e00004, r18-e00005, r18-e00006, r18-e00007, r18-e00008, r18-e00009, r18-e00010, r18-e00011, r18-e00012, r18-e00013, r18-e00014, r18-e00015, r18-e00016, r18-e00017, r18-e00018

## Round 19

Trace `world-builder-live/run/1f11e0b6563942638d3b8ab11625c37a`, $0.0000.

Read: Same full chain as round 6, every move changing stock (e.g. r19-e00005 assemble moves graphite and slats into pencils, r19-e00015 deliver moves a pencil from eli to lee, r19-e00009 lee sells to ava). Orders waiting keep rising by 3 (r19-e00018): selling never reduces them, and ben is never sold to.

- ava: accepted r19-e00001 did=place-pencil-order
- ben: accepted r19-e00003 did=place-pencil-order
- eli: accepted r19-e00005 did=assemble-pencils
- gia: accepted r19-e00007 did=prepare-graphite
- lee: accepted r19-e00009 did=sell-pencil
- mara: accepted r19-e00011 did=harvest-logs
- noah: accepted r19-e00013 did=cut-wood-slats
- sam: accepted r19-e00015 did=deliver-pencils

World events: r19-e00001, r19-e00002, r19-e00003, r19-e00004, r19-e00005, r19-e00006, r19-e00007, r19-e00008, r19-e00009, r19-e00010, r19-e00011, r19-e00012, r19-e00013, r19-e00014, r19-e00015, r19-e00016, r19-e00017, r19-e00018

## Round 20

Trace `world-builder-live/run/108d5625c710414897d8c23ff251cbc0`, $0.0000.

Read: Same full chain as round 6, every move changing stock (e.g. r20-e00005 assemble moves graphite and slats into pencils, r20-e00015 deliver moves a pencil from eli to lee, r20-e00009 lee sells to ava). Orders waiting keep rising by 3 (r20-e00018): selling never reduces them, and ben is never sold to.

- ava: accepted r20-e00001 did=place-pencil-order
- ben: accepted r20-e00003 did=place-pencil-order
- eli: accepted r20-e00005 did=assemble-pencils
- gia: accepted r20-e00007 did=prepare-graphite
- lee: accepted r20-e00009 did=sell-pencil
- mara: accepted r20-e00011 did=harvest-logs
- noah: accepted r20-e00013 did=cut-wood-slats
- sam: accepted r20-e00015 did=deliver-pencils

World events: r20-e00001, r20-e00002, r20-e00003, r20-e00004, r20-e00005, r20-e00006, r20-e00007, r20-e00008, r20-e00009, r20-e00010, r20-e00011, r20-e00012, r20-e00013, r20-e00014, r20-e00015, r20-e00016, r20-e00017, r20-e00018

## Round 21

Trace `world-builder-live/run/d7ad186dca53411396c71505e13e0928`, $0.0000.

Read: Same full chain as round 6, every move changing stock (e.g. r21-e00005 assemble moves graphite and slats into pencils, r21-e00015 deliver moves a pencil from eli to lee, r21-e00009 lee sells to ava). Orders waiting keep rising by 3 (r21-e00018): selling never reduces them, and ben is never sold to.

- ava: accepted r21-e00001 did=place-pencil-order
- ben: accepted r21-e00003 did=place-pencil-order
- eli: accepted r21-e00005 did=assemble-pencils
- gia: accepted r21-e00007 did=prepare-graphite
- lee: accepted r21-e00009 did=sell-pencil
- mara: accepted r21-e00011 did=harvest-logs
- noah: accepted r21-e00013 did=cut-wood-slats
- sam: accepted r21-e00015 did=deliver-pencils

World events: r21-e00001, r21-e00002, r21-e00003, r21-e00004, r21-e00005, r21-e00006, r21-e00007, r21-e00008, r21-e00009, r21-e00010, r21-e00011, r21-e00012, r21-e00013, r21-e00014, r21-e00015, r21-e00016, r21-e00017, r21-e00018

## Round 22

Trace `world-builder-live/run/b110776312e14937aea1b393444fb02c`, $0.0000.

Read: Same full chain as round 6, every move changing stock (e.g. r22-e00005 assemble moves graphite and slats into pencils, r22-e00015 deliver moves a pencil from eli to lee, r22-e00009 lee sells to ava). Orders waiting keep rising by 3 (r22-e00018): selling never reduces them, and ben is never sold to.

- ava: accepted r22-e00001 did=place-pencil-order
- ben: accepted r22-e00003 did=place-pencil-order
- eli: accepted r22-e00005 did=assemble-pencils
- gia: accepted r22-e00007 did=prepare-graphite
- lee: accepted r22-e00009 did=sell-pencil
- mara: accepted r22-e00011 did=harvest-logs
- noah: accepted r22-e00013 did=cut-wood-slats
- sam: accepted r22-e00015 did=deliver-pencils

World events: r22-e00001, r22-e00002, r22-e00003, r22-e00004, r22-e00005, r22-e00006, r22-e00007, r22-e00008, r22-e00009, r22-e00010, r22-e00011, r22-e00012, r22-e00013, r22-e00014, r22-e00015, r22-e00016, r22-e00017, r22-e00018

## Round 23

Trace `world-builder-live/run/acc880a4c70b4ad092f7216aa970df0c`, $0.0000.

Read: Same full chain as round 6, every move changing stock (e.g. r23-e00005 assemble moves graphite and slats into pencils, r23-e00015 deliver moves a pencil from eli to lee, r23-e00009 lee sells to ava). Orders waiting keep rising by 3 (r23-e00018): selling never reduces them, and ben is never sold to.

- ava: accepted r23-e00001 did=place-pencil-order
- ben: accepted r23-e00003 did=place-pencil-order
- eli: accepted r23-e00005 did=assemble-pencils
- gia: accepted r23-e00007 did=prepare-graphite
- lee: accepted r23-e00009 did=sell-pencil
- mara: accepted r23-e00011 did=harvest-logs
- noah: accepted r23-e00013 did=cut-wood-slats
- sam: accepted r23-e00015 did=deliver-pencils

World events: r23-e00001, r23-e00002, r23-e00003, r23-e00004, r23-e00005, r23-e00006, r23-e00007, r23-e00008, r23-e00009, r23-e00010, r23-e00011, r23-e00012, r23-e00013, r23-e00014, r23-e00015, r23-e00016, r23-e00017, r23-e00018

## Round 24

Trace `world-builder-live/run/cee79b03cfcf43b68852191ebff43b0a`, $0.0000.

Read: Same full chain as round 6, every move changing stock (e.g. r24-e00005 assemble moves graphite and slats into pencils, r24-e00015 deliver moves a pencil from eli to lee, r24-e00009 lee sells to ava). Orders waiting keep rising by 3 (r24-e00018): selling never reduces them, and ben is never sold to.

- ava: accepted r24-e00001 did=place-pencil-order
- ben: accepted r24-e00003 did=place-pencil-order
- eli: accepted r24-e00005 did=assemble-pencils
- gia: accepted r24-e00007 did=prepare-graphite
- lee: accepted r24-e00009 did=sell-pencil
- mara: accepted r24-e00011 did=harvest-logs
- noah: accepted r24-e00013 did=cut-wood-slats
- sam: accepted r24-e00015 did=deliver-pencils

World events: r24-e00001, r24-e00002, r24-e00003, r24-e00004, r24-e00005, r24-e00006, r24-e00007, r24-e00008, r24-e00009, r24-e00010, r24-e00011, r24-e00012, r24-e00013, r24-e00014, r24-e00015, r24-e00016, r24-e00017, r24-e00018

## Round 25

Trace `world-builder-live/run/d4a9d7326c634270a9dff56640c1fbab`, $0.0000.

Read: Same full chain as round 6, every move changing stock (e.g. r25-e00005 assemble moves graphite and slats into pencils, r25-e00015 deliver moves a pencil from eli to lee, r25-e00009 lee sells to ava). Orders waiting keep rising by 3 (r25-e00018): selling never reduces them, and ben is never sold to.

- ava: accepted r25-e00001 did=place-pencil-order
- ben: accepted r25-e00003 did=place-pencil-order
- eli: accepted r25-e00005 did=assemble-pencils
- gia: accepted r25-e00007 did=prepare-graphite
- lee: accepted r25-e00009 did=sell-pencil
- mara: accepted r25-e00011 did=harvest-logs
- noah: accepted r25-e00013 did=cut-wood-slats
- sam: accepted r25-e00015 did=deliver-pencils

World events: r25-e00001, r25-e00002, r25-e00003, r25-e00004, r25-e00005, r25-e00006, r25-e00007, r25-e00008, r25-e00009, r25-e00010, r25-e00011, r25-e00012, r25-e00013, r25-e00014, r25-e00015, r25-e00016, r25-e00017, r25-e00018

## Round 26

Trace `world-builder-live/run/42a31ce9987347bfbe6aca8af01f7dc2`, $0.0000.

Read: Same full chain as round 6, every move changing stock (e.g. r26-e00005 assemble moves graphite and slats into pencils, r26-e00015 deliver moves a pencil from eli to lee, r26-e00009 lee sells to ava). Orders waiting keep rising by 3 (r26-e00018): selling never reduces them, and ben is never sold to.

- ava: accepted r26-e00001 did=place-pencil-order
- ben: accepted r26-e00003 did=place-pencil-order
- eli: accepted r26-e00005 did=assemble-pencils
- gia: accepted r26-e00007 did=prepare-graphite
- lee: accepted r26-e00009 did=sell-pencil
- mara: accepted r26-e00011 did=harvest-logs
- noah: accepted r26-e00013 did=cut-wood-slats
- sam: accepted r26-e00015 did=deliver-pencils

World events: r26-e00001, r26-e00002, r26-e00003, r26-e00004, r26-e00005, r26-e00006, r26-e00007, r26-e00008, r26-e00009, r26-e00010, r26-e00011, r26-e00012, r26-e00013, r26-e00014, r26-e00015, r26-e00016, r26-e00017, r26-e00018

## Round 27

Trace `world-builder-live/run/505453ec6f8e4264bc04364b007902fc`, $0.0000.

Read: Same full chain as round 6, every move changing stock (e.g. r27-e00005 assemble moves graphite and slats into pencils, r27-e00015 deliver moves a pencil from eli to lee, r27-e00009 lee sells to ava). Orders waiting keep rising by 3 (r27-e00018): selling never reduces them, and ben is never sold to.

- ava: accepted r27-e00001 did=place-pencil-order
- ben: accepted r27-e00003 did=place-pencil-order
- eli: accepted r27-e00005 did=assemble-pencils
- gia: accepted r27-e00007 did=prepare-graphite
- lee: accepted r27-e00009 did=sell-pencil
- mara: accepted r27-e00011 did=harvest-logs
- noah: accepted r27-e00013 did=cut-wood-slats
- sam: accepted r27-e00015 did=deliver-pencils

World events: r27-e00001, r27-e00002, r27-e00003, r27-e00004, r27-e00005, r27-e00006, r27-e00007, r27-e00008, r27-e00009, r27-e00010, r27-e00011, r27-e00012, r27-e00013, r27-e00014, r27-e00015, r27-e00016, r27-e00017, r27-e00018

## Round 28

Trace `world-builder-live/run/d87b439cd69c470bbafb4d357c57c143`, $0.0000.

Read: Same full chain as round 6, every move changing stock (e.g. r28-e00005 assemble moves graphite and slats into pencils, r28-e00015 deliver moves a pencil from eli to lee, r28-e00009 lee sells to ava). Orders waiting keep rising by 3 (r28-e00018): selling never reduces them, and ben is never sold to.

- ava: accepted r28-e00001 did=place-pencil-order
- ben: accepted r28-e00003 did=place-pencil-order
- eli: accepted r28-e00005 did=assemble-pencils
- gia: accepted r28-e00007 did=prepare-graphite
- lee: accepted r28-e00009 did=sell-pencil
- mara: accepted r28-e00011 did=harvest-logs
- noah: accepted r28-e00013 did=cut-wood-slats
- sam: accepted r28-e00015 did=deliver-pencils

World events: r28-e00001, r28-e00002, r28-e00003, r28-e00004, r28-e00005, r28-e00006, r28-e00007, r28-e00008, r28-e00009, r28-e00010, r28-e00011, r28-e00012, r28-e00013, r28-e00014, r28-e00015, r28-e00016, r28-e00017, r28-e00018

## Round 29

Trace `world-builder-live/run/e3c902b0f7f843519dc4b98f1e689e53`, $0.0000.

Read: Same full chain as round 6, every move changing stock (e.g. r29-e00005 assemble moves graphite and slats into pencils, r29-e00015 deliver moves a pencil from eli to lee, r29-e00009 lee sells to ava). Orders waiting keep rising by 3 (r29-e00018): selling never reduces them, and ben is never sold to.

- ava: accepted r29-e00001 did=place-pencil-order
- ben: accepted r29-e00003 did=place-pencil-order
- eli: accepted r29-e00005 did=assemble-pencils
- gia: accepted r29-e00007 did=prepare-graphite
- lee: accepted r29-e00009 did=sell-pencil
- mara: accepted r29-e00011 did=harvest-logs
- noah: accepted r29-e00013 did=cut-wood-slats
- sam: accepted r29-e00015 did=deliver-pencils

World events: r29-e00001, r29-e00002, r29-e00003, r29-e00004, r29-e00005, r29-e00006, r29-e00007, r29-e00008, r29-e00009, r29-e00010, r29-e00011, r29-e00012, r29-e00013, r29-e00014, r29-e00015, r29-e00016, r29-e00017, r29-e00018

