---
description: Satin (unstable) — KeylessDeploy. Stub of the Satin specification: the rules this page will specify.
spec: Satin
maturity: unstable
---

# KeylessDeploy

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
This page is a stub. It lists what the page will specify; the specification text is written after the outline is reviewed.
{% endhint %}

Abstract: Keyless deployment (Nick's method) as a native creation: which calls are deployments, the fifteen steps the call makes, the creation it starts, the signer's nonce rule, the answer, and what a limit does to a deployment.

## Specification

The rules this page will specify, by their proposed ids:

- `SATIN-KEY-001` — Address 0x6342…0003; bytecode and code hash unchanged; the interface declares the errors without the four removed.
- `SATIN-KEY-002` — A keylessDeploy(bytes,uint256) call that is the transaction's own frame (depth 0, CALL, the address, the selector) deploys the carried creation as an ordinary creation frame, a child of the call, whatever code the state holds there.
- `SATIN-KEY-003` — A keylessDeploy call a contract makes runs the bytecode: NotIntercepted() without value, an empty revert with value.
- `SATIN-KEY-004` — A rule's refusal reverts the call with its error (state and history gas given back, regular gas spent); an out-of-gas step halts the call.
- `SATIN-KEY-005` — The fifteen steps in order (100,000 overhead; no value; decoding; nonce 0; initcode size; gasLimitOverride covers the signed limit; recovery with a low or high s; signer nonce at most 1; EIP-3607 unless disabled; an empty signer's state gas; the forward covers; no code at the deploy address; balance covers the value; CREATE's charges and records; the forward still covers).
- `SATIN-KEY-006` — Steps 1 to 13 keep Rex6's order, so a call several rules refuse reports the Rex6 error.
- `SATIN-KEY-007` — The signer and deploy-address reads load the accounts warm (the deploy address without its code), uncharged; no charge depends on their warmth.
- `SATIN-KEY-008` — Step 12 checks code alone: an address holding a nonce but no code passes, and the creation then collides there and fails (ExecutionHalted).
- `SATIN-KEY-009` — A creation at the deploy address that returns empty code is refused its empty deposit and reverts (EmptyCodeDeployed), as is a constructor that destroyed its own account.
- `SATIN-KEY-010` — A signer that is the beneficiary is detained at the signer read, after step 7 and before step 8, with the call's 100,000 as the read's compute.
- `SATIN-KEY-011` — The creation starts by the signer at the deploy address one level below the call, forwarding min(gasLimitOverride, remaining gas) with the withheld part drawn first and no 98/100 cap, the reservoir share of what step 14 left and the child share of the three budgets; ORIGIN and GASPRICE are the transaction's own.
- `SATIN-KEY-012` — The signer's nonce record, and its growth when the bump creates the signer, are counted on the call at its settlement.
- `SATIN-KEY-013` — The signer's nonce: from 0 the bump stays; from 1, when the creation's bump is the last nonce change, it is taken back whether the deployment succeeded or failed, the record counted after and its history given back when none stands; a signer whose own code spent a nonce keeps every bump.
- `SATIN-KEY-014` — The answer (gasUsed, deployedAddress, errorData): the deploy address and empty errorData when it holds code afterwards; otherwise the zero address and ExecutionReverted, ExecutionHalted or EmptyCodeDeployed.
- `SATIN-KEY-015` — gasUsed is what the creation spent from both pools, no intrinsic gas, before the EIP-3529 refund, net of every give-back inside it; the call's own charges of steps 1 and 14 are not in it; never less than the regular gas the creation spent.
- `SATIN-KEY-016` — A limit the creation crosses stops the creation and the call answers ExecutionReverted with the stop's data; a limit the call's own charges or the signer's nonce record cross stops the call, taking the deployment back; that stop is the transaction's.
- `SATIN-KEY-017` — The four Rex-era errors are not declared and never produced; AddressMismatch() and NoContractCreated() remain as unreachable answers.
- `SATIN-KEY-018` — With value, the 100,000 overhead is decided under detention first (a crossing stops the call with none of it billed), then NoEtherTransfer() is answered before anything moves.

## Spec History

- [Satin](../../upgrades/satin.md) — The reviewers' delta of Satin against Rex6.
