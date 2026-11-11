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

- `SATIN-ORCL-002` An `SLOAD` executed in the Oracle's own frame — a frame whose storage is the Oracle's: a frame running at the Oracle's address, the frames of `multiCall`'s `DELEGATECALL`s of the Oracle into itself included, and not a `DELEGATECALL` from another account into the Oracle's code, which runs on that account's storage — MUST load the slot from the state through the transaction's journal, then, unless the read is made during a system call, a deposit or a Mega System Transaction (see below), ask the node's oracle service for the slot, and push the service's value when the service gives one and the loaded value otherwise.
  The service's value MUST win over whatever the slot holds at the read, a value the Oracle's own frame wrote earlier in the transaction included; with no value from the service the read MUST push the slot's present value, that write included.
- `SATIN-ORCL-003` Every such read MUST be charged as a cold storage access, `COLD_SLOAD_COST`, however often the slot was read before, and the slot MUST be loaded whichever source answers, so that a later access finds it warm and a stateless witness carries it.
  The read is a read of volatile data for [gas detention](../evm/gas-detention.md), under the Oracle's cap.
- `SATIN-ORCL-004` The read MUST be made before the cold access is charged: the slot is loaded, the service asked when the read is one that asks it, and the read marked for gas detention (`SATIN-DET-003`), and only then is `COLD_SLOAD_COST` charged, as one charge, its warm base of 100 included: no part of the `SLOAD`'s gas is charged before the read.
  A frame whose regular gas, its withheld part included, cannot pay the cold access — whether it holds fewer than the 100 of the warm base or from 100 to 2,099 — MUST therefore load the slot, ask the service where it is asked, and mark the read, and then run out of gas at the `SLOAD`; the mark MUST stand for the rest of the transaction, though the frame halts.
  When the charge is gas detention's crossing (`SATIN-DET-018`) — the spendable part cannot pay it but the whole regular gas can — the frame is stopped and the `SLOAD` does not complete, and the slot stays loaded and the read marked all the same.
  A read refused because the frame's volatile-data access is off (see [MegaAccessControl](mega-access-control.md)) MUST NOT ask the service, and marks nothing.
- `SATIN-ORCL-005` During a system call, a deposit or a Mega System Transaction the node MUST NOT ask the oracle service for a value: an `SLOAD` in the Oracle's own frame MUST push the slot's value on the chain — its present value, a write made earlier in the same call or transaction included (`SATIN-ORCL-002`) — and MUST be loaded, priced and marked as any Oracle read is (`SATIN-ORCL-003`, `SATIN-ORCL-004`).
  Only the reads of a transaction that is neither a deposit nor a Mega System Transaction ask the service; the rule holds for the whole of the system call or transaction it covers and ends with it.
  The rule concerns reads: a `sendHint` call made in such a call or transaction is admitted, forwarded and counted by the rules of Hints below, as in any transaction, and asks the service for no value.
  It follows that no read of the block in which Satin activates asks the service: that block admits only deposits (see [Base Layer](../base-layer.md), `SATIN-BASE-006`, `SATIN-BASE-008`).

### Persistence of served values

- `SATIN-ORCL-012` For a transaction the block includes, the sequencer MUST persist on-chain every value of the oracle service that one of its Oracle reads pushed, unless the transaction's own writes explain it, by inserting a [Mega System Transaction](system-tx.md) that calls `setSlot` or `setSlots`, ordered before that transaction, so that every node replaying the block observes the same storage state.
  The sequencer MAY persist in the same way a value the service gave a read that pushed nothing — a read made before its charge whose frame then ran out of gas at the `SLOAD`, or was stopped at gas detention's crossing (`SATIN-ORCL-004`) — and need not: the replay of that read pushes nothing either, whatever the slot holds; a value so persisted MUST leave the slot holding, when the transaction starts, a value that still reproduces its reads (`SATIN-ORCL-013`).
  A system call, a deposit and a Mega System Transaction are given no value by the service (`SATIN-ORCL-005`), so nothing is persisted for them.
  The transaction's own writes explain a served value when the slot's present value at the read is one the transaction itself wrote to the slot earlier in it — by a restricted write the Oracle authorized (`SATIN-ORCL-011`) and no revert has taken back — and that value is the value served: the replay of the read pushes that write, and nothing written before the transaction need hold the value.
  A node that validates or replays a block runs no oracle service: each Oracle read it makes has no value from the service and pushes the slot's present value (`SATIN-ORCL-002`), which the Mega System Transactions before the reading transaction wrote, or, after a write of the transaction's own to the slot, that write.
  A transaction is therefore not included when a value this rule requires for it cannot be persisted before it in the block, its Mega System Transaction being skipped or refused.
- `SATIN-ORCL-013` A transaction MUST NOT be included in a block when an Oracle slot it reads has no value that, written before the transaction, would make the transaction's replay push, at each of its reads of that slot that pushed a value, the value that read pushed, the replay's read pushing the slot's present value, a write the transaction made to the slot earlier in it included (`SATIN-ORCL-002`); a read that pushed nothing — its frame out of gas or stopped at the `SLOAD` (`SATIN-ORCL-004`) — asks nothing of the slot's value.
  A transaction is left out by this rule only then: one for which such a value exists for every slot it reads is not.
  A deposit or a Mega System Transaction is never left out by it, since the service gives none of its reads a value (`SATIN-ORCL-005`): each pushes the slot's present value, as its replay does.
  A transaction that reads a slot the service answers, then sends a hint that has the service fetch another value, and then reads the slot again, answered that other value, with no write of its own to the slot between, is left out: one slot answers it two values, and no single value written before it reproduces both.
  A transaction that reads a slot the service answers 7, writes 8 to it by a restricted write the Oracle authorizes, and reads it again, answered 8, is not: the value 7 written before it reproduces the first read, and the second pushes the transaction's own write, which explains the value 8 (`SATIN-ORCL-012`).

### Hints

- `SATIN-ORCL-008` Only a `CALL` or a `STATICCALL` whose target is the Oracle and whose input's first four bytes are the selector of `sendHint(bytes32,bytes)` is a `sendHint` call.
  A `CALLCODE` or `DELEGATECALL` of the method — `multiCall`'s payloads among them — runs the Oracle's bytecode in a frame of the caller's own context, MUST NOT reach the service and MUST count nothing.
- `SATIN-ORCL-006` A `sendHint` call MUST be admitted, and its hint forwarded to the oracle service synchronously, when it is called, before the call returns, only when both of the following hold: the call's gas limit is more than zero, and the frame that makes it has its volatile-data access on (see [MegaAccessControl](mega-access-control.md)); whether the call carries value does not matter.
  The gas limit is the regular gas the call's frame starts with, a value call's stipend included, as Rex6 judges it: for a call opcode `min(requested_gas, forwarded_gas_cap)` plus `CALL_STIPEND` for a value-transferring `CALL` (see [Gas Forwarding](../evm/gas-forwarding.md), `SATIN-FWD-003`), so a value-transferring `CALL` that requests no gas starts its frame on the stipend, and its hint is admitted and counted.
  A `sendHint` that is the transaction's own call, a deposit's included, has no stipend (`SATIN-FWD-003` adds `CALL_STIPEND` only for the opcodes) and is judged on its first frame's whole regular gas: it is admitted whenever that gas is more than zero, whether or not the transaction carries value.
  A call that fails either condition MUST drop the hint and count nothing.
  Whether admitted or not, the call then reaches its frame start and runs the Oracle's bytecode, unless the rule `SATIN-ORCL-010` below answers it first.
  Admission comes before the frame start, where the caller's funds are checked (`SATIN-ICPT-007`): a `sendHint` carrying a value its caller cannot fund is admitted, forwarded and counted as any hint is, and its frame start then refuses the call, which fails with empty return data and runs no bytecode (`SATIN-OUT-010`); the hint stays counted (`SATIN-ORCL-009`).
- `SATIN-ORCL-007` The service MUST be handed the hint's `topic`, its `data`, and the address of the frame that made the call: the transaction's sender for a `sendHint` that is the transaction's own call.
- `SATIN-ORCL-009` An admitted call MUST count its whole input length as data size on the transaction, before the input is decoded, on no frame's budget, and MUST pay no history gas.
  A `sendHint` that is the transaction's own call MUST count its input twice: once as calldata in the transaction's body, and once as the hint.
  An admitted input MUST stay counted whatever the calling frame or the transaction does afterwards — a revert, a halt, a later stop, a failed deposit — and that includes an input that does not decode as `sendHint(bytes32,bytes)`, which reaches no service.
- `SATIN-ORCL-010` A `sendHint` call whose input length would take the transaction's data size over its data-size limit (see [Resource Limits](../evm/resource-limits.md)) MUST NOT be forwarded and MUST NOT be counted.
  The call MUST be answered with the data-size stop, `MegaLimitExceeded(0, limit)` (see [Limit Stops](../evm/limit-stops.md)), without running the Oracle's bytecode, whether or not its caller can fund the value it carries: the check is made at admission, before the frame start (`SATIN-ICPT-007`); the stop is the call's, which its caller can catch, and when the call is the transaction's own frame, the stop the transaction reports counts the data size the hint would have reached as used.
  The data size the transaction keeps, which the block's data-size budget counts, holds none of the hint's bytes.
  The check is against the transaction's limit alone: a hint's bytes are on no frame's budget.

## Constants

| Constant                  | Value                                                                | Description                                     |
| ------------------------- | -------------------------------------------------------------------- | ----------------------------------------------- |
| `ORACLE_CONTRACT_ADDRESS` | `0x6342000000000000000000000000000000000001`                         | The Oracle                                      |
| `ORACLE_CODE_HASH`        | `0x71a65239db8d0f1bb765fad36e34f57600420d103a4401ef7555bd50b229dc55` | Code hash of the Oracle version 2.0.0           |
| `COLD_SLOAD_COST`         | 2,100                                                                | The gas of a cold `SLOAD`, its warm base included |
| `CALL_STIPEND`            | 2,300                                                                | The stipend a value call adds to its child's gas limit ([Gas Forwarding](../evm/gas-forwarding.md)) |

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

**Why is nothing of the 2,100 charged before the read, the warm base included?**
`COLD_SLOAD_COST` is one charge of 2,100, the warm base's 100 included, and the read comes before all of it, as in Rex6, which charges the `SLOAD`'s static gas after the host's read; a node that charges the 100 first runs a frame short of it out of gas with nothing read, and marks each read it does make at a compute 100 higher than this specification's.
A worked example: an Oracle `SLOAD` is reached at a transaction compute of 3,000, with no earlier volatile read and the frame's spendable gas its whole regular gas.
- With 50 gas left, fewer than the warm base's 100, the slot is loaded, the service asked where `SATIN-ORCL-005` lets it be asked, and the read marked at a `compute_at_read` of 3,000, which sets the transaction's limit to 3,000 + 20,000,000 (`ORACLE_ACCESS_COMPUTE_GAS`, see [Gas Detention](../evm/gas-detention.md)) = 20,003,000; the `SLOAD` then runs out of gas, and the 50 the frame burns are not compute (`SATIN-DET-011`).
- With any amount from 100 to 2,099 left, the same: the slot loaded, the service asked, the read marked at 3,000 and the limit 20,003,000, and then out of gas.
- With 2,100 or more left, the same read and mark at 3,000, and then the 2,100 is charged and the `SLOAD` pushes its value, the compute rising to 5,100.

In each case `compute_at_read` is the compute before the 2,100.
Were the transaction's limit close enough that the spendable part could not pay the 2,100 while the whole regular gas could, the third case would be gas detention's crossing instead, and the frame would be stopped after the read (`SATIN-ORCL-004`).

**Why do system calls, deposits and Mega System Transactions not ask the service?**
A value the service gives must be on-chain before its reader, and none of these can have a Mega System Transaction ordered before it to put it there.
A pre-block call must be a function of the state a stateless validator is given, which carries no service answer for a step before the block's transactions.
Every deposit of a block precedes every other transaction of it, so no Mega System Transaction can precede a deposit, and a deposit, which L1 derivation requires, cannot be left out instead.
A Mega System Transaction is the sequencer's write of the values the service gave; a value served to its own read would need another one before it.
This is Rex6's practice: Rex6's specification has a served value persisted before the user transaction whose read it served, and the node Rex6 runs on opens its oracle service's window only around each user transaction it executes, and builds the Mega System Transaction that persists the window's values after the window closes, so no system call, deposit or Mega System Transaction was served; Satin states that practice as the rule (`SATIN-ORCL-005`).
No canonical pre-block call reads the Oracle in any case: the EIP-2935 and EIP-4788 code reads none, and the rule holds whatever code sits at those addresses.
The block in which Satin activates asks the service for no read as a consequence: it admits only deposits.

**Contradiction in the published text fixed.** As first published, Satin had a deposit's Oracle read in an ordinary block ask the service (`SATIN-ORCL-002`), required the value served to it to be persisted by a Mega System Transaction ordered before the deposit (`SATIN-ORCL-012`), which no block can order, since every deposit precedes every other transaction, and then required the deposit, which no block may leave out, to be left out (`SATIN-ORCL-013`).
Satin now asks the service nothing for a deposit, as Rex6's node never did, so the deposit reads the slot on the chain and every rule holds; this fixes Satin's own text, not a Rex6 defect.

**Why count a hint before decoding and keep it counted?**
Two reasons, each on its own: a payload forwarded to the service cannot be taken back, and admitting and decoding an input is work the node has done whether or not the input decodes.
A hint is not appended to history, so it pays no history gas; it is data the node handled, so it counts as data size.

**Why does a value-bearing hint still reach the service?**
Admission is decided before the bytecode runs, on the call's gas limit, its selector and the caller's access switch, as Rex6 decides it, a value call's stipend included (below); a value call to the `view` method then reverts in the bytecode, but the hint was already handed over, as for any admitted hint whose call later fails.
A call whose caller cannot fund the value is no different: Rex6 ran its interceptors before it built the call's frame, where the funds are checked, so the hint is handed over and counted, and only then does the call fail for its value (`SATIN-ICPT-007`).

**Why does a value call's stipend count toward the hint's gas?**
Rex5 made a hint wait for gas to close a free side channel: a call with no gas cannot run the Oracle's bytecode, so its frame fails at once while its payload would still reach the service.
A value call that requests no gas is not that call: its frame starts on the stipend and runs the bytecode, which reverts on the value, and the caller paid for the stipend in the value transfer's cost (`VALUE_TRANSFER_COST` contains it, see [Gas Forwarding](../evm/gas-forwarding.md)).
Rex6 judges the call's gas limit, the stipend included, and Satin keeps that; the stipend is still not forwarded gas for detention's compute (`SATIN-DET-010`), which this condition does not change.
A transaction's own call has no stipend, and its gas limit is its first frame's whole regular gas: subtracting a stipend there would drop the hint of a transaction whose first frame holds 2,300 gas or less, a deposit's included, and undercount the data size the block keeps.

**Why is a hint over the data-size limit a stop of its call?**
Rex6 counted such a hint's bytes and halted the transaction with the data-size failure.
Satin counts none of them and stops only the call: the payload never left the node, so the data size the block keeps holds none of it, and the call's caller can recover from the stop as from any limit stop ([Limit Stops](../evm/limit-stops.md)), instead of losing the whole transaction to a hint.

## Security Considerations

- A node that prices an Oracle read by the slot's warmth makes a second read of a slot cheaper than on every other node, and changes the gas used of every transaction that reads it twice.
- A node that asks the service during a pre-block call computes a pre-block state no stateless validator can reproduce; one that asks it during a deposit or a Mega System Transaction gives it a value no transaction can persist before it.
- A sequencer that includes a transaction without persisting before it a served value the transaction's own writes do not explain, or a transaction whose reads of a slot no value written before it reproduces, produces a block every replaying node computes differently.
- A node that does not count a hint, or counts it only once it decoded, lets a transaction push data to the service past its data-size limit; one that takes the count back when the frame fails lets a transaction send unbounded hints from frames it then reverts.
- A node that forwards a hint the transaction's data-size limit refuses sends a payload the chain never accounted for.
- A node that checks a `sendHint`'s funds before admitting it drops a hint every other node forwards and counts when the caller cannot fund the value, and reports another data size for the transaction and the block.
- A node that leaves a value call's stipend out of a hint's gas, or subtracts one from a transaction's own call, drops hints other nodes admit, and reports another data size for the transaction and the block.
- A node that charges any part of an Oracle read's 2,100 before the read runs a frame short of it out of gas with no read made, or marks the read later, and so computes another detention limit than every other node.
- The Oracle's restricted writes run their body before the authorization check, so an unauthorized caller pays for the writes and logs it attempts before the call reverts; a node that checked authorization first would charge such a caller less than the bytecode does and compute another gas used.
  At the transaction boundary no slot is written and no log is emitted by an unauthorized caller.

## Spec History

- [MiniRex](../../upgrades/minirex.md) — Introduced the Oracle.
- [Rex2](../../upgrades/rex2.md) — Added `sendHint` to the bytecode.
- [Rex3](../../upgrades/rex3.md) — Made Oracle detention triggered by an `SLOAD` of the Oracle's storage.
- [Rex5](../../upgrades/rex5.md) — Oracle version 2.0.0 reads its authority from the SequencerRegistry; hint forwarding gated on a positive gas limit and counted before decoding.
- [Rex6](../../upgrades/rex6.md) — No hint from a frame whose volatile-data access is off; the Rex6 Oracle is specified in [Oracle](../../system-contracts/oracle.md).
- [Satin](../../upgrades/satin.md) — Every read loads the slot, system calls, deposits and Mega System Transactions ask the service nothing (so neither does the block in which Satin activates), a value a read was given but did not push may be persisted, a hint over the data-size limit is a stop of its call, and a transaction whose reads of a slot no value written before it reproduces, its own writes included, is left out; served values are persisted before their readers, as under Rex6, but for a value the reader's own earlier write explains.
