---
description: Satin (unstable) — Deposit Transactions. What a deposit pays and is held to, the account a deposit creates for its caller, when a deposit becomes a failed deposit, and what a failed deposit keeps and reports.
spec: Satin
maturity: unstable
---

# Deposit Transactions

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
{% endhint %}

Abstract: Deposit transactions under Satin: the history gas they pay and the pricing, limits and detention they are held to; the state gas of the caller account a deposit creates; the failed deposit — when a deposit becomes one, and what it applies, reports and keeps; and the prestates and envelopes that lie outside the specification.
This page gathers the deposit rules; where the detail of a rule is another page's, it links it.

## Motivation

A deposit is derived from L1 and must be included in the block the derivation puts it in: a node cannot refuse it as it refuses a user's transaction.
It pays no fee on L2, so whatever it consumes is paid by nobody on L2 — but it creates state and data the chain keeps, and it can run arbitrary code.
A deposit that cannot be executed must still be recorded, and the record must say exactly what it changed and used, or a block of such deposits would grow state while reporting none, and two nodes would apply different effects for the same failed deposit.

## Specification

### What a deposit pays and is held to

- `SATIN-DEP-001` That a deposit pays history gas as any transaction does — for its body, its calldata, its logs, its write records and its deposited code — is the rule `SATIN-HIST-016` (see [History Gas](../evm/history-gas.md)); a deposit whose gas limit cannot pay its intrinsic regular gas and its body's history gas fails validation, and so is a failed deposit (`SATIN-VAL-002`, `SATIN-DEP-004`).
- `SATIN-DEP-002` That a deposit which is not system-originated is priced by the SALT bucket its state lands in, held to every per-transaction limit and frame budget, and detained after a read of volatile data, as any transaction is, is the rule of `SATIN-STATE-009`, `SATIN-LIM-001` and `SATIN-DET-026`; which deposits are system-originated is `SATIN-MST-010` (see [Mega System Transactions](../system-contracts/system-tx.md)).
- `SATIN-DEP-003` A deposit — or a Mega System Transaction, which executes as one — whose caller is empty under EIP-161 when the deposit is executed (no account, or nonce zero, zero balance and no code: `SATIN-STATE-011`) MUST be charged that account's new-account state gas exactly once, before its first frame, as the first charge of `SATIN-SCHED-008`, priced at the caller's bucket (at `m = 1` for a system-originated one).
  The account MUST always be created and kept, whatever the deposit then does, and it MUST count as one unit of state growth; being one account, it cannot by itself cross the state-growth limit.
  A caller whose leaf the state holds but which is empty under EIP-161 is charged and counted as one the state holds no account for; the witness still answers it as a leaf (`SATIN-WIT-017`).
- `SATIN-DEP-009` That a deposit pays nothing for its gas, and that where the [EIP-7623](https://eips.ethereum.org/EIPS/eip-7623) floor binds its gas used only its receipt's gas used and the block's figures move, is the rule `SATIN-HIST-017` (see [History Gas](../evm/history-gas.md)).
- `SATIN-DEP-007` That a deposit whose own frame succeeds, reverts or is stopped by a limit settles as an ordinary transaction, a stop being a revert and not a failed deposit, is the rule `SATIN-STOP-010` with `SATIN-OUT-014` (see [Halts, Reverts and Stops](../evm/outcomes.md)).
- `SATIN-DEP-010` A deposit that creates a contract from a sender whose nonce is `MAX_NONCE`, which cannot be bumped, and whose balance, its mint credited, funds the deposit's value, MUST succeed with nothing created and nothing counted for the creation: no account at the address the creation would derive, no state gas for it, no record and no state growth, the gas of its first frame untouched.
  The value is checked first: a sender at `MAX_NONCE` that cannot fund the value makes the deposit a failed deposit (`SATIN-DEP-004`), before the nonce is considered.

### The failed deposit

- `SATIN-DEP-004` A deposit MUST become a failed deposit when it fails a validation check (see [Transaction Validation and Refusals](transaction-validation.md)), when it cannot pay a charge made before its first frame (the state gas of the caller account it creates, among them), or when its own frame halts — a first frame whose value the sender, its mint credited, cannot fund included.
  A failed deposit MUST bump its sender's nonce, MUST credit its mint to its sender, MUST use its whole gas limit, the reservoir included, and MUST apply nothing else: every other change its execution made is taken back.
- `SATIN-DEP-005` A failed deposit MUST report its whole gas limit as regular gas, and no state gas and no history gas, on the transaction's ledgers and on the block's.
  The caller account it creates for a sender that was empty under EIP-161 (`SATIN-STATE-011`) carries no state gas, unlike the one a deposit that runs to a success or a revert creates, and it MUST still count as one unit of state growth, on the transaction's reported usage and on the block's counter.
- `SATIN-DEP-006` A failed deposit MUST keep the data size of its body and of the Oracle hints it admitted (see [Oracle](../system-contracts/oracle.md)), and MUST return no withheld gas, no unspent gas and no reservoir to its sender.
- `SATIN-DEP-008` A deposit whose caller is the live system address MUST be a failed deposit (see [Mega System Transactions](../system-contracts/system-tx.md), `SATIN-MST-003`), and so MUST one handed to the node already carrying the promotion's source hash from that address.
  A deposit that carries the base layer's system-transaction flag, which the base layer refuses from Regolith on, MUST be a failed deposit too.
- `SATIN-DEP-012` A deposit that fails before its first frame MUST make no load for its first frame's start: nothing of its recipient, nor of the account its creation would create, beyond what it loads in another role (its sender, when the recipient is the sender, is loaded all the same); it MUST load its sender's code only once its intrinsic gas and floor checks have passed, so a deposit that fails one of them loads none of it.
  What a deposit that fails loads otherwise is what [The Stateless Witness](stateless-witness.md) specifies for every transaction.

### Outside the specification

- `SATIN-DEP-011` A state in which a deposit's sender's balance plus the deposit's mint exceeds `MAX_BALANCE` when the deposit is executed is an invalid prestate: the execution of such a deposit, whether it would succeed or fail, lies outside this specification.
- `SATIN-DEP-013` A deposit has no gas price: an envelope that presents itself as a deposit and carries a gas price is malformed, and its execution lies outside this specification.

A value transfer a deposit makes — its value, or a `CALL`'s, a `SELFDESTRUCT`'s or a creation's within it — that would push its recipient's balance above `MAX_BALANCE` lies outside this specification as any transaction's does (see [Base Layer](../base-layer.md), `SATIN-BASE-011`).

## Constants

| Constant      | Value    | Description                                     |
| ------------- | -------- | ----------------------------------------------- |
| `MAX_NONCE`   | 2^64 − 1 | The largest account nonce ([EIP-2681](https://eips.ethereum.org/EIPS/eip-2681)) |
| `MAX_BALANCE` | 2^256 − 1 | The largest account balance                    |

## Rationale

**Why does a deposit pay history gas and state gas?**
The bytes a deposit appends to the chain's history and the state it adds are stored by every node, as any transaction's are, so they are priced as any transaction's are, though nobody on L2 pays the price, since a deposit pays no fee: the charges bound what one deposit can append and create with its gas limit, as Rex6's storage gas did for a deposit's calldata, logs and code.
A deposit whose gas limit cannot pay its body's history gas is included as a failed deposit, its mint credited and its nonce bumped.

**Why is the created caller always kept and counted?**
The base layer creates a deposit's sender when it bumps its nonce or mints to it, whatever the deposit then does.
Counting it as state growth on every path keeps a block of failing deposits from growing state while reporting none; charging state gas for it only on the paths that run keeps a failed deposit's report one figure, its gas limit as regular gas.

**Rex6 defect fixed.** A deposit from an absent sender with a gas limit below its intrinsic gas failed before Rex6 counted its caller's growth, yet the failed deposit created the sender by its nonce bump and mint, so the block kept a new account its state-growth count never saw.
Satin counts the created caller as one unit of growth on every path, an early failure included (`SATIN-DEP-005`).

**Rex6 defect fixed.** A deposit whose sender was the live system address, which the registry can rotate to any address, was refused by Rex6 as an invalid system transaction, leaving a block the derivation requires unexecutable.
Satin includes it as a failed deposit (`SATIN-DEP-008`).

**Why does a failed deposit use its whole gas limit?**
That is the base layer's rule for a failed deposit since Regolith; Satin keeps it, the reservoir included, so that a deposit that cannot run is accounted by its gas limit alone.

**Why is a limit stop not a failed deposit?**
Rex6 halted a deposit that crossed gas detention or a transaction-level resource limit, which made it a failed deposit that used its whole gas limit and kept only its mint and nonce.
Satin's limits are stops of the frame that crosses them ([Limit Stops](../evm/limit-stops.md)), and a deposit's stop settles as any transaction's: the deposit ran, its sender is accountable for what ran, exactly as for any other transaction, and a caller inside it can recover from the stop.
Only a halt, a validation failure, or a charge before the first frame it cannot pay makes a deposit fail.

**Why is a mint that overflows the balance outside the specification?**
No chain can reach it: all the ether in existence is about 1.2 × 10^26 wei, far below 2^256.
The base layer's implementations disagree on it — saturating on success, a checked or a wrapping credit on failure — and defining one would bind every node to a behaviour no block can exercise.
A value transfer that would overflow its recipient's balance is outside the specification for the same reason, for a deposit as for any transaction (`SATIN-BASE-011`).

**Why does a deposit that fails early load nothing of its recipient?**
The read set is part of what a stateless validator is given; a deposit refused before its first frame decides nothing on its recipient, so loading it would put an account in the witness that no execution reads.

## Security Considerations

- A node that does not count a failed deposit's created caller lets a block of such deposits exceed the block's state-growth budget while reporting no growth.
- A node that returns unspent gas or reservoir for a failed deposit reports a gas used other nodes do not, and moves the block's cumulative gas.
- A node that refuses a deposit, instead of including it as a failed deposit, cannot build the block the derivation requires.
- A node that treats a stopped deposit as failed takes back the effects of what ran and keeps the mint only; the deposit's own frame's effects then differ from every other node's.
- A node that loads a failed deposit's recipient adds an account to the witness the replay never reads; a validator holding the minimal witness then fails to reproduce the node's read set.

## Spec History

- [Rex5](../../upgrades/rex5.md) — Accounted a deposit caller's new account.
- [Rex6](../../upgrades/rex6.md) — A deposit from the system address was refused with an error that left its block unexecutable.
- [Satin](../../upgrades/satin.md) — History gas for deposits, the created caller's state gas, the failed deposit's report, and a deposit from the system address included as a failed deposit.
