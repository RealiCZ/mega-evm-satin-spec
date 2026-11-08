---
description: Satin (unstable) — Oracle. The Oracle system contract under Satin; how an SLOAD in its own frame is answered by the oracle service, what such a read costs, and when a sendHint reaches the service and what it counts.
spec: Satin
maturity: unstable
---

# Oracle

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
{% endhint %}

Abstract: The Oracle system contract: its address, code and interface; how an `SLOAD` in the Oracle's own frame is answered by the node's oracle service; what such a read costs and loads; and when a `sendHint` call reaches the service, and what it counts as data size.

## Motivation

MegaETH serves externally sourced data — a sub-second timestamp, among others — from the Oracle's storage, filled lazily: a value is fetched from the node's oracle service when a transaction reads it, not written for every block in advance.
A read answered by a service rather than by the state is a read every node must answer, price and record identically, or the transaction's result depends on the node it runs on.
A hint is a payload a contract hands the service so that it fetches a value before the read; it leaves the node, so it cannot be taken back, and it costs the node work whether or not it decodes.
Without exact rules for when a read asks the service, what it costs, and when a hint is admitted and what it counts, two nodes compute different gas, different data size and different stops for the same transaction.

## Specification

### Address, code and interface

- `SATIN-ORCL-001` The Oracle MUST be the account at `ORACLE_CONTRACT_ADDRESS` holding the code of version 2.0.0 (`ORACLE_CODE_HASH`, see [System Contracts](overview.md)), whose interface and behaviour are the following.
  - **Storage.** The contract's storage is a flat map from a `uint256` slot to a `bytes32` value; each service that uses it is allotted a range of slots (the [High-Precision Timestamp](high-precision-timestamp.md)'s is slots 0 to 7).
  - **Reads.** `getSlot(uint256 slot) returns (bytes32 value)` returns the value at `slot`; `getSlots(uint256[] slots) returns (bytes32[] values)` returns the values at `slots`, in order. Both read by `SLOAD` in the Oracle's own frame.
  - **Restricted writes.** `setSlot(uint256 slot, bytes32 value)`, `setSlots(uint256[] slots, bytes32[] values)`, `emitLog(bytes32 topic, bytes data)` and `emitLogs(bytes32 topic, bytes[] dataVector)` write the slots or emit the logs, and then revert with `NotSystemAddress()` unless the immediate caller is the address `SequencerRegistry.currentSystemAddress()` returns (see [SequencerRegistry](sequencer-registry.md)). The body — every `SSTORE`, `LOG` and loop iteration — runs before that check and is charged as it runs; the revert takes back every write and log. `setSlots` with arrays of different lengths reverts with `InvalidLength(uint256 slotsLength, uint256 valuesLength)` before any `SSTORE` and before the check.
  - **Auxiliary.** `multiCall(bytes[] data) returns (bytes[] results)` executes each payload by `DELEGATECALL` into the Oracle and returns the results in order; at the first payload that fails it reverts with that payload's revert data when the data are not empty, and with `Error(string)` carrying `"Multicall: call failed"` when they are empty; `sendHint(bytes32 topic, bytes data)` is a no-op `view` method at the bytecode level.
- `SATIN-ORCL-011` The Oracle authorizes a write on its immediate caller alone: a write reaches its storage only from a frame whose caller is the live system address, whatever sent the transaction.
  Every transaction from that address other than a Mega System Transaction is invalid (see [Mega System Transactions](system-tx.md)), so among the transactions whose own frame calls the Oracle, only a Mega System Transaction writes it.
  Any transaction can still write it through code running at the live system address: through the [High-Precision Timestamp](high-precision-timestamp.md)'s `update` while that contract is the live system address (`SATIN-HPTS-001`), or through the code an EIP-7702 delegation of the system address runs, a deposit included; the registry accepts any non-zero address as the system address (`SATIN-REG-001`).

### Oracle reads

- `SATIN-ORCL-002` An `SLOAD` executed in the Oracle's own frame — a frame whose storage is the Oracle's: a frame running at the Oracle's address, the frames of `multiCall`'s `DELEGATECALL`s of the Oracle into itself included, and not a `DELEGATECALL` from another account into the Oracle's code, which runs on that account's storage — MUST load the slot from the state through the transaction's journal, then ask the node's oracle service for the slot, and push the service's value when the service gives one and the loaded value otherwise.
  The service's value MUST win over whatever the slot holds at the read, a value the Oracle's own frame wrote earlier in the transaction included; with no value from the service the read MUST push the slot's present value, that write included.
  Every read that asks the service MUST be recorded on the transaction's outcome with the service's answer, an answer of none included (see [The Stateless Witness](../block/stateless-witness.md)).
- `SATIN-ORCL-003` Every such read MUST be charged as a cold storage access, `COLD_SLOAD_COST`, however often the slot was read before, and the slot MUST be loaded whichever source answers, so that a later access finds it warm and a stateless witness carries it.
  The read is a read of volatile data for [gas detention](../evm/gas-detention.md), under the Oracle's cap.
- `SATIN-ORCL-004` A frame whose regular gas, its withheld part included, cannot pay the cold access MUST run out of gas at the `SLOAD` without loading the slot and without asking the service.
  A frame whose whole regular gas can pay it MUST load the slot and ask the service before the cold access is charged.
  When that charge is then gas detention's crossing (`SATIN-DET-018`) — the spendable part cannot pay it — the frame is stopped and the `SLOAD` does not complete, but the slot stays loaded, the service's answer stays recorded on the transaction's outcome (`SATIN-ORCL-002`), and the read is not marked for gas detention (`SATIN-DET-003`).
  A read refused because the frame's volatile-data access is off (see [MegaAccessControl](mega-access-control.md)) MUST NOT ask the service either.
- `SATIN-ORCL-005` During a system call the node MUST NOT ask the oracle service: an `SLOAD` in the Oracle's own frame MUST push the slot's value on the chain, MUST be loaded and priced as any Oracle read is, and MUST record no answer.
  The rule ends with the system call; a Mega System Transaction is a transaction, not a system call, and its reads ask the service.

### Hints

- `SATIN-ORCL-008` Only a `CALL` or a `STATICCALL` whose target is the Oracle and whose input's first four bytes are the selector of `sendHint(bytes32,bytes)` is a `sendHint` call.
  A `CALLCODE` or `DELEGATECALL` of the method — `multiCall`'s payloads among them — runs the Oracle's bytecode in a frame of the caller's own context, MUST NOT reach the service and MUST count nothing.
- `SATIN-ORCL-006` A `sendHint` call MUST be admitted, and its hint forwarded to the oracle service synchronously, when it is called, before the call returns, only when all of the following hold: the call is forwarded more than zero gas, it carries no value, and the frame that makes it has its volatile-data access on (see [MegaAccessControl](mega-access-control.md)).
  A call that fails any of them MUST drop the hint and count nothing.
  Whether admitted or not, the call then runs the Oracle's bytecode, but in the case of the rule `SATIN-ORCL-010` below.
- `SATIN-ORCL-007` The service MUST be handed the hint's `topic`, its `data`, and the address of the frame that made the call: the transaction's sender for a `sendHint` that is the transaction's own call.
- `SATIN-ORCL-009` An admitted call MUST count its whole input length as data size on the transaction, before the input is decoded, on no frame's budget, and MUST pay no history gas.
  A `sendHint` that is the transaction's own call MUST count its input twice: once as calldata in the transaction's body, and once as the hint.
  An admitted input MUST stay counted whatever the calling frame or the transaction does afterwards — a revert, a halt, a later stop, a failed deposit — and that includes an input that does not decode as `sendHint(bytes32,bytes)`, which reaches no service.
- `SATIN-ORCL-010` A `sendHint` call whose input length would take the transaction's data size over its data-size limit (see [Resource Limits](../evm/resource-limits.md)) MUST NOT be forwarded and MUST NOT be counted.
  The call MUST be answered with the data-size stop, `MegaLimitExceeded(0, limit)` (see [Limit Stops](../evm/limit-stops.md)), without running the Oracle's bytecode; the stop is the call's, which its caller can catch, and when the call is the transaction's own frame, the stop the transaction reports counts the data size the hint would have reached as used.
  The data size the transaction keeps, which the block's data-size budget counts, holds none of the hint's bytes.
  The check is against the transaction's limit alone: a hint's bytes are on no frame's budget.

## Constants

| Constant                  | Value                                                                | Description                                     |
| ------------------------- | -------------------------------------------------------------------- | ----------------------------------------------- |
| `ORACLE_CONTRACT_ADDRESS` | `0x6342000000000000000000000000000000000001`                         | The Oracle                                      |
| `ORACLE_CODE_HASH`        | `0x71a65239db8d0f1bb765fad36e34f57600420d103a4401ef7555bd50b229dc55` | Code hash of the Oracle version 2.0.0           |
| `COLD_SLOAD_COST`         | 2,100                                                                | The gas of a cold `SLOAD`, its warm base included |

## Rationale

**Why does the service win over the slot?**
The service answers with the value of the moment of the read; the slot holds what a Mega System Transaction wrote earlier, which may be older.
The value a frame wrote itself is only the contract's storage, which only the system address writes; giving the service precedence keeps the answer the service's whenever it has one.

**Why charge every Oracle read as cold?**
The answer can differ between two reads of the same slot — a hint in between can have the service fetch another value — so the second read is no cheaper for the node than the first.
A fixed price also makes the read's cost independent of how warm the slot happens to be.

**Why does the slot load even when the service answers?**
So that the read lands in the transaction's read set: a stateless validator that answers from the slot needs it, and a later write in the same transaction finds it warm as on every other node.

**Why does a system call not ask the service?**
A pre-block call must be a function of the state a stateless validator is given, which carries no service answer for a step before the block's transactions.
The EIP-2935 and EIP-4788 code reads no Oracle; the rule holds whatever code sits at those addresses.

**Why count a hint before decoding and keep it counted?**
Two reasons, each on its own: a payload forwarded to the service cannot be taken back, and admitting and decoding an input is work the node has done whether or not the input decodes.
A hint is not appended to history, so it pays no history gas; it is data the node handled, so it counts as data size.

**Why is a hint's value condition new?**
A value call to a `view` method reverts in the bytecode, so a valued hint would reach the service from a call that has no effect on the chain.
Rex6 forwarded such a hint; Satin drops it.

## Security Considerations

- A node that prices an Oracle read by the slot's warmth makes a second read of a slot cheaper than on every other node, and changes the gas used of every transaction that reads it twice.
- A node that asks the service during a pre-block call computes a pre-block state no stateless validator can reproduce.
- A node that does not count a hint, or counts it only once it decoded, lets a transaction push data to the service past its data-size limit; one that takes the count back when the frame fails lets a transaction send unbounded hints from frames it then reverts.
- A node that forwards a hint the transaction's data-size limit refuses sends a payload the chain never accounted for.
- The Oracle's restricted writes run their body before the authorization check, so an unauthorized caller pays for the writes and logs it attempts before the call reverts; a node that checked authorization first would charge such a caller less than the bytecode does and compute another gas used.
  At the transaction boundary no slot is written and no log is emitted by an unauthorized caller.

## Spec History

- [MiniRex](../../upgrades/minirex.md) — Introduced the Oracle.
- [Rex2](../../upgrades/rex2.md) — Added `sendHint` to the bytecode.
- [Rex3](../../upgrades/rex3.md) — Made Oracle detention triggered by an `SLOAD` of the Oracle's storage.
- [Rex5](../../upgrades/rex5.md) — Oracle version 2.0.0 reads its authority from the SequencerRegistry; hint forwarding gated on a positive gas limit and counted before decoding.
- [Rex6](../../upgrades/rex6.md) — No hint from a frame whose volatile-data access is off; the Rex6 Oracle is specified in [Oracle](../../system-contracts/oracle.md).
- [Satin](../../upgrades/satin.md) — The service wins over the slot, every read is cold and loads the slot, system calls ask nothing, a valued call is no hint, and a hint over the data-size limit is a stop.
