---
description: Satin (unstable) — The Stateless Witness. Stub of the Satin specification: the rules this page will specify.
spec: Satin
maturity: unstable
---

# The Stateless Witness

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
This page is a stub. It lists what the page will specify; the specification text is written after the outline is reviewed.
{% endhint %}

Abstract: What a stateless validator re-executing a block is given: the accounts, slots, code, block hashes, SALT capacities and oracle answers the block read, where each read lands, and the check a replay must pass.

## Specification

The rules this page will specify, by their proposed ids:

- `SATIN-WIT-001` — A block's witness holds every account and slot the block loads (pre-block steps and included transactions) as held before the block, absent accounts as absent with no slots, empty slots of held accounts as zero, with every such account's pre-block code; every hash BLOCKHASH read; every exported SALT bucket's capacity; the oracle answers the included transactions recorded, in block order.
- `SATIN-WIT-002` — A transaction loads every account and slot its execution reads (validation, fee settlement, every frame, reverted, halted and failed-deposit ones included); a failed frame's writes are taken back, not its reads.
- `SATIN-WIT-003` — The L1 block info a transaction is priced against is loaded by the pre-block phase for the whole block.
- `SATIN-WIT-004` — A read gas or a limit skipped loads nothing, except an authority the authorization preflight consulted.
- `SATIN-WIT-005` — Execution reports its loads in the states the block commits (each pre-block step's, each transaction's returned state, naming every account and slot loaded, written or not), independent of how the node caches state.
- `SATIN-WIT-006` — A slot of an account the chain does not hold before the block is not recorded; a validator answers it with zero.
- `SATIN-WIT-007` — The code in the witness is the chain's before the block, not the code a returned state carries.
- `SATIN-WIT-008` — Where each read lands: a transaction's returned state (sender, recipient or created address, every frame's loads, the fee recipients, the registry's account and slot, consulted authorities, a keyless signer and deploy address); the pre-block states, one per step in order, each committed whole and collected as committed.
- `SATIN-WIT-009` — BLOCKHASH reads outside the journal and is exported; SALT capacities and oracle answers are read outside the database and exported or recorded.
- `SATIN-WIT-010` — A validator is given beside the witness: the header, the chain configuration, the parent hash, the parent beacon block root, the extra data, the deposit-only flag, whether Satin activates, and the slot number the building node supplied.
- `SATIN-WIT-011` — The L1 block info: the contract at 0x4200…0015, slots 1, 3, 7, 8 and, only when the Ecotone scalars are empty, 5; read on the block's state; the pre-block phase reads the account and all five slots and commits them as a read-only state after every other step; a state without the contract records it absent; one that cannot serve them fails the block as an internal error.
- `SATIN-WIT-012` — The reads a validator makes again are skipped again on replay and need not be carried.
- `SATIN-WIT-013` — The SALT bucket export: the buckets answered with a valid capacity during the block, emptied at the block's start, failed lookups excluded; the witness proves every bucket in it; several executions take the union; pre-block calls and system transactions add none.
- `SATIN-WIT-014` — The block-hash export: every hash BLOCKHASH was served, emptied at the block's start.
- `SATIN-WIT-015` — The oracle records: each read a transaction makes through the service, with its answer (none allowed), in order on its outcome; a node takes the included transactions' records in block order; a validator either answers from them or runs no service and reads the Oracle's slots, with the conditions under which that reproduces the block.
- `SATIN-WIT-016` — A block replayed on exactly its witness produces the same receipts, state changes, gas ledgers, logs and block counters and reads nothing outside it; its exports are a subset of the building node's.
- `SATIN-WIT-017` — An address the state holds no account for is answered as no account, never as an empty account.

## Spec History

- [Satin](../../upgrades/satin.md) — The reviewers' delta of Satin against Rex6.
