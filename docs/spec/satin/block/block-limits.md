---
description: Satin (unstable) — Block Limits and Packing. Stub of the Satin specification: the rules this page will specify.
spec: Satin
maturity: unstable
---

# Block Limits and Packing

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
This page is a stub. It lists what the page will specify; the specification text is written after the outline is reviewed.
{% endhint %}

Abstract: What a block counts of its transactions, the three packing budgets and the transactions they never refuse, the block gas limit, and what a builder may do as policy that a validator never applies.

## Specification

The rules this page will specify, by their proposed ids:

- `SATIN-BLK-001` — A block counts per transaction its regular gas (as max(regular, floor)), state gas, history gas, history bytes, data size, KV updates and state growth.
- `SATIN-BLK-002` — Three counts are limited, each checked before the next transaction runs: BLOCK_DATA_LIMIT = 13,107,200, BLOCK_KV_UPDATE_LIMIT = 500,000, BLOCK_STATE_GROWTH_LIMIT = 1,000.
- `SATIN-BLK-003` — The transaction that moves a counter to or past its limit is included and a later ordinary transaction is skipped before it runs; a node may report the skip in the order data size, KV updates, state growth; a skip leaves no field in the block.
- `SATIN-BLK-004` — A builder that executes several candidates before committing one holds each to the counters, the block gas limit and the DA footprint again at commit; a validator's second check finds what its first found.
- `SATIN-BLK-005` — A builder does not commit a candidate whose sender's nonce or balance another commit moved since it executed; any other stale read is the builder's to handle.
- `SATIN-BLK-006` — A deposit and a Mega System Transaction are never refused by the three budgets or by building policy and count toward each; the block decides this before the transaction runs from its envelope and the live system address.
- `SATIN-BLK-007` — A Mega System Transaction is still held to the block gas limit and, its envelope being legacy, to the DA footprint.
- `SATIN-BLK-008` — Execution, state and history gas have no block limit beyond the block gas limit; history bytes are reported and not limited.
- `SATIN-BLK-009` — A transaction's declared gas limit fits in what the block has left.
- `SATIN-BLK-010` — The three packing budgets are protocol values fixed per spec; a validator holds a block to them and no other value.
- `SATIN-BLK-011` — A builder may pack tighter as policy (a per-transaction declared-gas, encoded-size or DA limit, block encoded-size or DA budgets, packing budgets below the protocol's), never refusing a deposit or a Mega System Transaction; a validator never applies a policy.
- `SATIN-BLK-012` — Satin sets no limit on a transaction's or block's encoded size.
- `SATIN-BLK-013` — A transaction is skipped for the block (and may be included later) when its gas limit or DA footprint does not fit, when the block reached a packing budget and it is neither a deposit nor a Mega System Transaction, or when it is a non-deposit in a deposit-only block; a block holding a transaction it should have skipped is invalid.

## Spec History

- [Satin](../../upgrades/satin.md) — The reviewers' delta of Satin against Rex6.
