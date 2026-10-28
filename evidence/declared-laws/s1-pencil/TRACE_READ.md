# Trace read: S1 live pencil build with declared laws

Run: owner allowance, deployed `a88af2f` (health `build_commit` a88af2f71df8), started 2026-10-28T08:46:48Z,
share `a48eDqVcj4z9`, 13 server rows (`run-log.jsonl`: 1 generate, 11 run, 1 readout). The 143 model calls
are in `llm-calls.jsonl`, pulled from the VPS `llm_observability.db` by time window (ids 21509-21651: 77
Concordia resident, 57 attempt interpreter, 6 mechanic authoring, 1 world authoring, 1 world kind, 1 readout;
all `openrouter/openai/gpt-6-luna`, no errors; $0.070 in all). Description: the one-line "I, Pencil" supply
chain (loggers, mill, graphite mine, lead works, factory, trucks, shops, customers).

This is the S1 live build of `docs/plans/declared_laws.md`: the world designer declares its own laws, and the
build record and page show them. The engine does not enforce laws yet (S2), so the law check below is made
by reading the events against the declared laws, not by the engine. Run once, reported as it came out.

## Findings

1. **The designer declared laws, and the build record holds exactly what it wrote (L1 passes).** The
   world-authoring reply (call 21510, trace `world-builder-live/world/1cfbf24f1a0349abb1f333913208b053`)
   declares 8 resources (cedar-logs, cedar-slats, graphite, clay, leads, pencils, boxed-pencils, cash) and 6
   total laws (`logs-conservation`, `slats-conservation`, `graphite-conservation`, `leads-conservation`,
   `pencils-conservation`, `boxed-pencils-conservation`). Parsed reply `laws` and `resources` equal the
   generate row's `result.bundle.laws` and `.resources` (Python `==`, both True). The generate row's
   summary lists the same 6 law ids. The page showed them: the driver saw the build note "Laws this world
   keeps" with all six sentences at 52.5 s (`s1p-driver.log` in the scratch run folder; the same text is in
   the run JSON's `steps`).
2. **Money changed hands on every trade, by the rules alone.** All 26 accepted trades (25 `buy-*`, 1
   `sell-pencil`) take from one holder's cash exactly what they add to another's (`law-check.txt`). The
   sale is r9-e00011: the customer's cash 1000 -> 999, the shop's 990 -> 991, a boxed pencil leaves shop
   stock and a pencil reaches the customer. But the designer declared no law for cash and no pairing law
   for any trade, although the contract's own example is a sale. Under S2 nothing would hold the money
   books; this run balanced them because the rules writer did.
3. **The declared laws are wrong in one direction: they list only the move that makes each good.** Of 71
   accepted events, 39 change a resource's total through a move or process its law does not list
   (`law-check.txt`): `saw-slats` uses logs (7), `make-leads` uses graphite (4), `make-pencils` uses slats
   and leads (2 each), `pack-pencils` uses pencils (1), `sell-pencil` unboxes a boxed pencil (1), and the
   processes `renew-cedar-logs` and `renew-graphite` add logs and graphite every round (11 each). S2 as
   planned would refuse every manufacturing step and the sale. Cause, from the prompt: the contract text
   (`scripts/generate_world_bundle.py:120`) says a total "changes only through those" with making examples
   and never asks for the moves that use a resource up; and the designer writes laws before the rules
   writer names any process, so it cannot list one. The rules writer was told the laws (the first authority
   rule) and still wrote the renew processes. Classification: contract defect plus an ordering gap; filed
   as #281, a precondition for S2.
4. **Either side of a trade can start it.** The seller started 19 of the 25 accepted trades (e.g.
   r2-e00007, Oregon Loggers runs `buy-logs` with buyer Cedar Mill, spending the mill's cash). In
   `buy-boxed-pencils` it is the other way round: the shop, the buyer, was refused "Actor matches mechanic
   selector" four times (r2-e00009, r7-e00011, r8-e00011, r10-e00010), and only the factory could sell to it
   (r8-e00009). Filed as #282.
5. **The build rewrote the rules after its test runs and kept the third set.** The first two test runs
   ran 24 turns with 128 and 137 accepted moves but `world_changes: 0`; the third had 48 and was kept. The
   page said "the last rules did not pass the test run" once. The delivery trucks were left out on purpose
   (`not_modeled`: "Multi-round delivery journeys and their countdowns"), and the National Truck Carrier
   correctly says each round it has nothing to carry.
6. **Residents act from what they see.** The shop waits after its order fails and retries once the
   factory has packed a pencil (r7: "The factory has now made pencils"); the mill keeps sawing while the
   factory buys slats. One free attempt was made: at r10 Cedar Mill tried "sell one cedar slat to the pencil
   factory"; the interpreter matched nothing (`unsupported_action`, nearest `buy-slats`). In r11 the mill
   then used `buy-slats` as the seller and it worked (r11-e00001), so the interpreter's "no action kind
   describes the mill selling slats" was wrong about the rules.
7. **44 moves were lost to `stale_revision`** (someone else changed the world first in the same round); 7
   were refused by a check and 1 matched no move. The page's line was "Round 10 · 44 allowed · 8 refused ·
   64 held back by the rules · 20 by itself".

## Trace ids opened

- `world-builder-live/kind/2c9b10f8c52e427c9e24b87ae79fafe1`: call 21509, world kind: not mainly about
  people (supply chain).
- `world-builder-live/world/1cfbf24f1a0349abb1f333913208b053`: calls 21510-21516: world authoring (21510,
  laws as in finding 1) and 6 mechanic-authoring calls (writing and rewriting the rules; the kept set is the third test run's).
- `world-builder-live/run/6dc14ac3483b4d8285b9d9843b0650ea` (round 1, calls 21517-21527),
  `world-builder-live/run/a4fedc73d6fa4bb5bbd59d46cb6cb47c` (round 2, 21528-21539),
  `world-builder-live/run/495e5cae57254b3f9eb7cc1ead868d0d` (round 3, 21540-21550),
  `world-builder-live/run/880ed11b011b4474bf447ad981cd9403` (round 4, 21551-21562),
  `world-builder-live/run/fb6ede6c217547e9af6b08a47823267b` (round 5, 21563-21574),
  `world-builder-live/run/7e51509b29724655bb92c88f3c20f02c` (round 6, 21575-21586),
  `world-builder-live/run/7285fbeff59b48be80325f1a768e0343` (round 7, 21587-21599),
  `world-builder-live/run/3f627f8048b844af9ca9a0b944d41491` (round 8, 21600-21612),
  `world-builder-live/run/5312fa270d284269a76756d43e2b14f1` (round 9, 21613-21625),
  `world-builder-live/run/a03d62f43bb04e66b0e0ffa1cfc28370` (round 10, 21626-21638),
  `world-builder-live/run/3e7e0f54c652404998d22185f6c383a3` (round 11, 21639-21650): each is 7 resident
  calls (one per business) plus 4-6 interpreter calls reading their attempts; what they showed is under
  each round.
- `world-builder-live/readout/b808af022aa041088a50f235a088e256`: call 21651, the "How goods moved through
  the chain" readout; its events (r3-e00001, r3-e00005, r6-e00009, r7-e00009, r9-e00011) match the run.

## Round 1

Tried a move: `cedar-mill`, `graphite-mine`, `lead-works`, `oregon-loggers`.
Cedar Mill asked for 10 logs (r1-e00001, refused: "The quantity is one", seller short); Graphite Mine mined
(r1-e00002); Lead Works asked for 10 graphite (r1-e00004, refused the same way); Oregon Loggers cut cedar
(r1-e00006). Pencil Factory, Pencil Shops and National Truck Carrier waited, each saying it saw no useful
move. Processes renew-cedar-logs (r1-e00007) and renew-graphite (r1-e00008) each added one unit, unlisted by
their laws.

## Round 2

Tried a move: `cedar-mill`, `graphite-mine`, `lead-works`, `oregon-loggers`, `pencil-shops`.
Cedar Mill bought a log (r2-e00001); Graphite Mine sold graphite to Lead Works (r2-e00003) and Lead Works
bought one (r2-e00005); Oregon Loggers sold a log to the mill (r2-e00007, seller-started); Pencil Shops
asked for 10 boxed pencils (r2-e00009, refused: not its move, quantity, factory has none). The factory and
the carrier waited.

## Round 3

Tried a move: `cedar-mill`, `graphite-mine`, `lead-works`, `oregon-loggers`.
Cedar Mill sawed slats (r3-e00001, logs 2 -> 1, unlisted in `logs-conservation`); Graphite Mine mined
(r3-e00003); Lead Works made a lead (r3-e00005, uses graphite and clay); Oregon Loggers sold a log
(r3-e00007). The shop waited, citing its failed order.

## Round 4

Tried a move: `cedar-mill`, `graphite-mine`, `lead-works`, `oregon-loggers`, `pencil-factory`.
Cedar Mill sawed (r4-e00001); Graphite Mine sold graphite (r4-e00003); Lead Works sold a lead to the factory
(r4-e00005); Oregon Loggers cut cedar (r4-e00007); Pencil Factory tried to buy a lead (r4-e00009, refused:
the lead works had none left after r4-e00005, the world changed between its look and its move).

## Round 5

Tried a move: `cedar-mill`, `graphite-mine`, `lead-works`, `oregon-loggers`, `pencil-factory`.
Cedar Mill sawed (r5-e00001); Graphite Mine mined (r5-e00003); Lead Works made a lead (r5-e00005); Oregon
Loggers sold a log (r5-e00007); Pencil Factory bought its first slat (r5-e00009).

## Round 6

Tried a move: `cedar-mill`, `graphite-mine`, `lead-works`, `oregon-loggers`, `pencil-factory`.
Cedar Mill sawed (r6-e00001); Graphite Mine sold graphite (r6-e00003); Lead Works sold a lead (r6-e00005);
Oregon Loggers sold a log (r6-e00007); Pencil Factory made the first pencil (r6-e00009: one slat, one lead,
ferrule, eraser and paint used, unlisted in `slats-conservation` and `leads-conservation`).

## Round 7

Tried a move: `cedar-mill`, `graphite-mine`, `lead-works`, `oregon-loggers`, `pencil-factory`, `pencil-shops`.
Cedar Mill sawed (r7-e00001); Graphite Mine mined (r7-e00003); Lead Works made a lead (r7-e00005); Oregon
Loggers sold a log (r7-e00007); Pencil Factory packed the pencil (r7-e00009, unlisted in
`pencils-conservation`); Pencil Shops tried to order again because "the factory has now made pencils"
(r7-e00011, refused: not its move).

## Round 8

Tried a move: `cedar-mill`, `graphite-mine`, `lead-works`, `oregon-loggers`, `pencil-factory`, `pencil-shops`.
Cedar Mill sawed (r8-e00001); Graphite Mine sold graphite (r8-e00003); Lead Works sold a lead (r8-e00005);
Oregon Loggers sold a log (r8-e00007); Pencil Factory sold the boxed pencil to the shop (r8-e00009, the
shop's cash 1000 -> 990); Pencil Shops' own order failed in the same round (r8-e00011).

## Round 9

Tried a move: `cedar-mill`, `graphite-mine`, `lead-works`, `oregon-loggers`, `pencil-factory`, `pencil-shops`.
Cedar Mill sawed (r9-e00001); Graphite Mine mined (r9-e00003); Lead Works made a lead (r9-e00005); Oregon
Loggers sold a log (r9-e00007); Pencil Factory bought a slat (r9-e00009); Pencil Shops sold the pencil to a
customer (r9-e00011, the run's one sale; the shop paid 10 for it and sold it for 1).

## Round 10

Tried a move: `cedar-mill`, `graphite-mine`, `lead-works`, `oregon-loggers`, `pencil-factory`, `pencil-shops`.
Cedar Mill tried a free attempt, "sell one cedar slat to the pencil factory", which matched no move
(unsupported, nearest buy-slats); Graphite Mine sold graphite (r10-e00002); Lead Works sold a lead
(r10-e00004); Oregon Loggers sold a log (r10-e00006); Pencil Factory made a second pencil (r10-e00008); Pencil
Shops' order was refused again (r10-e00010).

## Round 11

Tried a move: `cedar-mill`, `graphite-mine`, `lead-works`, `oregon-loggers`, `pencil-factory`.
Cedar Mill sold a slat as the seller in buy-slats (r11-e00001); Graphite Mine mined (r11-e00003); Lead Works
bought graphite (r11-e00005); Oregon Loggers cut cedar (r11-e00007); Pencil Factory bought a slat
(r11-e00009). Pencil Shops waited for clearer supply; the carrier again had nothing to carry.
