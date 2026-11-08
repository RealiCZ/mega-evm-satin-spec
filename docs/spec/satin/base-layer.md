---
description: Satin (unstable) — Base Layer. Stub of the Satin specification: the rules this page will specify.
spec: Satin
maturity: unstable
---

# Base Layer

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
This page is a stub. It lists what the page will specify; the specification text is written after the outline is reviewed.
{% endhint %}

Abstract: The base Satin builds on (Optimism Karst, Ethereum Osaka), the opcodes it adds, the inherited caps it does not apply, and the Karst block rules it keeps.

## Specification

The rules this page will specify, by their proposed ids:

- `SATIN-BASE-001` — Every standard EVM, transaction and block rule the Satin section does not override is Optimism Karst's, the Optimism changes of Jovian and Karst and the Ethereum changes of Osaka included.
- `SATIN-BASE-002` — EIP-7825's per-transaction gas limit cap is not applied; a transaction's gas limit is bounded by the block's gas limit.
- `SATIN-BASE-003` — EIP-8037's TX_MAX_TOTAL_GAS_LIMIT (2^32 − 1) is not applied.
- `SATIN-BASE-004` — DUPN (0xE6), SWAPN (0xE7) and EXCHANGE (0xE8) of EIP-8024 are enabled.
- `SATIN-BASE-005` — SLOTNUM (0x4B) of EIP-7843 pushes the block's slot number, an unsigned 64-bit value supplied with the block; a block supplied no number runs with zero.
- `SATIN-BASE-006` — A block in which Satin, or an Optimism fork at or after Jovian, activates admits only deposits; a non-deposit transaction in it makes the block invalid.
- `SATIN-BASE-007` — A fork activates in a block when it is active at the block's timestamp and not at the parent's, as the chain configuration schedules it; an unscheduled fork never activates.
- `SATIN-BASE-008` — A Mega System Transaction is refused in such a block, and the Satin activation block owes no Oracle write.
- `SATIN-BASE-009` — Each non-deposit transaction's data-availability footprint (compressed size × the L1 block contract's footprint gas scalar) accumulates against the block gas limit and is reported as blob gas used; a transaction that does not fit is not included; no scalar in state means zero.
- `SATIN-BASE-010` — Non-deposit transactions are priced against the L1 block information the block's L1 attributes deposit wrote, as the state stands before the first non-deposit transaction other than a Mega System Transaction; the footprint scalar is read again for each non-deposit transaction, a Mega System Transaction included.

## Spec History

- [Satin](../upgrades/satin.md) — The reviewers' delta of Satin against Rex6.
