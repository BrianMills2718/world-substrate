---
role: experiment-packet
status: blinded-review
reviewed_through: 2026-09-07
---

# Repair Bay mechanics review — blinded packet v0

## Reviewer task

Judge each candidate independently from the review information below. For each candidate, answer **approve** or **refuse** and briefly state the consequence that drove the decision. Some candidates may be acceptable and some may not be; the packet deliberately does not say how many.

Do not assume a compiler-accepted declaration is a good law. Judge whether the represented causal law matches the intended Repair Bay behavior.

## Intended world law

- Technicians have one represented hand-occupancy flag: a technician with `hands_free = false` is holding a tool and may not claim or receive another one.
- A tool may be claimed only when it is available in the shared `place:repair-bay` store.
- A handoff transfers a tool held by the actor to a **different** technician whose hands are free.
- Diagnosis applies only to a broken, undiagnosed machine using the diagnostic scanner held by the actor.
- Repair applies only to a diagnosed broken machine, using a matching tool held by the actor and a matching uninstalled part, with positive technician energy.
- A successful repair makes the machine operational, installs the part on that machine, costs one unit of technician energy, and adds one unit of tool wear.
- The world is complete only when **all** represented machines are operational.

All state paths below are compiler-validated. `last_cause_event_id` writes are engine-owned attribution and are omitted here for readability.

---

## Candidate A

**Action:** `repair`

**Rationale:** Repair consumes technician energy, installs the matching uninstalled part, makes the diagnosed machine operational, and increases wear on the held matching tool.

**Derived reads**
- `entities.<actor>.components.technician.energy`
- `entities.<machine>.components.machine.diagnosed`
- `entities.<machine>.components.machine.status`
- `entities.<machine>.components.machine.required_tool`
- `entities.<machine>.components.machine.required_part`
- `entities.<tool>.ownership.owner_ref`
- `entities.<tool>.components.tool.tool_kind`
- `entities.<tool>.components.tool.wear`
- `entities.<part>.components.part.installed`
- `entities.<part>.components.part.part_kind`

**Derived writes**
- `entities.<actor>.components.technician.energy`
- `entities.<machine>.components.machine.status`
- `entities.<machine>.components.machine.required_part`
- `entities.<part>.components.part.installed`
- `entities.<part>.components.part.installed_on`
- `entities.<tool>.components.tool.wear`

**Checks**
- machine is diagnosed: `machine.diagnosed == true`
- machine is broken: `machine.status == "broken"`
- tool is held by actor: `tool.owner_ref == actor:<actor>`
- tool matches requirement: `tool.tool_kind == machine.required_tool`
- part is uninstalled: `part.installed == false`
- part matches requirement: `part.part_kind == machine.required_part`
- actor has energy: `actor.energy > 0`

**Effects**
- `machine.status = "operational"`
- `machine.required_part = "none"`
- `part.installed = true`
- `part.installed_on = <machine id>`
- `actor.energy -= 1`
- `tool.wear += 1`

**Limits shown to reviewer**
- Refuses undiagnosed, operational, or mismatched repairs.
- Does not select or create parts.
- Requires positive technician energy.

---

## Candidate B

**Action:** `claim-tool`

**Rationale:** A free-handed technician can claim an available portable tool from the shared repair-bay store.

**Derived reads**
- `entities.<actor>.components.technician.hands_free`
- `entities.<tool>.portable.portable`

**Derived writes**
- `entities.<actor>.components.technician.hands_free`
- `entities.<tool>.ownership.owner_ref`

**Checks**
- actor has free hands: `actor.hands_free == true`
- tool is portable: `tool.portable == true`

**Effects**
- `tool.owner_ref = actor:<actor>`
- `actor.hands_free = false`

**Limits shown to reviewer**
- Refuses non-portable tools.
- Refuses claims by technicians whose hands are not free.

---

## Candidate C

**Action:** `repair`

**Rationale:** Repair consumes technician energy, installs the matching uninstalled part, makes the diagnosed machine operational, and increases wear on the held matching tool.

**Derived reads**
- `entities.<actor>.components.technician.energy`
- `entities.<machine>.components.machine.diagnosed`
- `entities.<machine>.components.machine.status`
- `entities.<machine>.components.machine.required_tool`
- `entities.<tool>.ownership.owner_ref`
- `entities.<tool>.components.tool.tool_kind`
- `entities.<tool>.components.tool.wear`
- `entities.<part>.components.part.installed`
- `entities.<part>.components.part.part_kind`

**Derived writes**
- `entities.<actor>.components.technician.energy`
- `entities.<machine>.components.machine.status`
- `entities.<part>.components.part.installed`
- `entities.<part>.components.part.installed_on`
- `entities.<tool>.components.tool.wear`

**Checks**
- machine is diagnosed: `machine.diagnosed == true`
- machine is broken: `machine.status == "broken"`
- tool is held by actor: `tool.owner_ref == actor:<actor>`
- tool matches requirement: `tool.tool_kind == machine.required_tool`
- part is uninstalled: `part.installed == false`
- part matches requirement: `part.part_kind == machine.required_tool`
- actor has energy: `actor.energy > 0`

**Effects**
- `machine.status = "operational"`
- `part.installed = true`
- `part.installed_on = <machine id>`
- `actor.energy -= 1`
- `tool.wear += 1`

**Limits shown to reviewer**
- Refuses undiagnosed, operational, or mismatched repairs.
- Does not select or create parts.
- Requires positive technician energy.

---

## Candidate D

**Terminal condition**

**Mode:** `any`

**Selector**
- categories: `machine`
- components: `machine`

**Check**
- `machine.status == "operational"`

Interpretation of the declaration: the terminal is reached when the configured mode evaluates true across the selected represented machines.

---

## Candidate E

**Action:** `diagnose`

**Rationale:** A technician can diagnose only a broken undiagnosed machine while holding the diagnostic scanner.

**Derived reads**
- `entities.<actor>.components.technician.hands_free`
- `entities.<machine>.components.machine.diagnosed`
- `entities.<machine>.components.machine.status`
- `entities.<scanner>.ownership.owner_ref`
- `entities.<scanner>.components.tool.tool_kind`

**Derived writes**
- `entities.<machine>.components.machine.diagnosed`

**Checks**
- scanner is held by actor: `scanner.owner_ref == actor:<actor>`
- actor is holding scanner: `actor.hands_free == false`
- machine is broken: `machine.status == "broken"`
- machine is undiagnosed: `machine.diagnosed == false`
- scanner kind is scanner: `scanner.tool_kind == "scanner"`

**Effects**
- `machine.diagnosed = true`

**Limits shown to reviewer**
- Does not change machine requirements or technician state.
- Refuses operational or already diagnosed machines.
- Refuses scanners not held by the acting technician.

---

## Candidate F

**Action:** `handoff-tool`

**Rationale:** A held tool can be transferred to a distinct technician whose hands are free.

**Derived reads**
- `entities.<tool>.ownership.owner_ref`
- recipient/actor identity

**Derived writes**
- `entities.<tool>.ownership.owner_ref`
- `entities.<actor>.components.technician.hands_free`
- `entities.<recipient>.components.technician.hands_free`

**Checks**
- tool is held by actor: `tool.owner_ref == actor:<actor>`
- recipient differs from actor: `<recipient id> != <actor id>`

**Effects**
- `tool.owner_ref = actor:<recipient>`
- `actor.hands_free = true`
- `recipient.hands_free = false`

**Limits shown to reviewer**
- Refuses self-handoff.
- Refuses tools not held by the actor.

---

## Response format

Reply with one line per candidate, for example:

`A — approve/refuse — short reason`

Also add a confidence from 1–5 for each decision if convenient. Do not inspect other repository files while completing the blinded pass; the result is most useful if based only on this packet.
