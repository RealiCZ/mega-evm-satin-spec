---
description: Satin (unstable) — EIP-7708 Transfer Logs. Stub of the Satin specification: the rules this page will specify.
spec: Satin
maturity: unstable
---

# EIP-7708 Transfer Logs

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
This page is a stub. It lists what the page will specify; the specification text is written after the outline is reviewed.
{% endhint %}

Abstract: The Transfer log every movement of value to another account emits, which movements log nothing, the burns that stay silent, and what a transfer log counts.

## Specification

The rules this page will specify, by their proposed ids:

- `SATIN-LOG-001` — EIP-7708 applies: every movement of value to another account (the transaction's value, a value CALL, a creation's endowment, a SELFDESTRUCT that moves a balance) emits Transfer(address indexed from, address indexed to, uint256 value) from 0xff…fe with topic 0xddf252ad….
- `SATIN-LOG-002` — The log appears in the receipt in execution order among the contracts' own logs; a failed frame's transfer logs are discarded with its other logs.
- `SATIN-LOG-003` — A CALLCODE, a call to the caller itself and a transaction's value sent to its own sender move nothing to another account and emit no log.
- `SATIN-LOG-004` — A deposit's value is logged; its mint is not.
- `SATIN-LOG-005` — Only EIP-7708's Transfer log applies: EIP-8246 is not applied, a balance can still be burned, and a burn never logs (a same-transaction account's SELFDESTRUCT to itself; an account destroyed in the transaction removed at its end).
- `SATIN-LOG-006` — A transfer log is data size, TRANSFER_LOG_SIZE = 160, counted where the value moves (with the frame start that moves it, or with the SELFDESTRUCT); it is not a write record, pays no history gas and draws no history allowance.
- `SATIN-LOG-007` — A frame start the caller's account refuses moves and logs nothing; a creation with an endowment onto an occupied address moves and logs nothing and counts nothing.

## Spec History

- [Satin](../../upgrades/satin.md) — The reviewers' delta of Satin against Rex6.
