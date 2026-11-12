---
description: Satin (unstable) — System Calls and the Pre-Block Sequence. The gas a system call runs on, the steps a block takes before its transactions and their order, and how a failed pre-block step ends the block.
spec: Satin
maturity: unstable
---

# System Calls and the Pre-Block Sequence

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
{% endhint %}

Abstract: How a system call's gas is split between regular gas and a reservoir, the budget every pre-block call runs on, the steps a block takes before its first transaction — the EIP calls, the system contracts' deployment, the role change, the resolution of the live system address — and their order, the predicate that decides whether the SequencerRegistry has a role change due, and what a failed pre-block step does to the block.

## Motivation

Before its transactions a block updates protocol state: the EIP-2935 block-hash history, the EIP-4788 beacon root, the system contracts, which it installs where they are missing or altered, and, when one is due, the SequencerRegistry's role change; and it resolves the system address its transactions are classified against.
These calls are made by the protocol, not by a user, so nobody pays for them; but they run code, and under EIP-8037 their gas has two pools.
If the budget of a pre-block call depended on the block's gas limit, or its state gas could not be paid, the same block would succeed on one node and fail on another; and a step the nodes made in a different order, or not at all, would leave a different state for the block's first transaction.

## Specification

### The gas of a system call

- `SATIN-PBLK-001` A system call MUST run on at most `SYSTEM_CALL_REGULAR_GAS_LIMIT` of regular gas, the rest of its gas limit being its state-gas reservoir, as [EIP-8037](https://eips.ethereum.org/EIPS/eip-8037) specifies for system calls; `GAS` inside a system call MUST read at most `SYSTEM_CALL_REGULAR_GAS_LIMIT`.
  A transaction is not a system call, a Mega System Transaction included: every transaction's gas is split by the execution cap (see [Two-Pool Gas](../evm/gas-model.md)).
  A system call is the protocol's own work and is exempt as [Mega System Transactions](../system-contracts/system-tx.md) (`SATIN-MST-008`) specifies.
- `SATIN-PBLK-002` Each pre-block call MUST run from `SYSTEM_CALLER` on `PRE_BLOCK_CALL_GAS_LIMIT` of gas, whatever the block's gas limit: `SYSTEM_CALL_REGULAR_GAS_LIMIT` of regular gas and a reservoir of `PRE_BLOCK_CALL_GAS_LIMIT − SYSTEM_CALL_REGULAR_GAS_LIMIT`, the state gas of `SYSTEM_CALL_RESERVOIR_SLOTS` new storage slots at `m = 1`.
  A state charge MUST draw the call's pools as any frame's does: its legacy share, for a fresh slot, from the regular gas, then the reservoir, then the rest from the regular gas (see [Two-Pool Gas](../evm/gas-model.md), [State Gas and SALT Pricing](../evm/state-gas.md)).
  A pre-block call does not draw on the block's gas limit.

### The pre-block sequence

- `SATIN-PBLK-003` Before its first transaction, a block MUST, in this order:
  1. make the EIP-2935 call to `HISTORY_STORAGE_ADDRESS` with the parent block's hash;
  2. make the EIP-4788 call to `BEACON_ROOTS_ADDRESS` with the parent beacon block root; a block without a parent beacon block root MUST be invalid, as EIP-4788 defines;
  3. in the block in which Satin activates, and in no other, check the EIP-7997 factory, as [Activation and Rex-Era Carry-Over](activation.md) specifies (`SATIN-ACT-005`);
  4. deploy the Oracle, the High-Precision Timestamp, KeylessDeploy, MegaAccessControl and MegaLimitControl, in that order, each as a state of its own ([System Contracts](../system-contracts/overview.md), `SATIN-SYSC-003`);
  5. read whether the SequencerRegistry has a role change due in the block (`SATIN-PBLK-004`), and when it has, call `applyPendingChanges()` on it;
  6. deploy the SequencerRegistry ([SequencerRegistry](../system-contracts/sequencer-registry.md), `SATIN-REG-008`);
  7. resolve the block's live system address from the registry (`SATIN-REG-002`).

  A block whose number is zero, the genesis block, MUST make no EIP-2935 call and no EIP-4788 call, and its parent beacon block root MUST be zero, as those EIPs define; it makes the other steps as every block does.
  Each step's state MUST be committed on its own, in that order — each deployment's, and the read-only entries of steps 3 to 7, included — before the next step and before the block's first transaction.
- `SATIN-PBLK-004` A role change MUST be due in the block when the SequencerRegistry's account exists and, for the system-address role (pending address in slot 7, activation block in slot 8) or for the sequencer role (pending address in slot 9, activation block in slot 10), the pending address slot holds a non-zero value and the activation block slot holds a value at most the block's number.
  The read MUST load the registry's account and, for each role, its pending address slot, and its activation block slot only when the pending address is non-zero; an absent registry has no change due and MUST be recorded as absent.
  The read writes nothing; its loads are a read-only state of the pre-block phase (see [The Stateless Witness](stateless-witness.md)).

### Failure

- `SATIN-PBLK-006` A pre-block call that does not succeed MUST make the block invalid, before its state is used.
  A database error the node's database declares fatal is an internal error of the node, not a verdict on the block; any other failure of a pre-block call — a database error not declared fatal, another execution error, a result that is not a success — MUST make the block invalid.
  A database error in the factory check, in a deployment, in the due-change read or in the resolution of the live system address is always an internal error of the node: a node whose database cannot serve them cannot execute the block, whatever its transactions.
  A registry the deployment cannot migrate (`SATIN-REG-008`), and one the resolution finds absent, holding other code or naming no system address (`SATIN-REG-004`), MUST make the block invalid.

### Retired ids

- `SATIN-PBLK-005` Retired, merged into `SATIN-ORCL-005` (see [Oracle](../system-contracts/oracle.md)): an Oracle read during a system call asks no oracle service.

## Constants

| Constant                        | Value                                        | Description                                                        |
| ------------------------------- | -------------------------------------------- | ------------------------------------------------------------------ |
| `SYSTEM_CALL_REGULAR_GAS_LIMIT` | 30,000,000                                   | The most regular gas a system call runs on                         |
| `SYSTEM_CALL_RESERVOIR_SLOTS`   | 16                                           | New storage slots a pre-block call's reservoir pays for at `m = 1` |
| `SLOT_STATE_GAS`                | 97,920                                       | State gas of one new storage slot at `m = 1` (see [State Gas and SALT Pricing](../evm/state-gas.md)) |
| `PRE_BLOCK_CALL_GAS_LIMIT`      | 31,566,720                                   | `SYSTEM_CALL_REGULAR_GAS_LIMIT + SYSTEM_CALL_RESERVOIR_SLOTS × SLOT_STATE_GAS` |
| `SYSTEM_CALLER`                 | `0xfffffffffffffffffffffffffffffffffffffffe` | The caller of every pre-block call                                 |
| `HISTORY_STORAGE_ADDRESS`       | `0x0000F90827F1C53a10cb7A02335B175320002935` | The EIP-2935 history contract                                      |
| `BEACON_ROOTS_ADDRESS`          | `0x000F3df6D732807Ef1319fB7B8bB8522d0Beac02` | The EIP-4788 beacon roots contract                                 |

## Rationale

**Why a fixed budget?**
Rex6 ran the pre-block calls on `max(block_gas_limit, 30,000,000)`, so the budget moved with the block.
A fixed budget makes every pre-block call's gas a protocol value; the block's gas limit, which the calls do not draw on, has no reason to set it.

**Why sixteen slots of reservoir?**
EIP-8037 sizes a system call's reservoir as the state gas of `SYSTEM_MAX_SSTORES_PER_CALL` = 16 new slots.
On MegaETH's chains the EIP-2935 and EIP-4788 addresses hold those EIPs' own code, and `applyPendingChanges()` writes at most six new slots when it applies both roles, so the reservoir pays all of a pre-block call's state gas but the legacy share of each fresh slot, which its regular gas pays; other code at those addresses runs on the same budget, and what the reservoir cannot pay comes from the regular gas.
None of these calls reads `GAS`, so how the budget is split changes no call's result.

**Why this order?**
The EIP calls come first, as the base layer has them; the factory check precedes every MegaETH step, so that a chain without the factory is refused before anything is deployed; the system contracts are then deployed as Rex6 deploys them, the five flat contracts first, and the registry's role change applied before the registry's own deployment, as Rex6 orders them; the live system address is resolved last, on the state every other step left, as Rex6 resolves it after its pre-block changes.

**Why commit each step before the next?**
Rex6 ran every pre-block step against the state before the block and committed their outcomes afterwards, in order, so a step did not see what an earlier one wrote, and an outcome committed later could put back account information an earlier one had changed — the reason Rex6 must run the registry's apply before its deployment.
Satin commits each step before it makes the next, so every step sees the ones before it and no commit carries a stale account; the canonical steps touch separate accounts and compute the same either way, and Rex6's apply-before-deploy order is kept.

**Rex6 defect fixed.** At block number 2^64 − 1, a role whose pending address is non-zero and whose activation block is 2^64, a value its slot can hold, is not due, yet Rex6's precheck saturated the activation block to 2^64 − 1, the largest 64-bit value, found the change due and made an `applyPendingChanges()` call that changed nothing, adding the call and its reads to the block.
Satin compares the slot's whole value with the block number (`SATIN-PBLK-004`), as the registry's bytecode does.

**Why read the due change at the storage level?**
The read lands in the witness, so it must name exactly the slots a validator needs; a contract-level description ("a pending change whose activation block has come") would leave open which slots are loaded.

**Why is a database failure in the reads an internal error?**
The reads decide nothing about the block by themselves: they serve a check, a deployment or the system address.
A node that cannot make them cannot execute the block at all, which is a fault of the node, not evidence that the block is wrong.

**Rex6 defect fixed.** A fatal database error inside a pre-block call — the node's own storage failing during the EIP-2935, EIP-4788 or `applyPendingChanges()` call — made Rex6 report the block invalid, so a node whose database broke rejected a valid block.
Satin reports such an error as the node's internal error, as it does for a transaction's reads, and invalidates the block only for a failure of the call itself or a database error not declared fatal (`SATIN-PBLK-006`).

## Security Considerations

- A node whose pre-block budget followed the block's gas limit could fail a pre-block call on a small block that every other node accepts.
- A node that skipped the due-change read, or read it after the transactions began, would classify the block's transactions against a system address the other nodes did not see.
- A node that resolved the live system address before the deployment and the role change would classify the block's transactions against an address those steps replaced.
- A node that reported a database failure in a pre-block read as an invalid block would reject a valid block because of its own fault.

## Spec History

- [Rex5](../../upgrades/rex5.md) — Introduced the pre-block role change and the `max(block_gas_limit, 30,000,000)` budget.
- [Rex6](../../upgrades/rex6.md) — Ran the role change before the registry's deploy step.
- [Satin](../../upgrades/satin.md) — The split system-call budget, the fixed pre-block budget, the factory check at activation, Rex6's deployment and resolution as pre-block steps, and each step committed before the next.
