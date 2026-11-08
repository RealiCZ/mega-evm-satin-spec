---
description: Satin (unstable) — EIP-7702 Authorizations Before the First Frame. Stub of the Satin specification: the rules this page will specify.
spec: Satin
maturity: unstable
---

# EIP-7702 Authorizations Before the First Frame

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
This page is a stub. It lists what the page will specify; the specification text is written after the outline is reviewed.
{% endhint %}

Abstract: How a transaction's authorization list is decided before its first frame: the simulation, the totals held to the KV and state-growth limits, the all-or-nothing skip, and the charges and warmth of an applied list.

## Specification

The rules this page will specify, by their proposed ids:

- `SATIN-AUTH-001` — Before the first frame the list is decided by simulating EIP-7702 application in list order; the simulation writes nothing and warms nothing.
- `SATIN-AUTH-002` — An entry whose chain id is neither zero nor the chain's, whose nonce is 2^64 − 1, or whose signature recovers no authority is skipped without reading its authority.
- `SATIN-AUTH-003` — Every other entry loads its authority's account with its code; an account holding code other than a delegation is skipped and its simulated nonce is not bumped.
- `SATIN-AUTH-004` — The effective nonce: after earlier acceptances for the same authority, the simulated nonce; for the sender with none, its nonce after validation's bump; otherwise the account's nonce; a mismatch skips, a match applies and bumps the simulated nonce.
- `SATIN-AUTH-005` — The simulation walks the whole list without stopping at a crossing; each distinct authority that passed the gates is loaded once, later entries using the simulated nonce and the loaded code.
- `SATIN-AUTH-006` — A failed read of an authority the simulation consults is a database fault: no outcome; a fatal database error is an internal error, any other makes the block invalid; never a refusal for the limit.
- `SATIN-AUTH-007` — The simulation charges no cold-access gas; the intrinsic 7,816 per entry is already charged for every entry.
- `SATIN-AUTH-008` — The list's totals: one write record per distinct authority it would change other than the sender, one growth unit per distinct authority it would create, account-creation state gas once per new authority.
- `SATIN-AUTH-009` — Delegation-indicator state gas at most once per authority: only for an accepted non-zero designator, with no indicator at the transaction's start and none set earlier in the list; a clear charges none; a zero target still bumps the nonce and can create the account; the indicator is not growth.
- `SATIN-AUTH-010` — If the KV or growth totals would exceed the transaction limit, none of the list applies and none of its state gas or history is charged, and the transaction's own frame is stopped before it runs with MegaLimitExceeded of the crossed kind and the transaction limit; both crossed names kind 1.
- `SATIN-AUTH-011` — A skipped list keeps no authority account, record, state gas or history, writes no delegation and bumps no nonce beyond the sender's; the intrinsic regular gas, the body's history and data size stay.
- `SATIN-AUTH-012` — On a skip the consulted authorities are not made warm, except one already warm from the transaction's start (sender, call recipient, beneficiary, access-list address, precompile, SequencerRegistry).
- `SATIN-AUTH-013` — The skip is all or nothing and is settled as a revert-class stop of the first frame.
- `SATIN-AUTH-014` — A list that fits is applied: EIP-7702 warms every authority the application loads; an entry skipped by its chain id, its 2^64 − 1 nonce or its signature is neither loaded nor warmed; one skipped for its code or its nonce is loaded and warmed.
- `SATIN-AUTH-015` — The authorities' state gas and record history are charged when the list is applied and reduce what the first frame is given; one that cannot be paid takes the pre-frame out-of-gas path (for a non-deposit an out-of-gas halt, not a stop); the limit is decided before those charges.
- `SATIN-AUTH-016` — When the list fits, a later stop of the first frame keeps the authorizations, their state gas, records and history.
- `SATIN-AUTH-017` — A deposit's created caller is not an authorization: it is always created and kept, and cannot alone cross the growth limit.
- `SATIN-AUTH-018` — The list rule is decided during execution where the accounts are read; it is not a pool rejection.

## Spec History

- [Satin](../../upgrades/satin.md) — The reviewers' delta of Satin against Rex6.
