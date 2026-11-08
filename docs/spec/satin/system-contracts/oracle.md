---
description: Satin (unstable) — Oracle. Stub of the Satin specification: the rules this page will specify.
spec: Satin
maturity: unstable
---

# Oracle

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
This page is a stub. It lists what the page will specify; the specification text is written after the outline is reviewed.
{% endhint %}

Abstract: The Oracle under Satin: how an SLOAD in its own frame answers from the oracle service, what such a read costs, and when a sendHint reaches the service and what it counts.

## Specification

The rules this page will specify, by their proposed ids:

- `SATIN-ORCL-001` — Address 0x6342…0001, version 2.0.0 bytecode; its read, restricted-write and auxiliary interfaces and its storage layout are Rex6's.
- `SATIN-ORCL-002` — An SLOAD in the Oracle's own frame loads the slot, then asks the oracle service; the service's value wins over whatever the slot holds, the frame's own earlier write included; with no value the slot's present value answers.
- `SATIN-ORCL-003` — Every such read is charged as a cold access (2,100), however often the slot was read, and the slot is loaded whichever source answers.
- `SATIN-ORCL-004` — A frame whose regular gas, withheld part included, cannot pay the cold access reads and asks nothing; a refused read asks nothing.
- `SATIN-ORCL-005` — A system call never asks the service: its read answers the chain's value and records no answer; a Mega System Transaction still asks.
- `SATIN-ORCL-006` — A sendHint reaches the service synchronously only when forwarded gas, carrying no value, from a frame whose volatile-data access is on; otherwise it is dropped and counts nothing; the call runs the Oracle's bytecode either way.
- `SATIN-ORCL-007` — The service is handed the hint's topic, its data and the address of the calling frame (the sender for a sendHint that is the transaction's own call).
- `SATIN-ORCL-008` — Only a CALL or STATICCALL to the Oracle is a sendHint; a CALLCODE or DELEGATECALL of the method reaches no service and counts nothing.
- `SATIN-ORCL-009` — An admitted hint counts the call's whole input length as data size on the transaction, before decoding, and pays no history; a top-level sendHint counts its input twice; the count stays whatever happens afterwards, an undecodable input included.
- `SATIN-ORCL-010` — A hint whose length would take the transaction over its data-size limit is neither forwarded nor counted and the call is answered with the stop without running bytecode; the block counts none of its bytes; the check is against the transaction limit alone.
- `SATIN-ORCL-011` — The Oracle authorizes writes on the sender alone, so no transaction from the system address other than a Mega System Transaction reaches it.

## Spec History

- [Satin](../../upgrades/satin.md) — The reviewers' delta of Satin against Rex6.
