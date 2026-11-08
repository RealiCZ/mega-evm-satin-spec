---
description: Satin (unstable) — Halts, Reverts and Stops. The one rule that decides how a frame and a transaction end — which crossings revert and can be caught, which endings halt, which transactions are rejected or become failed deposits, and which faults give a transaction no outcome — with each exception linked to the page that holds its detail.
spec: Satin
maturity: unstable
---

# Halts, Reverts and Stops

{% hint style="warning" %}
**Unstable** — Satin is under active development: every value and rule on this page may change before Satin is frozen.
{% endhint %}

Abstract: Every resource limit and gas detention's compute limit reverts only the frame that crosses it, and its caller can catch the stop; this page states that rule and every ending that is not such a stop, and links each to the page that specifies it.
It gathers rules whose detail lives elsewhere and restates none of that detail.

## Motivation

A transaction can end in many ways — rejected before inclusion, included as a failed deposit, run to a success, a revert, a halt or a limit stop — and a frame can revert, halt or be stopped.
The rules that decide which happens are spread over the pages that own each mechanism, and a single exception misplaced (a limit that halts, a size check that reverts, a database error settled as a failure) changes receipts, gas used and state.
An implementer needs one place that names every class of ending and every exception to the revert rule, so that no site is classified by guesswork.

## Specification

### The outcome classes

- `SATIN-OUT-001` Every transaction a node is given MUST end in exactly one of these classes:
  - **rejected** before inclusion, when it fails validation and is not a deposit ([Transaction Validation and Refusals](../block/transaction-validation.md));
  - **included as a failed deposit** ([Deposit Transactions](../block/deposits.md));
  - **executed** to a success, a revert, a halt, or a limit stop of its own frame;
  - **no outcome**, when the node meets a fault (`SATIN-OUT-015`).

### The revert-or-halt rule

- `SATIN-OUT-002` Every resource limit and gas detention's compute limit MUST revert only the frame that crosses it, and its caller MAY catch the stop; no limit halts a frame or a transaction.
  What the stop reverts, keeps and reports is [Limit Stops](limit-stops.md); which limits exist is [Resource Limits](resource-limits.md) and [Gas Detention](gas-detention.md).

### The exceptions

These endings enforce a size, a payment or a protocol rule, and none of them is a limit stop:

- `SATIN-OUT-003` Initcode over `MAX_INITCODE_SIZE` and deployed code over `MAX_CONTRACT_SIZE` MUST end as [Contract Size Limits](contract-limits.md) specifies — a creation transaction rejected, a creation opcode halting its frame, a creation halting — and a keyless deployment's initcode over the limit is refused by its own rule ([KeylessDeploy](../system-contracts/keyless-deploy.md)).
- `SATIN-OUT-004` An input over an OP precompile's size limit MUST fail the call as [Precompiles](precompiles.md) specifies (`SATIN-PCMP-005`): a halt of the call, not a stop.
- `SATIN-OUT-005` A failed deposit MUST use its whole gas limit and report no stop ([Deposit Transactions](../block/deposits.md)).
- `SATIN-OUT-006` A charge made before the first frame that the transaction cannot pay MUST end the transaction out of gas without running a frame, as `SATIN-SCHED-009` and `SATIN-SCHED-010` specify ([Gas Schedule and Intrinsic Gas](gas-schedule.md)): a non-deposit is included out of gas, and a deposit becomes a failed deposit.
- `SATIN-OUT-007` A real out-of-gas, a precompile given less than its price, an invalid opcode, and every other exceptional halt of the base layer ([Base Layer](../base-layer.md)) MUST halt and consume the halting frame's regular gas (`SATIN-POOL-014`).
  Under gas detention a regular charge beyond the frame's whole regular gas halts as without the read (`SATIN-DET-020`), and a creation that cannot pay a code-deposit charge runs out of gas and leaves no code (`SATIN-SCHED-011`).
- `SATIN-OUT-008` A refused volatile read MUST revert its frame with `VolatileDataAccessDisabled(uint8)`, as [MegaAccessControl](../system-contracts/mega-access-control.md) specifies; it is a revert, and not a limit stop.
- `SATIN-OUT-009` A system contract's own refusal (for example `NonZeroTransfer()` or `NotIntercepted()`) MUST revert with its own error and is not a limit stop ([Call Interception](../system-contracts/interception.md)); a keyless deployment's rule refusal reverts the call and an out-of-gas step halts it, as [KeylessDeploy](../system-contracts/keyless-deploy.md) specifies.
- `SATIN-OUT-010` A call past the call-depth limit, or with a value its caller cannot fund, MUST fail with empty return data and count nothing (`SATIN-LIM-015`); it is neither a halt of the caller nor a stop.
- `SATIN-OUT-011` A precompile that fails MUST consume all the gas forwarded to it ([Precompiles](precompiles.md)), and a start answered with that failure is not replaced by a stop (`SATIN-LIM-014`).
- `SATIN-OUT-012` A creation opcode in a static frame, or short of its operands, MUST halt its frame; under gas detention the charges a `CREATE2` makes before it reads its salt can be the crossing, which stops the frame where the stack underflow would have halted it (`SATIN-SIZE-006`).

### How the transaction's own frame ends

- `SATIN-OUT-013` A halt of the transaction's own frame ends the transaction as `SATIN-POOL-017` settles it, with a failed receipt; for a deposit it is a failed deposit (`SATIN-DEP-004`, [Deposit Transactions](../block/deposits.md)).
- `SATIN-OUT-014` A revert of the transaction's own frame ends the transaction with a failed receipt, as `SATIN-POOL-017` settles it, and a limit stop of that frame as `SATIN-STOP-009` settles it; for a deposit either is a revert, not a failed deposit (`SATIN-STOP-010`).
- `SATIN-OUT-016` A transaction that fails validation MUST report no stop (`SATIN-STOP-003`): a non-deposit is rejected; a deposit, a system deposit refused under Regolith and a deposit whose body is over the data-size limit included, is included as a failed deposit; and a Mega System Transaction is a legacy transaction until it passes its own checks, so failing one of them is a rejection ([Mega System Transactions and the Protocol's Own Transactions](../system-contracts/system-tx.md)).

### Faults

- `SATIN-OUT-015` A failed bucket-capacity read (`SATIN-STATE-007`) or a failed database read MUST NOT be an outcome of the transaction, for a deposit as for any transaction: the transaction MUST NOT be settled, as a failed deposit or otherwise, and the node MUST report an internal error or an invalid block by the error's cause, as `SATIN-VAL-010` ([Transaction Validation and Refusals](../block/transaction-validation.md)) classifies it.

### Outside the specification

- `SATIN-OUT-017` What a tracer or inspector is shown of an execution is outside this specification, and a node MAY show it any frames — for a transaction whose first frame cannot pay a charge made before it runs, one halted root frame or none; two nodes that agree on every outcome, gas figure, state change, log and read set conform whatever they show a tracer.
- `SATIN-OUT-018` This specification names no halt reason: a halt is identified only as a halt, and a node MAY label a halt with any reason, which is part of no receipt, state or witness.
  In particular the label of a failed `DUP`, `DUPN`, `SWAPN` or `EXCHANGE` (a stack underflow, a stack overflow or an invalid immediate) is not specified.

### Retired ids

None.

## Constants

| Constant            | Value     | Description                                                              |
| ------------------- | --------- | ------------------------------------------------------------------------ |
| `MAX_INITCODE_SIZE` | 1,048,576 | The most bytes an initcode may hold ([Contract Size Limits](contract-limits.md)) |
| `MAX_CONTRACT_SIZE` | 524,288   | The most bytes deployed code may hold ([Contract Size Limits](contract-limits.md)) |

## Rationale

**Why one page for every ending?**
The revert-or-halt rule is the property reviewers hold every site of an implementation to, and its exceptions are where implementations diverge.
Listing each exception once, with the page that owns it, lets a reviewer check a site against the classification without restating, and possibly contradicting, the detail.

**Why are size checks and precompile limits halts, not stops?**
They are Ethereum's and Optimism's own checks, at MegaETH's sizes; making them stops would change the inherited behaviour of a creation or a precompile call and the gas they consume, which tools built for the base layer expect.

**Why is a database fault no outcome?**
A failed read is a defect of the node or of its witness, not something the transaction did; settling the transaction would make the block depend on which node failed.

**Why no halt reasons?**
A halt's label is reported to tracers and RPC clients but is in no receipt and changes no state; the two implementations label some stack errors differently with equal gas, output and state.
Naming one label would make an implementation non-conforming for a difference no validator can see.

**Why is tracing outside the specification?**
An inspector observes execution; what it is shown does not change what the chain computes, and fixing it would constrain implementations for no consensus effect.

## Security Considerations

- If a limit halted a frame, a callee could consume its caller's gas by crossing it deliberately, which the revert rule exists to prevent.
- If a size or precompile-input check were made a stop, a creation or a precompile call would return gas the base layer consumes, and gas used would differ from every node that keeps the inherited halt.
- If a node settled a transaction on a database or bucket fault, its block would differ from a healthy node's, and a stateless validator with an incomplete witness would accept a wrong block instead of failing.
- This page preserves the invariant that every transaction ends in exactly one class, and that the only endings that consume a frame's gas are halts.

## Spec History

- [Satin](../../upgrades/satin.md) — Replaced the halts of Rex6's [Resource Limits](../../evm/resource-limits.md), [Compute Gas](../../evm/compute-gas.md) and [Gas Detention](../../evm/gas-detention.md) with the revert-class stop, so no limit halts a transaction.
