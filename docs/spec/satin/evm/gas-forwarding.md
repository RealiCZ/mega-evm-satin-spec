---
description: Satin (unstable) — Gas Forwarding. How much regular gas a call or creation forwards (98/100 of the caller's remaining regular gas in place of EIP-150's 63/64), the value-transfer stipend, the reservoir share a child receives, and how the forward differs from the frame-budget share.
spec: Satin
maturity: unstable
---

# Gas Forwarding

{% hint style="warning" %}
**Unstable** — Satin is under active development: every value and rule on this page may change before Satin is frozen.
{% endhint %}

Abstract: A call or creation forwards at most `remaining − remaining × 2 / 100` of its caller's regular gas, plus the 2,300 stipend for a value-transferring `CALL` or `CALLCODE`; the [reservoir](../../glossary.md#reservoir) is outside that cap and is shared by its own rule.

## Motivation

EIP-150's 63/64 rule exists to stop the call-depth attack: each nested call keeps less gas than its parent, so a deep call stack runs out of gas before it reaches the depth limit.
MegaETH runs blocks with gas limits up to 10 billion, and at that scale 63/64 still leaves enough gas at depth 1,024 for the attack to work.

A gas pool split into regular gas and a reservoir adds a second question: a hard-coded gas argument written for one pool would also bound the state gas a callee can pay, which on MegaETH's state prices is far larger than the regular gas such an argument was chosen for.

## Specification

- `SATIN-FWD-001` `CALL`, `CALLCODE`, `DELEGATECALL`, `STATICCALL`, `CREATE` and `CREATE2` MUST cap the regular gas they forward at

  `forwarded_gas_cap = parent_remaining_gas − parent_remaining_gas × GAS_RETAINED_NUMERATOR / GAS_RETAINED_DENOMINATOR`

  - `parent_remaining_gas` — the caller's regular gas at the point of `SATIN-FWD-002`.
  - The division is integer division, truncating toward zero.

  This cap applies in place of EIP-150's 63/64 rule.
- `SATIN-FWD-002` `parent_remaining_gas` MUST be the caller's remaining regular gas after every charge the opcode makes before the forward ([History Gas and the History Allowance](history-gas.md) orders them).
  For a value-transferring `CALL` or `CALLCODE` those charges include the value-transfer cost of `VALUE_TRANSFER_COST`, which already contains the `CALL_STIPEND`, so the stipend is not taken from `parent_remaining_gas` again.
- `SATIN-FWD-003` The child's regular gas MUST be `min(requested_gas, forwarded_gas_cap)`, plus `CALL_STIPEND` for a value-transferring `CALL` or `CALLCODE` and for no other opcode.
  - `requested_gas` — the gas operand of the call.

  The stipend MUST be added to the child after the cap and MUST NOT be taken from the caller's remaining regular gas; `requested_gas` MUST NOT raise the forwarded portion above `forwarded_gas_cap`.
  A value-transferring `CALL` whose caller has 10,000 regular gas left after the value-transfer charge forwards a cap of 9,800: the child receives 12,100 and the caller keeps 200.
  The history allowance a value call grants ([History Gas and the History Allowance](history-gas.md)) is not part of the child's gas.
- `SATIN-FWD-004` `CREATE` and `CREATE2` have no gas operand: each MUST forward `forwarded_gas_cap` and MUST add no stipend.
  The regular-gas forward of a keyless deployment's creation is specified on [KeylessDeploy](../system-contracts/keyless-deploy.md).
- `SATIN-FWD-005` The reservoir MUST NOT be part of `forwarded_gas_cap` or of `requested_gas`.
  A child MUST receive the reservoir share of `SATIN-POOL-011` ([Two-Pool Gas](gas-model.md)), the transaction's own frame and a system call's outermost frame the whole reservoir (`SATIN-POOL-010`), whatever regular gas the start forwards: a call that forwards no regular gas still forwards the share.
- `SATIN-FWD-006` The reservoir share and the forward cap MUST be computed by the subtraction of `SATIN-FWD-001` and `SATIN-POOL-011`, which a node MUST NOT replace by the frame-budget multiplication `remaining × FRAME_DATA_SHARE_NUMERATOR / FRAME_DATA_SHARE_DENOMINATOR` of [Resource Limits](resource-limits.md); the two give different integers.
  The subtraction gives a child 98 of a remaining 99, and the whole remaining value whenever that value is below 50, so a remaining 1 gives the child 1 and the caller 0; the multiplication gives 97 of 99 and 0 of 1.
- `SATIN-FWD-007` A system-originated transaction and a system call MUST apply the reservoir split of `SATIN-POOL-011` like any other execution: their exemption from the per-transaction limits ([Mega System Transactions and the Protocol's Own Transactions](../system-contracts/system-tx.md)) does not exempt them from it.

### Retired ids

None.

## Constants

| Constant                       | Value  | Description                                                                     |
| ------------------------------ | ------ | ------------------------------------------------------------------------------- |
| `GAS_RETAINED_NUMERATOR`       | 2      | Numerator of the part of its regular gas or reservoir a caller keeps at a start |
| `GAS_RETAINED_DENOMINATOR`     | 100    | Denominator of that part                                                         |
| `CALL_STIPEND`                 | 2,300  | Stipend a value-transferring `CALL` or `CALLCODE` adds to the child              |
| `VALUE_TRANSFER_COST`          | 11,300 | Regular gas of a call's value transfer, `CALL_STIPEND` included                  |
| `FRAME_DATA_SHARE_NUMERATOR`   | 98     | Numerator of the frame-budget share ([Resource Limits](resource-limits.md))      |
| `FRAME_DATA_SHARE_DENOMINATOR` | 100    | Denominator of the frame-budget share                                            |

## Rationale

**Why 98/100 instead of 63/64?**
Keeping 2% at each level instead of about 1.56% reduces the gas left at deep call depth fast enough that, at gas limits up to 10 billion, a call stack runs out of gas before the depth limit.
The fraction is the one MiniRex introduced and Rex extended to every call opcode.

**Why is the stipend outside the cap?**
The 2,300 stipend lets a callee reached through a value transfer run a minimal `receive()` hook whatever its caller forwards.
The value-transfer cost of 11,300 already pays for it, so adding it after the cap neither takes it from the caller twice nor lets a caller raise its forward above the cap with it.

**Why is the reservoir off the gas argument?**
EIP-8037 passes the whole reservoir to a child because a hard-coded gas argument chosen for regular gas would otherwise starve a callee of state gas, at MegaETH's state prices by orders of magnitude.
Satin keeps the gas argument off the reservoir and keeps 2/100 of it on the caller, the same fraction as the regular forward, so a caller that catches a limit stop below it still has something to carry on with.

**Why two different 98/100 rules?**
The regular forward and the reservoir share use EIP-150's subtraction, the form the inherited forwarding rule has, so a caller with little gas left forwards all of it; the frame budgets of the resource limits use a multiplication rounded down, so a frame budget never rounds up past 98/100 of its parent's.
They agree on most values and differ only at small remainders; both are specified so that no node approximates one with the other.

## Security Considerations

- If a node forwarded more than `forwarded_gas_cap`, enough regular gas would survive at deep call depth to sustain a call-depth denial-of-service at MegaETH's block gas limits.
- A contract ported from Ethereum that infers a starved call from the gas it has left after the call — `gasleft() < gasInitial / 64`, or `< gasRequested / 63` — cannot rely on that check on MegaETH.
  Its thresholds come from EIP-150's 63/64 rule, while a caller here keeps 2/100 of the regular gas it has at the point of `SATIN-FWD-002`, more than 1/64; whether the check fires then depends on where `gasInitial` was measured, on the charges made between that point and the forward and after it (the start's records' history gas, `SATIN-HIST-009`), and on how far the request exceeds what the caller can forward.
  So a starved call can pass the check, and the check can fire for a call that received all it asked for.
  With no reservoir, and each callee spending all it was given: a caller with 1,000,000 of regular gas at the forward that requests 990,000 forwards 980,000, less than it asked, and keeps 20,000, above 990,000 / 63, so the starved call passes; one with 100,000 that requests 1,000,000 forwards 98,000 and keeps 2,000, below 1,000,000 / 63, so the check fires; one with 1,000,000 that requests 980,000 forwards all of it and keeps 20,000, but a start that makes two records then charges it 7,040 of history gas and it keeps 12,960, below 980,000 / 63, so the check fires for a call that was not starved.
  The 2/100 a caller keeps has held since MiniRex; Satin adds the history charge after the forward, and its give-back rule neither causes nor cures any of this ([Two-Pool Gas](gas-model.md)).
- If the stipend were taken from the caller's remaining gas, or added before the cap, a value call's caller would keep less than the rule allows, or a caller could forward more than the cap.
- If the reservoir share were bounded by the gas argument, a callee with a hard-coded gas argument could not pay for the state it creates, and a contract written for one gas pool would fail calls its pool could pay.
- If a system call kept its whole reservoir from its children, a pre-block call's callee could not pay the state gas of the slots it writes.

## Spec History

- [Satin](../../upgrades/satin.md) — Kept the Rex6 98/100 forwarding rule and the value-transfer stipend of [Gas Forwarding](../../evm/gas-forwarding.md), applied to regular gas, added the 98/100 reservoir share, and replaced the storage gas stipend with the history allowance.
