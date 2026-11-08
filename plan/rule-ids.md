# Satin Rule Ids — Proposal

A proposal for the owner: one stable id per normative rule of the Satin section, so that tests, fixtures, reviews and the two implementations can name the rule they exercise.
It is applied only to [outline.md](outline.md) and to the stubs' rule lists so far; no specification text carries an id until the owner accepts the scheme ([QF-09](questions.md#qf-09)).

## Form

`SATIN-<AREA>-<NNN>`

- `SATIN` — the spec line the rule belongs to.
- `<AREA>` — the code of the page the rule was first written on, two to five capital letters (table below).
- `<NNN>` — a three-digit number, assigned in order of first writing within the area, from `001`.

Examples: `SATIN-POOL-005` (the execution cap and the initial split of the gas limit), `SATIN-STOP-004` (the crossing frame reverts with `MegaLimitExceeded`), `SATIN-KEY-005` (the fifteen keyless steps).

| Area | Page |
| --- | --- |
| `BASE` | `satin/base-layer.md` |
| `POOL` | `satin/evm/gas-model.md` |
| `SCHED` | `satin/evm/gas-schedule.md` |
| `STATE` | `satin/evm/state-gas.md` |
| `HIST` | `satin/evm/history-gas.md` |
| `TAKE` | `satin/evm/take-backs.md` |
| `FWD` | `satin/evm/gas-forwarding.md` |
| `LIM` | `satin/evm/resource-limits.md` |
| `ACCT` | `satin/evm/resource-accounting.md` |
| `AUTH` | `satin/evm/authorizations.md` |
| `SD` | `satin/evm/selfdestruct.md` |
| `STOP` | `satin/evm/limit-stops.md` |
| `DET` | `satin/evm/gas-detention.md` |
| `OUT` | `satin/evm/outcomes.md` |
| `LOG` | `satin/evm/transfer-logs.md` |
| `SIZE` | `satin/evm/contract-limits.md` |
| `PCMP` | `satin/evm/precompiles.md` |
| `SYSC` | `satin/system-contracts/overview.md` |
| `ICPT` | `satin/system-contracts/interception.md` |
| `ORCL` | `satin/system-contracts/oracle.md` |
| `HPTS` | `satin/system-contracts/high-precision-timestamp.md` |
| `KEY` | `satin/system-contracts/keyless-deploy.md` |
| `MAC` | `satin/system-contracts/mega-access-control.md` |
| `MLC` | `satin/system-contracts/mega-limit-control.md` |
| `REG` | `satin/system-contracts/sequencer-registry.md` |
| `MST` | `satin/system-contracts/system-tx.md` |
| `VAL` | `satin/block/transaction-validation.md` |
| `DEP` | `satin/block/deposits.md` |
| `PBLK` | `satin/block/system-calls.md` |
| `BLK` | `satin/block/block-limits.md` |
| `WIT` | `satin/block/stateless-witness.md` |
| `ACT` | `satin/block/activation.md` |

The index pages (`satin/overview.md`, `satin/evm/overview.md`, `satin/block/overview.md`) state no rule and have no area.
The outline assigns 384 ids over 31 areas; the area `TAKE`, added with the page of write and take-back patterns, takes its ids from `SATIN-TAKE-001` in the page's order.

## One rule, one id

- A rule is one sentence, list item or table row with normative weight that a test could pass or fail on its own: one requirement, or one closely bound group (a check and the error it names, a charge and its order).
- A table whose rows are each a rule (the gas entry table, the SSTORE transition table, the keyless steps, the destruction table) has one id for the table and cites a row as `SATIN-SCHED-003/<row>`, the row named by its first cell (`SATIN-KEY-005/step-12`).
- Descriptive text (Motivation, Rationale, examples, Security Considerations) carries no id.

## How it is written

The id is written once, as inline code at the start of the paragraph or list item that states the rule:

```markdown
- `SATIN-POOL-011` <the rule about a child frame's reservoir share, in normative language>
```

A leading id is visible in the gitbook, searchable with `grep`, and survives reformatting of the sentence after it.
GitBook makes anchors only from headings, so the id is not a link target; a link to a rule links the page section and names the id in its text.

Rejected forms: a heading per rule (hundreds of headings, and a heading cannot hold a rule's full text); an HTML comment (invisible to readers and to reviewers of the rendered page); an id derived from the rule's text (changes with every rewording).

## How ids survive edits

1. An id is assigned once and never reused, renumbered or reassigned to a different rule.
2. **Rewording** that keeps the behaviour keeps the id.
3. **Moving** a rule to another page keeps the id; the area code stays the one of its first page.
4. **Splitting** a rule keeps the id on the part that keeps its main requirement; every other part takes the next free number of its area.
5. **Merging** rules keeps the lowest id and retires the others.
6. **A change of behaviour** retires the id and assigns a new one, so a fixture that cites an id always means one behaviour.
   While Satin is unstable a change of behaviour still retires the id: tests written against the old behaviour then fail by name rather than silently.
7. **Retired ids** are listed at the end of the page's Specification section, each with the id that replaced it, or "removed".
8. A spec after Satin that changes a Satin rule retires the Satin id from that spec on and gives the new behaviour an id of its own line (for example `SATIN1-POOL-001`, if the next spec is named Satin1); the Satin id keeps naming the Satin behaviour for replay.

The numbering in the outline is the first assignment; ids from the outline that phase 2 merges, splits or drops follow the rules above, so no id the outline published is reused.

## How tests and fixtures cite them

- **Unit and integration tests** in either implementation name the rules they exercise in a doc comment on the test, one id per line: `/// Spec: SATIN-POOL-011`.
  A test that exercises a table row names the row: `/// Spec: SATIN-KEY-005/step-12`.
- **Fixtures and scenarios** (JSON or TOML inputs shared by the two implementations, differential scenarios, probe lines) carry a `rules` field: `"rules": ["SATIN-STOP-006", "SATIN-ORCL-010"]`.
- **Review findings and questions** cite the rule id instead of a line number of a page, which moves with every edit.
- **A check in CI** (in the repository that holds the tests) reads every cited id and fails when an id does not exist in the Satin section or is retired, and lists the ids no test cites, so the coverage of the specification by tests is visible.
- **An index** (`satin/rule-index.md`, generated from the pages) lists every id with its page, its one-line summary and its status (active or retired), for readers and for the CI check.
  It is generated, never edited by hand.

## What stays open

- The area codes and the 384 numbers of the outline are a first assignment; the owner may rename an area before any id is written into a page ([QF-09](questions.md#qf-09)).
- Whether the citation comment form (`/// Spec:`) suits both implementations' test layouts is for their maintainers.
