---
description: Satin (unstable) — Satin Transactions and Blocks Overview. An index of the Satin pages on transaction validation, deposits, the pre-block system calls, the block's limits, the stateless witness and activation.
spec: Satin
maturity: unstable
---

# Satin Transactions and Blocks Overview

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
{% endhint %}

Abstract: An index of the Satin pages that specify how transactions are admitted to a block and how a block is executed around them: validation, deposits, the pre-block system calls, the block's limits and packing, the stateless witness, and activation.

## Scope

These pages specify what lies around a transaction's execution: whether a transaction may be included at all, how a deposit is executed when it cannot be refused, what the block does before its first transaction, what the block counts and when it skips a transaction, what a stateless validator is given to re-execute the block, and when and on what state Satin starts.
How a transaction executes once it runs is specified by the [execution pages](../evm/overview.md), and the system contracts it may call by the [system-contract pages](../system-contracts/overview.md).

## Specifications

- [Transaction Validation and Refusals](transaction-validation.md) — The checks a transaction is held to before inclusion: the body against the data-size limit, the intrinsic gas with the body's history gas, the calldata floor, the execution cap, the system-address shape and the chain id; the order of Satin's own checks; and why a deposit is never rejected.
- [Deposit Transactions](deposits.md) — What a deposit pays and is held to, the state gas of the caller account it creates, the failed deposit and what it applies, reports and keeps, and the prestates outside the specification.
- [System Calls and the Pre-Block Sequence](system-calls.md) — The split of a system call's gas, the fixed pre-block budget, the pre-block steps — the EIP calls, the system contracts' deployment, the role change, the resolution of the live system address — and their order, the due-change predicate, and what a failed pre-block step does.
- [Block Limits and Packing](block-limits.md) — What a block counts, the three packing budgets that never refuse a deposit and hold a Mega System Transaction as any other, when a transaction is skipped, the checked commit of a candidate, and building policy.
- [The Stateless Witness](stateless-witness.md) — What a block's witness holds, where each read lands, the inputs given beside it, the exports of block hashes and SALT buckets, the L1 block slots a fee computation or a footprint read, and the replay check.
- [Activation and Rex-Era Carry-Over](activation.md) — `satinTime` and the chain configuration, the base forks, the deposit-only activation block and its factory check, activation from genesis, the configuration the spec fixes, and the state Satin requires.

## Spec History

- [Rex6](../../upgrades/rex6.md) — The block-level limits and pre-block calls of the Rex era, specified on the Rex6 pages.
- [Satin](../../upgrades/satin.md) — Packing budgets, the pre-block sequence, the stateless witness, and activation on the state the Rex era left.
