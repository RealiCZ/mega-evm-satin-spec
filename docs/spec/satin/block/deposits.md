---
description: Satin (unstable) — Deposit Transactions. Stub of the Satin specification: the rules this page will specify.
spec: Satin
maturity: unstable
---

# Deposit Transactions

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
This page is a stub. It lists what the page will specify; the specification text is written after the outline is reviewed.
{% endhint %}

Abstract: Deposits under Satin: what they pay and are held to, the account a deposit creates for its caller, when a deposit becomes a failed deposit and what a failed deposit keeps.

## Specification

The rules this page will specify, by their proposed ids:

- `SATIN-DEP-001` — A deposit pays no history gas, its body, calldata and deposited code included.
- `SATIN-DEP-002` — A deposit that is not system-originated is priced by bucket, held to every per-transaction limit and frame budget, and detained.
- `SATIN-DEP-003` — A deposit-like transaction whose caller does not exist is charged that account's new-account state gas exactly once, before the first frame; the account is always created and kept and is one unit of state growth.
- `SATIN-DEP-004` — A deposit that fails a validation check, cannot pay a charge made before its first frame, or whose own frame halts is a failed deposit: its sender's nonce is bumped, its mint credited, its whole gas limit (reservoir included) used, and nothing else applied.
- `SATIN-DEP-005` — A failed deposit reports its whole gas limit as regular gas and no state or history gas on any ledger; its created caller carries no state gas and counts one unit of growth on the transaction and the block.
- `SATIN-DEP-006` — A failed deposit keeps the data size of its body and of the hints it admitted, and returns no withheld gas, unspent gas or reservoir.
- `SATIN-DEP-007` — A deposit that succeeds, reverts or is stopped by a limit settles as an ordinary transaction (a stop is a revert, not a failed deposit).
- `SATIN-DEP-008` — A deposit from the live system address, and one handed to the node already carrying the promotion's source hash, is a failed deposit; a system deposit is refused under Regolith and fails.
- `SATIN-DEP-009` — Where the floor binds, a deposit is charged nothing; only its receipt's and the block's figures move.
- `SATIN-DEP-010` — A deposit creating from a sender whose nonce cannot be bumped (2^64 − 1) succeeds with nothing created and nothing counted.
- `SATIN-DEP-011` — A failed deposit whose mint would overflow its sender's balance.
- `SATIN-DEP-012` — Whether a deposit that fails before its first frame loads its recipient.
- `SATIN-DEP-013` — A deposit carrying a gas price.

## Spec History

- [Satin](../../upgrades/satin.md) — The reviewers' delta of Satin against Rex6.
