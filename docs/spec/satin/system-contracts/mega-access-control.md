---
description: Satin (unstable) — MegaAccessControl. Switching volatile-data access off for a call subtree: the contract and its three methods, where a read is refused, what a refused read pays, and the access types its error carries.
spec: Satin
maturity: unstable
---

# MegaAccessControl

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
{% endhint %}

Abstract: The MegaAccessControl system contract, through which a frame switches volatile-data access off for itself and every frame below it: the contract's interface and the semantics of its three methods, where a read of volatile data is refused while access is off, the gas a refused read pays, and the access-type values its error carries.

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

- `SATIN-MAC-003` In a frame whose volatile-data access is off, every volatile read (see [Gas Detention](../evm/gas-detention.md)) MUST be refused, where the opcode loads the value and after the opcode read its operands: an opcode that fails on its operands — a stack underflow, for example — MUST fail as it would with access on.
  The load comes before the opcode pushes its result, so a read on a full stack MUST be refused rather than overflow the stack.
  A `BLOCKHASH` MUST be refused as `BLOCKHASH`, access type 7, whatever its operand.
- `SATIN-MAC-004` A refused read MUST revert the frame with `VolatileDataAccessDisabled(accessType)` on the gas the frame had after the opcode's static gas: the refused read pays its static gas, and nothing else — not a cold access, not a copy's memory, not a call's value transfer.
  What the opcode charged after its static gas and before the load — the memory and the copy cost of `EXTCODECOPY`, a call's memory and value-transfer cost — MUST be given back.
  A refused read marks nothing for gas detention and asks no oracle service.
  The static gas by opcode:

| Opcode                                                                                    | Static gas                |
| ----------------------------------------------------------------------------------------- | ------------------------- |
| `NUMBER`, `TIMESTAMP`, `COINBASE`, `PREVRANDAO`, `GASLIMIT`, `BASEFEE`, `BLOBBASEFEE`, `SLOTNUM` | `BASE_STATIC_GAS`         |
| `SELFBALANCE`                                                                             | `SELFBALANCE_STATIC_GAS`  |
| `BLOCKHASH`                                                                               | `BLOCKHASH_STATIC_GAS`    |
| `BALANCE`, `EXTCODEHASH`, `CALL`, `CALLCODE`, `DELEGATECALL`, `STATICCALL`, `SLOAD` of the Oracle's storage | `WARM_ACCESS_STATIC_GAS`  |
| `EXTCODESIZE`, `EXTCODECOPY`                                                              | `EXTCODE_STATIC_GAS`      |
| `SELFDESTRUCT`                                                                            | `SELFDESTRUCT_STATIC_GAS` |

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
- `SATIN-MAC-007` A call opcode's load of its target's EIP-7702 delegate MUST be refused, as the beneficiary's account (type 10), when the delegate is the block beneficiary, at that load.

## Constants

| Constant                        | Value                                                                | Description                                                       |
| ------------------------------- | -------------------------------------------------------------------- | ----------------------------------------------------------------- |
| `MEGA_ACCESS_CONTROL_ADDRESS`   | `0x6342000000000000000000000000000000000004`                         | MegaAccessControl                                                 |
| `MEGA_ACCESS_CONTROL_CODE_HASH` | `0x96d0f3ba6b474e9684a97e4388ec8dbb7929818b51e6b4f19f885ccbdf642f9b` | MegaAccessControl version 1.0.0                                   |
| `BASE_STATIC_GAS`               | 2                                                                    | Static gas of the block-environment opcodes                       |
| `SELFBALANCE_STATIC_GAS`        | 5                                                                    | Static gas of `SELFBALANCE`                                       |
| `BLOCKHASH_STATIC_GAS`          | 20                                                                   | Static gas of `BLOCKHASH`                                         |
| `WARM_ACCESS_STATIC_GAS`        | 100                                                                  | Static gas of a warm account or storage access                    |
| `EXTCODE_STATIC_GAS`            | 200                                                                  | Static gas of `EXTCODESIZE` and `EXTCODECOPY`, EIP-8038's two warm accesses |
| `SELFDESTRUCT_STATIC_GAS`       | 5,000                                                                | Static gas of `SELFDESTRUCT`                                      |

## Rationale

**Why a system contract rather than an opcode?**
The switch is MegaETH's own, with no Ethereum counterpart; a contract with a Solidity interface reaches it from existing toolchains without a new opcode.

**Why refuse after the operands?**
An opcode that fails on its operands has not reached a read, so it fails as it would anywhere; refusing at the load also gives every refusable opcode one rule.
Rex6 refused the unconditionally volatile opcodes before their operands were checked and charged a refused read nothing; Satin refuses at the load and charges the static gas, the cost of reaching it.

**Why give back what was charged after the static gas?**
The memory, the copy and the value transfer pay for a read and a transfer that do not happen.
The static gas is what reaching the opcode costs; keeping it makes a refused read cost something, as any executed opcode does.

**Why is a parent's switch final for its subtree?**
A frame switches access off because it does not trust the code below it; a child that could switch it back on would defeat the switch.

**Why may a `STATICCALL` reach the methods?**
They change only an execution-local switch, not state, so a `view` entry point can protect itself as any other can.

**Why is `SLOTNUM` value 12?**
The contract's enum ends at 11 and its bytecode is unchanged, so `SLOTNUM`, added by the Satin base, takes the next value; a handler decodes the argument as a `uint8`, since the enum's decoder reverts on 12.

## Security Considerations

- A node that does not refuse a read below a frame that switched access off lets untrusted code detain the transaction, which is what the switch exists to prevent.
- A node that charges a refused read its dynamic gas, or none of its static gas, computes another gas used for every transaction whose subtree is refused.
- A node that lets a child switch its parent's restriction back on lets the code the parent distrusts read volatile data.
- The switch is not state; a node that persisted it, or kept it past the frame that set it, would refuse reads of frames that never asked for it.

## Spec History

- [Rex4](../../upgrades/rex4.md) — Introduced MegaAccessControl.
- [Rex6](../../upgrades/rex6.md) — Refused a beneficiary-executed `SELFDESTRUCT` and a delegate that is the beneficiary, and stopped hints while access is off; the Rex6 contract is specified in [MegaAccessControl](../../system-contracts/mega-access-control.md).
- [Satin](../../upgrades/satin.md) — Reads refused at the load, after the operands, paying their static gas; access type 12 for `SLOTNUM`.
