---
description: Satin (unstable) — Transaction Validation and Refusals. Stub of the Satin specification: the rules this page will specify.
spec: Satin
maturity: unstable
---

# Transaction Validation and Refusals

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
This page is a stub. It lists what the page will specify; the specification text is written after the outline is reviewed.
{% endhint %}

Abstract: The checks a transaction is held to before inclusion, their order and the error each names, the chain-id rule, and what a pool can check without state.

## Specification

The rules this page will specify, by their proposed ids:

- `SATIN-VAL-001` — A transaction is rejected when its body, with WRITE_RECORD_SIZE bytes for every authorization entry (applied or not), exceeds the transaction data-size limit, unless it is system-originated.
- `SATIN-VAL-002` — A transaction is rejected when its gas limit is below its intrinsic regular gas plus its body's history gas (CallGasCostMoreThanGasLimit), when its floor exceeds its gas limit (GasFloorMoreThanGasLimit), or when its gas limit exceeds EXECUTION_CAP while its intrinsic regular gas or floor exceeds the cap (GasFloorMoreThanGasLimit).
- `SATIN-VAL-003` — The checks' order, the first failure naming the error: the body against the data-size limit before any gas; the gas limit against the intrinsic regular gas alone; the floor; the execution cap; the gas limit against the intrinsic regular gas plus the body's history.
- `SATIN-VAL-004` — A transaction that passes validation cannot cross the data-size limit before its first frame.
- `SATIN-VAL-005` — A transaction is rejected when sent from the live system address without the system shape.
- `SATIN-VAL-006` — A transaction is rejected when it carries a chain id that is not the chain's, or is a typed transaction without one; a legacy transaction without a chain id is valid unless it is a Mega System Transaction; the check holds whatever the node's configuration says.
- `SATIN-VAL-007` — A transaction is rejected when it is a Mega System Transaction failing the chain-id, nonce or EIP-3607 check, or when it fails any inherited validation.
- `SATIN-VAL-008` — A deposit is never rejected for a validation failure: it is included as a failed deposit; a read the node fails to make is not a validation check.
- `SATIN-VAL-009` — What a transaction pool can decide without state, and what it cannot (whether a recipient, created account or authority is new; the start records' history).

## Spec History

- [Satin](../../upgrades/satin.md) — The reviewers' delta of Satin against Rex6.
