---
description: Satin (unstable) — Gas Detention. Stub of the Satin specification: the rules this page will specify.
spec: Satin
maturity: unstable
---

# Gas Detention

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
This page is a stub. It lists what the page will specify; the specification text is written after the outline is reviewed.
{% endhint %}

Abstract: Gas detention on withheld gas: what is volatile, how compute is measured, the limit a read sets, how a frame's regular gas is split into spendable and withheld parts, the crossing, and the precompile and interceptor cases.

## Specification

The rules this page will specify, by their proposed ids:

- `SATIN-DET-001` — Volatile data: the block environment (NUMBER, TIMESTAMP, COINBASE, PREVRANDAO, GASLIMIT, BASEFEE, BLOBBASEFEE, SLOTNUM, BLOCKHASH); the beneficiary's account through the account opcodes, the call opcodes and the delegate they follow, SELFDESTRUCT at either end, a sender, recipient or delegating recipient, an applied authority or a keyless signer that is the beneficiary; the Oracle's storage through SLOAD in the Oracle's frame.
- `SATIN-DET-002` — BLOBHASH is not volatile.
- `SATIN-DET-003` — A read is marked where the value is loaded and only once the opcode completed; a load that fails, and a read whose opcode then fails, mark nothing.
- `SATIN-DET-004` — Every BLOCKHASH is a read of the block environment, whatever its operand.
- `SATIN-DET-005` — A call to the EIP-2935 history contract is a block-environment read; an SLOAD of the storage the EIP-2935 and EIP-4788 pre-block calls write is not volatile.
- `SATIN-DET-006` — A CREATE or CREATE2 is never marked as a read nor refused, even with the beneficiary as creator or created address.
- `SATIN-DET-007` — A frame running as the beneficiary marks the beneficiary's account by its own SELFBALANCE, SELFDESTRUCT and the other reads.
- `SATIN-DET-008` — A transaction whose sender, recipient or applied authority is the beneficiary is detained from its start.
- `SATIN-DET-009` — Compute is every regular charge the frames make, whoever funds it: the running frame's regular gas spent plus every suspended caller's, each less what it forwarded, less spilled state and history gas, less what halting frames burned.
- `SATIN-DET-010` — What a callee runs on a value call's 2,300 stipend counts as compute, and the stipend never lowers compute when it returns.
- `SATIN-DET-011` — What a halting frame burns is not compute; a precompile that runs out of gas burns its forward without counting it, unless it is the crossing.
- `SATIN-DET-012` — A read sets limit = compute_at_read + cap, BLOCK_ENV_ACCESS_COMPUTE_GAS = 20,000,000 for the block environment and the beneficiary, ORACLE_ACCESS_COMPUTE_GAS = 20,000,000 for the Oracle; the limit only goes down.
- `SATIN-DET-013` — The caps are protocol values fixed per spec, both below 199,987,900, the most compute a transaction can spend.
- `SATIN-DET-014` — Once a limit is set every frame's regular gas is split into a spendable part (limit − compute, or zero) and a withheld part, at the read's completion, at every frame start or resume, and after an SSTORE.
- `SATIN-DET-015` — Only a regular charge is limited to the spendable part; every other reader of the frame's gas (GAS, the forward and its clamp, the SSTORE minimum-gas check, the cold-load checks, a child's returned gas, the settlement) sees both parts.
- `SATIN-DET-016` — At the settlement the withheld part is unspent gas returned to the sender and not part of the gas used that caps the EIP-3529 refund; a failed deposit returns none of it.
- `SATIN-DET-017` — A forward and a spill of state or history gas draw the withheld part first.
- `SATIN-DET-018` — The crossing: a regular charge the spendable part cannot pay but the frame's whole regular gas can is not made, the gas is put back, and the frame is stopped with MegaLimitExceeded(2, limit); what was spent before stays spent; the caller gets back everything the frame had, the withheld part included.
- `SATIN-DET-019` — At the crossing the transaction's compute is at most the limit; a caller the stop returns into is held to what the limit leaves; what halting frames burn adds nothing, so compute since a read is at most its cap.
- `SATIN-DET-020` — A regular charge beyond the frame's whole regular gas, and every other out-of-gas, halts as without the read.
- `SATIN-DET-021` — A precompile call's own regular charges come first; a call forwarded more than the frame's allowance is decided from the precompile's price: within the allowance it runs on its whole forward, past the allowance and within the forward it does not run and is the crossing, past the forward it runs and fails.
- `SATIN-DET-022` — The value has not moved when the price is consulted, so the crossing is kind 2 whatever records the value transfer would have made.
- `SATIN-DET-023` — Every precompile of the Satin set has a price; an input over a size limit is priced at zero.
- `SATIN-DET-024` — An input priced between the allowance and the forward that would fail a later check is the crossing too; a call refused on its caller's account runs no precompile and is answered as without the read.
- `SATIN-DET-025` — A system contract's intercepted answer that spent more regular gas than the allowance is the crossing, and its whole regular spend is the one charge that crossed (none of it billed).
- `SATIN-DET-026` — A system-originated transaction and a system call are never detained.
- `SATIN-DET-027` — A precompile a node adds or replaces is outside the Satin set and outside the specification.

## Spec History

- [Satin](../../upgrades/satin.md) — The reviewers' delta of Satin against Rex6.
