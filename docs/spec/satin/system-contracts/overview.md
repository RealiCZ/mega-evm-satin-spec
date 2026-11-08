---
description: Satin (unstable) — System Contracts. Stub of the Satin specification: the rules this page will specify.
spec: Satin
maturity: unstable
---

# System Contracts

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
This page is a stub. It lists what the page will specify; the specification text is written after the outline is reviewed.
{% endhint %}

Abstract: The registry of MegaETH system contracts under Satin: their addresses, the rule that their bytecode is the Rex-era bytecode, and how they differ from precompiles.

## Specification

The rules this page will specify, by their proposed ids:

- `SATIN-SYSC-001` — Six system contracts at fixed addresses under 0x6342…: the Oracle, the High-Precision Timestamp, KeylessDeploy, MegaAccessControl, MegaLimitControl and the SequencerRegistry.
- `SATIN-SYSC-002` — Their bytecode and ABI are Rex6's, but for the four errors IKeylessDeploy no longer declares.
- `SATIN-SYSC-003` — Satin deploys, upgrades and seeds no system contract; its activation block checks that they are present.
- `SATIN-SYSC-004` — A system contract is an account with code, not a precompile; an intercepted method is answered by the node, everything else runs the contract's bytecode.

## Spec History

- [Satin](../../upgrades/satin.md) — The reviewers' delta of Satin against Rex6.
