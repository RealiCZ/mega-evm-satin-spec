---
description: Satin (unstable) — Resource Limits. The three limited dimensions (data size, KV updates, state growth) per transaction and per frame, how frame budgets are derived, clamped and merged, the order in which one operation is held to them, how a frame start is held, and the rule that the limits are protocol values of the spec.
spec: Satin
maturity: unstable
---

# Resource Limits

{% hint style="warning" %}
**Unstable** — Satin is under active development: every value and rule on this page may change before Satin is frozen.
{% endhint %}

Abstract: A transaction is limited in three [resource dimensions](../../glossary.md#resource-dimension) — data size, KV updates and state growth — and every [call frame](../../glossary.md#call-frame) has a budget in each, 98/100 of what its caller has left; this page specifies the limits, the budgets, the signed nets they are held against, the order in which one operation is held to them, and when a frame start is held.

## Motivation

Gas prices what a transaction consumes, but it does not bound what a block must carry: at the minimum bucket 1,000 fresh slots cost 97,920,000 state gas, which a transaction above the execution cap can pay, and a transaction can append megabytes of logs if its gas limit allows.
A node that executes, stores and serves blocks within a fixed time needs a hard bound on the bytes a transaction appends, on the state entries it changes and on the state it adds, whatever its gas limit.

A bound held only on the transaction lets a callee take the transaction to the limit and leave its caller nothing to carry on with: once a caller can catch a callee's stop ([Limit Stops](limit-stops.md)), a callee that used up the whole limit would make the catch pointless.
And a limit that differs between chains, or that a node is handed with a block, makes the same block valid on one node and invalid on another.

## Specification

### The three dimensions

- `SATIN-LIM-001` A node MUST limit every transaction in three dimensions, each with a transaction limit and a frame budget:

  | Dimension    | Counted in                                                     | Kind | Transaction limit       | Frame budget |
  | ------------ | -------------------------------------------------------------- | ---- | ----------------------- | ------------ |
  | Data size    | Bytes of the data-size items ([Resource Accounting](resource-accounting.md)) | 0    | `TX_DATA_LIMIT`         | Yes          |
  | KV updates   | [Write records](../../glossary.md#write-record)                | 1    | `TX_KV_UPDATE_LIMIT`    | Yes          |
  | State growth | New accounts and new storage slots                             | 3    | `TX_STATE_GROWTH_LIMIT` | Yes          |

  The kind is the discriminant a stop in that dimension carries ([Limit Stops](limit-stops.md)).
  Compute is not a fourth limit: it is regular gas, bounded by the execution cap ([Two-Pool Gas](gas-model.md)) and by [gas detention](gas-detention.md), whose stops carry kind 2.
  A system-originated transaction and a system call are not held to these limits, and still have their usage counted ([Mega System Transactions and the Protocol's Own Transactions](../system-contracts/system-tx.md)).
- `SATIN-LIM-009` A node MUST NOT hold a frame to any per-frame cap other than its frame budgets in these three dimensions and the regular gas it was forwarded.

### Frame budgets

- `SATIN-LIM-002` The transaction's own frame MUST receive, in each dimension, what the transaction has left once the body and the counts made before the first frame are counted (`SATIN-LIM-005`).
  A creation transaction's own frame is that frame, not a child: it receives the whole of what the transaction has left.
- `SATIN-LIM-003` Every child frame MUST receive, in each dimension,

  `budget = parent_remaining × FRAME_DATA_SHARE_NUMERATOR / FRAME_DATA_SHARE_DENOMINATOR`

  - `parent_remaining` — what the parent has left in that dimension (`SATIN-LIM-004`); the three dimensions share one definition of it.
  - The division rounds down.

  A `CREATE` or `CREATE2` MUST take that share of what the creator has left at the opcode, before the creator's nonce record of `SATIN-LIM-008` is counted.
  A creator that has 1,000 of state growth left, and whose nonce bump adds none, gives the creation a state-growth budget of 980.
- `SATIN-LIM-004` A frame's net in a dimension MUST be signed: what it added, minus what it gave back, plus the nets its successful children merged in.
  A fall of state growth, a write record taken back, or data size given back can make the net negative.
  The frame's remaining MUST be `min(budget, max(0, budget − net))`: it stays inside the budget the frame was given when the net is negative, so a negative net never raises what the frame passes to a child.
  A frame with a state-growth budget of 1,000 that has added 100 has 900 left, and the child it starts receives 882; if that child removes those 100, its net is −100 and its remaining stays 882, so the frame it starts receives 864.
- `SATIN-LIM-005` The transaction's net in a dimension MUST be what is counted on no frame — the body, the applied authorities' records ([EIP-7702 Authorizations Before the First Frame](authorizations.md)), the caller account a deposit creates ([Deposit Transactions](../block/deposits.md)), and every admitted Oracle hint ([Oracle](../system-contracts/oracle.md)) — plus the net of every frame on the stack, a frame's net including a child's only once that child succeeded and merged.
  The transaction's remaining MUST be `min(limit, max(0, limit − net))`, with `limit` the transaction limit of the dimension.
- `SATIN-LIM-006` When a frame succeeds, its signed net MUST merge into its caller's net, and the caller's remaining MUST be computed again from the caller's own budget; the merge can raise the caller's remaining up to that budget.
  After the child of `SATIN-LIM-004` succeeds, its caller's net is 0 and its remaining is again 1,000, so a later child receives 980.
  When a frame fails, its net MUST be discarded and its caller's net is unchanged; the credits inside the failed frame are discarded with it, the state-gas refill, the write-record takeback and the code's data size and history gas of a same-transaction destruction included ([SELFDESTRUCT and the Destruction Table](selfdestruct.md)).
  A fall with no earlier rise leaves the frame's remaining at its budget; later rises may consume that fall, and the kept net still cannot pass the budget.
- `SATIN-LIM-007` The KV-update and state-growth counts a transaction reports MUST each be `max(net, 0)` of the transaction's net in that dimension at its end.
- `SATIN-LIM-008` A creator's nonce record, and the creator's state growth when the bump creates the creator's account (as a keyless signer's bump can), MUST be counted on the creator once the creation returned with the nonce bumped, MUST be held to the creator's budget and not the creation's, and MUST survive the creation's failure.
  The created account's write record and its state growth are the creation's own, held to the creation's budget.

### Order at one site

- `SATIN-LIM-010` At a completed write or a decided frame start, an operation that crosses more than one of data size (kind 0), KV updates (kind 1) and state growth (kind 3) MUST stop on the first of those three, in that order.
  Compute (kind 2) MUST be decided at the regular charge, before the write is counted: a regular charge that crosses gas detention means the opcode does not complete, so its data size, KV updates and state growth are not counted, and kind 2 is the stop.
  A call to a precompile whose price crosses gas detention is decided from the price before its value moves, and is held to the price alone (`SATIN-DET-022`, [Gas Detention](gas-detention.md)).
- `SATIN-LIM-011` Within one dimension the frame budget MUST be tested before the transaction limit.
  When the frame budget is crossed, the stop MUST name that budget, its `limit` being that budget, also when the transaction limit of the same dimension is crossed too.
  When the frame budget is not crossed — no budget applies, or the frame's own budget still holds the write — a crossing of the transaction limit MUST name that limit, its `limit` being the transaction limit.
- `SATIN-LIM-012` A node MUST NOT hold an Oracle hint's bytes, which are counted on the transaction and on no frame, or the authorization list, which is decided before the first frame, to any frame budget.
  A framed write can therefore cross the transaction's data-size limit alone, after hints used what the transaction had left, while its frame's budget still holds it; the stop then names the transaction limit, and the admitted hint bytes stay counted.
  A framed write of KV updates or of state growth cannot cross the transaction limit without crossing its frame budget, since once a frame runs those dimensions have no usage that sits on no frame.

### Frame starts

- `SATIN-LIM-013` A frame start MUST be held to the limits once it is decided — once the value moved and, for a creation, the creator's nonce was bumped and the created account made — and MUST be held to what the start kept: the write records, the state growth and the transfer log of the accounts it changed ([Resource Accounting](resource-accounting.md), [EIP-7708 Transfer Logs](transfer-logs.md)).
  A start that crosses is stopped before the frame runs an instruction ([Limit Stops](limit-stops.md)).
- `SATIN-LIM-014` A start answered with a failure — a precompile that fails after its value moved — kept nothing, its failure taking back the value and the transfer log: it MUST count nothing and MUST NOT be stopped by a limit, and its result is the precompile's failure, which consumes the gas forwarded to it.
- `SATIN-LIM-015` A start the caller's account refuses — a value the caller cannot fund, a creation whose creator nonce cannot be bumped — MUST count nothing, MUST be stopped by no limit, and MUST be charged nothing at its opcode ([History Gas and the History Allowance](history-gas.md)).
  A creation transaction whose sender's nonce cannot be bumped MUST likewise create nothing: its own frame starts no creation, counts nothing, is stopped by no limit, and the transaction succeeds without a created account ([Deposit Transactions](../block/deposits.md) for a deposit).
- `SATIN-LIM-016` A creation onto an occupied address ([SELFDESTRUCT and the Destruction Table](selfdestruct.md)) fails on the collision after its creator's nonce was bumped, and MUST NOT be stopped for what its start would count: its failure discards the created account's record and its transfer log, and the creator's nonce record, which survives it, MUST be counted on the creator when the creation returns (`SATIN-LIM-008`).
  The created account was not new, so the collision adds no state growth.

### The limits are protocol values

- `SATIN-LIM-017` The transaction limits of `SATIN-LIM-001`, the frame share of `SATIN-LIM-003`, the detention caps ([Gas Detention](gas-detention.md)) and the block's data-size, KV and state-growth limits ([Block Limits and Packing](../block/block-limits.md)) are protocol values of the spec, the same on every chain.
  A node MUST hold every transaction and block it executes or validates to them, and MUST NOT take them from a chain configuration or from values handed with a block.
  How a node executes a call, a gas estimate or a simulation outside a block is outside this specification.

### Retired ids

- `SATIN-LIM-018` Retired: removed. The expectation that an execution outside a block uses the same limits and caps is node documentation, not a rule of block execution.

## Constants

| Constant                       | Value      | Description                                                          |
| ------------------------------ | ---------- | -------------------------------------------------------------------- |
| `TX_DATA_LIMIT`                | 13,107,200 | Data-size limit of one transaction, in bytes                         |
| `TX_KV_UPDATE_LIMIT`           | 500,000    | KV-update limit of one transaction, in write records                 |
| `TX_STATE_GROWTH_LIMIT`        | 1,000      | State-growth limit of one transaction, in new accounts and new slots |
| `FRAME_DATA_SHARE_NUMERATOR`   | 98         | Numerator of the share of its parent's remaining a child receives    |
| `FRAME_DATA_SHARE_DENOMINATOR` | 100        | Denominator of that share                                            |

## Rationale

**Why no compute limit among the resource limits?**
Satin pays computation in regular gas, which the execution cap bounds per transaction; a separate compute dimension would count every regular charge a second time.
Gas detention still bounds computation after a read of volatile data, as a limit of its own with its own stop kind.

**Why frame budgets?**
A child receives 98/100 of its caller's regular gas and of its reservoir, and state and history gas draw the reservoir first, so the gas forward alone does not bound what a child can append.
Without a frame budget a callee could take the transaction to a limit and leave its caller, which can catch the stop, nothing to carry on with; 98/100 keeps a caller's own work within reach of what it calls, the same fraction as gas forwarding.

**Why signed nets clamped at the budget?**
A child may remove state its caller added, and a write record taken back or a slot cleared must give its room back, or a transaction that writes and restores could be stopped for writes it does not keep.
Clamping the remaining at the budget keeps a negative net from enlarging what a frame passes on, so a budget can never exceed 98/100 of its parent's.

**Why this order across dimensions?**
Data size, KV updates, state growth is the order Rex6 checks, so a decoder that names the first crossed dimension names the same one under Satin; compute is decided earlier, at the charge, because a write whose charge cannot be paid never happens.

**Why protocol values rather than configuration?**
A limit is part of what makes a block valid; if a chain's configuration or a block's inputs carried it, two nodes could validate the same block differently.
A later spec that changes a limit states its own value.

**Why is execution outside a block left to nodes?**
A call or gas estimate is not part of the chain, and a node may run it under other limits as its own policy; only block execution and validation decide what the chain holds.

## Security Considerations

- If a node held a frame only to the transaction limit, a callee could exhaust a limit and leave the caller that catches the stop no room, so a contract could not protect its own work from what it calls.
- If a negative net raised a frame's remaining above its budget, a callee could undo its caller's state to inflate the budgets of the frames it starts, and a transaction could keep more than the frame shares allow along one path.
- If the creator's nonce record were held to the creation's budget, a creation that fails would leave a record counted against nothing; if it did not survive the failure, a transaction could bump nonces without counting them.
- If a node took the limits from configuration, a block valid on one node would be invalid on another.
- This page preserves the invariant that a transaction never keeps more data size, KV updates or state growth than its limits, and that no frame keeps more than its budget.

## Spec History

- [Satin](../../upgrades/satin.md) — Replaced the Rex6 [Resource Limits](../../evm/resource-limits.md), which had a fourth compute dimension and halted on usage outside every frame's budget, with three dimensions whose every crossing stops the crossing frame, signed nets clamped at the frame budget, and limits fixed as protocol values.
