---
description: Satin (unstable) — Gas Forwarding. Stub of the Satin specification: the rules this page will specify.
spec: Satin
maturity: unstable
---

# Gas Forwarding

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
This page is a stub. It lists what the page will specify; the specification text is written after the outline is reviewed.
{% endhint %}

Abstract: How much regular gas a call or creation forwards (98/100 of the caller's remaining gas in place of 63/64), the value-transfer stipend, and how the forward differs from the reservoir share and the frame budget.

## Specification

The rules this page will specify, by their proposed ids:

- `SATIN-FWD-001` — CALL, CALLCODE, DELEGATECALL, STATICCALL, CREATE and CREATE2 cap the regular gas they forward at parent_remaining_gas − parent_remaining_gas × 2 / 100 (integer division), in place of EIP-150's 63/64.
- `SATIN-FWD-002` — parent_remaining_gas is the caller's regular gas after the opcode's charges before the forward, the 11,300 value transfer (which contains the 2,300 stipend) included.
- `SATIN-FWD-003` — The child's regular gas is min(requested_gas, forwarded_gas_cap), plus the 2,300 stipend for a value-transferring CALL or CALLCODE only; the stipend is outside the cap and not taken from the caller.
- `SATIN-FWD-004` — CREATE and CREATE2 forward forwarded_gas_cap and add no stipend.
- `SATIN-FWD-005` — The reservoir is not part of the cap; a call that forwards no regular gas still forwards the reservoir share.
- `SATIN-FWD-006` — The reservoir-share subtraction and the frame-budget multiplication are different integers (98 of 99 and the whole value below 50, against 97 of 99 and 0 of 1).
- `SATIN-FWD-007` — A system-originated transaction and a system call are not exempt from the reservoir split.

## Spec History

- [Satin](../../upgrades/satin.md) — The reviewers' delta of Satin against Rex6.
