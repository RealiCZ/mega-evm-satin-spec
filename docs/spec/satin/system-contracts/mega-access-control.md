---
description: Satin (unstable) — MegaAccessControl. Switching volatile-data access off for a call subtree: the contract and its three methods, where a read is refused, what a refused read pays, and the access types its error carries.
spec: Satin
maturity: unstable
---

# MegaAccessControl

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
{% endhint %}

Abstract: The MegaAccessControl system contract, through which a frame switches volatile-data access off for itself and every frame below it: the contract's interface and the semantics of its three methods, where a read of volatile data is refused while access is off, what the refused frame pays (nothing, except that a call refused at its target's EIP-7702 delegate pays its target's access and its memory expansion), and the access-type values its error carries.

## Motivation

A read of [volatile data](../../glossary.md#volatile-data) — the block environment, the block beneficiary's account, the Oracle's storage — subjects a transaction to [gas detention](../evm/gas-detention.md) for the rest of its execution.
A contract that calls untrusted code cannot stop that code from reading volatile data and so detaining the whole transaction.
MegaAccessControl lets a frame refuse such reads in its whole call subtree before the untrusted code runs; a refused read then reverts its frame instead of detaining the transaction.
Where the refusal happens, and what the refused frame pays, decide the gas and the result every node computes for it.

## Specification

### The contract and its methods

- `SATIN-MAC-001` MegaAccessControl MUST be the account at `MEGA_ACCESS_CONTROL_ADDRESS` holding the code `MEGA_ACCESS_CONTROL_CODE_HASH` (see [System Contracts](overview.md)), whose interface is:

```solidity
interface IMegaAccessControl {
    enum VolatileDataAccessType {
        BlockNumber,  // 0
        Timestamp,    // 1
        Coinbase,     // 2
        Difficulty,   // 3
        GasLimit,     // 4
        BaseFee,      // 5
        PrevRandao,   // 6
        BlockHash,    // 7
        BlobBaseFee,  // 8
        BlobHash,     // 9
        Beneficiary,  // 10
        Oracle        // 11
    }

    error NotIntercepted();
    error NonZeroTransfer();
    error VolatileDataAccessDisabled(VolatileDataAccessType accessType);
    error DisabledByParent();

    function disableVolatileDataAccess() external view;
    function enableVolatileDataAccess() external view;
    function isVolatileDataAccessDisabled() external view returns (bool disabled);
}
```

  All three methods are intercepted for a `CALL` or a `STATICCALL`, under the rules of [Call Interception](interception.md), its value policy included (`SATIN-ICPT-003`); a `DELEGATECALL` or `CALLCODE`, and any other selector, run the bytecode, whose fallback reverts with `NotIntercepted()`.
  The methods change only an execution-local switch, the same under `CALL` and `STATICCALL`: they write no account or storage, emit no log and move no value.
  The switch is held per transaction, for the frame that made the call — the caller, one level above the frame the call would start:
  - `disableVolatileDataAccess()` switches volatile-data access off for the caller's frame and every frame below it; a switch already off from a frame above the caller stays as it is.
  - `enableVolatileDataAccess()` switches access back on when the switch was set by the caller's own frame or is not set, and succeeds; when a frame above the caller set it, the call MUST revert with `DisabledByParent()` and change nothing.
  - `isVolatileDataAccessDisabled()` returns `true` when access is off for the caller's frame, set by that frame or by a frame above it, and `false` otherwise.
  - The switch MUST turn back on when the frame that set it returns, whatever it returns with, so a frame it calls afterwards at the same level is not restricted.
  - A call that is the transaction's own frame has no caller frame: `disableVolatileDataAccess()` succeeds and switches nothing, `enableVolatileDataAccess()` succeeds, and `isVolatileDataAccessDisabled()` returns `false`.
- `SATIN-MAC-002` `disableVolatileDataAccess()` MUST switch access off only once its answer is settled; an answer that gas detention turns into the compute stop (see [Call Interception](interception.md), `SATIN-ICPT-005`) MUST leave the switch as it was.

### Refused reads

- `SATIN-MAC-003` In a frame whose volatile-data access is off, every volatile read (see [Gas Detention](../evm/gas-detention.md)) MUST be refused:
  - an opcode that is volatile whatever its operands — `NUMBER`, `TIMESTAMP`, `COINBASE`, `PREVRANDAO`, `GASLIMIT`, `BASEFEE`, `BLOBBASEFEE`, `SLOTNUM` and `BLOCKHASH` — MUST be refused before its operands are checked and before any of its gas is charged, so a `BLOCKHASH` on an empty stack is refused rather than halting on the underflow;
  - an opcode that is volatile only for the account or the storage it reads — `BALANCE`, `SELFBALANCE`, `EXTCODESIZE`, `EXTCODECOPY`, `EXTCODEHASH`, the four call opcodes, `SELFDESTRUCT`, and `SLOAD` of the Oracle's storage — MUST first have every operand it takes on the stack: such an opcode that fails on its operands — a stack underflow, for example — MUST fail as it would with access on.
    Once its operands are there, it MUST be refused when what it reads is the beneficiary's account or the Oracle's storage, as its operands and its frame show it: the target operand of `BALANCE`, `EXTCODESIZE`, `EXTCODECOPY`, `EXTCODEHASH` or a call opcode; the executing frame's own address for `SELFBALANCE`, and for `SELFDESTRUCT`, whose target operand is checked too; the frame's storage for an `SLOAD`.
    The refusal MUST come before the opcode charges anything and before any other check its body makes — a memory expansion, a copy, a static-context check, a value transfer, a state charge — so an `EXTCODECOPY` of the beneficiary with a large length, or a call to it the frame could not fund, is refused rather than running out of gas;
  - a call opcode whose target operand is not the block beneficiary MUST be refused when its target's one-hop EIP-7702 delegate is the beneficiary, at the load of that delegate and not before the call's own steps, as `SATIN-MAC-007` specifies.

  Every refusal comes before the opcode pushes a result, so a read on a full stack MUST be refused rather than overflow the stack.
  A `BLOCKHASH` MUST be refused as `BLOCKHASH`, access type 7, whatever its operand.
- `SATIN-MAC-004` A refused read MUST revert the frame with `VolatileDataAccessDisabled(accessType)`, unless it is a call refused at its target's EIP-7702 delegate (`SATIN-MAC-007`) whose cold surcharge is gas detention's crossing, which MUST stop the frame with `MegaLimitExceeded(2, limit)` instead ([Limit Stops](../evm/limit-stops.md)).
  A read refused before the opcode's body, by the first two items of `SATIN-MAC-003`, MUST NOT consume any gas: neither the opcode's static gas nor any dynamic cost (a cold access, a copy's memory, a call's memory or value transfer).
  The frame MUST revert on the gas it held when the opcode was reached, nothing having been charged, and a frame whose regular gas is below the opcode's static gas, or below what the opcode's body would charge, MUST be refused all the same and MUST NOT run out of gas.
  A call refused at its target's delegate has made its earlier steps and read its target's account and code, which is not a volatile read; it MUST pay its target's access and its memory expansion, and nothing else:
  - its regular gas, the spendable and the withheld part, MUST be restored to what it held when the opcode was reached;
  - it MUST then be charged, as regular charges and in this order: its static cost, `WARM_STORAGE_READ_COST`; its memory expansion; and, when the target was not warm, its cold surcharge, `COLD_ACCOUNT_ACCESS − WARM_STORAGE_READ_COST`, last;
  - its memory expansion is this opcode's own growth of memory for its input and output ranges together, at the base layer's price, and nothing for a range already within the frame's memory; it is not the frame's whole memory cost.

  The first two charges leave the call's gas as it was just after its memory expansion, so the static cost and the memory expansion remain charged and count as compute (`SATIN-DET-009`); the value-transfer cost of a call that carries value is given back, and the refused delegate's access is never charged.
  The cold surcharge MUST come last: when it is gas detention's crossing, the gas is put back to what it was just before it (`SATIN-DET-018`), so the memory expansion stays charged at the stop as well.
  Nothing before the delegate's load draws on the reservoir, so the restoration and the charges leave it as the opcode found it; the frame's end then rolls back its own state and history charges as any revert or stop does (`SATIN-POOL-014`).
  A refused read marks nothing for gas detention and asks no oracle service.

- `SATIN-MAC-005` The error's argument MUST be ABI-encoded as a `uint8`, with the value of the table below.
  Values 3 and 9 MUST NOT be produced.
  Value 12 is outside the contract's `VolatileDataAccessType` enum.

| `accessType` | Read refused                     |
| ------------ | -------------------------------- |
| 0            | `NUMBER`                         |
| 1            | `TIMESTAMP`                      |
| 2            | `COINBASE`                       |
| 4            | `GASLIMIT`                       |
| 5            | `BASEFEE`                        |
| 6            | `PREVRANDAO` (`0x44`)            |
| 7            | `BLOCKHASH`                      |
| 8            | `BLOBBASEFEE`                    |
| 10           | The block beneficiary's account  |
| 11           | The Oracle's storage             |
| 12           | `SLOTNUM`                        |

- `SATIN-MAC-006` A `CREATE` or `CREATE2` MUST NOT be refused in a frame whose access is off, even when its creator or its created address is the block beneficiary: its loads of them are the creation's own checks, not volatile reads.
- `SATIN-MAC-007` In a frame whose volatile-data access is off, a call opcode (`CALL`, `CALLCODE`, `DELEGATECALL` or `STATICCALL`) whose target operand is not the block beneficiary MUST read its target only at the target's load, after the steps before it, and MUST make the steps that come before its delegate's load as it would with access on:
  - its static cost, `WARM_STORAGE_READ_COST`, and the static-context check of a `CALL` that carries value;
  - its memory expansion (`SATIN-MAC-004`), and the value-transfer cost of a `CALL` or `CALLCODE` that carries value ([Gas Schedule and Intrinsic Gas](../evm/gas-schedule.md), `SATIN-SCHED-003`);
  - the load of its target's account and code, skipped with an out-of-gas halt when the target is not warm and the regular gas left, both parts counted (`SATIN-DET-015`), is below the cold surcharge, `COLD_ACCOUNT_ACCESS − WARM_STORAGE_READ_COST`;
  - when the target holds an EIP-7702 delegation indicator, the delegation guard, which halts the call out of gas unless the regular gas left, both parts counted, covers the target's cold surcharge, not yet deducted (the surcharge for a target that was not warm, zero for one that was), plus `WARM_STORAGE_READ_COST` for the delegate's access; the static cost the call has paid is not counted again.

  A call that fails at one of these steps, or is stopped at one as gas detention's crossing (`SATIN-DET-018`), has not reached its delegate's load and MUST end as it would with access on; it has read its target's account and code exactly when it made the target's load, which a cold load skipped for its surcharge does not make.
  When the call reaches its delegate's load and that one-hop delegate is the block beneficiary, the load MUST be refused as the beneficiary's account (type 10) before anything else on the call's path: before the target's cold surcharge is deducted, before any new-account state gas, the forward and the start's history gas, and before any frame starts.
  The beneficiary's account MUST NOT be loaded, and the call's gas MUST be settled as `SATIN-MAC-004` states.
  For these rules the target was warm when it was among EIP-2929's accessed addresses as they stood when the call reached the target's load: the addresses warm from the transaction's start (`SATIN-SCHED-012`, `SATIN-SCHED-014`), and every address an earlier access warmed that no rollback has taken back, the authorities the authorization list's application warmed included (`SATIN-AUTH-014`); the call's own load of the target does not count.
  No charge of that settlement can run out of gas: the static cost and the memory expansion were paid from the same gas before the delegate's load, and the delegation guard held the regular gas left after them and after the value-transfer cost to at least the cold surcharge plus `WARM_STORAGE_READ_COST`.
  The cold surcharge MUST therefore be paid, or be gas detention's crossing when the spendable part cannot pay it (`SATIN-DET-018`), and MUST NOT halt the frame out of gas.
  The frame's end, the revert or the stop, MUST leave the target's account and code in the transaction's read set (`SATIN-WIT-002`, `SATIN-WIT-012`), and MUST roll EIP-2929's accessed addresses back to the ending frame's checkpoint, taken when that frame started: the warming the frame took, its warming of the target included, is undone, and a warmth from before the frame started stays.
  Whenever the call makes its target's load, the load is a required read: a failed read of the target's account or code MUST be reported as `SATIN-VAL-010` classifies a failed read of the transaction's execution, and MUST NOT be taken as a target without a delegate ([Transaction Validation and Refusals](../block/transaction-validation.md)).

## Constants

| Constant                        | Value                                                                | Description                                                       |
| ------------------------------- | -------------------------------------------------------------------- | ----------------------------------------------------------------- |
| `MEGA_ACCESS_CONTROL_ADDRESS`   | `0x6342000000000000000000000000000000000004`                         | MegaAccessControl                                                 |
| `MEGA_ACCESS_CONTROL_CODE_HASH` | `0x96d0f3ba6b474e9684a97e4388ec8dbb7929818b51e6b4f19f885ccbdf642f9b` | MegaAccessControl version 1.0.0                                   |
| `WARM_STORAGE_READ_COST`        | 100                                                                  | Warm account access, a call's static cost ([Gas Schedule and Intrinsic Gas](../evm/gas-schedule.md)) |
| `COLD_ACCOUNT_ACCESS`           | 3,000                                                                | Cold account access, the warm cost included ([Gas Schedule and Intrinsic Gas](../evm/gas-schedule.md)) |

## Rationale

**Why a system contract rather than an opcode?**
The switch is MegaETH's own, with no Ethereum counterpart; a contract with a Solidity interface reaches it from existing toolchains without a new opcode.

**Why refuse a block-environment read before its operands, and an account read after them?**
An opcode that reads the block environment is volatile whatever its stack holds, so nothing its operands could say changes the refusal, and Rex6 refuses it before it looks at them; an opcode that reads an account or a slot is volatile only for the one its operands name, so it must read them first, and one that fails on them has reached no read and fails as it would anywhere, as Rex6 states.
Once its operands name the beneficiary, Rex6 refuses the opcode before its body runs, a call target's delegate resolved for the check, so nothing the body would charge or check — a memory expansion, a copy, a value transfer — can halt it first; Satin keeps all three rules for what the operands name, and checks a call target's delegate where the call loads it (below).

**Rex6 defect fixed.** With access off, an `EXTCODECOPY` whose only operand on the stack was the block beneficiary, its three other operands missing, was refused by Rex6's code as a volatile read, although Rex6's text gives a malformed conditionally volatile opcode its stack-underflow halt; a `CALL` that had its target on the stack but not its other operands behaved the same.
Satin refuses such an opcode only once every operand it takes is on the stack (`SATIN-MAC-003`), as Rex6's text states.

**Rex6 defect fixed.** In a frame whose volatile-data access was off, a `CALLCODE` with all seven operands, no value, an input range of 1 MiB, an output of zero length and 1,000 regular gas, whose code-source address delegates by EIP-7702 to the beneficiary, was refused for free by Rex6 when the node could read that address, but when that read failed Rex6's best-effort lookup took the address as delegating nowhere, and the call went on to its memory expansion and halted out of gas, so a failed local read changed the transaction's result.
Satin reads that address only when the call reaches its load, after its memory expansion (`SATIN-MAC-007`), so this call halts out of gas on its memory on every node and reads nothing; a call that does reach the load makes a required read, whose failure gives the transaction no outcome, as every failed read of a transaction's execution does (`SATIN-VAL-010`), so the result never depends on whether the node could read.

**Why does a read refused before the opcode's body cost nothing?**
The refused opcode never executes, and Rex6 charges it nothing, not even its static gas, returning the frame's gas as it was when the opcode was reached; a refusal is therefore a revert whatever the frame holds, also below the opcode's static gas, and Satin keeps that rule for every read its operands or its frame name.
A call refused at its target's delegate is the one refusal that pays, for the reasons below.

**Why is a call to a delegator refused at its delegate's load, and why does it pay its target's access?**
A call whose target operand is not the beneficiary reads volatile data only when its target delegates to the beneficiary, and only the target's account and code show whether it does.
Rex6 resolved that delegate before the call charged anything, so a frame that could not pay even the call's static cost still read its target: a loop with access off read cold accounts and their code into the witness for about 160 gas each, against `COLD_ACCOUNT_ACCESS` (3,000), and the early read contradicted the witness rules, under which a read that gas skipped is not made (`SATIN-WIT-004`, `SATIN-WIT-012`).
Satin runs the call's steps as with access on and refuses at the delegate's load, so the target is read only by a call that has paid its earlier steps and holds the gas for the target's access.
The target is not volatile, and its read is complete when the delegate is refused, so the frame pays for it as for any account access: `COLD_ACCOUNT_ACCESS` for a cold target, `WARM_STORAGE_READ_COST` for a warm one.
A free refusal at the load would have kept the reads cheap: the beneficiary's address is fixed, so accounts that delegate to it are created once and called by anyone, and in a loop each was read and refused for about 181 gas.
The value-transfer cost is given back because no value moves, and the delegate's access is not charged because the delegate is not read.
This is a change from [Rex6](../../upgrades/rex6.md), which read the target before any charge and refused such a call for free, and a caller sees its effects.
For a call that reaches the delegate refusal, the retained regular charge is the opcode's own memory expansion plus 3,000 for a cold target or 100 for a warm target; when the cold surcharge is gas detention's crossing, only 100 and the memory expansion remain charged.
A call that fails or is stopped before the target's load, or whose cold load is skipped for insufficient whole regular gas, does not read the target.
A target and its code already loaded before a delegation-guard failure remain in the transaction's read set.
Either failure returns different gas from Rex6's free refusal, and the first also leaves out of the read set a target Rex6 read.
A cold surcharge that is gas detention's crossing ends the frame with the 68 bytes of `MegaLimitExceeded(2, limit)` instead of the 36 bytes of `VolatileDataAccessDisabled(10)`.

**Why does a delegate refusal keep the call's memory expansion charged?**
The call expands its memory before it loads its target, so by the refusal the node has done that work.
Given back, the expansion would count neither as compute nor against gas detention, and a loop could repeat it for almost nothing: a 200,000,000-gas transaction whose helper called a warm delegator of the beneficiary with a 3 MiB output range made 658,337 such calls, each keeping 117 gas, and grew about 1.9 TiB of memory; with the expansion charged, the same transaction makes 10 calls and grows 30 MiB.
The expansion is the call's own growth of memory, so a range the frame's memory already holds adds nothing.
It is charged again before the cold surcharge because the crossing puts the gas back to what it was before the charge that crossed: a surcharge charged before the memory would give the memory back at the stop.

**What can a detained frame still read for less than a cold access?**
Under gas detention a cold load is decided on the frame's whole regular gas, its withheld part included, while each charge is held to the spendable part (`SATIN-DET-015`, `SATIN-DET-018`), so near the limit a load can complete and the charge after it cross.
On this path that charge is the cold surcharge.
Such a stop reads one target and keeps at least the call's static cost, `WARM_STORAGE_READ_COST`, as compute, which no revert or stop gives back, and the first can come only once the allowance, what the limit leaves the transaction, is below `COLD_ACCOUNT_ACCESS` after the call's memory expansion; so at most 29 such reads fit in a transaction's last allowance window, whatever the program.
The base layer's call path has a tail of its own, which this rule inherits and does not change: a call whose target and non-beneficiary delegate are both cold loads both accounts before it deducts their combined charge, 5,900 after its static cost, so its window is an allowance below 6,000, it reads two accounts a call, and at most 59 such calls, 118 accounts, fit in it.
A pre-built call stack that discards each returned status reads 116 accounts in 58 calls; reusing that status as the next call's gas operand permits 59 calls and 118 account reads.
Both bounds are accepted: they follow from deciding a load on the whole regular gas and a charge on the spendable part, they apply once, at the end of a transaction's allowance, and a loop with any overhead of its own reaches fewer reads.

**Why is `BLOBHASH` not refused?**
It is not a volatile read ([Gas Detention](../evm/gas-detention.md), `SATIN-DET-002`): it reads the transaction's own blob hashes, which no other transaction shares.
Rex6 refused it, with access type 9, because its volatile set carried it over from the block environment; Satin, on the ruling that a value no other transaction shares is no volatile data, neither refuses nor detains it, and value 9 is never produced.

**Why is a parent's switch final for its subtree?**
A frame switches access off because it does not trust the code below it; a child that could switch it back on would defeat the switch.

**Why may a `STATICCALL` reach the methods?**
They change only an execution-local switch, not state, so a `view` entry point can protect itself as any other can.

**Why is `SLOTNUM` value 12?**
The contract's enum ends at 11 and its bytecode is unchanged, so `SLOTNUM`, added by the Satin base, takes the next value; a handler decodes the argument as a `uint8`, since the enum's decoder reverts on 12.

## Security Considerations

- A node that does not refuse a read below a frame that switched access off lets untrusted code detain the transaction, which is what the switch exists to prevent.
- A node that charges a read refused before the opcode's body any gas, or lets a frame that cannot pay the opcode's static gas run out of gas instead of refusing it, computes another gas used and another result for every transaction whose subtree is refused.
- A node that resolves a call target's delegate before the call's own steps reads accounts and code its frames never paid for, so a loop with access off fills the witness with cold accounts at a small fraction of `COLD_ACCOUNT_ACCESS`, and its read set differs from every other node's.
- A node that settles a delegate refusal otherwise computes another gas used: one that gives the target's access back reopens that loop; one that gives the memory expansion back, or decides the cold surcharge before charging the memory again, lets a loop make the node grow memory it is not paid for; and one that reports a cold surcharge that is gas detention's crossing as `VolatileDataAccessDisabled(10)` returns other revert data and misses a stop the transaction must report.
- A node that lets a child switch its parent's restriction back on lets the code the parent distrusts read volatile data.
- The switch is not state; a node that persisted it, or kept it past the frame that set it, would refuse reads of frames that never asked for it.

## Spec History

- [Rex4](../../upgrades/rex4.md) — Introduced MegaAccessControl.
- [Rex6](../../upgrades/rex6.md) — Refused a beneficiary-executed `SELFDESTRUCT` and a delegate that is the beneficiary, and stopped hints while access is off; the Rex6 contract is specified in [MegaAccessControl](../../system-contracts/mega-access-control.md).
- [Satin](../../upgrades/satin.md) — Access type 12 for `SLOTNUM`, `BLOBHASH` no longer refused, an account read refused only once all its operands are on the stack, and a call whose target delegates to the beneficiary refused at the delegate's load, after the call's own steps, paying its target's access and its memory expansion.
