---
description: Satin (unstable) — Precompiles. Stub of the Satin specification: the rules this page will specify.
spec: Satin
maturity: unstable
---

# Precompiles

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
This page is a stub. It lists what the page will specify; the specification text is written after the outline is reviewed.
{% endhint %}

Abstract: The Satin precompile set: Optimism Karst's, with KZG point evaluation at MegaETH's price, and the input size limits the OP specification sets.

## Specification

The rules this page will specify, by their proposed ids:

- `SATIN-PCMP-001` — The precompile set is Karst's, with KZG point evaluation (0x0A) at a fixed 100,000 gas; every precompile not listed is as Karst defines it.
- `SATIN-PCMP-002` — ModExp (0x05) runs on the Osaka schedule (EIP-7823 and EIP-7883).
- `SATIN-PCMP-003` — P256VERIFY (0x100) costs 6,900 gas (EIP-7951).
- `SATIN-PCMP-004` — Input limits: BN254 pairing (0x08) 57,600 bytes; BLS12-381 G1 MSM (0x0C) 288,960; G2 MSM (0x0E) 278,784; pairing (0x0F) 156,672.
- `SATIN-PCMP-005` — An input over a size limit fails the call before any gas check, a call forwarded no gas included, and consumes the forward.
- `SATIN-PCMP-006` — KZG point evaluation: a call given less than 100,000 fails with an out-of-gas before any verification; a success is charged exactly 100,000; a failure with at least 100,000 consumes the whole forward.
- `SATIN-PCMP-007` — ModExp's EIP-7823 bound is checked after its 500 minimum price and before its formula price.
- `SATIN-PCMP-008` — A call to a precompile address is dispatched and priced by the called address, whatever code that address holds.

## Spec History

- [Satin](../../upgrades/satin.md) — The reviewers' delta of Satin against Rex6.
