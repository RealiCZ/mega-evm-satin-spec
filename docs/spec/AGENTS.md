# Specification — Writing Rules

This layer is the **formal MegaETH specification** — the complete, normative definition of MegaETH's verifiable behavior.
It is not limited to the EVM; it covers the entire set of behaviors that define a correct MegaETH node: transaction processing, resource metering, system contracts, oracle services, and protocol state management.
It targets protocol implementers, auditors, and anyone who needs to verify or reproduce MegaETH's exact behavior.

**Scope principle**: If a behavior affects whether a node produces correct outputs given the same inputs, it belongs in this spec.
This includes but is not limited to EVM execution — gas accounting, resource limits, system contract semantics, oracle data lifecycle, and upgrade activation rules are all in scope.

## Page Structure

Every spec page MUST include YAML frontmatter with a `spec` field — the latest stable spec that this page's main content describes (e.g., `Rex3`).
This field is the single source of truth for which spec version the page reflects.
When the latest stable spec changes, update this field and the page content together.

**Exception**: Upgrade pages under `upgrades/` do not need a `spec` frontmatter field.
Their spec association is conveyed by the page title and filename.

**Exception**: Pages of the Satin section (`satin/`) describe Satin while it is unstable: their frontmatter carries `spec: Satin` and `maturity: unstable` (see [The Satin Section](#the-satin-section)).

Every spec page MUST follow this section order:

```
# Page Title
Abstract: 1-2 sentence summary of what this page specifies.

## Motivation
The problem statement: what problem exists that this spec solves.
Describes the concrete failure modes or limitations that necessitate this behavior.
This section explains WHY the spec exists, not how it works.

## Specification
The normative behavioral definition.
Subsections organized by logical component.
All behavioral rules use MUST/MUST NOT/SHALL/SHOULD/MAY per RFC 2119.

## Constants
Table of all named constants with values and descriptions.
Every constant referenced in the Specification section MUST appear here.
Placed after the Specification so readers encounter the behavioral rules first
and can reference constants as needed.

## Rationale
Design decisions: why this specific solution over alternatives.
Each decision is a named paragraph explaining the trade-off.
This section explains WHY specific choices were made.

## Security Considerations
What could go wrong if this spec is implemented incorrectly or incompletely.
Concrete attack vectors, economic risks, or safety invariants that implementers must preserve.

## Spec History
Links to upgrade pages showing how this behavior evolved across specs.
```

**Sections may be omitted** when they genuinely don't apply (e.g., a glossary page has no Constants or Motivation).
But for any page that defines behavioral rules, the full structure SHOULD be followed.
Security Considerations SHOULD be included on any page that defines gas accounting, resource limits, state mutation, or economic rules, but it is not required.
It MAY be omitted for pages that are purely structural (e.g., glossary, overview indexes).
Existing pages that omit the section do not need to be retroactively updated solely to add it.

### Spec History Format

For **overview pages**, the Spec History section SHOULD be a simple list of specs linking to their upgrade pages.
Each item SHOULD include one short sentence summarizing the main change introduced by that spec.
Do not use tables or detailed changelog breakdowns there.

Example:

```markdown
## Spec History

- [MiniRex](../upgrades/minirex.md) — Introduced the initial MegaEVM execution model.
- [Rex](../upgrades/rex.md) — Revised gas forwarding and storage-gas semantics.
- [Rex1](../upgrades/rex1.md) — Fixed detained compute-gas reset behavior.
- [Rex2](../upgrades/rex2.md) — Added KeylessDeploy and enabled SELFDESTRUCT with EIP-6780 semantics.
- [Rex3](../upgrades/rex3.md) — Revised oracle detention to use SLOAD-based triggering.
- [Rex4](../upgrades/rex4.md) — Introduces per-call-frame limits, relative detention, and storage gas stipend.
```

For **concept pages**, the Spec History section MAY summarize what changed at each spec if that helps explain the evolution of the behavior.

Rules for the Spec History table:

- Only list specs that changed behavior relevant to this page. Do not list specs that inherited behavior unchanged (unless noting "No changes" is clarifying).
- The "Change" column is a short summary (one sentence). Detailed previous/new behavior belongs in the linked upgrade page.
- The "Key values" column shows the concrete values introduced at that spec — constants, limits, formulas. Use "N/A" if the change is purely behavioral with no new numeric values.
- Link each spec name to its upgrade page under `upgrades/`.

**Overview-page exception**: overview/index pages that summarize and organize links to authoritative subpages SHOULD omit Motivation and Rationale.
For those pages, use a lighter structure such as:

```
# Page Title
Abstract: 1-2 sentence summary.

## Stable Scope
What stable behavior the overview summarizes.

## Specifications
Grouped summaries of the relevant concept pages.

## Spec History
Optional, if it helps orient readers.
```

## Accuracy

- **Verify constants against source code.**
  Every numeric value (gas limits, storage gas bases, detention caps, contract addresses) MUST be verified against the implementation source (`mega-evm`, `mega-reth`, etc.) before writing or updating.
  Do not copy values from other documentation pages without cross-checking.
- **Attribute behavior to the correct spec.**
  If a behavior was introduced in Rex3, reference Rex3 — not Rex4, even if Rex4 inherits it.
  Each spec's contribution must be precisely scoped.
- **Do not invent guarantees.**
  The specification MUST NOT introduce constraints or behavioral rules that are not verified against the implementation.
  If uncertain, surface the ambiguity to the user rather than guessing.

## Tone & Language

- **Normative and precise.** Use MUST, MUST NOT, SHALL, SHOULD, MAY per RFC 2119 when defining behavior. Every behavioral rule in the Specification section MUST use normative language.
- **Exhaustive.** Cover every corner case. Readability may be sacrificed for completeness.
- **No developer guidance.** Do not include "tips", "best practices", "how to use", or recommendations like "Use `eth_estimateGas`" or "Use transient storage". That belongs in developer documentation outside this spec.
- **No user-facing language.** Do not address the reader as "you" in the Specification section. Do not explain "what this means for you". That belongs in user or developer documentation outside this spec.
- **Self-contained.** The spec never links to external user docs or developer docs. It may link to external references (EIPs, Ethereum Yellow Paper, OP Stack specs) and to other spec pages.
- **No implementation details.** Do not reference specific code patterns, function names, or implementation strategies (e.g., `spec.is_enabled(MINI_REX)`). Describe the required behavior, not how to implement it.

## Specification Section Rules

### Normative Language

- **Uppercase only.**
  Per RFC 8174, only UPPERCASE keywords (MUST, SHOULD, MAY, etc.) carry normative weight.
  Lowercase "must", "should", "may" are plain English with no special meaning.
  The formal BCP 14 boilerplate lives on the [Specification overview page](overview.md) — individual spec pages do not repeat it.
- Use "A node MUST..." for required behavior.
- Use "A node MUST NOT..." for prohibited behavior.
- Use "SHOULD" only when non-compliance is acceptable in defined circumstances.
- Do not use normative keywords outside the Specification and Security Considerations sections.
  Motivation, Rationale, and Spec History use plain English.
- Descriptive prose (background, context) does not require normative keywords.

### Constants

- Every numeric value used in the Specification MUST be defined as a named constant in the Constants table.
- Do not embed magic numbers in formulas — reference the constant name.
- Each constant row MUST include: name, value, and a one-line description.

### Formulas

- Express formulas as inline code blocks: `` `total_gas = compute_gas + storage_gas` ``.
- Define every variable immediately after the formula.
- For complex logic, use pseudocode in fenced code blocks.

### Edge Cases

- State edge cases explicitly as normative rules (e.g., "For state that does not yet exist, the node MUST...").
- Do not leave behavior undefined — if the spec doesn't say what happens, implementers will guess differently.

### Universal Claims

A rule stated for "every X" is read as covering every X, so it must be checked against every X before it is written.
Two habits keep that honest:

- **Declare the page's lower bound.** A page whose rules do not apply from Equivalence onward MUST say where they start, once, before stating them — as `evm/compute-gas.md` does with "Compute gas metering begins at MiniRex." Without it, every later sentence on the page silently claims to cover Equivalence, which runs the unmodified upstream instruction table and therefore has none of MegaETH's wrappers, storage-gas charges, or resource lanes.
- **Spec ranges are behavior ranges.** A range like "from MiniRex onward" or "MiniRex through Rex5" is read on behavior: an alias rung counts as its behavior target (`MINI_REX_1` counts as Equivalence), a convention `hardfork-spec.md` states once — do not add per-sentence alias caveats to range statements.
- **Look for the counterexample before writing the quantifier.** For a claim spanning specs, resolve it through the per-spec instruction table selection; for one spanning opcodes or call schemes, check each named opcode's own wrapper. Where the implementation has an exception, name the exception in the rule rather than leaving the rule clean — an implementer following a rule mega-evm does not keep will diverge, and a halt reason or charge ordering is observable.

### Charging Lifecycle

- For any cost or fee, specify WHEN it is charged: before execution, at the opcode, or post-execution.
- Specify what happens on failure: is the cost consumed, refunded, or rolled back?

### Spec Versioning

A spec has two independent properties, and they MUST NOT be conflated:

- **Maturity** — `unstable` (semantics may still change) or `frozen` (semantics are fixed forever).
  At most one spec is unstable at a time, and when one exists it is always the latest.
- **Network status** — `not scheduled`, `scheduled`, or `active`, tracked **per network** (mainnet and testnet each have their own).
  A frozen spec is not automatically live: it takes effect on a network only at the block where that network activates it.

Documentation placement follows **maturity**, not network status:

- Main content in concept pages MUST describe the latest **frozen** spec's behavior only.
  Previous spec behavior belongs in the Spec History table or upgrade pages.
  Unstable spec behavior MUST be placed in `<details>` blocks, never in main prose or tables.
- **Satin-section exception**: Satin, the unstable spec, is specified in its own section, `satin/`, in main prose and tables, and in no `<details>` block (see [The Satin Section](#the-satin-section)).
  The `<details>` rules of this section apply to every page outside `satin/`, but no Satin content is added to a page outside `satin/` other than the roster pages and the glossary.
- **The latest spec is implicit.**
  Do not mention the latest spec name in the Specification, Constants, or Motivation sections.
  The `spec` frontmatter field declares which spec the page describes; it names the latest frozen spec, whether or not that spec is live anywhere.
  Readers should be able to read the main content without encountering "as of Rex3" or "in Rex3" qualifiers.
  The Rationale section MAY reference spec names when explaining historical design decisions.
- Wrap unstable spec content in `<details>` blocks with a clear label (e.g., "SpecName (unstable): ...").
- Unstable content MUST still use normative language within the `<details>` block.
- Do NOT use `<details>` to mark a frozen-but-unscheduled spec.
  Its content belongs in main prose like any other frozen spec; network status is conveyed by the upgrade overview's activation tabs, not by hiding the specification.
  Activation timestamps live in `upgrades/overview.md` alone — an individual upgrade page carries none, so there is one place to edit when a spec is scheduled.
- **Glossary exception**: glossary entries for unstable-spec terms do not use `<details>` blocks.
  Instead, mark them with inline text (e.g., "_(SpecName, unstable)_") at the start of the definition.
- **Roster-page exception**: a page whose subject is the spec ladder itself (`overview.md`, `hardfork-spec.md`, `upgrades/overview.md`, and the progression line in `glossary.md`) MUST carry the unstable spec in its progression and its per-spec summary, outside `<details>`.
  A reader looking up which specs exist must not be shown a ladder that stops one short of reality, and a `<details>` block cannot express "this rung exists".
  Every such entry MUST label the spec unstable where it is described, and MUST stay a summary — the normative text lives in the concept pages, still gated by `<details>` there, or, for Satin, in the Satin section, which the entry links.
- **Replay-page exception**: a page whose subject is a cross-spec measurement that a replaying node must implement for every spec simultaneously (currently only `evm/compute-gas.md`) MAY carry per-frozen-spec behavior — spec-named rows, tables, and qualifiers — in its main Specification and Constants sections.
  Such a page MUST state the current behavior first and derive historical behavior from it, MUST justify the departure in its Rationale section, and MUST still keep unstable-spec behavior in `<details>` blocks.
  Spec names in its main content are linked on first use per page; repeats stay unlinked.

**Sealing a spec** (moving it from unstable to frozen) is therefore a documentation operation: lift its `<details>` blocks into main prose, replacing the behavior they superseded; move that superseded behavior into each page's Spec History; advance every `spec:` frontmatter field; and record the new spec's activation status on its upgrade page.
Sealing Satin is the move described in [Sealing Satin](#sealing-satin) instead.

## The Satin Section

Satin restates MegaETH's execution layer on a new base rather than adding to Rex6's rules, so it is not written as `<details>` blocks inside the Rex-era pages.
Its complete, standalone specification is a section of its own, and the Rex-era pages stay as they are until Satin is frozen.

### Location

- The Satin section is the directory `satin/`: `satin/overview.md` and `satin/base-layer.md`, then `satin/evm/` (execution), `satin/system-contracts/` (system contracts) and `satin/block/` (transactions and blocks).
  A Satin page that succeeds a Rex-era page has that page's file name (`satin/evm/gas-forwarding.md` succeeds `evm/gas-forwarding.md`).
- Every Satin behavior is specified in the Satin section, standalone.
  A Satin page never relies on a Rex-era page for a rule: a Rex6 rule that Satin keeps is stated again on the Satin page, as Satin's.
  A Satin page MAY link a Rex-era page in its Rationale or Spec History, never for a rule.
- `upgrades/satin.md` is the reviewers' delta of Satin against Rex6, and the draft the Satin section is written from.
  Once a Satin page is written, that page is the specification of what it covers, and the delta is brought in line with it.
- `SUMMARY.md` lists the Satin section as a part of its own, labelled unstable.
- Every page of the Satin section follows [Page Structure](#page-structure) and every other rule of this file, except where this section says otherwise.

### Maturity While Unstable

- Every page under `satin/` carries `spec: Satin` and `maturity: unstable` in its frontmatter, and opens, right after its title, with a `{% hint style="warning" %}` stating that Satin is unstable and that the page may change before Satin is frozen.
- Its normative text is main prose and tables, in normative language, as on any concept page: the Satin section uses no `<details>` block, because every page in it is Satin's.
- The latest spec is implicit inside the section as well: a Satin page does not qualify its rules with "in Satin" or "as of Satin".
- While the Satin section exists, Satin is added to no page outside it except the roster pages and the glossary, which carry it as their exceptions in [Spec Versioning](#spec-versioning) say and link the Satin section.

### The Rex-Era Pages

- The pages under `evm/` and `system-contracts/` keep describing Rex6 (`spec: Rex6`) and are not edited for Satin.
  A correction of their Rex6 content is the only change they take.
- The upgrade pages `upgrades/minirex.md` through `upgrades/rex6.md` are history and stay as they are.

### Sealing Satin

When Satin is frozen, the Satin section becomes the main body and the Rex-era pages become history, in one change:

1. Move every Rex-era concept page from `evm/` and `system-contracts/` to `history/rex6/evm/` and `history/rex6/system-contracts/`, unchanged but for its links.
2. Move the Satin section up one level: `satin/evm/` to `evm/`, `satin/system-contracts/` to `system-contracts/`, `satin/block/` to `block/` and `satin/base-layer.md` to `base-layer.md`; fold `satin/overview.md` into `overview.md`.
3. Remove `maturity` and the unstable hint from every moved page; keep `spec: Satin`.
4. Give every moved page a Spec History that links its Rex6 predecessor under `history/rex6/` and the upgrade pages.
5. Rewrite the links, and make `SUMMARY.md` list the Satin pages as the main body and the Rex6 pages in a "History" part.
6. Bring `upgrades/satin.md` to the [Upgrade Page Rules](#upgrade-page-rules), an informative summary of the delta, and record Satin's activation status in `upgrades/overview.md`.

A spec after Satin uses the `<details>` rules of [Spec Versioning](#spec-versioning) on the Satin pages, unless it restates the execution layer again, in which case it gets a section of its own by this procedure.

### Rule Ids

- Every normative rule of the Satin section carries a stable id `SATIN-<AREA>-<NNN>`: `AREA` is the code of the page the rule lives on, written in capital letters (for example `POOL` for Two-Pool Gas), and `NNN` is a three-digit number.
- The id is written once, as inline code at the start of the paragraph or list item that states the rule: "`SATIN-POOL-005` A node MUST …".
- An id is assigned once and never reused or renumbered.
  A rule that moves to another page keeps its id; a rule that is split keeps its id on one part and the other parts take new numbers; a rule that is removed retires its id, and the page lists its retired ids at the end of its Specification section.
- Tests and fixtures cite a rule by its id.
- The scheme is a proposal awaiting the owner's decision; until it is adopted, ids appear only in the stubs and the outline.

## Motivation and Rationale Section Rules

### Motivation

- Describe the concrete problem: what breaks, what is underpriced, what attack becomes possible.
- Use specific numbers where possible (e.g., "base fee of 0.001 gwei", "up to 10 billion gas per block").
- Do NOT describe the solution — that is the Specification section's job.

### Rationale

- Each design decision is a **named paragraph** starting with bold text (e.g., "**Why `base × (multiplier − 1)` instead of `base × multiplier`?**").
- Explain the trade-off: what was considered, what was rejected, and why.
- Reference historical changes where applicable (e.g., "MiniRex used X, Rex changed to Y because...").

## Security Considerations Section Rules

This section exists because EIP-1 makes Security Considerations a blocking requirement for any Ethereum specification, and RFC 2119 §7 warns that "the effects on security of not implementing a MUST or SHOULD may be very subtle."

- Describe **concrete** risks, not generic warnings.
  State what goes wrong: underpriced operations, denial-of-service vectors, state corruption, economic exploits.
- Frame each risk as a consequence of incorrect implementation.
  "If a node fails to charge storage gas on contract creation, an attacker can exhaust state storage at compute-gas cost only."
- Do not repeat the Specification section.
  The Specification says what MUST happen; Security Considerations says what breaks if it does not.
- Name the invariants that the spec preserves.
  "This spec preserves the invariant that total detained gas never exceeds the block gas limit."
- If no security considerations apply, state so explicitly: "This page has no security considerations."
  Do not silently omit the section — that is ambiguous (forgot vs. none).

## Upgrade Page Rules

Upgrade pages under `upgrades/` are the authoritative record of what changed at each spec.
They complement concept pages: concept pages describe the current behavior, upgrade pages describe the delta.

Alias specs get no upgrade page of their own: an alias rung introduces no behavioral delta, so a dedicated page could only restate its target.
The authoritative record of an alias hardfork is its entry in `overview.md` (activation timestamps and a one-line description) plus the alias section of `hardfork-spec.md` (semantics).
Do not add per-alias pages such as `minirex1.md`.

### Required Structure

Every upgrade page MUST follow this structure:

```markdown
---
description: <SpecName> network upgrade — <one-line summary>.
---

# <SpecName> Network Upgrade

This page is an informative summary of the <SpecName> specification.

## Summary

2-4 paragraphs: what changed, what problem it solves, developer impact.

## What Changed

### <Change Name>

#### Previous behavior

- Precise description of behavior before this spec.
- Include concrete values, formulas, or rules that were in effect.

#### New behavior

- Precise description of behavior introduced by this spec.
- Include the new values, formulas, or rules.

### <Next Change Name>

...

## Developer Impact

What contract authors, integrators, and tooling authors need to know.

## Safety and Compatibility

Backward-compatibility boundaries, failure-mode differences.

## References

Links to the implementation repo, related EIPs, or other specs.
```

### Precision Requirements

- Every "Previous behavior" section MUST state the exact prior values, formulas, or rules — not just "it was different."
  A reader should be able to implement the previous spec from the "Previous behavior" text alone.
- Every "New behavior" section MUST state the exact new values, formulas, or rules.
- Do not merge changes so aggressively that the previous/new mapping becomes unclear.
  Each behavioral change gets its own subsection under "What Changed."
- If a change fixes a bug in a prior spec, state what the buggy behavior was and what the corrected behavior is.

## What Belongs Here

- EVM behavioral definitions (gas costs, opcode semantics, resource limits)
- System contract specifications (addresses, interfaces, execution semantics)
- Oracle service specifications (storage layout, timing guarantees, gas detention)
- Hardfork/spec progression and per-upgrade behavioral deltas
- Glossary of protocol terms

## What Does NOT Belong Here

- Developer tips or best practices → developer documentation (outside this spec)
- Code examples showing how to use a feature → developer documentation
- User-facing explanations → user documentation (outside this spec)
- Integration configuration → developer documentation
- "Why should I care about this?" framing → developer documentation
- Implementation-specific code patterns or API references → developer documentation
- Recommendations ("Use X instead of Y") → developer documentation

## Source of Truth

The user is the ultimate source of truth.
This documentation is the canonical written specification of MegaETH's verifiable behavior, but user instructions override both the docs and the implementation when there is ambiguity or conflict.

The implementation repositories are side channels for verification only.
Agents MUST inspect the relevant implementation in `mega-evm`, `mega-reth`, and any other repository that materially affects the documented behavior to confirm whether the specification matches the current implementation, but implementation code is not the final authority.

If an agent finds or suspects any discrepancy between user intent, this specification, and the implementation behavior across `mega-evm`, `mega-reth`, or other relevant repositories, the agent MUST NOT silently resolve it.
Instead, the agent MUST surface the discrepancy clearly and ask the user to confirm the intended behavior before changing the spec text.

Do not describe this spec as "mirrored from mega-evm/docs".
The old `mega-evm/docs` content is transitional and may be removed.

## Linking Rules

- **Link glossary terms on first use.**
  The first mention of a MegaETH-specific term on a page SHOULD link to its glossary entry.
  Do not over-link — subsequent uses on the same page need not be linked.
- **Link spec names to their upgrade pages.**
  When a spec is mentioned by name (e.g., MiniRex, Rex, Rex3), link it to the corresponding upgrade page under `upgrades/`.
- **Anchor targets must be headings.**
  Any content that is the target of a `#fragment` link MUST be a markdown heading (`##`, `###`, etc.), not bold text or other inline formatting.
  GitBook generates anchors only from headings.

## Formatting Preferences

- Use tables for structured data (gas costs, opcode lists, resource limits, constants).
- Use unambiguous table values. Write "Unlimited", "No limit", or "N/A" — never use bare dashes ("—") which are ambiguous (not applicable? unknown? unlimited?).
- Use `<details>` blocks for unstable-spec features only — never for a frozen spec that is merely unscheduled.
- Use `{% hint style="info" %}` sparingly — only for non-normative notes that help implementers understand design intent. Never for developer tips.
- Use `{% hint style="warning" %}` for unstable spec warnings.
  A frozen-but-unscheduled spec gets `{% hint style="info" %}` instead: it is a status note, not a caveat about correctness.
- Do NOT use `{% hint style="success" %}` in spec pages — it implies developer guidance.
- Do NOT use `{% hint style="danger" %}` for normative rules — normative rules belong in plain prose with MUST/MUST NOT. Reserve `{% hint style="danger" %}` only for deprecation notices.
