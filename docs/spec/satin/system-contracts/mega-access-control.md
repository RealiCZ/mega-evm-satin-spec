---
description: Satin (unstable) — MegaAccessControl. Switching volatile-data access off for a call subtree: the contract and its three methods, where a read is refused, that a refused read pays nothing, and the access types its error carries.
spec: Satin
maturity: unstable
---

# MegaAccessControl

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
{% endhint %}

Abstract: The MegaAccessControl system contract, through which a frame switches volatile-data access off for itself and every frame below it: the contract's interface and the semantics of its three methods, where a read of volatile data is refused while access is off, which costs the refused frame nothing, and the access-type values its error carries.

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

  All three methods are intercepted for a `CALL` or a `STATICCALL`, under the rules of [Call Interception](interception.md), a value-bearing call answered with `NonZeroTransfer()`; a `DELEGATECALL` or `CALLCODE`, and any other selector, run the bytecode, whose fallback reverts with `NotIntercepted()`.
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
    Once its operands are there, it MUST be refused when what it reads is the beneficiary's account or the Oracle's storage, as its operands and its frame show it: the target operand of `BALANCE`, `EXTCODESIZE`, `EXTCODECOPY`, `EXTCODEHASH` or a call opcode, or a call target's one-hop EIP-7702 delegate (`SATIN-MAC-007`); the executing frame's own address for `SELFBALANCE`, and for `SELFDESTRUCT`, whose target operand is checked too; the frame's storage for an `SLOAD`.
    The refusal MUST come before the opcode charges anything and before any other check its body makes — a memory expansion, a copy, a static-context check, a value transfer, a state charge — so an `EXTCODECOPY` of the beneficiary with a large length, or a call to it the frame could not fund, is refused rather than running out of gas.

  Either refusal comes before the opcode pushes a result, so a read on a full stack MUST be refused rather than overflow the stack.
  A `BLOCKHASH` MUST be refused as `BLOCKHASH`, access type 7, whatever its operand.
- `SATIN-MAC-004` A refused read MUST revert the frame with `VolatileDataAccessDisabled(accessType)` and MUST NOT consume any gas: neither the opcode's static gas nor any dynamic cost — a cold access, a copy's memory, a call's memory or value transfer.
  The frame MUST revert on the gas it held when the opcode was reached, nothing having been charged, and a frame whose regular gas is below the opcode's static gas, or below what the opcode's body would charge, MUST be refused all the same and MUST NOT run out of gas.
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
- `SATIN-MAC-007` A call opcode whose target's EIP-7702 delegate is the block beneficiary MUST be refused as the beneficiary's account (type 10), by the rule of `SATIN-MAC-003`: in a frame whose access is off, the opcode reads its target's account and code — not the delegate's — to find the delegate's address, one hop, before it charges anything, unless the target is itself the beneficiary; that read lands in the transaction's read set but makes neither account warm, so a call it does not refuse is priced as it would be with access on.
  The read is required: a failed read of the target's account or code MUST be reported as `SATIN-VAL-010` classifies a failed read of the transaction's execution, and MUST NOT be taken as a target without a delegate ([Transaction Validation and Refusals](../block/transaction-validation.md)).

## Constants

| Constant                        | Value                                                                | Description                                                       |
| ------------------------------- | -------------------------------------------------------------------- | ----------------------------------------------------------------- |
| `MEGA_ACCESS_CONTROL_ADDRESS`   | `0x6342000000000000000000000000000000000004`                         | MegaAccessControl                                                 |
| `MEGA_ACCESS_CONTROL_CODE_HASH` | `0x96d0f3ba6b474e9684a97e4388ec8dbb7929818b51e6b4f19f885ccbdf642f9b` | MegaAccessControl version 1.0.0                                   |

## Rationale

**Why a system contract rather than an opcode?**
The switch is MegaETH's own, with no Ethereum counterpart; a contract with a Solidity interface reaches it from existing toolchains without a new opcode.

**Why refuse a block-environment read before its operands, and an account read after them?**
An opcode that reads the block environment is volatile whatever its stack holds, so nothing its operands could say changes the refusal, and Rex6 refuses it before it looks at them; an opcode that reads an account or a slot is volatile only for the one its operands name, so it must read them first, and one that fails on them has reached no read and fails as it would anywhere, as Rex6 states.
Once its operands name the beneficiary, Rex6 refuses the opcode before its body runs, a call target's delegate resolved for the check, so nothing the body would charge or check — a memory expansion, a copy, a value transfer — can halt it first; Satin keeps all three rules.

**Rex6 defect fixed.** With access off, an `EXTCODECOPY` whose only operand on the stack was the block beneficiary, its three other operands missing, was refused by Rex6's code as a volatile read, although Rex6's text gives a malformed conditionally volatile opcode its stack-underflow halt; a `CALL` that had its target on the stack but not its other operands behaved the same.
Satin refuses such an opcode only once every operand it takes is on the stack (`SATIN-MAC-003`), as Rex6's text states.

**Rex6 defect fixed.** In a frame whose volatile-data access was off, a `CALLCODE` with all seven operands, no value, an input range of 1 MiB, an output of zero length and 1,000 regular gas, whose code-source address delegates by EIP-7702 to the beneficiary, was refused for free by Rex6 when the node could read that address, but when that read failed Rex6's best-effort lookup took the address as delegating nowhere, and the call went on to its memory expansion and halted out of gas, so a failed local read changed the transaction's result.
Satin makes the delegate lookup a required read (`SATIN-MAC-007`): its failure gives the transaction no outcome, as every failed read of a transaction's execution does (`SATIN-VAL-010`), and the result never depends on whether the node could read.

**Why does a refused read cost nothing?**
The refused opcode never executes, and Rex6 charges it nothing, not even its static gas, returning the frame's gas as it was when the opcode was reached; a refusal is therefore a revert whatever the frame holds, also below the opcode's static gas, and Satin keeps that rule.

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
- A node that charges a refused read any gas, or lets a frame that cannot pay the opcode's static gas run out of gas instead of refusing it, computes another gas used and another result for every transaction whose subtree is refused.
- A node that lets a child switch its parent's restriction back on lets the code the parent distrusts read volatile data.
- The switch is not state; a node that persisted it, or kept it past the frame that set it, would refuse reads of frames that never asked for it.

## Spec History

- [Rex4](../../upgrades/rex4.md) — Introduced MegaAccessControl.
- [Rex6](../../upgrades/rex6.md) — Refused a beneficiary-executed `SELFDESTRUCT` and a delegate that is the beneficiary, and stopped hints while access is off; the Rex6 contract is specified in [MegaAccessControl](../../system-contracts/mega-access-control.md).
- [Satin](../../upgrades/satin.md) — Access type 12 for `SLOTNUM`, `BLOBHASH` no longer refused, and an account read refused only once all its operands are on the stack.
