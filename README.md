# MegaETH Specification

This repository holds the normative specification of MegaETH's verifiable behaviour: how MegaETH processes transactions, enforces resource limits and manages protocol state.
Any node implementation that produces the same outputs given the same inputs for every case this specification defines is a correct MegaETH node.

The specification lives in [`docs/spec/`](docs/spec/), laid out for GitBook ([`.gitbook.yaml`](docs/spec/.gitbook.yaml)): [`overview.md`](docs/spec/overview.md) is its front page and [`SUMMARY.md`](docs/spec/SUMMARY.md) its table of contents.
It has two parts.

- **Rex6, the latest frozen spec.**
  The pages outside `docs/spec/satin/` describe Rex6:
  - [`overview.md`](docs/spec/overview.md), [`hardfork-spec.md`](docs/spec/hardfork-spec.md) and [`glossary.md`](docs/spec/glossary.md);
  - [`evm/`](docs/spec/evm/), the MegaEVM;
  - [`system-contracts/`](docs/spec/system-contracts/);
  - [`upgrades/`](docs/spec/upgrades/), the network upgrade pages, MiniRex through Rex6.

  Each of them except the upgrade pages carries `spec: Rex6` in its front matter.
- **Satin, the next spec, which is unstable.**
  The Satin section, [`docs/spec/satin/`](docs/spec/satin/), restates MegaETH's execution layer on a new base, Optimism Karst (Ethereum Osaka), as a complete specification of its own.
  Satin is unstable and not scheduled on any network.
  Every Satin page carries `spec: Satin` and `maturity: unstable` in its front matter and opens with a warning that Satin is unstable and that the page may change before Satin is frozen.
  [`upgrades/satin.md`](docs/spec/upgrades/satin.md) is the reviewers' delta of Satin against Rex6; where a Satin page is written, that page is the specification of what it covers.

When Satin is frozen, the Satin section becomes the main body and the Rex6 pages move to a history part ([`docs/spec/AGENTS.md`](docs/spec/AGENTS.md), "Sealing Satin").

## Where to start

- [`docs/spec/overview.md`](docs/spec/overview.md): how MegaETH differs from Ethereum and Optimism, the spec progression, and the meaning of the normative key words.
- [`docs/spec/satin/overview.md`](docs/spec/satin/overview.md): the entry point of the Satin section: what Satin is, its base, its pages in reading order, and how its rules are identified.
- [`docs/spec/satin/rules.md`](docs/spec/satin/rules.md): the rule index, every rule id of the Satin section with the rule's first sentence and a link to the page that states it in full.
- [`docs/spec/satin/glamsterdam.md`](docs/spec/satin/glamsterdam.md): an informative map of Ethereum's Glamsterdam upgrade onto Satin; where it and a rule differ, the rule holds.
- [`docs/spec/satin/base-layer.md`](docs/spec/satin/base-layer.md): Optimism Karst as the base, the opcodes Satin adds, the inherited transaction gas caps it does not apply, and the Karst block rules it keeps.
- [`docs/spec/SUMMARY.md`](docs/spec/SUMMARY.md): the whole table of contents.

## How the Satin text is written

- **Normative language.**
  The key words MUST, MUST NOT, SHALL, SHOULD and MAY are read as BCP 14 (RFC 2119, RFC 8174) defines them, and only when they appear in capitals ([`docs/spec/overview.md`](docs/spec/overview.md)).
- **Rule ids.**
  Every normative rule carries a stable id `SATIN-<AREA>-<NNN>`, written once, as inline code at the start of the paragraph or list item that states it: "`SATIN-POOL-005` A node MUST …".
  `AREA` is the code of the page the rule was first written on, and `NNN` is a three-digit number.
  A table whose rows are each a rule carries one id, and a row is cited as `<id>/<first cell>`.
- **One home per rule.**
  No rule is stated twice.
  A page that gathers rules whose detail lives elsewhere states the unified rule once and links the page that holds the detail.
- **Rules in the text, edges in the cases.**
  Worked examples and edge figures live in the conformance cases, not in the rules: each case cites the rules it pins by rule id, and the specification names no case.
  A case is added before an example it replaces leaves the text; a figure that motivates a rule may stay in an Abstract or a Rationale.

The area codes and the page each names ([`plan/rule-ids.md`](plan/rule-ids.md)):

| Area | Page |
| --- | --- |
| `BASE` | [Base Layer](docs/spec/satin/base-layer.md) |
| `POOL` | [Two-Pool Gas](docs/spec/satin/evm/gas-model.md) |
| `SCHED` | [Gas Schedule and Intrinsic Gas](docs/spec/satin/evm/gas-schedule.md) |
| `STATE` | [State Gas and SALT Pricing](docs/spec/satin/evm/state-gas.md) |
| `HIST` | [History Gas and the History Allowance](docs/spec/satin/evm/history-gas.md) |
| `TAKE` | [Write and Take-Back Patterns](docs/spec/satin/evm/take-backs.md) |
| `FWD` | [Gas Forwarding](docs/spec/satin/evm/gas-forwarding.md) |
| `LIM` | [Resource Limits](docs/spec/satin/evm/resource-limits.md) |
| `ACCT` | [Resource Accounting](docs/spec/satin/evm/resource-accounting.md) |
| `AUTH` | [EIP-7702 Authorizations Before the First Frame](docs/spec/satin/evm/authorizations.md) |
| `SD` | [SELFDESTRUCT and the Destruction Table](docs/spec/satin/evm/selfdestruct.md) |
| `STOP` | [Limit Stops](docs/spec/satin/evm/limit-stops.md) |
| `DET` | [Gas Detention](docs/spec/satin/evm/gas-detention.md) |
| `OUT` | [Halts, Reverts and Stops](docs/spec/satin/evm/outcomes.md) |
| `LOG` | [EIP-7708 Transfer Logs](docs/spec/satin/evm/transfer-logs.md) |
| `SIZE` | [Contract Size Limits](docs/spec/satin/evm/contract-limits.md) |
| `PCMP` | [Precompiles](docs/spec/satin/evm/precompiles.md) |
| `SYSC` | [System Contracts](docs/spec/satin/system-contracts/overview.md) |
| `ICPT` | [Call Interception](docs/spec/satin/system-contracts/interception.md) |
| `ORCL` | [Oracle](docs/spec/satin/system-contracts/oracle.md) |
| `HPTS` | [High-Precision Timestamp](docs/spec/satin/system-contracts/high-precision-timestamp.md) |
| `KEY` | [KeylessDeploy](docs/spec/satin/system-contracts/keyless-deploy.md) |
| `MAC` | [MegaAccessControl](docs/spec/satin/system-contracts/mega-access-control.md) |
| `MLC` | [MegaLimitControl](docs/spec/satin/system-contracts/mega-limit-control.md) |
| `REG` | [SequencerRegistry](docs/spec/satin/system-contracts/sequencer-registry.md) |
| `MST` | [Mega System Transactions and the Protocol's Own Transactions](docs/spec/satin/system-contracts/system-tx.md) |
| `VAL` | [Transaction Validation and Refusals](docs/spec/satin/block/transaction-validation.md) |
| `DEP` | [Deposit Transactions](docs/spec/satin/block/deposits.md) |
| `PBLK` | [System Calls and the Pre-Block Sequence](docs/spec/satin/block/system-calls.md) |
| `BLK` | [Block Limits and Packing](docs/spec/satin/block/block-limits.md) |
| `WIT` | [The Stateless Witness](docs/spec/satin/block/stateless-witness.md) |
| `ACT` | [Activation and Rex-Era Carry-Over](docs/spec/satin/block/activation.md) |

The index pages ([`satin/overview.md`](docs/spec/satin/overview.md), [`satin/evm/overview.md`](docs/spec/satin/evm/overview.md), [`satin/block/overview.md`](docs/spec/satin/block/overview.md)) state no rule and have no area.

## The conformance suite

The conformance suite is [Mega EEST](https://github.com/RealiCZ/mega-eest).
Each of its cases cites the rules it pins by rule id, in its `rules` field, and names by commit the snapshot of this repository it was written against.

## `plan/`

[`plan/`](plan/) is the working material the Satin section was written from.
It is not normative: the specification is the pages under `docs/spec/`.

- [`inventory.md`](plan/inventory.md): every source a Satin rule comes from and what each covers.
- [`outline.md`](plan/outline.md): the page list of the Satin section in reading order and, for every page, each rule it was to specify, with its sources.
- [`questions.md`](plan/questions.md): the questions the owner had to decide before the Satin text was written, each with its evidence, options and decision.
- [`decisions.md`](plan/decisions.md): the owner's decisions, each with its reason: the answers to `questions.md`, and the later items (QI) that arose from comparing the Satin rules with Rex6 and from checks of the written text.
- [`rule-ids.md`](plan/rule-ids.md): the rule-id registry: the id form, the area codes, how ids survive edits, and how tests and fixtures cite them (the scheme was adopted by [QF-09](plan/questions.md#qf-09)).
- [`changes-evm.md`](plan/changes-evm.md) and [`changes-blocks.md`](plan/changes-blocks.md): the change lists, by rule id, of where an implementation differs from the text of the Satin pages and what must change; the first covers the execution pages, the second the overview, the base layer, the system contracts and the block pages.

## `scripts/rule-index.py`

[`scripts/rule-index.py`](scripts/rule-index.py) generates [`docs/spec/satin/rules.md`](docs/spec/satin/rules.md) from the pages of the Satin section; that page is not edited by hand.
It finds each rule id written as inline code at the start of a paragraph or list item, and lists as retired the ids under a "Retired" heading or whose text starts with "Retired".
It fails, writing nothing, when:

- an id is defined on more than one line;
- an id is both active and retired;
- a relative link on a Satin page names a file that does not exist;
- a page has no title.

With `--check` it also fails when `rules.md` is not up to date with the pages.
From the repository root, with Python 3:

```sh
python3 scripts/rule-index.py           # write docs/spec/satin/rules.md
python3 scripts/rule-index.py --check   # fail when docs/spec/satin/rules.md is not up to date
```

## How changes land

- Changes land as pull requests against `main`.
- Every page follows the writing rules in [`docs/spec/AGENTS.md`](docs/spec/AGENTS.md): page structure, normative language, constants, and the conventions of the Satin section.
- The pages under `evm/` and `system-contracts/` keep describing Rex6 and are not edited for Satin; a correction of their Rex6 content is the only change they take.
- `docs/spec/satin/rules.md` is regenerated with `scripts/rule-index.py`, never edited by hand.
- Rule ids ([`docs/spec/AGENTS.md`](docs/spec/AGENTS.md), [`plan/rule-ids.md`](plan/rule-ids.md)):
  - an id is assigned once and never reused, renumbered or reassigned to a different rule;
  - rewording that keeps the behaviour keeps the id;
  - a rule that moves to another page keeps its id, and its area code stays that of its first page;
  - a rule that is split keeps its id on the part that keeps its main requirement, and every other part takes the next free number of its area;
  - merging rules keeps the lowest id and retires the others;
  - a change of behaviour retires the id and assigns a new one, so a fixture that cites an id always means one behaviour;
  - retired ids are listed at the end of their page's Specification section, each with the id that replaced it, or "removed".
