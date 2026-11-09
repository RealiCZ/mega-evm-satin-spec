---
description: Satin (unstable) — Oracle. The Oracle system contract under Satin; how an SLOAD in its own frame is answered by the oracle service, what such a read costs, how a served value is persisted before its reader, and when a sendHint reaches the service and what it counts.
spec: Satin
maturity: unstable
---

# Oracle

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
{% endhint %}

Abstract: The Oracle system contract: its address, code and interface; how an `SLOAD` in the Oracle's own frame is answered by the node's oracle service; what such a read costs and loads; how the sequencer persists a value the service gave before the transaction that read it, and which transactions it cannot persist; and when a `sendHint` call reaches the service, and what it counts as data size.

## Motivation

MegaETH serves externally sourced data — a sub-second timestamp, among others — from the Oracle's storage, filled lazily: a value is fetched from the node's oracle service when a transaction reads it, not written for every block in advance.
A read answered by a service rather than by the state is a read every node must answer and price identically, and whose value the block itself must carry, or the transaction's result depends on the node it runs on.
A hint is a payload a contract hands the service so that it fetches a value before the read; it leaves the node, so it cannot be taken back, and it costs the node work whether or not it decodes.
Without exact rules for when a read asks the service, what it costs, and when a hint is admitted and what it counts, two nodes compute different gas, different data size and different stops for the same transaction.

## Specification

### Address, code and interface

- `SATIN-ORCL-001` The Oracle MUST be the account at `ORACLE_CONTRACT_ADDRESS` holding the code of version 2.0.0 (`ORACLE_CODE_HASH`, see [System Contracts](overview.md)), whose interface and behaviour are the following.
  - **Storage.** The contract's storage is a flat map from a `uint256` slot to a `bytes32` value; each service that uses it is allotted a range of slots (the [High-Precision Timestamp](high-precision-timestamp.md)'s is slots 0 to 7).
  - **Reads.** `getSlot(uint256 slot) returns (bytes32 value)` returns the value at `slot`; `getSlots(uint256[] slots) returns (bytes32[] values)` returns the values at `slots`, in order. Both read by `SLOAD` in the Oracle's own frame.
  - **Restricted writes.** `setSlot(uint256 slot, bytes32 value)`, `setSlots(uint256[] slots, bytes32[] values)`, `emitLog(bytes32 topic, bytes data)` and `emitLogs(bytes32 topic, bytes[] dataVector)` write the slots or emit the logs, and then revert with `NotSystemAddress()` unless the immediate caller is the address `SequencerRegistry.currentSystemAddress()` returns (see [SequencerRegistry](sequencer-registry.md)). The body — every `SSTORE`, `LOG` and loop iteration — runs before that check and is charged as it runs; the revert takes back every write and log. `setSlots` with arrays of different lengths reverts with `InvalidLength(uint256 slotsLength, uint256 valuesLength)` before any `SSTORE` and before the check.
  - **Auxiliary.** `multiCall(bytes[] data) returns (bytes[] results)` executes each payload by `DELEGATECALL` into the Oracle and returns the results in order; at the first payload that fails it reverts with that payload's revert data when the data are not empty, and with `Error(string)` carrying `"Multicall: call failed"` when they are empty; `sendHint(bytes32 topic, bytes data)` is a no-op `view` method at the bytecode level.
- `SATIN-ORCL-011` A restricted write MUST be authorized as the Oracle's bytecode authorizes it, and by no further rule of the node's: once the body has run, the write stands when the immediate caller of the Oracle's frame is the address `SequencerRegistry.currentSystemAddress()` returns, and the call reverts with `NotSystemAddress()` otherwise, whatever sent the transaction and whatever the transaction's type.
  The sequencer writes the Oracle through Mega System Transactions (see [Mega System Transactions](system-tx.md)); code running at the live system address writes it as well — the [High-Precision Timestamp](high-precision-timestamp.md)'s `update` while that contract is the live system address (`SATIN-HPTS-001`), or the code an EIP-7702 delegation of the system address runs, a deposit's call among them — since the registry accepts any non-zero address as the system address (`SATIN-REG-001`).

### Oracle reads

- `SATIN-ORCL-002` An `SLOAD` executed in the Oracle's own frame — a frame whose storage is the Oracle's: a frame running at the Oracle's address, the frames of `multiCall`'s `DELEGATECALL`s of the Oracle into itself included, and not a `DELEGATECALL` from another account into the Oracle's code, which runs on that account's storage — MUST load the slot from the state through the transaction's journal, then ask the node's oracle service for the slot, and push the service's value when the service gives one and the loaded value otherwise.
  The service's value MUST win over whatever the slot holds at the read, a value the Oracle's own frame wrote earlier in the transaction included; with no value from the service the read MUST push the slot's present value, that write included.
- `SATIN-ORCL-003` Every such read MUST be charged as a cold storage access, `COLD_SLOAD_COST`, however often the slot was read before, and the slot MUST be loaded whichever source answers, so that a later access finds it warm and a stateless witness carries it.
  The read is a read of volatile data for [gas detention](../evm/gas-detention.md), under the Oracle's cap.
- `SATIN-ORCL-004` The read MUST be made before the cold access is charged: the slot is loaded, the service asked, and the read marked for gas detention (`SATIN-DET-003`), and only then is `COLD_SLOAD_COST` charged.
  A frame whose regular gas, its withheld part included, cannot pay the cold access MUST therefore load the slot, ask the service and mark the read, and then run out of gas at the `SLOAD`; the mark MUST stand for the rest of the transaction, though the frame halts.
  When the charge is gas detention's crossing (`SATIN-DET-018`) — the spendable part cannot pay it but the whole regular gas can — the frame is stopped and the `SLOAD` does not complete, and the slot stays loaded and the read marked all the same.
  A read refused because the frame's volatile-data access is off (see [MegaAccessControl](mega-access-control.md)) MUST NOT ask the service, and marks nothing.
- `SATIN-ORCL-005` During a system call, and for every transaction of the block in which Satin activates, the node MUST NOT ask the oracle service: an `SLOAD` in the Oracle's own frame MUST push the slot's value on the chain, and MUST be loaded, priced and marked as any Oracle read is.
  The rule for a system call ends with the system call; a Mega System Transaction is a transaction, not a system call, and its reads ask the service.
  The block in which Satin activates admits only deposits (see [Base Layer](../base-layer.md), `SATIN-BASE-008`), so no Mega System Transaction in it can persist a value before a reader.

### Persistence of served values

- `SATIN-ORCL-012` For a transaction the block includes, every value the oracle service gave one of its Oracle reads that the transaction's own writes do not explain MUST be persisted on-chain by a [Mega System Transaction](system-tx.md) the sequencer inserts, which calls `setSlot` or `setSlots` and MUST be ordered before that transaction, so that every node replaying the block observes the same storage state.
  The transaction's own writes explain a served value when the slot's present value at the read is one the transaction itself wrote to the slot earlier in it — by a restricted write the Oracle authorized (`SATIN-ORCL-011`) and no revert has taken back — and that value is the value served: the replay of the read pushes that write, and nothing written before the transaction need hold the value.
  A node that validates or replays a block runs no oracle service: each Oracle read it makes has no value from the service and pushes the slot's present value (`SATIN-ORCL-002`), which the Mega System Transactions before the reading transaction wrote, or, after a write of the transaction's own to the slot, that write.
  A transaction is therefore not included when a value this rule requires for it cannot be persisted before it in the block, its Mega System Transaction being skipped or refused.
- `SATIN-ORCL-013` A transaction MUST NOT be included in a block when an Oracle slot it reads has no value that, written before the transaction, would make the transaction's replay push at each of its reads of that slot what its execution pushed, the replay's read pushing the slot's present value, a write the transaction made to the slot earlier in it included (`SATIN-ORCL-002`).
  A transaction is left out by this rule only then: one for which such a value exists for every slot it reads is not.
  A transaction that reads a slot the service answers, then sends a hint that has the service fetch another value, and then reads the slot again, answered that other value, with no write of its own to the slot between, is left out: one slot answers it two values, and no single value written before it reproduces both.
  A transaction that reads a slot the service answers 7, writes 8 to it by a restricted write the Oracle authorizes, and reads it again, answered 8, is not: the value 7 written before it reproduces the first read, and the second pushes the transaction's own write, which explains the value 8 (`SATIN-ORCL-012`).

### Hints

- `SATIN-ORCL-008` Only a `CALL` or a `STATICCALL` whose target is the Oracle and whose input's first four bytes are the selector of `sendHint(bytes32,bytes)` is a `sendHint` call.
  A `CALLCODE` or `DELEGATECALL` of the method — `multiCall`'s payloads among them — runs the Oracle's bytecode in a frame of the caller's own context, MUST NOT reach the service and MUST count nothing.
- `SATIN-ORCL-006` A `sendHint` call MUST be admitted, and its hint forwarded to the oracle service synchronously, when it is called, before the call returns, only when both of the following hold: the call is forwarded more than zero gas, and the frame that makes it has its volatile-data access on (see [MegaAccessControl](mega-access-control.md)); whether the call carries value does not matter.
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

**Rex6 defect fixed.** With slot `s` holding 7 and the service also answering 7, a transaction calling `multiCall([getSlot(s), setSlot(s, 8)])` paid the cold price for the `SSTORE` on a node that ran a service, which did not load the slot when the service answered, and the warm price on a replaying node, which loaded it at the read, so the two computed a different gas used.
Satin loads the slot at every Oracle read, whichever source answers (`SATIN-ORCL-003`), so the read lands in the transaction's read set and a later access finds the slot warm on every node.

**Why must a served value be on-chain before its reader?**
A node that validates or replays the block has no service; it reads every Oracle value from the slot, so the value the service gave the sequencer must be in the slot when the read runs: written before the reading transaction by a Mega System Transaction, or written by the reading transaction itself earlier in it.
Rex6 put this obligation on the sequencer, and Satin keeps it: the block carries the values, and nothing beside the block carries the service's answers.
Rex6 states the obligation for every value the service gives; Satin states it for every value the reading transaction's own writes do not explain (`SATIN-ORCL-012`), because the replay of a read after such a write pushes the write (`SATIN-ORCL-002`), not a value written before the transaction, and needs no Mega System Transaction for it.

**Rex6 defect fixed.** A transaction that read an Oracle slot, sent a hint that had the service fetch another value, and read the slot again, writing nothing to it between, was answered two values for one slot, and no single Mega System Transaction ordered before it could persist both, so a replaying node computed another result than the sequencer.
Satin leaves such a transaction out of the block (`SATIN-ORCL-013`), and only such a one: a transaction is left out when no value written before it reproduces all its reads of a slot, its own writes included.
A transaction that reads 7, writes 8 to the slot by a restricted write the Oracle authorizes, and reads 8 is therefore included, the value 7 persisted before it reproducing the first read and its own write the second.

**Why does an unaffordable Oracle read still ask the service and mark the read?**
Rex6 made the read, and registered it for detention, before charging its cold access, so that a frame which then runs out of gas leaves the registration standing for the rest of the transaction; Satin keeps that order, and loads the slot as every Oracle read does.

**Why does a system call not ask the service?**
A pre-block call must be a function of the state a stateless validator is given, which carries no service answer for a step before the block's transactions, and no Mega System Transaction can be ordered before a pre-block step to persist one.
Rex6's node asked the service in a system call as in a transaction; Satin does not, a change no canonical pre-block call observes: the EIP-2935 and EIP-4788 code reads no Oracle, and the rule holds whatever code sits at those addresses.
The block in which Satin activates asks the service for no read either: it admits only deposits, so no Mega System Transaction can persist a value in it before a reader.

**Why count a hint before decoding and keep it counted?**
Two reasons, each on its own: a payload forwarded to the service cannot be taken back, and admitting and decoding an input is work the node has done whether or not the input decodes.
A hint is not appended to history, so it pays no history gas; it is data the node handled, so it counts as data size.

**Why does a value-bearing hint still reach the service?**
Admission is decided before the bytecode runs, on the call's gas, its selector and the caller's access switch, as Rex6 decides it; a value call to the `view` method then reverts in the bytecode, but the hint was already handed over, as for any admitted hint whose call later fails.

**Why is a hint over the data-size limit a stop of its call?**
Rex6 counted such a hint's bytes and halted the transaction with the data-size failure.
Satin counts none of them and stops only the call: the payload never left the node, so the data size the block keeps holds none of it, and the call's caller can recover from the stop as from any limit stop ([Limit Stops](../evm/limit-stops.md)), instead of losing the whole transaction to a hint.

## Security Considerations

- A node that prices an Oracle read by the slot's warmth makes a second read of a slot cheaper than on every other node, and changes the gas used of every transaction that reads it twice.
- A node that asks the service during a pre-block call computes a pre-block state no stateless validator can reproduce.
- A sequencer that includes a transaction without persisting before it a served value the transaction's own writes do not explain, or a transaction whose reads of a slot no value written before it reproduces, produces a block every replaying node computes differently.
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
- [Satin](../../upgrades/satin.md) — Every read loads the slot, system calls and the block in which Satin activates ask the service nothing, a hint over the data-size limit is a stop of its call, and a transaction whose reads of a slot no value written before it reproduces, its own writes included, is left out; served values are persisted before their readers, as under Rex6, but for a value the reader's own earlier write explains.
