---
description: Satin (unstable) — the entry point of the Satin section, the complete and standalone specification of MegaETH's execution layer under Satin.
spec: Satin
maturity: unstable
---

# Satin Specification

{% hint style="warning" %}
**Unstable** — Satin is under active development: every value and rule in the Satin section may change before Satin is frozen.
{% endhint %}

Abstract: The entry point of the Satin section: what Satin is, its maturity, the base it builds on, how the section is organized, and how its rules are identified.

## Scope

Satin is the MegaETH spec that follows [Rex6](../upgrades/rex6.md) on the spec ladder.
It is unstable and not scheduled on any network.

Satin does not add to Rex6's rules one by one: it restates MegaETH's execution layer on a new base, Optimism Karst (Ethereum Osaka).
The Satin section is therefore a complete specification of its own.
Every rule a Satin block executes on is stated in it, a rule Satin keeps from the Rex era included, and a reader never needs a Rex-era page to execute a Satin block.
A Rex-era rule the Satin section does not state does not apply to a Satin block.
The pages outside this section keep describing Rex6, the latest frozen spec.

The key words "MUST", "MUST NOT", "SHALL", "SHOULD" and "MAY" on the pages of this section are to be read as the [Specification overview](../overview.md) defines them (BCP 14).

### Rule ids

Every normative rule of the section carries a stable id of the form `SATIN-<AREA>-<NNN>`, written once, as inline code at the start of the paragraph or list item that states the rule, on the page that is the rule's home.
`AREA` names the page the rule was first written on, and `NNN` is a three-digit number.
An id is never reused or renumbered: a rule that is removed retires its id, and its page lists the retired ids at the end of its Specification section.
A table whose rows are each a rule carries one id, and a row is cited as `<id>/<first cell>`.
Tests, fixtures and reviews cite a rule by its id.
[Satin Rules](rules.md) lists every id of the section with a one-line summary and a link to its home page.

A page that gathers rules whose detail lives elsewhere — [Halts, Reverts and Stops](evm/outcomes.md), [Deposit Transactions](block/deposits.md) — states the unified rule once and links the page that holds the detail; no rule is stated twice.
A worked example lives in the conformance cases (Mega EEST), not in a rule: the rule cites the case that pins an edge by its case id, as `satin/sstore/clear/specification-example`, and a case is added before the example it replaces leaves the text.
A figure that motivates a rule may stay in an Abstract or a Rationale.

## Specifications

### The base

- [Base Layer](base-layer.md) — Optimism Karst (Ethereum Osaka) as the base, the opcodes Satin adds, the inherited transaction gas caps it does not apply, and the Karst block rules it keeps.

### Execution

- [Satin EVM Overview](evm/overview.md) — the index of the execution pages.
- [Two-Pool Gas](evm/gas-model.md) — regular gas under the execution cap, the state-gas reservoir, and the three gas ledgers.
- [Gas Schedule and Intrinsic Gas](evm/gas-schedule.md) — the Amsterdam schedule and EIP-2780 intrinsic gas.
- [State Gas and SALT Pricing](evm/state-gas.md) — state gas scaled by the SALT bucket the state lands in.
- [History Gas and the History Allowance](evm/history-gas.md) — the price of the bytes a transaction appends to history.
- [Write and Take-Back Patterns](evm/take-backs.md) — every write a transaction makes and takes back, and what each ledger and count does with it.
- [Gas Forwarding](evm/gas-forwarding.md) — the 98/100 forward of regular gas and of the reservoir.
- [Resource Limits](evm/resource-limits.md) — data size, KV updates and state growth per transaction and per frame.
- [Resource Accounting](evm/resource-accounting.md) — what each dimension counts and when.
- [EIP-7702 Authorizations Before the First Frame](evm/authorizations.md) — how an authorization list is decided, charged and counted.
- [SELFDESTRUCT and the Destruction Table](evm/selfdestruct.md) — what a destruction gives back.
- [Limit Stops](evm/limit-stops.md) — the revert-class stop every limit makes.
- [Gas Detention](evm/gas-detention.md) — detention on withheld gas after a volatile read.
- [Halts, Reverts and Stops](evm/outcomes.md) — how a frame and a transaction end.
- [EIP-7708 Transfer Logs](evm/transfer-logs.md) — the log every movement of value emits.
- [Contract Size Limits](evm/contract-limits.md) — the code and initcode size limits.
- [Precompiles](evm/precompiles.md) — the precompile set and its prices.

### System contracts

- [System Contracts](system-contracts/overview.md) — the six system contracts, their addresses and code, and their deployment in every block.
- [Call Interception](system-contracts/interception.md) — how the node answers a call to an intercepted method.
- [Oracle](system-contracts/oracle.md) — Oracle reads answered by the oracle service, and hints.
- [High-Precision Timestamp](system-contracts/high-precision-timestamp.md) — the timestamp wrapper over the Oracle's storage.
- [KeylessDeploy](system-contracts/keyless-deploy.md) — keyless deployment as a native creation.
- [MegaAccessControl](system-contracts/mega-access-control.md) — switching volatile-data access off for a call subtree.
- [MegaLimitControl](system-contracts/mega-limit-control.md) — the `remainingComputeGas()` query.
- [SequencerRegistry](system-contracts/sequencer-registry.md) — the registry of the system address and the sequencer.
- [Mega System Transactions and the Protocol's Own Transactions](system-contracts/system-tx.md) — the system-address transaction and what the protocol's own work is exempt from.

### Transactions and blocks

- [Satin Transactions and Blocks Overview](block/overview.md) — the index of the transaction and block pages.
- [Transaction Validation and Refusals](block/transaction-validation.md) — the checks a transaction is held to before inclusion.
- [Deposit Transactions](block/deposits.md) — what a deposit pays, and the failed deposit.
- [System Calls and the Pre-Block Sequence](block/system-calls.md) — the calls a block makes before its transactions.
- [Block Limits and Packing](block/block-limits.md) — the block's counters, its packing budgets and building policy.
- [The Stateless Witness](block/stateless-witness.md) — what a stateless validator re-executes a block from.
- [Activation and Rex-Era Carry-Over](block/activation.md) — when Satin takes effect and what it requires of the chain.

### The rule list

- [Satin Rules](rules.md) — every rule id of the section, generated from the pages.
- [Satin and Glamsterdam](glamsterdam.md) — an informative map of Ethereum's Glamsterdam onto Satin: what Satin adopts, changes and does not take, and the MegaETH mechanisms with no Glamsterdam counterpart.

## Spec History

- [Rex6](../upgrades/rex6.md) — The latest frozen spec, which Satin follows; its rules are specified on the pages outside this section.
- [Satin](../upgrades/satin.md) — The reviewers' delta of Satin against Rex6.
