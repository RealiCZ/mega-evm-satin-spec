---
description: Satin (unstable) — Resource Limits. Stub of the Satin specification: the rules this page will specify.
spec: Satin
maturity: unstable
---

# Resource Limits

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
This page is a stub. It lists what the page will specify; the specification text is written after the outline is reviewed.
{% endhint %}

Abstract: The three limited dimensions (data size, KV updates, state growth) per transaction and per frame, how frame budgets are derived and merged, the order in which one operation is held to them, and the rule that the limits are fixed per spec.

## Specification

The rules this page will specify, by their proposed ids:

- `SATIN-LIM-001` — Three dimensions are limited per transaction, each with a frame budget: data size (bytes of the byte table) TX_DATA_LIMIT = 13,107,200; KV updates (write records) TX_KV_UPDATE_LIMIT = 500,000; state growth (new accounts and slots) TX_STATE_GROWTH_LIMIT = 1,000; compute is not a fourth limit.
- `SATIN-LIM-002` — The transaction's own frame gets what the transaction has left in each dimension once the body and the pre-frame counts are counted.
- `SATIN-LIM-003` — A child gets parent_remaining × FRAME_DATA_SHARE_NUMERATOR (98) / FRAME_DATA_SHARE_DENOMINATOR (100), rounded down, in each of the three dimensions; a CREATE or CREATE2 takes that share at the opcode.
- `SATIN-LIM-004` — A frame's net is signed (added, less given back, plus successful children's nets); its remaining is min(budget, max(0, budget − net)), so a negative net never raises what it forwards.
- `SATIN-LIM-005` — The transaction's net is what sits on no frame (the body, the applied authorities' records, a deposit's caller, every admitted hint) plus the net of every frame on the stack; its remaining is the same clamp against the transaction limit.
- `SATIN-LIM-006` — A successful frame's signed net merges into its caller, whose remaining is computed again from its own budget; a failed frame's net and the credits inside it are discarded.
- `SATIN-LIM-007` — The KV and state-growth counts a transaction reports are max(net, 0).
- `SATIN-LIM-008` — A creator's nonce record, and its state growth when the bump creates the creator, are counted on the creator when the creation returns, held to the creator's budget, and survive the creation's failure; the creation's budget is the share taken before that record.
- `SATIN-LIM-009` — Satin sets no further per-frame cap.
- `SATIN-LIM-010` — At one completed write or decided frame start, an operation crossing several dimensions stops on the first of data size (kind 0), KV updates (kind 1), state growth (kind 3); compute (kind 2) is decided at the regular charge, before the write is counted.
- `SATIN-LIM-011` — Within a dimension the frame budget is tested before the transaction limit: a crossed budget names the budget, otherwise a crossed transaction limit names that limit.
- `SATIN-LIM-012` — No frame budget applies to an Oracle hint's bytes or to the authorization list; a framed write can cross the transaction's data-size limit alone after hints used it; KV and growth cannot cross the transaction limit without crossing the frame budget.
- `SATIN-LIM-013` — A frame start is held to the limits once it is decided (the value moved; for a creation the nonce bumped and the account made), to what the start kept: its records, its state growth, its transfer log.
- `SATIN-LIM-014` — A start answered with a failure (a precompile that fails after its value moved) counts nothing and is not stopped.
- `SATIN-LIM-015` — A start the caller's account refuses (a value it cannot fund, a creator nonce that cannot be bumped) counts nothing, is stopped by no limit and is charged nothing.
- `SATIN-LIM-016` — A creation onto an occupied address is not stopped for what its start would count; the creator's surviving nonce record is counted on the creator; the collision adds no state growth.
- `SATIN-LIM-017` — The transaction limits, the frame share, the detention caps and the block budgets are protocol values of the spec, the same on every chain, never chain configuration or values handed with a block.
- `SATIN-LIM-018` — An execution outside a block (a call, a gas estimate, a simulation) is expected to use the same per-transaction limits and caps; a node that does not acts on its own policy and keeps eth_call and eth_estimateGas consistent.

## Spec History

- [Satin](../../upgrades/satin.md) — The reviewers' delta of Satin against Rex6.
