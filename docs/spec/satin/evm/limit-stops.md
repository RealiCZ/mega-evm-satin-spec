---
description: Satin (unstable) — Limit Stops. The revert-class stop every resource limit and gas detention's compute limit makes on the frame that crosses it — what the stop reverts and keeps, how a caller resumes, how a stopped transaction settles, how a frame start is stopped before it runs, and the MegaLimitExceeded revert data.
spec: Satin
maturity: unstable
---

# Limit Stops

{% hint style="warning" %}
**Unstable** — Satin is under active development: every value and rule on this page may change before Satin is frozen.
{% endhint %}

Abstract: A _limit stop_ is the revert a frame makes when it crosses a resource limit or gas detention's compute limit: the frame reverts with `MegaLimitExceeded(uint8 kind, uint64 limit)`, its caller resumes as after any failed call and may carry on, and a stop of the transaction's own frame settles the transaction like a revert.

## Motivation

A limit that halts the transaction makes every contract hostage to its deepest callee: one callee that writes too much, or reads volatile data and computes too long, takes the whole transaction down, consuming its caller's gas and every frame's work, and the caller has no way to protect itself.
A halt also burns the gas the transaction had left, so a sender pays for gas no instruction used because a limit, not an error of its own code, ended it.

The stop must also be enforced before the state it guards is used: a frame whose start already crosses a limit must not run, and a value it moved or an account it created must not survive the stop.
And a node, a builder or an RPC must be able to tell a stop from a contract that reverts with the same bytes.

## Specification

### The stop

- `SATIN-STOP-001` Every limit — the transaction's data-size, KV-update and state-growth limits ([Resource Limits](resource-limits.md)), a frame's budget in those dimensions, and gas detention's compute limit ([Gas Detention](gas-detention.md)) — MUST stop the frame that crosses it with a revert, and MUST NOT halt.
- `SATIN-STOP-002` A limit stop MUST exist in exactly four dimensions: data size (kind 0), KV updates (kind 1), compute under gas detention (kind 2) and state growth (kind 3).
  Nothing else is a limit stop; the endings that are not are listed on [Halts, Reverts and Stops](outcomes.md).
- `SATIN-STOP-003` The stop MUST apply only to a transaction that passes validation and pays every charge made before its first frame.
  A transaction that fails validation, or cannot pay a charge made before its first frame ([Gas Schedule and Intrinsic Gas](gas-schedule.md)), MUST report no stop: a non-deposit is rejected or runs out of gas, and a deposit becomes a failed deposit ([Deposit Transactions](../block/deposits.md)), whose body stays counted as data size.

For a transaction the stop applies to:

- `SATIN-STOP-004` The frame that crosses a limit MUST revert with `MegaLimitExceeded(uint8 kind, uint64 limit)` as its output, ABI-encoded as a Solidity custom error.
  The write or the charge that crossed MUST NOT be kept or made, and every write and log the frame made MUST be reverted, as a `REVERT` reverts them.
- `SATIN-STOP-005` Its caller MUST resume as after any revert: the call fails, its return data is the stop's revert data, and the gas the frame had MUST return to the caller — for gas detention's limit, the gas it had before the charge that crossed — its reservoir included ([Two-Pool Gas](gas-model.md)).
- `SATIN-STOP-006` What the frame counted MUST be discarded with it, so the caller resumes within every limit, with one exception.
  A failed frame's discard puts back what the frames above it kept when it started, a record of theirs it took back included, while an Oracle hint it admitted stays counted (`SATIN-STOP-012`); a hint sent into room such a take-back freed leaves the transaction over its data-size limit once the frame fails.
  The frame it returns into MUST then return the stop of the transaction's data-size limit before it runs another instruction, whether the frame below reverted, halted or was itself stopped.
- `SATIN-STOP-007` Otherwise a caller that carries on MUST be held to what the transaction has left, and a write or a charge of its own that crosses a limit again MUST stop the caller's frame in turn.
- `SATIN-STOP-008` A caller that catches the stop MUST run on as after any failed call, unless `SATIN-STOP-006` stops it as it resumes; a transaction whose frames catch every stop below its own frame MAY succeed, keeping what its frames did and nothing of a frame that was stopped.

A transaction therefore never keeps more data size, KV updates or state growth than its limits, and never computes past gas detention's limit but by what [Gas Detention](gas-detention.md) allows.

### A stop of the transaction's own frame

- `SATIN-STOP-009` A stop of the transaction's own frame is the transaction's result, and the transaction MUST settle like an EIP-8037 revert: every write and log its frames made MUST be reverted, the value its first frame carried and that frame's write record included; the sender pays the intrinsic gas, the body's history gas, the charges of what it keeps from before the first frame (`SATIN-STOP-011`), and what ran; the unspent regular gas and the reservoir return to the sender (`SATIN-POOL-017`).
  The transaction MUST be included with a failed receipt, and its usage counts toward the block's counters ([Block Limits and Packing](../block/block-limits.md)).
- `SATIN-STOP-010` A deposit whose own frame is stopped MUST settle as `SATIN-STOP-009` states, as a revert: it is not a failed deposit, which only a deposit that fails validation, cannot pay a charge made before its first frame, or whose own frame halts becomes ([Deposit Transactions](../block/deposits.md)).
- `SATIN-STOP-011` A stop of the transaction's own frame MUST NOT revert what was applied before the first frame, as a revert of the first frame does not:
  - the sender's nonce and the fees it pays; for a deposit, its mint and the caller account it created, with that account's state gas;
  - the EIP-7702 authorizations admitted before the first frame ([EIP-7702 Authorizations Before the First Frame](authorizations.md)): their authorities' nonce and delegation writes, their state gas, their write records, and the history gas those records cost.
    A list the list rule skipped was not admitted, and the stop keeps nothing of it.
- `SATIN-STOP-012` An Oracle hint a frame admitted is not the frames' state: it MUST stay counted as data size through any stop, whether its payload reached the oracle service or failed to decode.
  A hint that would itself cross the data-size limit MUST be neither forwarded nor counted, and its call is answered with the stop ([Oracle](../system-contracts/oracle.md)).

### Enforcement before a frame runs

- `SATIN-STOP-013` A frame whose start crosses a limit (`SATIN-LIM-013`) MUST be stopped before it runs an instruction, and what its start moved MUST be reverted with it: the value, the transfer log, a created account.
- `SATIN-STOP-014` A frame answered with a success without running — a call to an account with no code, a precompile that answers — whose start crosses MUST have its answer replaced by the stop, on the gas its caller forwarded, untouched.
  A frame answered with a failure kept nothing, and its answer MUST NOT be replaced by a stop: a precompile that fails consumes the gas forwarded to it, as without a limit.
  A precompile whose price crosses gas detention moves nothing, and MUST be held to the price alone: its result is the compute stop, whatever records its value transfer would have made (`SATIN-DET-022`).
- `SATIN-STOP-015` A stopped creation MUST keep its creator's nonce bump, and that write's record MUST be counted on the creator when the creation returns: the creator MUST be held to its limits with it before it runs on, and be stopped if it crosses one (`SATIN-LIM-008`).
- `SATIN-STOP-016` A frame answered without running whose answer is then rewritten to the stop — by gas detention ([Gas Detention](gas-detention.md)) — MUST have what its start moved reverted with it, as a frame that fails has.
- `SATIN-STOP-017` A node MUST NOT stop a transaction for data size counted before its first frame: validation rejects a transaction whose body, with a write record for each authorization entry, would cross the data-size limit ([Transaction Validation and Refusals](../block/transaction-validation.md)), so nothing counted before the first frame crosses it.
  KV updates and state growth can cross before the first frame only on the authorization list, which is then skipped ([EIP-7702 Authorizations Before the First Frame](authorizations.md)).

### The revert data

- `SATIN-STOP-018` The stop's `kind` and `limit` MUST be:

  | `kind` | Dimension               | `limit`                                                                                            |
  | ------ | ----------------------- | -------------------------------------------------------------------------------------------------- |
  | 0      | Data size               | The frame budget crossed, or the transaction limit when no frame budget was crossed, in bytes     |
  | 1      | KV updates              | The frame budget crossed, or the transaction limit when no frame budget was crossed, in write records |
  | 2      | Compute (gas detention) | The compute limit of the binding read: the transaction's compute at that read plus the cap, in gas |
  | 3      | State growth            | The frame budget crossed, or the transaction limit when no frame budget was crossed, in new accounts and new slots |

  Kinds 0, 1 and 3 MUST name the frame budget when that budget is crossed, also when the transaction limit of the same dimension is crossed too, and the transaction limit otherwise, whether or not a frame budget applies to the operation (`SATIN-LIM-011`).
- `SATIN-STOP-019` A stop MUST carry the kind discriminant `SATIN-STOP-018` gives its dimension, and a node MUST NOT produce any other kind value.
- `SATIN-STOP-020` Only a limit stop MUST carry `MegaLimitExceeded`, and every limit stop MUST carry it.
  A refusal that is not a limit stop MUST NOT carry it: a refused volatile read reverts with `VolatileDataAccessDisabled(uint8)` ([MegaAccessControl](../system-contracts/mega-access-control.md)), the system contracts' and a keyless deployment's refusals carry their own errors ([KeylessDeploy](../system-contracts/keyless-deploy.md)), a call past the call-depth limit or with a value its caller cannot fund fails with empty return data, and a halt has no return data.
- `SATIN-STOP-021` The revert data alone MUST NOT be taken to identify a stop: a contract can revert with the same bytes, and so can a caller that re-raises the stop a frame below returned.
  The stop of a transaction is the crossing that produced the result of its own frame, and execution MUST report it: the transaction's data-size, KV or state-growth limit, gas detention's compute limit, or that frame's own budget in data size, KV or state growth; it MUST report none when that result is not the stop's revert, a stop a caller caught included.

### Retired ids

None.

## Constants

| Constant                   | Value                                         | Description                                                  |
| -------------------------- | --------------------------------------------- | ------------------------------------------------------------ |
| `MegaLimitExceeded`        | `error MegaLimitExceeded(uint8 kind, uint64 limit)` | The revert data of every limit stop                     |
| `KIND_DATA_SIZE`           | 0                                             | Kind of a data-size stop                                     |
| `KIND_KV_UPDATES`          | 1                                             | Kind of a KV-update stop                                     |
| `KIND_COMPUTE`             | 2                                             | Kind of a gas-detention stop                                 |
| `KIND_STATE_GROWTH`        | 3                                             | Kind of a state-growth stop                                  |

## Rationale

**Why a revert, never a halt?**
A revert ends only the frame that crossed, returns its unspent gas, and lets its caller decide what to do; a halt ends the transaction and consumes its gas.
Rex6 reverted a frame that crossed its budget but halted a transaction that crossed through usage outside every frame's budget; Satin has no such usage at runtime (the body is refused at validation, the authorization list is skipped, a hint that would cross is not admitted), so every crossing can be a revert of the frame that made it.

**Why does a stop of the first frame settle like a revert?**
The sender did nothing wrong by reaching a limit, and the gas the transaction had left paid for nothing; settling as an EIP-8037 revert charges for what ran and returns the rest, as a contract's own revert does.

**Why are pre-frame writes kept?**
They are not the frames' doing: the nonce and fees are validation's, a deposit's mint is L1's, and an applied authorization list was admitted against the limits before any frame ran.
A revert of the first frame does not revert them, so neither does a stop.

**Why the discriminants Rex6 used?**
A decoder of Rex6's revert data decodes Satin's without change; Satin's kind 2 is the compute stop of gas detention, the dimension Rex6 used kind 2 for.

**Why must a stop be reported rather than read from the output?**
The bytes of `MegaLimitExceeded` are an ordinary custom error any contract can return, and a caller that catches a stop can re-raise it; only the execution knows whether the transaction's own frame ended on a crossing.
An RPC that maps a stop to an error, or a builder that handles a stopped transaction, must use that report.

## Security Considerations

- If a limit halted instead of stopping, a callee could consume its caller's whole gas by crossing a limit on purpose, and a contract could not isolate untrusted calls.
- If the crossing write were kept, a transaction could exceed its limits by exactly one write per frame, and the block's counters would exceed the limits the protocol sets.
- If a frame whose start crosses were allowed to run an instruction, the value it moved or the account it created would be used before the stop reverts it.
- If a node inferred a stop from the output bytes, a contract could make a successful transaction look stopped, or a caught stop look like the transaction's result.
- If the hint exception of `SATIN-STOP-006` were not applied, a frame could free room by failing, have a callee fill it with hints, and leave the transaction over its data-size limit with no frame stopped.
- This page preserves the invariant that no limit ever halts a transaction, and that a transaction keeps at most its limits in every dimension at every instruction.

## Spec History

- [Satin](../../upgrades/satin.md) — Made every crossing a revert of the crossing frame that its caller can catch, where Rex6's [Resource Limits](../../evm/resource-limits.md) and [Compute Gas](../../evm/compute-gas.md) halted a transaction on usage outside every frame's budget and on the detained compute limit; kept the `MegaLimitExceeded(uint8, uint64)` encoding and its kind values.
