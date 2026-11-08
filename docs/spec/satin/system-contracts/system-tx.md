---
description: Satin (unstable) — Mega System Transactions and the Protocol's Own Transactions. Stub of the Satin specification: the rules this page will specify.
spec: Satin
maturity: unstable
---

# Mega System Transactions and the Protocol's Own Transactions

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
This page is a stub. It lists what the page will specify; the specification text is written after the outline is reviewed.
{% endhint %}

Abstract: Which transactions are Mega System Transactions, how one is validated and promoted to a deposit, which transactions are system-originated, and what that exempts them from.

## Specification

The rules this page will specify, by their proposed ids:

- `SATIN-MST-001` — The system shape is tested on the transaction's own fields: type 0x0, a call (not a creation) to an address on MEGA_SYSTEM_TX_WHITELIST (the Oracle).
- `SATIN-MST-002` — A transaction of the system shape whose caller is the live system address is a Mega System Transaction.
- `SATIN-MST-003` — A transaction from the live system address without the system shape is invalid, whatever its type: a non-deposit is rejected, a deposit is a failed deposit (one carrying the promotion's source hash included).
- `SATIN-MST-004` — A transaction from any other address, a retired system address included, is an ordinary transaction.
- `SATIN-MST-005` — A Mega System Transaction is validated before promotion, a failure being a rejection: it carries the chain's id, its nonce is the system address's, and the system address has no code (EIP-3607); it then executes as a deposit.
- `SATIN-MST-006` — The promotion stamps the source hash keccak256("MEGA_SYSTEM_TRANSACTION").
- `SATIN-MST-007` — A transaction is system-originated when it is a Mega System Transaction before or after promotion, when its caller is 0xff…fe, or when it is a deposit carrying the promotion's source hash, decided from its own fields wherever it is executed.
- `SATIN-MST-008` — A system-originated transaction and every system call are priced at m = 1 without reading a bucket, pay no history gas, are stopped by no per-transaction limit or frame budget, are not detained, and still have their usage counted.
- `SATIN-MST-009` — A system-originated transaction's usage is reported and counts toward the block's counters; the pre-block calls count toward neither the counters nor the limits.
- `SATIN-MST-010` — A user's deposit is not system-originated.

## Spec History

- [Satin](../../upgrades/satin.md) — The reviewers' delta of Satin against Rex6.
