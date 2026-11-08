---
description: Satin (unstable) — Two-Pool Gas. Stub of the Satin specification: the rules this page will specify.
spec: Satin
maturity: unstable
---

# Two-Pool Gas

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
This page is a stub. It lists what the page will specify; the specification text is written after the outline is reviewed.
{% endhint %}

Abstract: EIP-8037's regular gas and state-gas reservoir in Satin's profile: the execution cap, the three kinds of charge, how frames receive and return the reservoir, the transaction's settlement and its three gas ledgers.

## Specification

The rules this page will specify, by their proposed ids:

- `SATIN-POOL-001` — EIP-8037 applies as of commit c406bdb2ff, with Satin's parameters (the execution cap, the cost per state byte scaled by the bucket multiplier).
- `SATIN-POOL-002` — Later EIP-8037 commits taken: the child-merge return (3ff5cff17a) as the reference implementation performs it, the first-frame failure outcome (9dcd72754f), no collision on storage (dbc6d457cb).
- `SATIN-POOL-003` — Later EIP-8037 commits declined: the transaction gas cap (d7087803ca) and the commit of the pre-execution spill (9dcd72754f).
- `SATIN-POOL-004` — Satin's EIP-8037 profile is frozen at commit dbc6d457cb (18 September 2026): a later change to EIP-8037 does not apply under Satin, whatever the EIP's status becomes.
- `SATIN-POOL-005` — The execution cap EXECUTION_CAP = 200,000,000; at the start of execution regular_budget = min(gas_limit, EXECUTION_CAP) − intrinsic_regular_gas and reservoir = max(0, gas_limit − EXECUTION_CAP).
- `SATIN-POOL-006` — The intrinsic state gas (the body's history gas) is taken from the reservoir first and only its excess from the regular budget.
- `SATIN-POOL-007` — A regular charge (every inherited opcode and intrinsic cost) draws only the regular budget.
- `SATIN-POOL-008` — A state charge and a history charge draw the reservoir first and spill onto the regular budget only past it.
- `SATIN-POOL-009` — GAS returns the regular budget the frame has left, not the reservoir.
- `SATIN-POOL-010` — The transaction's own frame and a system call's outermost frame receive the whole reservoir.
- `SATIN-POOL-011` — A child frame of the call opcodes, CREATE, CREATE2 or a keyless deployment receives reservoir_share = remaining − remaining × 2 / 100 of the caller's reservoir after every charge the caller makes for that start; the requested gas does not bound it; the caller keeps the rest.
- `SATIN-POOL-012` — Child-merge return on every start, answered or built: d = min(returned reservoir, caller's outstanding spill); the caller's regular gas rises by d, its spill falls by d, its reservoir rises by the returned reservoir less d; the reservoir the caller kept is never drawn; state and history charges share the spill.
- `SATIN-POOL-013` — A successful child's own spill is added to the caller's spill before the unwind; a reverted or halted child's is not.
- `SATIN-POOL-014` — A frame that reverts or halts gives back its state and history charges as EIP-8037 specifies (the reservoir-paid part to the reservoir, the spilled part to the regular budget); a revert returns the unspent regular gas to the caller, a halt consumes it, the returned spill included.
- `SATIN-POOL-015` — The caller's own charge for a leaf the child did not add is given back after the merge.
- `SATIN-POOL-016` — An authority charge made before the first frame is not committed out of the outstanding spill; the reservoir the first frame returns unwinds it with any other outstanding spill; a failure of the first frame returns no reservoir that charge drew.
- `SATIN-POOL-017` — When the transaction ends the reservoir left returns to the sender, and so does the unspent regular gas unless the transaction's own frame halted, a revert and a limit stop included.
- `SATIN-POOL-018` — The receipt's gas used is what the transaction spent from both pools after the inherited refund and floor rules; when the spend less the refund is below the floor, gas used is the floor, no refund is made, and the floor's excess is drawn from the unspent regular gas and the reservoir alike.
- `SATIN-POOL-019` — Three ledgers: regular = total − state − history, state = the state charges kept, history = the history charges kept, the body included; spilled state or history gas stays on its own ledger.
- `SATIN-POOL-020` — The EIP-7623 floor, as EIP-7976 and EIP-7981 amend it, is computed and validated as Amsterdam does; the block's execution ledger counts max(regular, floor), history gas taken out of regular before the floor applies.
- `SATIN-POOL-021` — Satin has no separate compute-gas limit: compute is regular gas, bounded by the execution cap and by gas detention.
- `SATIN-POOL-022` — Satin's departures from EIP-8037: the reservoir share, history gas on the reservoir and the shared spill, the destruction-table refill.

## Spec History

- [Satin](../../upgrades/satin.md) — The reviewers' delta of Satin against Rex6.
