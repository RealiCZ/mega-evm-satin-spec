---
description: Satin (unstable) — Mega System Transactions and the Protocol's Own Transactions. Which transactions are Mega System Transactions, how one is validated and promoted to a deposit, which executions are the protocol's own, and what that exempts them from.
spec: Satin
maturity: unstable
---

# Mega System Transactions and the Protocol's Own Transactions

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
{% endhint %}

Abstract: The Mega System Transaction — the legacy transaction from the live system address through which the sequencer writes the Oracle — how it is recognized, validated and promoted to a deposit, and which executions are the protocol's own work, exempt from SALT pricing, history gas, the per-transaction limits and gas detention.

## Motivation

The sequencer must write the values the oracle service served into the Oracle's storage, in the block, before the transactions that read them.
Those writes are the protocol's maintenance, not a user's activity: they pay no fee, and a resource limit or gas detention must never make them fail, or the block could not carry the values its transactions read.
The exemption is only safe if the transactions that receive it are exactly the protocol's own: a user transaction that could pass as one would run fee-free and unlimited.

## Specification

### Mega System Transactions

- `SATIN-MST-001` A transaction MUST be taken to have the system shape when, judged on its own fields alone, it is of type `0x0` (legacy) and is a call — not a creation — to an address on `MEGA_SYSTEM_TX_WHITELIST`.
- `SATIN-MST-002` A transaction of the system shape whose caller is the live system address (see [SequencerRegistry](sequencer-registry.md), `SATIN-REG-002`) MUST be a Mega System Transaction.
- `SATIN-MST-003` A transaction whose caller is the live system address and that does not have the system shape MUST be invalid, whatever its type: a transaction other than a deposit MUST be rejected (see [Transaction Validation and Refusals](../block/transaction-validation.md)), and a deposit, which never has the system shape, MUST be included as a failed deposit, which runs no call (see [Deposit Transactions](../block/deposits.md)); that includes a deposit handed to the node already carrying the promotion's source hash.
- `SATIN-MST-004` A transaction whose caller is any other address MUST NOT be a Mega System Transaction, and MUST be validated and charged as a user's: that includes a transaction from an address a rotation retired, which is no longer the live system address.
- `SATIN-MST-005` A Mega System Transaction MUST be validated before it is promoted to a deposit, and a failure MUST be a rejection: it MUST carry a chain id, equal to the chain's; its nonce MUST equal the system address's nonce; and the system address MUST hold no code other than an EIP-7702 delegation indicator, as [EIP-3607](https://eips.ethereum.org/EIPS/eip-3607) requires of any sender.
  These checks MUST be made whatever the node's configuration says.
  Once it passes them, the transaction MUST be executed as a deposit from the system address to its recipient, with its value, gas limit and input, no mint, and the gas price zero: no signature, nonce, fee or balance-for-fee check of its own is made, no fee is charged and no fee recipient is credited, the caller its recipient sees is the system address, and the system address's nonce is bumped as a deposit's sender's is.
  A check the deposit then fails, or a first frame that halts, makes it a failed deposit (see [Deposit Transactions](../block/deposits.md)).
- `SATIN-MST-006` The promotion MUST stamp the deposit with the source hash `MEGA_SYSTEM_TRANSACTION_SOURCE_HASH`.

### The protocol's own work

- `SATIN-MST-007` A transaction MUST be system-originated when, and only when, it is a Mega System Transaction, before or after its promotion.
  A transaction from any other caller is not system-originated, whatever its fields carry: a transaction whose caller is `SYSTEM_CALLER`, and a deposit handed to the node already carrying `MEGA_SYSTEM_TRANSACTION_SOURCE_HASH`, are ordinary transactions unless they are Mega System Transactions, and a deposit from the live system address is a failed deposit (`SATIN-MST-003`).
  A system call — a pre-block call (see [System Calls and the Pre-Block Sequence](../block/system-calls.md)) — is not a transaction, and is the protocol's own work as well.
- `SATIN-MST-008` A system-originated transaction and every system call:
  - MUST be priced at the multiplier `m = 1` and MUST NOT read a SALT bucket's capacity (see [State Gas and SALT Pricing](../evm/state-gas.md));
  - MUST pay no history gas, their body and deposited code included (see [History Gas](../evm/history-gas.md));
  - MUST NOT be stopped by any per-transaction limit or frame budget, in data size, KV updates or state growth (see [Resource Limits](../evm/resource-limits.md));
  - MUST NOT be detained, whatever they read (see [Gas Detention](../evm/gas-detention.md));
  - MUST still have their usage counted in every dimension.
- `SATIN-MST-009` A system-originated transaction's usage MUST be reported, and MUST count toward the block's counters (see [Block Limits and Packing](../block/block-limits.md)); a pre-block call's usage MUST count toward neither the block's counters nor its limits.
- `SATIN-MST-010` A user's deposit is not system-originated: it MUST be priced by bucket, held to every per-transaction limit and frame budget, and detained, although it pays no history gas (see [Deposit Transactions](../block/deposits.md)).

## Constants

| Constant                              | Value                                                                | Description                                                  |
| ------------------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------ |
| `MEGA_SYSTEM_TX_WHITELIST`            | { `0x6342000000000000000000000000000000000001` }                     | The contracts a Mega System Transaction may call: the Oracle |
| `MEGA_SYSTEM_TRANSACTION_SOURCE_HASH` | `0x852c082c0faff590c6300c2c34815d1f79882552fa95ba413cd5aeb1dba84957` | `keccak256("MEGA_SYSTEM_TRANSACTION")`                       |
| `SYSTEM_CALLER`                       | `0xfffffffffffffffffffffffffffffffffffffffe`                         | The caller of the pre-block system calls                     |

## Rationale

**Why test the shape on the transaction's own fields?**
The shape decides how the transaction is validated, before anything of it runs; it must not depend on what the transaction would do.

**Why is every other transaction from the system address invalid?**
The Oracle authorizes writes on the sender alone; a system key that could send other transactions could reach the Oracle through them with no validation the system shape gets, or deploy and call arbitrary code fee-free.
Rex6 refused such a transaction with an error that left its block unexecutable when it was a deposit; Satin includes such a deposit as a failed deposit, so the engine no longer relies on the L1 portal refusing deposits from every system address a rotation installs.

**Why validate before promotion?**
A deposit checks no signature, nonce or chain id, because L1 derivation protects it from replay; a Mega System Transaction has no such protection.
The chain id keeps it from being replayed on another chain, the nonce on this one, and EIP-3607 keeps a contract address from sending it.
The checks are fixed on, as the chain-id check of every transaction is, so a simulation validates it exactly as a block does.

**Why only Mega System Transactions?**
In a block the protocol's own transactions are the promoted Mega System Transactions: no transaction a block derives from L1 carries the promotion's source hash, and nobody holds a key for `SYSTEM_CALLER`.
Deciding system origin on the Mega System Transaction alone keeps the exemption from reaching a transaction the protocol did not make, in a simulation as in a block.

**Why exempt the protocol's work from the limits but count it?**
The sequencer must always be able to include the oracle writes the block's transactions depend on, so no limit may stop them; their usage is still state and data the block keeps, so it counts on the block's counters.

## Security Considerations

- A whitelist check that admitted another target would let the system key call arbitrary contracts fee-free and unlimited; adding an address to `MEGA_SYSTEM_TX_WHITELIST` changes which transactions are privileged and needs a new spec.
- A creation from the system address treated as a Mega System Transaction would deploy arbitrary code at no cost.
- A node that skipped the chain-id or nonce check would accept a replayed system transaction, rewriting the Oracle with stale values.
- A node that treated a deposit carrying the promotion's source hash as system-originated would exempt a transaction the protocol did not promote from every limit.

## Spec History

- [MiniRex](../../upgrades/minirex.md) — Introduced Mega System Transactions from a fixed system address.
- [Rex5](../../upgrades/rex5.md) — Resolved the system address from the SequencerRegistry per block, and restored the chain-id, nonce and EIP-3607 checks.
- [Rex6](../../upgrades/rex6.md) — Exempted system-originated transactions from the resource limits and detention; the Rex6 rules are specified in [Mega System Transactions](../../system-contracts/system-tx.md).
- [Satin](../../upgrades/satin.md) — The live system address read by every transaction, every other transaction from it invalid, and the exemption extended to history gas.
