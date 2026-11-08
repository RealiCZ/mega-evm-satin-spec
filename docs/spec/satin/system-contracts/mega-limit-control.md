---
description: Satin (unstable) — MegaLimitControl. Stub of the Satin specification: the rules this page will specify.
spec: Satin
maturity: unstable
---

# MegaLimitControl

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
This page is a stub. It lists what the page will specify; the specification text is written after the outline is reviewed.
{% endhint %}

Abstract: The remainingComputeGas() query under Satin: what it answers once compute is regular gas and detention withholds gas.

## Specification

The rules this page will specify, by their proposed ids:

- `SATIN-MLC-001` — Address 0x6342…0005, interface, bytecode, interception scope and value policy unchanged.
- `SATIN-MLC-002` — remainingComputeGas() answers the lesser of the calling frame's own regular gas with the gas the call forwarded counted back, and, once a read set a limit, what the limit leaves the transaction, read when the call reaches the interceptor.
- `SATIN-MLC-003` — The answer is regular gas only; the reservoir is not in it.
- `SATIN-MLC-004` — A transaction that calls the contract directly hears its own frame's regular gas, or less when detained from its start.

## Spec History

- [Satin](../../upgrades/satin.md) — The reviewers' delta of Satin against Rex6.
