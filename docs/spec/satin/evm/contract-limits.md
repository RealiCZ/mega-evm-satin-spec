---
description: Satin (unstable) — Contract Size Limits. Stub of the Satin specification: the rules this page will specify.
spec: Satin
maturity: unstable
---

# Contract Size Limits

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
This page is a stub. It lists what the page will specify; the specification text is written after the outline is reviewed.
{% endhint %}

Abstract: The deployed-code and initcode size limits, how crossing them ends a creation, and the order in which the creation opcodes make their checks and charges.

## Specification

The rules this page will specify, by their proposed ids:

- `SATIN-SIZE-001` — Deployed code is at most MAX_CONTRACT_SIZE = 524,288 bytes.
- `SATIN-SIZE-002` — Initcode is at most MAX_INITCODE_SIZE = 1,048,576 bytes, twice the code limit.
- `SATIN-SIZE-003` — Initcode over the limit halts the creating frame at the creation opcode, deployed code over the limit halts the creation, each consuming the halting frame's gas; neither is a limit stop.
- `SATIN-SIZE-004` — A non-deposit creation transaction whose initcode is over the limit is rejected at validation.
- `SATIN-SIZE-005` — The creation opcodes' check and charge order: the static context; the value, offset and size operands and the size's range; the initcode size; EIP-3860's initcode cost; the offset's range and the memory (neither for empty initcode); for CREATE2 the salt, then 12,000 and the hashing cost; for CREATE 12,000; Satin adds no charge ahead of these.
- `SATIN-SIZE-006` — So a creation in a static frame fails before reading operands, and a CREATE2 short of its salt pays the initcode cost and the memory first, which under detention can be the crossing.

## Spec History

- [Satin](../../upgrades/satin.md) — The reviewers' delta of Satin against Rex6.
