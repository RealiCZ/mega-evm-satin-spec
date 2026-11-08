---
description: Satin (unstable) — Satin EVM Overview. The index of Satin's execution pages: two-pool gas, the gas schedule, state and history gas, the write and take-back patterns, forwarding, the resource limits and their accounting, authorizations, SELFDESTRUCT, the limit stop, gas detention, outcomes, transfer logs, size limits and precompiles.
spec: Satin
maturity: unstable
---

# Satin EVM Overview

{% hint style="warning" %}
**Unstable** — Satin is under active development: every value and rule on this page may change before Satin is frozen.
{% endhint %}

Abstract: An index of the pages that specify how a transaction and a system call execute: how gas is split into pools and ledgers and what each charge costs, which resource limits hold a frame and a transaction and how crossing one stops a frame, how gas detention bounds computation after a read of volatile data, and the opcode-level changes to transfers, creations and precompiles.

## Scope

These pages specify execution: everything from the start of a transaction's or a system call's execution to its settlement.
The base layer these rules build on is [Base Layer](../base-layer.md); validation before execution, deposits, the pre-block calls, block limits and the stateless witness are specified under [Transactions and Blocks](../block/overview.md), and the system contracts under [System Contracts](../system-contracts/overview.md).
Each rule of these pages carries an id `SATIN-<AREA>-<NNN>` written at the start of the paragraph or list item that states it.

## Specifications

### Gas

- [Two-Pool Gas](gas-model.md) (`POOL`) — the regular-gas budget under the 200,000,000 [execution cap](../../glossary.md#execution-cap) and the state-gas [reservoir](../../glossary.md#reservoir); the three kinds of charge; how frames receive, return and give back the reservoir; the transaction's settlement and its three gas ledgers.
- [Gas Schedule and Intrinsic Gas](gas-schedule.md) (`SCHED`) — the Amsterdam schedule with its three changes, the entry table, the EIP-2780 intrinsic regular gas and floor, the charges made before the first frame and their out-of-gas path, the code-deposit charge order, and the addresses warm from a transaction's start.
- [State Gas and SALT Pricing](state-gas.md) (`STATE`) — `entry × m` on EIP-8037's byte counts at the cost per state byte, the [SALT bucket](../../glossary.md#salt-bucket) multiplier, where each state charge is made and how it is given back.
- [History Gas and the History Allowance](history-gas.md) (`HIST`) — the price per byte of what a transaction appends to history, the byte table, when each history charge is made and given back, the refill order, the exemptions, and the [history allowance](../../glossary.md#history-allowance) of a value call.
- [Write and Take-Back Patterns](take-backs.md) (`TAKE`) — every pattern in which a write is made and taken back, from a slot written `0 → x → 0` to a failed deposit, with what each gas ledger, the EIP-3529 refund counter and each resource count does, and which frame a give-back goes to.
- [Gas Forwarding](gas-forwarding.md) (`FWD`) — the 98/100 cap on forwarded regular gas, the value-transfer stipend, and the reservoir share a child receives.

### Resource limits

- [Resource Limits](resource-limits.md) (`LIM`) — data size, KV updates and state growth per transaction and per frame, the frame budgets and their merge, the order at one site, frame starts, and the rule that the limits are protocol values.
- [Resource Accounting](resource-accounting.md) (`ACCT`) — what each dimension counts: the data-size items, [write records](../../glossary.md#write-record) and state growth with its `SSTORE` transition table.
- [EIP-7702 Authorizations Before the First Frame](authorizations.md) (`AUTH`) — the simulation that decides an authorization list, the all-or-nothing skip, and the charges and warmth of an applied list.
- [SELFDESTRUCT and the Destruction Table](selfdestruct.md) (`SD`) — EIP-6780 destruction, the table that refills and takes back what a transaction created and destroys, the marked account, and the creation-collision rule.

### Stops, detention and outcomes

- [Limit Stops](limit-stops.md) (`STOP`) — the revert-class stop every limit makes, what it reverts and keeps, how a stopped transaction settles, and the `MegaLimitExceeded` revert data.
- [Gas Detention](gas-detention.md) (`DET`) — volatile data, compute, the limit a read sets, the spendable and withheld parts of a frame's regular gas, the crossing, and the precompile and interceptor cases.
- [Halts, Reverts and Stops](outcomes.md) (`OUT`) — the one rule that decides how a frame and a transaction end, and every exception to it, each linked to the page that holds its detail.

### Opcode-level changes

- [EIP-7708 Transfer Logs](transfer-logs.md) (`LOG`) — the `Transfer` log every movement of value emits, what logs nothing, and what a transfer log counts.
- [Contract Size Limits](contract-limits.md) (`SIZE`) — the deployed-code and initcode limits and the creation opcodes' check order.
- [Precompiles](precompiles.md) (`PCMP`) — the precompile set, KZG point evaluation at 100,000 gas, the input size limits, and how a precompile address is dispatched and priced.

## Spec History

- [Satin](../../upgrades/satin.md) — Restated the execution layer on Optimism Karst with EIP-8037 two-pool gas, history gas, catchable limit stops and gas detention on withheld gas; the Rex6 execution pages it succeeds start at [EVM Overview](../../evm/overview.md).
