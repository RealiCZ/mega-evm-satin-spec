---
description: Satin (unstable) — MegaLimitControl. The remainingComputeGas() query: what it answers once compute is regular gas and gas detention withholds gas.
spec: Satin
maturity: unstable
---

# MegaLimitControl

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
{% endhint %}

Abstract: The MegaLimitControl system contract and its one intercepted method, `remainingComputeGas()`, which answers how much regular gas the calling frame may still spend, given its own gas and any limit gas detention set.

## Motivation

A frame's `GAS` reads its whole regular gas, withheld part included (see [Gas Detention](../evm/gas-detention.md)), so after a read of volatile data it no longer tells the frame how much it may spend before the compute limit stops it.
A contract that batches work until a threshold, or decides whether to attempt a costly call, needs that figure; without a defined answer it would guess, and two nodes answering differently would steer the same contract down different paths.

## Specification

- `SATIN-MLC-001` MegaLimitControl MUST be the account at `MEGA_LIMIT_CONTROL_ADDRESS` holding the code `MEGA_LIMIT_CONTROL_CODE_HASH` (see [System Contracts](overview.md)), whose interface is:

```solidity
interface IMegaLimitControl {
    error NotIntercepted();
    error NonZeroTransfer();

    function remainingComputeGas() external view returns (uint64 remaining);
}
```

  `remainingComputeGas()` is intercepted for a `CALL` or a `STATICCALL`, under the rules of [Call Interception](interception.md), a value-bearing call answered with `NonZeroTransfer()`; a `DELEGATECALL` or `CALLCODE`, and any other selector, run the bytecode, whose fallback reverts with `NotIntercepted()`.
- `SATIN-MLC-002` `remainingComputeGas()` MUST return, ABI-encoded as a `uint64`, `remaining = min(own, allowance)`, read when the call reaches the interceptor, where:
  - `own` is the calling frame's own regular gas after the call deducted its forward, plus the gas the call forwarded, counted back;
  - `allowance` is, once a read of volatile data set a compute limit for the transaction, what that limit leaves the transaction at the start of the call's frame (`limit − compute`, zero once the compute is past the limit; see [Gas Detention](../evm/gas-detention.md)), and is absent, leaving `remaining = own`, while no limit is set.
- `SATIN-MLC-003` The answer MUST count regular gas only: the reservoir is not part of it, so a transaction whose gas limit is above the execution cap hears at most the regular gas the execution cap leaves it.
- `SATIN-MLC-004` A transaction that calls the contract directly has no calling frame: `own` is the gas its own frame was given, so it MUST hear its own frame's regular gas, or less when it is detained from its start (its sender is the block beneficiary, or an EIP-7702 authority it applies is).

## Constants

| Constant                       | Value                                                                | Description                      |
| ------------------------------ | -------------------------------------------------------------------- | -------------------------------- |
| `MEGA_LIMIT_CONTROL_ADDRESS`   | `0x6342000000000000000000000000000000000005`                         | MegaLimitControl                 |
| `MEGA_LIMIT_CONTROL_CODE_HASH` | `0x3927f2a4803c5e18153ff5742d0fa1acd9ad04538e4e6037cb4a9b28694ca87f` | MegaLimitControl version 1.0.0   |

## Rationale

**Why count the forward back?**
The call forwards gas to MegaLimitControl only to ask it; the answer spends none of it and returns it whole, so the caller can still spend it after the call returns.
Counting it back answers what the caller has, not what it has while the call is in flight.

**Why regular gas only?**
Compute is regular gas; the reservoir pays only state and history gas, and a frame cannot spend it on computation, so including it would overstate what the frame can compute.

**Why one figure?**
A contract needs one number — how much it can still spend — and the lesser of the two is the only one that predicts when it will be stopped.
Rex6 answered the lesser of a per-frame compute budget and the detained transaction limit; Satin has no compute-gas budget beyond regular gas and detention, and Rex6's per-frame budget could report more compute than a child forwarded little gas can pay for, so the answer is now bounded by the caller's own regular gas.

## Security Considerations

- A node that answered the whole regular gas, withheld part included, would let a contract plan work the compute limit then stops, changing its control flow against every other node.
- The answer depends on the gas the call forwarded; a node that answered before counting it back would report the caller less than it has.

## Spec History

- [Rex4](../../upgrades/rex4.md) — Introduced MegaLimitControl.
- [Rex6](../../upgrades/rex6.md) — The Rex6 query is specified in [MegaLimitControl](../../system-contracts/mega-limit-control.md).
- [Satin](../../upgrades/satin.md) — The answer is regular gas, bounded by detention's allowance.
