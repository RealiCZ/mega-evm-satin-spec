---
description: Satin (unstable) — Limit Stops. Stub of the Satin specification: the rules this page will specify.
spec: Satin
maturity: unstable
---

# Limit Stops

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
This page is a stub. It lists what the page will specify; the specification text is written after the outline is reviewed.
{% endhint %}

Abstract: The revert-class stop: every resource limit and gas detention's compute limit stops the frame that crosses it with a revert its caller can catch; what the stop reverts and keeps, how a stopped transaction settles, and the revert data.

## Specification

The rules this page will specify, by their proposed ids:

- `SATIN-STOP-001` — Every limit (the transaction's data-size, KV and growth limits, a frame's budget in those, gas detention's compute limit) stops the frame that crosses it with a revert, never a halt.
- `SATIN-STOP-002` — A limit stop exists in exactly four dimensions: data size (0), KV updates (1), compute under detention (2), state growth (3); nothing else is a limit stop.
- `SATIN-STOP-003` — The stop applies only to a transaction that passes validation and pays every pre-frame charge; any other reports no stop (a rejection, or a failed deposit whose body stays counted).
- `SATIN-STOP-004` — The crossing frame reverts with MegaLimitExceeded(uint8 kind, uint64 limit) as its output; the crossing write or charge is not made; every write and log of the frame is reverted as a REVERT reverts them.
- `SATIN-STOP-005` — The caller resumes as after any revert: the call fails, its return data is the stop's revert data, and the gas the frame had (before the crossing charge, for detention) returns to it, reservoir included.
- `SATIN-STOP-006` — What the frame counted is discarded with it, but for one case: when a hint the frame admitted filled room a take-back freed, the frame it returns into returns the transaction's data-size stop before running another instruction.
- `SATIN-STOP-007` — A caller that carries on is held to what the transaction has left, and a crossing of its own stops it in turn.
- `SATIN-STOP-008` — A caller that catches the stop runs on; a transaction whose frames catch every stop below its own frame can succeed.
- `SATIN-STOP-009` — A stop of the transaction's own frame is the transaction's result and settles like an EIP-8037 revert (writes and logs reverted, the first frame's value and record included; the sender pays the intrinsic gas, the body's history, the kept pre-frame charges and what ran; the unspent regular gas and the reservoir return); failed receipt; counts toward the block's counters.
- `SATIN-STOP-010` — A deposit whose own frame is stopped settles as a revert, not as a failed deposit.
- `SATIN-STOP-011` — A stop of the transaction's own frame does not revert what was applied before the first frame: the sender's nonce and fees; a deposit's mint and created caller with its state gas; the admitted authorizations with their writes, state gas, records and history.
- `SATIN-STOP-012` — An Oracle hint a frame admitted stays counted as data size through any stop; a hint that would itself cross is neither forwarded nor counted.
- `SATIN-STOP-013` — A frame whose start crosses a limit is stopped before it runs an instruction, with what its start moved reverted (the value, the transfer log, a created account).
- `SATIN-STOP-014` — A frame answered with a success without running (an account with no code, a precompile that answers) has its answer replaced by the stop on the untouched forward; one answered with a failure is not replaced; a precompile whose price crosses gas detention moves nothing and is held to the price alone, its result the compute stop.
- `SATIN-STOP-015` — A stopped creation keeps its creator's nonce bump, whose record is counted on the creator when the creation returns, the creator held to its limits before it runs on.
- `SATIN-STOP-016` — A frame answered without running whose answer is rewritten to the stop has what its start moved reverted.
- `SATIN-STOP-017` — Nothing counted before the first frame crosses the data-size limit; KV and growth can cross there only on the authorization list, which is then skipped.
- `SATIN-STOP-018` — The revert data: kind 0, 1 and 3 carry the crossed frame budget, or the transaction limit when no budget was crossed; kind 2 carries the compute limit of the binding read.
- `SATIN-STOP-019` — The kind discriminants are Rex6's.
- `SATIN-STOP-020` — Only a limit stop carries MegaLimitExceeded; other refusals carry their own errors (VolatileDataAccessDisabled, the system contracts' and keyless deployment's errors), a call past the depth limit or with an unfundable value fails with empty return data, and a halt has none.
- `SATIN-STOP-021` — The revert data alone does not identify a stop: the stop of a transaction is the crossing that produced the result of its own frame, which execution reports.

## Spec History

- [Satin](../../upgrades/satin.md) — The reviewers' delta of Satin against Rex6.
