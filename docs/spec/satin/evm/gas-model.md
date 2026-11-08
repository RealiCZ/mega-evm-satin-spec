---
description: Satin (unstable) — Two-Pool Gas. EIP-8037's regular gas and state-gas reservoir in Satin's profile, the 200,000,000 execution cap, the three kinds of charge, how frames receive, return and give back the reservoir, the transaction's settlement and its three gas ledgers.
spec: Satin
maturity: unstable
---

# Two-Pool Gas

{% hint style="warning" %}
**Unstable** — Satin is under active development: every value and rule on this page may change before Satin is frozen.
{% endhint %}

Abstract: A transaction's gas is split into two pools, a regular-gas budget held under the [execution cap](../../glossary.md#execution-cap) and a state-gas [reservoir](../../glossary.md#reservoir) that holds the rest of its gas limit; this page specifies how each kind of charge draws the pools, how frames receive and return the reservoir, and how a transaction settles its spend on three ledgers.

## Motivation

On a single gas pool, the gas a transaction raises its limit by to pay for new state is also gas it can spend on computation.
MegaETH's state is priced far above Ethereum's, so a transaction that creates a few thousand slots needs a gas limit of hundreds of millions, and every unit of it could be spent on computation unless a second, separate ledger counts computation and stops it.
That second ledger, a compute-gas limit kept beside the gas pool, made every opcode's cost appear twice, made `GAS` report gas the transaction could not compute with, and halted a transaction whose intrinsic usage alone crossed it.

A single pool also lets a hard-coded gas argument starve a callee: a contract that forwards 30,000 gas to a callee that has to pay 97,920 for one fresh slot fails a call that a separate state budget would have funded.
And the bytes a transaction appends to the chain's history (its body, logs, write records and deployed code) cost every node storage and bandwidth without being state, so neither computation's nor state's price fits them.

## Specification

### EIP-8037 and its profile

- `SATIN-POOL-001` A node MUST apply [EIP-8037](https://eips.ethereum.org/EIPS/eip-8037) as of [commit `c406bdb2ff`](https://github.com/ethereum/EIPs/commit/c406bdb2ffbf2fbf9d85698e97b3b2e8b6e79112) (4 September 2026), with the parameters this page and [State Gas and SALT Pricing](state-gas.md) set: the execution cap, and the cost per state byte scaled by the bucket multiplier.
  The rules of the EIP a transaction's outcome depends on are stated on this page and on the pages it links; the EIP is cited for their provenance.
- `SATIN-POOL-002` A node MUST apply these later changes to EIP-8037: the child-merge return of [commit `3ff5cff17a`](https://github.com/ethereum/EIPs/commit/3ff5cff17a11ab31273ee14ebea0df8bbc4f4aef) (4 September 2026), as `SATIN-POOL-012` states it; the failure outcome of [commit `9dcd72754f`](https://github.com/ethereum/EIPs/commit/9dcd72754f3fe4b48a4dbeffee669dc4c60f7ec5) (14 September 2026), as `SATIN-POOL-016` states it; and the collision rule of [commit `dbc6d457cb`](https://github.com/ethereum/EIPs/commit/dbc6d457cbf90d5f9d55552f3fd91d58b88cc898) (18 September 2026), under which a creation does not collide on storage, as [SELFDESTRUCT and the Destruction Table](selfdestruct.md) states it.
- `SATIN-POOL-003` A node MUST NOT apply the transaction gas cap of [commit `d7087803ca`](https://github.com/ethereum/EIPs/commit/d7087803ca236498c73f64665df0ddac7d621950) (14 September 2026): a transaction's gas limit is not capped at `TX_MAX_TOTAL_GAS_LIMIT` and stays bounded by the block's gas limit (see [Base Layer](../base-layer.md)).
  A node MUST NOT apply the commit of the pre-execution spill of [commit `9dcd72754f`](https://github.com/ethereum/EIPs/commit/9dcd72754f3fe4b48a4dbeffee669dc4c60f7ec5): a spill made before the first frame stays outstanding and is unwound by the reservoir the first frame returns (`SATIN-POOL-016`).
- `SATIN-POOL-004` The profile of EIP-8037 a node applies MUST be the one `SATIN-POOL-001` to `SATIN-POOL-003` and `SATIN-POOL-022` define, frozen at [commit `dbc6d457cb`](https://github.com/ethereum/EIPs/commit/dbc6d457cbf90d5f9d55552f3fd91d58b88cc898) (18 September 2026).
  A node MUST NOT apply a change made to EIP-8037 after that commit, whatever the EIP's status becomes; the removal of an unused counter ([commit `052029f362`](https://github.com/ethereum/EIPs/commit/052029f3625328d6f51dec8e62a7090201e66f17)), the co-author lines and the move to Last Call change no rule a transaction executes.
- `SATIN-POOL-022` A node MUST apply these departures from EIP-8037, each specified where it is linked:
  - the reservoir share: a child frame receives `reservoir_share` of the reservoir its caller has left and the caller keeps the rest (`SATIN-POOL-011`), where EIP-8037 passes the whole reservoir;
  - history gas: a history charge draws the reservoir first, shares the spill with state charges, is given back with them when its frame fails, and is booked on a ledger of its own; the history gas of the transaction's body is the intrinsic state gas ([History Gas and the History Allowance](history-gas.md));
  - the destruction-table refill: the first effective `SELFDESTRUCT` of an account created in the same transaction refills the state gas of each part of it absent at the transaction's start ([SELFDESTRUCT and the Destruction Table](selfdestruct.md)), where EIP-8037 specifies that this destruction produces no state-gas refill.

### The two pools

- `SATIN-POOL-005` At the start of a transaction's execution a node MUST split its gas limit into a regular budget and a reservoir:

  ```
  regular_budget = min(gas_limit, EXECUTION_CAP) − intrinsic_regular_gas
  reservoir      = max(0, gas_limit − EXECUTION_CAP)
  ```

  - `gas_limit` — the transaction's gas limit.
  - `EXECUTION_CAP` — the execution cap, the most regular gas one transaction can hold.
  - `intrinsic_regular_gas` — the regular part of the transaction's intrinsic gas ([Gas Schedule and Intrinsic Gas](gas-schedule.md)).

  Validation guarantees that `intrinsic_regular_gas` does not exceed `min(gas_limit, EXECUTION_CAP)` ([Transaction Validation and Refusals](../block/transaction-validation.md)).
- `SATIN-POOL-006` The intrinsic state gas, which is the history gas of the transaction's body ([History Gas and the History Allowance](history-gas.md)), MUST be taken from the reservoir first and only its excess from the regular budget, before the first frame starts.
  The excess taken from the regular budget is outstanding spill of the transaction (`SATIN-POOL-008`).
- `SATIN-POOL-021` A node MUST NOT keep a separate compute-gas limit or ledger.
  Computation is paid in regular gas, bounded by the execution cap and, once a transaction read volatile data, by [gas detention](gas-detention.md).

### Three kinds of charge

- `SATIN-POOL-007` A regular charge — every inherited opcode cost, static or dynamic, and every regular part of the intrinsic gas — MUST draw only the regular gas of the frame that makes it.
  A regular charge the frame's regular gas cannot pay is an out-of-gas of that frame.
- `SATIN-POOL-008` A state charge ([State Gas and SALT Pricing](state-gas.md)) and a history charge ([History Gas and the History Allowance](history-gas.md)) MUST draw the reservoir of the frame that makes it first.
  When the reservoir cannot pay the whole charge, the reservoir MUST be drawn to zero and the rest, the spill, MUST be drawn from the frame's regular gas; a frame whose regular gas cannot pay the spill runs out of gas.
  The spill MUST be added to the frame's _outstanding spill_: the state and history gas its regular gas paid that no give-back or return has yet credited back to it.
  State charges and history charges share one outstanding spill per frame.
- `SATIN-POOL-009` `GAS` MUST push the regular gas the frame has left, and MUST NOT include the reservoir.

A give-back of state or history gas inside a frame follows the refill order of [History Gas and the History Allowance](history-gas.md): the frame's regular gas first, up to its outstanding spill, and the rest to its reservoir.

### Frames

- `SATIN-POOL-010` The transaction's own frame MUST receive the whole reservoir left once the intrinsic state gas and the charges made before the first frame are paid, and a system call's outermost frame MUST receive the whole reservoir of the system call ([System Calls and the Pre-Block Sequence](../block/system-calls.md)).
- `SATIN-POOL-011` A child frame started by `CALL`, `CALLCODE`, `DELEGATECALL`, `STATICCALL`, `CREATE` or `CREATE2`, and the creation a keyless deployment starts ([KeylessDeploy](../system-contracts/keyless-deploy.md)), MUST receive

  `reservoir_share = remaining − remaining × GAS_RETAINED_NUMERATOR / GAS_RETAINED_DENOMINATOR`

  - `remaining` — the reservoir the caller has left after every charge the caller makes for that start, the history of the start's records included ([History Gas and the History Allowance](history-gas.md)).
  - The division is integer division, truncating toward zero.

  The caller MUST keep `remaining − reservoir_share`.
  The regular gas the caller asks to forward MUST NOT bound `reservoir_share`: a start that forwards no regular gas still receives the share ([Gas Forwarding](gas-forwarding.md)).
- `SATIN-POOL-012` When a start returns — whether it was answered without building a frame (a precompile, a call to an account with no code, an interceptor's answer) or a built frame returned — the reservoir the child returns MUST first unwind the caller's outstanding spill, and the rest MUST join the reservoir the caller kept:

  ```
  d = min(returned_reservoir, caller_outstanding_spill)
  caller_regular_gas      += d
  caller_outstanding_spill −= d
  caller_reservoir        += returned_reservoir − d
  ```

  - `returned_reservoir` — the reservoir the child holds when it returns, after its own rollback when it failed (`SATIN-POOL-014`).
  - `caller_outstanding_spill` — the caller's outstanding spill, after `SATIN-POOL-013` has applied.

  The reservoir the caller kept at the start MUST NOT be drawn to unwind its spill.
  When the caller has no outstanding spill, the caller holds the reservoir it had after the charges it made for the start plus the returned reservoir.
- `SATIN-POOL-013` When the child succeeded, its outstanding spill MUST be added to the caller's outstanding spill before `SATIN-POOL-012` applies.
  When the child reverted or halted, its outstanding spill MUST NOT be added: its rollback already credited that spill to the regular gas it returns, and a halt consumes it.
- `SATIN-POOL-014` When a frame reverts or halts, the state and history charges it made, and those its successful children merged into it, MUST be given back as EIP-8037 specifies: the part the reservoir paid returns to the reservoir, so the frame's reservoir is again the reservoir it received when it started, and the part that spilled returns to the frame's regular gas, its outstanding spill becoming zero.
  A revert then returns the frame's unspent regular gas, that returned spill included, to its caller; an exceptional halt consumes the frame's regular gas, that returned spill included.
  A failed child therefore returns the reservoir share it was given, however its start was answered.
- `SATIN-POOL-015` When a start for which the caller charged an account leaf's state gas — a value `CALL` to an account that is empty under EIP-161, or a `CREATE` or `CREATE2` onto an empty address — returns without that leaf added, because the child failed, the caller MUST be given that charge back after `SATIN-POOL-012` applied, by the refill order of [History Gas and the History Allowance](history-gas.md).
- `SATIN-POOL-016` A state or history charge made for an authority before the first frame ([EIP-7702 Authorizations Before the First Frame](authorizations.md)), and any spill it made, MUST stay outstanding on the transaction when the first frame starts, and the reservoir the first frame returns MUST unwind that spill by `SATIN-POOL-012`, together with any other spill outstanding on the transaction.
  A failure of the first frame MUST NOT return reservoir that such a charge drew: the first frame received the reservoir that charge left, and its rollback restores only that (`SATIN-POOL-014`).

### The transaction

- `SATIN-POOL-017` When a transaction ends, the reservoir left MUST return to the sender, and so MUST the unspent regular gas unless the transaction's own frame halted; this holds when the transaction's own frame reverted and when it was stopped by a limit ([Limit Stops](limit-stops.md)).
  A failed deposit is the exception: it uses its whole gas limit, the reservoir included, and nothing returns ([Deposit Transactions](../block/deposits.md)).
- `SATIN-POOL-018` The receipt's gas used MUST be what the transaction spent from both pools — regular, state and history gas together — after the inherited EIP-3529 refund and the floor rule of `SATIN-POOL-020`.
  When that spend less the refund is below the floor, the gas used MUST be the floor and no refund MUST be made: the sender is returned its gas limit less the floor, the floor's excess over the spend being drawn from the unspent regular gas and the reservoir alike.
- `SATIN-POOL-019` A node MUST split a transaction's gas used into three ledgers, all paid from the two pools:

  | Ledger      | Value                                                     |
  | ----------- | --------------------------------------------------------- |
  | Regular gas | `total − state − history`                                 |
  | State gas   | The state charges the transaction kept                    |
  | History gas | The history charges the transaction kept, its body's included |

  - `total` — the receipt's gas used.
  - `state`, `history` — the state and history charges kept, net of every give-back.

  State or history gas that spilled onto regular gas MUST stay on its own ledger.
  The ledgers of a failed deposit are specified on [Deposit Transactions](../block/deposits.md).
- `SATIN-POOL-020` The EIP-7623 floor, as EIP-7976 and EIP-7981 amend it, MUST be computed and validated as the Amsterdam schedule computes it, from the base and per-byte costs of [Gas Schedule and Intrinsic Gas](gas-schedule.md).
  The figure a block counts on its execution ledger for a transaction MUST be `max(regular, floor)`, with `regular` the transaction's regular-gas ledger, from which history gas is taken out before the floor applies ([Block Limits and Packing](../block/block-limits.md)).
  <!-- pending owner decision: QG-07 the EIP-7623, EIP-7976 and EIP-7981 revisions to pin -->

### Retired ids

None.

## Constants

| Constant                    | Value       | Description                                                                          |
| --------------------------- | ----------- | ------------------------------------------------------------------------------------ |
| `EXECUTION_CAP`             | 200,000,000 | The most regular gas one transaction holds; gas above it is the reservoir             |
| `GAS_RETAINED_NUMERATOR`    | 2           | Numerator of the part of its reservoir a caller keeps at a start                     |
| `GAS_RETAINED_DENOMINATOR`  | 100         | Denominator of the part of its reservoir a caller keeps at a start                   |
| `TX_MAX_TOTAL_GAS_LIMIT`    | 2^32 − 1    | EIP-8037's transaction gas cap, which a node does not apply (`SATIN-POOL-003`)       |

## Rationale

**Why an execution cap with a reservoir above it?**
EIP-8037 separates the gas that pays for computation from the gas that pays for new state.
Splitting the gas limit at 200,000,000, the compute-gas limit Rex6 kept on a separate ledger, keeps that bound on computation while letting a transaction raise its gas limit for state alone.
Satin therefore keeps no compute-gas ledger: the regular budget is the compute bound, `GAS` reports it, and a transaction can no longer cross a compute limit through its intrinsic usage, which Rex6 had to halt.

**Why a reservoir share instead of passing the whole reservoir?**
EIP-8037 passes the whole reservoir to a child so that a hard-coded gas argument cannot starve a callee of state gas.
Satin keeps the gas argument off the reservoir for the same reason, but keeps 2/100 of it on the caller, as gas forwarding keeps 2/100 of regular gas: a callee that spends its whole share still leaves its caller something to carry on with, which matters because a caller can catch a limit stop below it ([Limit Stops](limit-stops.md)).

**Why the child-merge return as the reference implementation performs it?**
The return unwinds the caller's spill before the rest joins the reservoir, so state gas the caller paid out of regular gas comes back as regular gas once a child returns reservoir it did not need.
Drawing only the returned reservoir, never the part the caller kept, keeps the caller's retained share intact, which the share exists for.

**Why does history gas share the reservoir and the spill?**
The bytes a transaction appends to history are paid like new state: they are not computation, so they should not consume the execution cap first, and a callee forwarded little regular gas should still be able to log.
Sharing one outstanding spill keeps a single refill order for every give-back, so a give-back of either kind cancels its charge exactly.

**Why freeze the profile at a commit?**
EIP-8037 is a draft that kept changing while Satin was written.
A node executing Satin must execute the same rules years later, so Satin names the commits it takes and declines and treats any later change to the EIP as an input to a later spec.

**Why not the pre-execution spill commit of `9dcd72754f`?**
Committing the spill made before the first frame would keep the first frame's returned reservoir from unwinding it, so an authority charge paid from regular gas would stay paid from regular gas even when the transaction's own frame returned reservoir it did not use.

## Security Considerations

- If `GAS` or the forward included the reservoir, a transaction with a gas limit above the execution cap could compute past `EXECUTION_CAP`, and gas detention's bound on computation would not hold.
- If a regular charge could draw the reservoir, a transaction could buy computation at a gas limit priced for state; the invariant is that the regular charges a transaction makes never exceed the regular budget it started with, since the reservoir reaches regular gas only by unwinding spill that state or history charges took from it.
- If the child-merge return drew the reservoir a caller kept, a callee could drain its caller's retained share through a spill of the caller, and a caller catching a stop below it could be left unable to carry on.
- If a failed frame's state and history charges were not given back, a callee could make its caller pay for state the callee's revert discarded; if a halt did not consume the returned spill, a halting frame would refund regular gas a halt must consume.
- If a node applied a later revision of EIP-8037, it would execute a different chain from a node that applies the frozen profile.

## Spec History

- [Satin](../../upgrades/satin.md) — Replaced the Rex6 [Dual Gas Model](../../evm/dual-gas-model.md) and the [compute-gas ledger](../../evm/compute-gas.md) with EIP-8037 regular gas and a state-gas reservoir under a 200,000,000 execution cap, three gas ledgers, and a 98/100 reservoir share for child frames.
