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
- `SATIN-POOL-002` A node MUST apply these later changes to EIP-8037: the collision rule of [commit `dbc6d457cb`](https://github.com/ethereum/EIPs/commit/dbc6d457cbf90d5f9d55552f3fd91d58b88cc898) (18 September 2026), under which a creation does not collide on storage, as [SELFDESTRUCT and the Destruction Table](selfdestruct.md) states it; and, of the child-merge return of [commit `3ff5cff17a`](https://github.com/ethereum/EIPs/commit/3ff5cff17a11ab31273ee14ebea0df8bbc4f4aef) (4 September 2026) and the failure outcome of [commit `9dcd72754f`](https://github.com/ethereum/EIPs/commit/9dcd72754f3fe4b48a4dbeffee669dc4c60f7ec5) (14 September 2026), what the give-back rule of `SATIN-POOL-022` leaves of them: a returned reservoir joins the reservoir its caller kept and never draws it (`SATIN-POOL-012`), and a failure of the transaction's own frame returns no reservoir that a charge made before that frame drew (`SATIN-POOL-024`).
- `SATIN-POOL-003` A node MUST NOT apply the transaction gas cap of [commit `d7087803ca`](https://github.com/ethereum/EIPs/commit/d7087803ca236498c73f64665df0ddac7d621950) (14 September 2026): a transaction's gas limit is not capped at `TX_MAX_TOTAL_GAS_LIMIT` and stays bounded by the block's gas limit (see [Base Layer](../base-layer.md)).
  A node MUST NOT apply the commit of the pre-execution spill of [commit `9dcd72754f`](https://github.com/ethereum/EIPs/commit/9dcd72754f3fe4b48a4dbeffee669dc4c60f7ec5) as a rule of its own: under the give-back rule of `SATIN-POOL-022` the part of any charge that regular gas paid stays spent, a charge made before the first frame included (`SATIN-POOL-024`).
- `SATIN-POOL-004` The profile of EIP-8037 a node applies MUST be the one `SATIN-POOL-001` to `SATIN-POOL-003` and `SATIN-POOL-022` define, frozen at [commit `dbc6d457cb`](https://github.com/ethereum/EIPs/commit/dbc6d457cbf90d5f9d55552f3fd91d58b88cc898) (18 September 2026).
  The give-back rule and the legacy share of `SATIN-POOL-022` are departures from that commit, made in Satin's own words, and not the adoption of a later revision.
  A node MUST NOT apply a change made to EIP-8037 after that commit, whatever the EIP's status becomes; the removal of an unused counter ([commit `052029f362`](https://github.com/ethereum/EIPs/commit/052029f3625328d6f51dec8e62a7090201e66f17)), the co-author lines and the move to Last Call change no rule a transaction executes.
- `SATIN-POOL-022` A node MUST apply these departures from EIP-8037, each specified where it is linked:
  - the reservoir share: a child frame receives `reservoir_share` of the reservoir its caller has left and the caller keeps the rest (`SATIN-POOL-011`), where EIP-8037 passes the whole reservoir;
  - history gas: a history charge draws the reservoir first and the frame's regular gas for the rest, is given back as a state charge is, into a reservoir, and is booked on a ledger of its own; the history gas of the transaction's body is the intrinsic state gas ([History Gas and the History Allowance](history-gas.md));
  - the destruction-table refill: the first effective `SELFDESTRUCT` of an account created in the same transaction refills the state gas of each part of it absent at the transaction's start ([SELFDESTRUCT and the Destruction Table](selfdestruct.md)), where EIP-8037 specifies that this destruction produces no state-gas refill;
  - the give-back rule: every give-back of state or history gas credits a reservoir and never regular gas, so a frame's regular gas never rises within the frame but by the unused regular gas a child returns (`SATIN-HIST-012`, `SATIN-POOL-012`, `SATIN-POOL-014`), where EIP-8037 at that commit credits a refill to regular gas first, up to the state gas the frame's regular gas paid (its outstanding spill, in last-in, first-out order), unwinds that spill when a child returns reservoir, and returns it to regular gas when the frame reverts;
  - the legacy share: a state charge an opcode makes for a new slot, a new account or a created account takes the part of it its pre-Satin price exceeds the charge's regular cost from regular gas first, before the reservoir pays (`SATIN-STATE-012`).

  The last two follow the rule [ethereum/EIPs#12581](https://github.com/ethereum/EIPs/pull/12581) proposes for EIP-8037 (head `2ba9176f` when read, not merged), restated here in Satin's own words; the pull request is their provenance, not a rule of this specification.

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
  The excess taken from the regular budget is spent, as every part of a state or history charge that regular gas pays is (`SATIN-POOL-008`).
- `SATIN-POOL-021` A node MUST NOT keep a separate compute-gas limit or ledger.
  Computation is paid in regular gas, bounded by the execution cap and, once a transaction read volatile data, by [gas detention](gas-detention.md).

### Three kinds of charge

- `SATIN-POOL-007` A regular charge — every inherited opcode cost, static or dynamic, and every regular part of the intrinsic gas — MUST draw only the regular gas of the frame that makes it.
  A regular charge the frame's regular gas cannot pay is an out-of-gas of that frame.
- `SATIN-POOL-008` A state charge ([State Gas and SALT Pricing](state-gas.md)) and a history charge ([History Gas and the History Allowance](history-gas.md)) MUST draw the pools of the frame that makes it in this order: first the charge's legacy share (`SATIN-STATE-012`), which only a state charge an opcode makes for a new slot, a new account or a created account has, from the frame's regular gas; then the frame's reservoir, until it is zero; then the rest, the spill, from the frame's regular gas.
  A frame whose regular gas cannot pay the legacy share, or the spill, MUST run out of gas, whatever its reservoir holds.
  The part of a state or history charge that regular gas pays is spent: no give-back, no rollback and no return MUST ever credit it to regular gas again (`SATIN-HIST-012`).
- `SATIN-POOL-009` `GAS` MUST push the regular gas the frame has left, and MUST NOT include the reservoir.

A give-back of state or history gas inside a frame credits the reservoir of the frame that makes it, never its regular gas ([History Gas and the History Allowance](history-gas.md), `SATIN-HIST-007`, `SATIN-HIST-012`).
Every pattern of a write and its take-back, with what each ledger does, is listed on [Write and Take-Back Patterns](take-backs.md).

### Frames

- `SATIN-POOL-010` The transaction's own frame MUST receive the whole reservoir left once the intrinsic state gas and the charges made before the first frame are paid, and a system call's outermost frame MUST receive the whole reservoir of the system call ([System Calls and the Pre-Block Sequence](../block/system-calls.md)).
- `SATIN-POOL-011` A child frame started by `CALL`, `CALLCODE`, `DELEGATECALL`, `STATICCALL`, `CREATE` or `CREATE2`, and the creation a keyless deployment starts ([KeylessDeploy](../system-contracts/keyless-deploy.md)), MUST receive

  `reservoir_share = remaining − remaining × GAS_RETAINED_NUMERATOR / GAS_RETAINED_DENOMINATOR`

  - `remaining` — the reservoir the caller has left after every charge the caller makes for that start, the history of the start's records included ([History Gas and the History Allowance](history-gas.md)).
  - The division is integer division, truncating toward zero.

  The caller MUST keep `remaining − reservoir_share`.
  The regular gas the caller asks to forward MUST NOT bound `reservoir_share`: a start that forwards no regular gas still receives the share ([Gas Forwarding](gas-forwarding.md)).
- `SATIN-POOL-012` When a start returns — whether it was answered without building a frame (a precompile, a call to an account with no code, an interceptor's answer) or a built frame returned — the reservoir the child returns MUST join the reservoir the caller kept at the start, `remaining − reservoir_share` (`SATIN-POOL-011`), and the caller's regular gas MUST rise by the regular gas the child returns and by nothing else: the child's unused regular gas after a success, a revert or a stop, and none after an exceptional halt.
  The returned reservoir — the reservoir the child holds when it returns, after its own rollback when it failed (`SATIN-POOL-014`) — MUST NOT be credited to the caller's regular gas.
  A caller with 100 reservoir after the start's charges keeps 2 and gives the child 98; a child that returns all 98 leaves the caller 100, whatever regular gas the caller paid for state before.
- `SATIN-POOL-014` When a frame reverts, or is stopped by a limit, the state and history charges it made, and those its successful children merged into it, net of the give-backs it and they received (`SATIN-HIST-007`), MUST be given back into its own reservoir:

  `reservoir = reservoir + net_charged`

  - `reservoir` — the frame's reservoir when it fails.
  - `net_charged` — the state and history gas charged since the frame started, by the frame and by the children that succeeded and merged into it, legacy shares included, less every give-back they received; it is negative for a frame that took back more than it charged.

  The frame's reservoir is then the reservoir it received when it started plus the part of those charges that regular gas paid, and its unspent regular gas, which does not include that part, returns to its caller (`SATIN-POOL-012`).
  When a frame halts exceptionally, its reservoir MUST become the reservoir it received when it started, and its regular gas, with the part of those charges it paid, is consumed.
  A failed frame's charges therefore never return to regular gas: a revert keeps in the reservoir what regular gas paid for the state and history it undoes, and a halt consumes it.
- `SATIN-POOL-015` When a start for which the caller charged an account leaf's state gas — a value `CALL` to an account that is empty under EIP-161, or a `CREATE` or `CREATE2` onto an address empty under EIP-161 — returns without that leaf added, because the child failed or, for a `CALL`, because the start was refused after the charge (a value the caller cannot fund, a call past the call-depth limit), the caller MUST be given that charge back, its legacy share included, into its reservoir, after the reservoir the child returns joined it (`SATIN-POOL-012`, [History Gas and the History Allowance](history-gas.md)).
  The new-account or created-account state gas charged for the transaction's own frame before it starts (`SATIN-SCHED-008` step 4) MUST likewise be given back into the transaction's reservoir when that frame fails or is stopped, after that frame's rollback, so it returns to the sender at the settlement whether the frame reverted, was stopped or halted.
- `SATIN-POOL-024` A state or history charge made before the first frame — the caller a deposit creates, an authorization's charges ([EIP-7702 Authorizations Before the First Frame](authorizations.md)), the history of the records made outside a frame, the state gas of the first frame's recipient or created account ([Gas Schedule and Intrinsic Gas](gas-schedule.md)) — has no legacy share: it MUST draw the reservoir first and the regular budget for the rest, the part the regular budget pays being spent, and the first frame receives the reservoir it left (`SATIN-POOL-010`).
  A failure of the first frame MUST NOT return reservoir that such a charge drew: that frame's rollback gives it the reservoir it received (`SATIN-POOL-014`), and each such charge is kept or given back by its own rule (`SATIN-AUTH-016`, `SATIN-HIST-005`, `SATIN-POOL-015`).

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

  - `total` — what the transaction spent from both pools, the intrinsic gas included, before the EIP-3529 refund and before the floor of `SATIN-POOL-020`; it is not the receipt's gas used of `SATIN-POOL-018`, which is that spend less the refund and at least the floor.
  - `state`, `history` — the state and history charges kept, net of every give-back.

  The EIP-3529 refund MUST NOT lower any ledger, and the floor MUST NOT raise one: the receipt's gas used and the three ledgers are separate figures.
  A call that clears one cold slot whose original value is not zero, and does nothing else, spends 27,106 regular gas and 30,800 history gas; its refund is `min(11,616, floor(57,906 / 5)) = 11,581`, its receipt's gas used 46,325, and its regular ledger 27,106.
  State or history gas that regular gas paid, a legacy share or a spill, MUST stay on its own ledger.
  The ledgers of a failed deposit are specified on [Deposit Transactions](../block/deposits.md).
- `SATIN-POOL-020` The EIP-7623 floor, as EIP-7976 and EIP-7981 amend it, MUST be computed and validated as the Amsterdam schedule computes it, from the base and per-byte costs of [Gas Schedule and Intrinsic Gas](gas-schedule.md).
  The figure a block counts on its execution ledger for a transaction MUST be `max(regular, floor)`, with `regular` the transaction's regular-gas ledger, from which history gas is taken out before the floor applies ([Block Limits and Packing](../block/block-limits.md)).
  The floor MUST be that of EIP-7623 as of [commit `451cd9e1ec`](https://github.com/ethereum/EIPs/commit/451cd9e1ecb30b19be1c02199760a70d6248e604) (15 May 2025), amended by EIP-7976 and EIP-7981 at the commits of `SATIN-SCHED-001`.

### Retired ids

- `SATIN-POOL-013` Retired: removed. A child's state and history charges are no longer tracked by the pool that paid them, and a returned reservoir joins its caller's without crediting regular gas (`SATIN-POOL-012`).
- `SATIN-POOL-016` Retired: replaced by `SATIN-POOL-024`. Charges made before the first frame are no longer unwound by the reservoir the first frame returns.

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

**Why does no give-back reach regular gas?**
Contracts written for Rex, and for Ethereum before Amsterdam, read the gas left after a failed call to tell a starved call from a logic error, and record a failure for good only when they hold more gas than a starved call could have left them; the check assumes that gas a frame spent does not come back while the transaction runs, and Rex6 never gave storage gas back at all.
EIP-8037 at the pinned commit credits a give-back to regular gas first, up to what regular gas paid: a slot set before a call and cleared after it raises `GAS` by its price, 97,920 × `m` of state gas and 3,520 of history gas for its record, and an intermediary that writes, logs or creates state and then reverts on a deeper failure returns to its caller every state and history charge it and its callees made.
On MegaETH this is the common case: a transaction at or below the 200,000,000 execution cap has no reservoir, so every such charge is paid from regular gas and every give-back would return there, and history gas and the SALT multiplier make the amounts larger than Ethereum's.
Crediting every give-back to a reservoir keeps `GAS` from rising within a frame, and costs the sender nothing: unused reservoir returns at the settlement, so the total paid is the same.
The rule is the one ethereum/EIPs#12581 proposes for EIP-8037; Satin takes it in its own words rather than waiting for the EIP.

**Why does a returned reservoir only join the caller's?**
A reservoir pays state and history, and what is left returns to the sender; turning a returned reservoir into regular gas would let a child's unused state budget, or a revert's kept charges, buy computation in the caller.
Joining only the part the caller kept leaves the caller's retained share intact, which the share exists for.

**Why does history gas share the reservoir?**
The bytes a transaction appends to history are paid like new state: they are not computation, so they should not consume the execution cap first, and a callee forwarded little regular gas should still be able to log.
A history give-back follows the same rule as a state give-back, so a log or a write record a frame undoes never returns to regular gas either.

**Why freeze the profile at a commit?**
EIP-8037 is a draft that kept changing while Satin was written.
A node executing Satin must execute the same rules years later, so Satin names the commits it takes and declines and treats any later change to the EIP as an input to a later spec.

**Why is the pre-execution spill commit of `9dcd72754f` not taken?**
It makes the part of a charge made before the first frame that regular gas paid stay paid; under the give-back rule every part regular gas pays stays paid, so the commit adds nothing of its own.

## Security Considerations

- If `GAS` or the forward included the reservoir, a transaction with a gas limit above the execution cap could compute past `EXECUTION_CAP`, and gas detention's bound on computation would not hold.
- If a regular charge could draw the reservoir, a transaction could buy computation at a gas limit priced for state; the invariant is that the regular charges a transaction makes never exceed the regular budget it started with, and the reservoir never reaches regular gas.
- If a give-back, a rollback or a returned reservoir were credited to regular gas, a frame's `GAS` would rise within the frame by gas spent on state and history: a lock slot cleared after a failed call would refund its price to `GAS`, and an honest intermediary that bubbles a deeper failure with `REVERT` would return everything it spent on state, logs and records, so a contract that records a failure only when enough gas is left after a starved call — safe under Rex6 — would record it for an attacker who starved the call on purpose.
- If a returned reservoir drew the reservoir a caller kept, a callee could drain its caller's retained share, and a caller catching a stop below it could be left unable to carry on.
- If a failed frame's state and history charges were not given back into its reservoir, the sender would pay for state the frame's revert discarded; if a halt kept what regular gas paid for them, a halting frame would keep gas a halt must consume.
- What the give-back rule does not close: after a revert, the failed call's state and history charges sit in its reservoir and return to the caller, so they can still pay the state a failure handler in the caller creates; a sender who adds a reservoir pays a handler's state from it, which the legacy share (`SATIN-STATE-012`) bounds for slots, accounts and created accounts only; and every fixed gas budget written for Rex's prices — a gas argument, a stored per-call limit, a 2,300 stipend — has to be derived again for state creation, which without a reservoir costs about five times as much regular gas at multiplier 1 (a cold fresh slot 113,540, against Rex6's 22,100).
- The cost the rule accepts: a slot set and cleared in a transaction without a reservoir keeps its charge out of regular gas until the transaction ends; the give-back sits in the reservoir of the frame that cleared it, usable only for state and history, and returns to the sender at the settlement.
- If a node applied a later revision of EIP-8037, it would execute a different chain from a node that applies the frozen profile.

## Spec History

- [Satin](../../upgrades/satin.md) — Replaced the Rex6 [Dual Gas Model](../../evm/dual-gas-model.md) and the [compute-gas ledger](../../evm/compute-gas.md) with EIP-8037 regular gas and a state-gas reservoir under a 200,000,000 execution cap, three gas ledgers, and a 98/100 reservoir share for child frames.
