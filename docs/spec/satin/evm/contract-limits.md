---
description: Satin (unstable) — Contract Size Limits. The deployed-code limit of 524,288 bytes and the initcode limit of 1,048,576 bytes, how crossing either ends a creation, and the order in which the creation opcodes make their checks and charges.
spec: Satin
maturity: unstable
---

# Contract Size Limits

{% hint style="warning" %}
**Unstable** — Satin is under active development: every value and rule on this page may change before Satin is frozen.
{% endhint %}

Abstract: Deployed code is limited to 524,288 bytes and initcode to twice that; crossing either is Ethereum's size check at MegaETH's sizes — a halt or a rejection — and not a limit stop, and the creation opcodes make their checks and charges in a fixed order.

## Motivation

Ethereum's EIP-170 limit of 24,576 bytes of code and EIP-3860's 49,152 bytes of initcode exist to bound the work of loading, hashing and analysing code; at MegaETH's throughput and hardware those bounds are far below what a node can handle, and they force large applications to split into proxy and library contracts that cost more to call.

The order in which a creation opcode makes its checks and charges is observable: under gas detention a charge made before a check can be the crossing that stops a frame, where the check alone would have halted it.

## Specification

- `SATIN-SIZE-001` Deployed code MUST be at most `MAX_CONTRACT_SIZE` bytes.
- `SATIN-SIZE-002` Initcode MUST be at most `MAX_INITCODE_SIZE` bytes, twice `MAX_CONTRACT_SIZE`.
- `SATIN-SIZE-003` These are Ethereum's size checks at MegaETH's sizes, not resource limits: initcode over `MAX_INITCODE_SIZE` MUST halt the creating frame at the creation opcode, and deployed code over `MAX_CONTRACT_SIZE` MUST halt the creation, each consuming the halting frame's regular gas.
  Neither is a limit stop ([Halts, Reverts and Stops](outcomes.md)).
- `SATIN-SIZE-004` A creation transaction other than a deposit whose initcode is over `MAX_INITCODE_SIZE` MUST be rejected at validation ([Transaction Validation and Refusals](../block/transaction-validation.md)); a deposit is never rejected, and one that fails this check is a failed deposit ([Deposit Transactions](../block/deposits.md)).
  A keyless deployment's initcode over the limit is refused by its own rule ([KeylessDeploy](../system-contracts/keyless-deploy.md)).
- `SATIN-SIZE-005` `CREATE` and `CREATE2` MUST make their checks and charges in this order, and a node MUST add no charge ahead of them:
  1. the static context;
  2. the value, offset and size operands, and the size's range;
  3. the initcode size against `MAX_INITCODE_SIZE`;
  4. EIP-3860's initcode cost;
  5. the offset's range and the memory the initcode is read from, neither checked for empty initcode;
  6. for `CREATE2`, the salt operand, then `CREATE_ACCESS` and the hashing cost of the initcode; for `CREATE`, `CREATE_ACCESS`.

  The charges the creation makes for its start follow these ([History Gas and the History Allowance](history-gas.md)).
- `SATIN-SIZE-006` A creation in a static frame therefore MUST fail before its operands are read, and a `CREATE2` short of its salt MUST pay the initcode cost and the memory before it fails on the missing operand.
  The halt consumes the frame's gas either way, but under gas detention one of those charges can be the crossing, which stops the frame with a revert where the stack underflow would have halted it ([Gas Detention](gas-detention.md)).

### Retired ids

None.

## Constants

| Constant            | Value     | Description                                                   |
| ------------------- | --------- | ------------------------------------------------------------- |
| `MAX_CONTRACT_SIZE` | 524,288   | The most bytes deployed code may hold (512 KiB)                |
| `MAX_INITCODE_SIZE` | 1,048,576 | The most bytes an initcode may hold (1 MiB)                    |
| `CREATE_ACCESS`     | 12,000    | Regular gas of a creation's access ([Gas Schedule and Intrinsic Gas](gas-schedule.md)) |

## Rationale

**Why 512 KiB of code?**
It is the limit MegaETH has run since MiniRex, large enough that applications need not split into proxies, and small enough that loading and hashing a contract stays cheap on a sequencer.

**Why twice the code limit for initcode?**
EIP-3860 sets initcode to twice the code limit, so that a constructor can carry the code it deploys and the data it needs; Rex6 set initcode to the code limit plus 24,576 bytes, which left a 512 KiB contract's constructor almost no room.
Satin restores EIP-3860's ratio.

**Why halts and not stops?**
These are the base layer's own size checks; keeping them as halts keeps the gas a failing creation consumes what every Ethereum tool expects, and only the resource limits, which are MegaETH's, stop with a revert.

**Why fix the order of the checks?**
The order is the base layer's; stating it makes the one observable consequence explicit: a `CREATE2` short of its salt pays for its initcode first, which under detention turns a would-be halt into a stop.

## Security Considerations

- If a node checked the initcode size after charging its memory, a frame could be made to expand memory for an initcode it then refuses, and its gas used would differ from every other node's.
- If either size check were made a revert, a failing creation would return gas the base layer consumes, and receipts would differ.
- If a node used Rex6's initcode limit, a creation between 548,864 and 1,048,576 bytes of initcode would halt on one node and run on another.

## Spec History

- [Satin](../../upgrades/satin.md) — Kept Rex6's 524,288-byte code limit of [Contract Size Limits](../../evm/contract-limits.md), raised the initcode limit from 548,864 to 1,048,576 bytes, and stated the creation opcodes' check order.
