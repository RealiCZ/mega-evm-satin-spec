---
description: Satin (unstable) — SequencerRegistry. Stub of the Satin specification: the rules this page will specify.
spec: Satin
maturity: unstable
---

# SequencerRegistry

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
This page is a stub. It lists what the page will specify; the specification text is written after the outline is reviewed.
{% endhint %}

Abstract: The SequencerRegistry under Satin: the Rex-era contract, read by every transaction for the live system address, its role changes applied by the pre-block step.

## Specification

The rules this page will specify, by their proposed ids:

- `SATIN-REG-001` — Address 0x6342…0006, version 2.0.0 bytecode, storage layout, interface, read methods, change scheduling, two-step admin transfer, no interception: Rex6's.
- `SATIN-REG-002` — Every transaction reads the registry when validated: its account and, from the transaction's own state, its _currentSystemAddress slot; with the version 2.0.0 code hash and a non-zero slot the slot names the live system address; the code is compared by hash, never loaded or run.
- `SATIN-REG-003` — The account and the slot are warm for the rest of the transaction; the read is not charged, writes nothing, and lands in the transaction's returned state.
- `SATIN-REG-004` — An absent registry, other code, or a zero slot names no live system address.
- `SATIN-REG-005` — A role change is scheduled for a later block only and applied by that block's pre-block call; an applyPendingChanges() inside a block finds nothing due.
- `SATIN-REG-006` — The registry's roles are what it holds, seeded by the legacy forks; Satin reads none of their configuration keys.
- `SATIN-REG-007` — A registry read the node fails to make gives the transaction no outcome.

## Spec History

- [Satin](../../upgrades/satin.md) — The reviewers' delta of Satin against Rex6.
