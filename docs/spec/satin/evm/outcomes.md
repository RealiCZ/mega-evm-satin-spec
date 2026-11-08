---
description: Satin (unstable) — Halts, Reverts and Stops. Stub of the Satin specification: the rules this page will specify.
spec: Satin
maturity: unstable
---

# Halts, Reverts and Stops

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
This page is a stub. It lists what the page will specify; the specification text is written after the outline is reviewed.
{% endhint %}

Abstract: The one rule that decides how a frame and a transaction end under Satin: which crossings revert and can be caught, which endings halt, which transactions are rejected or become failed deposits, and which faults give a transaction no outcome at all.

## Specification

The rules this page will specify, by their proposed ids:

- `SATIN-OUT-001` — The outcome classes of a transaction: rejected before inclusion; included as a failed deposit; executed to a success, a revert, a halt or a limit stop of its own frame; or no outcome when the node meets a fault.
- `SATIN-OUT-002` — The revert-or-halt rule: every resource limit and gas detention's compute limit reverts only the frame that crosses it, and its caller can catch the stop; no limit halts a transaction.
- `SATIN-OUT-003` — Exception: initcode over MAX_INITCODE_SIZE (a creation transaction rejected, a creation opcode halting the creating frame, a keyless deployment refused with InitCodeTooLarge) and deployed code over MAX_CONTRACT_SIZE (the creation halts).
- `SATIN-OUT-004` — Exception: an OP precompile input over its size limit halts the call before any gas check, consuming its forward.
- `SATIN-OUT-005` — Exception: a failed deposit uses its whole gas limit and reports no stop.
- `SATIN-OUT-006` — Exception: a pre-frame charge the transaction cannot pay runs out of gas without running a frame (a non-deposit is included out of gas; a deposit becomes a failed deposit).
- `SATIN-OUT-007` — A real out-of-gas, a precompile given less than its price, an invalid opcode, and every other exceptional halt of the base layer still halt and consume the frame's gas; a regular charge beyond the frame's whole gas halts even under detention; a creation that cannot pay a code-deposit charge runs out of gas and leaves no code.
- `SATIN-OUT-008` — A refused volatile read reverts the frame with VolatileDataAccessDisabled(uint8); it is not a limit stop.
- `SATIN-OUT-009` — A system contract's own refusal (for example NonZeroTransfer() or NotIntercepted()) reverts with its own error and is not a limit stop; a keyless deployment's rule refusal reverts the call (its state and history gas given back, its regular gas spent); an out-of-gas step halts the call.
- `SATIN-OUT-010` — A call past the call-depth limit, or with a value its caller cannot fund, fails with empty return data and counts nothing.
- `SATIN-OUT-011` — A precompile that fails consumes all the gas forwarded to it.
- `SATIN-OUT-012` — A creation opcode in a static frame, or short of its operands, halts; under detention the initcode cost and memory a CREATE2 charges before its salt can be the crossing (a revert) where the underflow would halt.
- `SATIN-OUT-013` — A halt of the transaction's own frame: failed receipt, the unspent regular gas consumed, the reservoir returned; for a deposit a failed deposit.
- `SATIN-OUT-014` — A revert or a limit stop of the transaction's own frame: failed receipt, the unspent regular gas and the reservoir returned.
- `SATIN-OUT-015` — A failed bucket-capacity read or database read is never an outcome: the transaction is not settled and the node reports an internal error or an invalid block by the error's cause.
- `SATIN-OUT-016` — A transaction that fails validation: a non-deposit is rejected; a deposit (a system deposit refused under Regolith and one whose body is over the data-size limit included) is a failed deposit; a Mega System Transaction is a legacy transaction until it passes its own checks.
- `SATIN-OUT-017` — What a tracer is shown for a first frame whose runtime gas phase cannot be paid (one halted root frame, or none).
- `SATIN-OUT-018` — The halt reason named for a failed DUP, DUPN, SWAPN or EXCHANGE.

## Spec History

- [Satin](../../upgrades/satin.md) — The reviewers' delta of Satin against Rex6.
