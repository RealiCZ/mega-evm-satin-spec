---
description: Satin (unstable) — System Calls and the Pre-Block Sequence. Stub of the Satin specification: the rules this page will specify.
spec: Satin
maturity: unstable
---

# System Calls and the Pre-Block Sequence

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
This page is a stub. It lists what the page will specify; the specification text is written after the outline is reviewed.
{% endhint %}

Abstract: The gas a system call runs on, the calls a block makes before its transactions and their order, the Oracle rule inside a system call, and how a failed pre-block call ends the block.

## Specification

The rules this page will specify, by their proposed ids:

- `SATIN-PBLK-001` — A system call runs on at most SYSTEM_CALL_REGULAR_GAS_LIMIT = 30,000,000 of regular gas, the rest of its gas limit being its reservoir; GAS inside reads at most 30,000,000; a transaction, a Mega System Transaction included, is not a system call.
- `SATIN-PBLK-002` — Each pre-block call runs from 0xff…fe on PRE_BLOCK_CALL_GAS_LIMIT = 31,566,720 (30,000,000 regular and a reservoir of sixteen fresh slots at m = 1), whatever the block's gas limit; state gas the reservoir cannot pay spills.
- `SATIN-PBLK-003` — Before its transactions a block, in order: makes the EIP-2935 call; makes the EIP-4788 call (a block without a parent beacon block root is invalid); in Satin's activation block only, checks the predeploys; reads whether the SequencerRegistry has a role change due and if so calls applyPendingChanges(); reads the L1 block contract's account and five fee slots.
- `SATIN-PBLK-004` — Whether a role change is due, read from the registry's pending slots.
- `SATIN-PBLK-005` — A system call never asks the oracle service: an SLOAD in the Oracle's frame reads the chain's value, priced as an Oracle read, and records no answer; the rule ends with the call.
- `SATIN-PBLK-006` — A pre-block call that does not succeed makes the block invalid before its state is used; a database error the database declares fatal is an internal error; a database error in the activation check, the due-change read or the L1 info read is always an internal error.

## Spec History

- [Satin](../../upgrades/satin.md) — The reviewers' delta of Satin against Rex6.
