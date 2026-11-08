---
description: Satin (unstable) — SELFDESTRUCT and the Destruction Table. Stub of the Satin specification: the rules this page will specify.
spec: Satin
maturity: unstable
---

# SELFDESTRUCT and the Destruction Table

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
This page is a stub. It lists what the page will specify; the specification text is written after the outline is reviewed.
{% endhint %}

Abstract: SELFDESTRUCT under EIP-6780 in Satin: the destruction table that refills the state gas and takes back the records of what a transaction created and destroys, the marked account afterwards, the beneficiary's rise, the order of a destruction's effects, and the creation-collision rule.

## Specification

The rules this page will specify, by their proposed ids:

- `SATIN-SD-001` — EIP-6780 semantics are inherited: a SELFDESTRUCT deletes an account only when the account was created in the same transaction.
- `SATIN-SD-002` — The first effective SELFDESTRUCT of an account created in the same transaction applies the destruction table to every part of it (leaf, code, slots), by its value at the transaction's start and before the destruction.
- `SATIN-SD-003` — A slot's value at the transaction's start is its original value at first access; a slot first accessed after the creation reads zero; one accessed before keeps the value it held.
- `SATIN-SD-004` — The table's rows: account leaf (absent or present at the start), deployed code (absent then present, absent then absent, present unreachable), slot (zero then non-zero, zero then zero, non-zero then any).
- `SATIN-SD-005` — A refill is the price that part was charged (entry × that charge's multiplier) and goes to the destroying frame, also when another frame paid; the absent leaf's charge is this transaction's charge for that leaf.
- `SATIN-SD-006` — State growth falls for the absent leaf and for each zero-then-non-zero slot and nothing else; the leaf's fall stands even when the creation added no rise.
- `SATIN-SD-007` — A record the table takes back returns its data size to the destroying frame's budget and its history gas to that frame, and the KV count falls; for a succeeding transaction frame this is the record's history once, and the settlement does not give it back again.
- `SATIN-SD-008` — Deployed code is not a record nor growth; code on the absent-then-present row returns its data size and history gas the same way.
- `SATIN-SD-009` — The give-back follows the refill order, is not an EIP-3529 refund, is credited with the completed write after every charge the opcode makes, and never raises the frame's remaining above its budget.
- `SATIN-SD-010` — When the destroying frame succeeds the give-back is unspent gas that returns up the chain; when it, or a frame containing it, fails, the mark and every effect of the table are discarded and records it took back stand again.
- `SATIN-SD-011` — A later SELFDESTRUCT of the same account while the mark stands applies the table for nothing.
- `SATIN-SD-012` — A SELFDESTRUCT of an account not created in the transaction applies no table and does not mark the account.
- `SATIN-SD-013` — While the mark stands the account adds no growth and keeps no state gas: an SSTORE of its slots neither rises nor falls nor charges nor refills (its regular gas unchanged).
- `SATIN-SD-014` — Code deposited after a constructor destroyed its own account pays no state gas but its data size and history gas, which no later destruction takes back.
- `SATIN-SD-015` — Value sent to the marked account is no rise and no record; the account is removed at the transaction's end with whatever it holds, and that removal takes nothing back again.
- `SATIN-SD-016` — A creation collides when the address holds non-empty code or a non-zero nonce, never on storage alone (EIP-7610 is not applied); what that means for the slots of such an address.
- `SATIN-SD-017` — An EIP-161-empty account whose leaf the state holds (non-empty storage) is the present-leaf row: the creation may charge new-account state gas and count a rise, and the destruction refills and subtracts neither.
- `SATIN-SD-018` — A SELFDESTRUCT that moves a non-zero balance to a distinct non-existent account is a rise (a repeated destruction included), a zero balance is not; the rise is held only after the operation's give-back.
- `SATIN-SD-019` — The order of a destruction: compute is decided first (a detention crossing applies nothing); then the table's give-back; then the positive effects in the order data size, KV updates, state growth (the records it makes, its transfer log, the beneficiary's growth); a crossing positive effect stops the frame and the operation keeps nothing.
- `SATIN-SD-020` — A SELFDESTRUCT's volatile reads of either end are committed only after its last fallible step.

## Spec History

- [Satin](../../upgrades/satin.md) — The reviewers' delta of Satin against Rex6.
