---
description: Satin (unstable) — Mega System Transactions and the Protocol's Own Transactions. Which transactions are Mega System Transactions, how one is validated and promoted to a deposit, which executions are the protocol's own, and what that exempts them from.
spec: Satin
maturity: unstable
---

# Mega System Transactions and the Protocol's Own Transactions

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
{% endhint %}

Abstract: The Mega System Transaction — the legacy transaction from the live system address through which the sequencer writes the Oracle — how it is recognized, validated and promoted to a deposit, and which executions are the protocol's own work, exempt from SALT pricing, the per-transaction limits and gas detention, a system call from history gas as well.

## Motivation

The sequencer must write the values the oracle service served into the Oracle's storage, in the block, before the transactions that read them.
Those writes are the protocol's maintenance, not a user's activity: they pay no fee, and a per-transaction resource limit or gas detention must never make one fail once the block includes it, or the block could not carry the values its transactions read.
The exemption is only safe if the transactions that receive it are exactly the protocol's own: a user transaction that could pass as one would run fee-free and unlimited.

## Specification

### Mega System Transactions

- `SATIN-MST-001` A transaction MUST be taken to have the system shape when, judged on its own fields alone, it is of type `0x0` (legacy) and is a call — not a creation — to an address on `MEGA_SYSTEM_TX_WHITELIST`.
- `SATIN-MST-002` A transaction of the system shape whose caller is the live system address (see [SequencerRegistry](sequencer-registry.md), `SATIN-REG-002`) MUST be a Mega System Transaction.
- `SATIN-MST-003` A transaction whose caller is the live system address and that does not have the system shape MUST be invalid, whatever its type: a transaction other than a deposit MUST be rejected (see [Transaction Validation and Refusals](../block/transaction-validation.md)), and a deposit, which never has the system shape, MUST be included as a failed deposit, which runs no call (see [Deposit Transactions](../block/deposits.md)); that includes a deposit handed to the node already carrying the promotion's source hash.
- `SATIN-MST-004` A transaction whose caller is any other address MUST NOT be a Mega System Transaction, and MUST be validated and charged as a user's: that includes a transaction from an address a rotation retired, which is no longer the live system address.
- `SATIN-MST-005` A Mega System Transaction MUST be validated before it is promoted to a deposit, and a failure MUST be a rejection: it MUST carry a chain id, equal to the chain's; its nonce MUST equal the system address's nonce; and the system address MUST hold no code other than an EIP-7702 delegation indicator, as [EIP-3607](https://eips.ethereum.org/EIPS/eip-3607) requires of any sender.
  The chain-id check MUST be made whatever the node's configuration says (`SATIN-VAL-006`); the nonce and EIP-3607 checks are those every sender is held to, and a configuration that switches either off for a user's transaction switches it off for a Mega System Transaction too.
  Once it passes them, the transaction MUST be executed as a deposit from the system address to its recipient, with its value, gas limit and input, no mint, and the gas price zero: no signature, nonce, fee or balance-for-fee check of its own is made, no fee is charged and no fee recipient is credited, the caller its recipient sees is the system address, and the system address's nonce is bumped as a deposit's sender's is.
  A check the deposit then fails, or a first frame that halts, makes it a failed deposit (see [Deposit Transactions](../block/deposits.md)).
- `SATIN-MST-006` The promotion MUST stamp the deposit with the source hash `MEGA_SYSTEM_TRANSACTION_SOURCE_HASH`.

### The protocol's own work

- `SATIN-MST-007` A transaction MUST be system-originated when it is a Mega System Transaction, before or after its promotion; when its caller is `SYSTEM_CALLER`, the caller of the pre-block calls; or when it is a deposit carrying `MEGA_SYSTEM_TRANSACTION_SOURCE_HASH`, whoever its caller.
  The test MUST be made on the transaction's own fields, in a block as outside one: a transaction of any type from `SYSTEM_CALLER`, or a deposit carrying that source hash, is the protocol's wherever it is executed, a call or a simulation included.
  Only a deposit carries a source hash: a transaction handed to a node with one is a deposit, and is executed as one, whatever type its other fields name.
  A deposit carrying that source hash from the live system address is system-originated and, by `SATIN-MST-003`, a failed deposit.
  A system call — a pre-block call (see [System Calls and the Pre-Block Sequence](../block/system-calls.md)) — is the protocol's own work as well.
- `SATIN-MST-008` A system-originated transaction and every system call:
  - MUST be priced at the multiplier `m = 1` and MUST NOT read a SALT bucket's capacity (see [State Gas and SALT Pricing](../evm/state-gas.md));
  - MUST NOT be stopped by any per-transaction limit or frame budget, in data size, KV updates or state growth (see [Resource Limits](../evm/resource-limits.md));
  - MUST NOT be detained, whatever they read (see [Gas Detention](../evm/gas-detention.md));
  - MUST still have their usage counted in every dimension.

  A system call MUST also pay no history gas, its deposited code included; a system-originated transaction MUST pay history gas as any transaction does, its body, its calldata, its logs, its write records and its deposited code (see [History Gas](../evm/history-gas.md)).
- `SATIN-MST-009` A system-originated transaction's usage MUST be reported, and MUST count toward the block's counters; a Mega System Transaction is held to the block's packing budgets as any other non-deposit transaction is (see [Block Limits and Packing](../block/block-limits.md), `SATIN-BLK-007`); a pre-block call's usage MUST count toward neither the block's counters nor its limits.
- `SATIN-MST-010` A user's deposit is not system-originated: it MUST be priced by bucket, held to every per-transaction limit and frame budget, and detained, and it pays history gas as any transaction does (see [Deposit Transactions](../block/deposits.md)).

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
The Oracle authorizes writes on its immediate caller, which for a transaction's own call is the sender; a system key that could send other transactions could reach the Oracle through them with no validation the system shape gets, or deploy and call arbitrary code fee-free.

**Rex6 defect fixed.** A deposit derived from L1 whose sender was the live system address — an address the registry may rotate to, which no fixed L1 rule can keep from sending deposits — was refused by Rex6 with an error that left its block unexecutable, although the derivation requires the block to hold it.
Satin includes such a deposit as a failed deposit, which runs no call (`SATIN-MST-003`), so the engine no longer relies on the L1 portal refusing deposits from every system address a rotation installs.

**Why validate before promotion?**
A deposit checks no signature, nonce or chain id, because L1 derivation protects it from replay; a Mega System Transaction has no such protection.
The chain id keeps it from being replayed on another chain, the nonce on this one, and EIP-3607 keeps a contract address from sending it.
The chain-id check is fixed on, as every transaction's is; the nonce and code checks follow the configuration switches every sender's follow, which block execution never turns off.

**Why decide system origin on the transaction's own fields?**
In a block the protocol's own transactions are the promoted Mega System Transactions: no transaction a block derives from L1 carries the promotion's source hash, and nobody holds a key for `SYSTEM_CALLER`.
Deciding on the fields alone gives a call or a simulation of the same transaction the same exemption a block gives it.

**Rex6 defect fixed.** A deposit handed to a Rex6 node carrying `MEGA_SYSTEM_TRANSACTION_SOURCE_HASH` from an ordinary sender was exempt as the protocol's own, by the code's test on its fields, although Rex6's text said a user's deposit is never system-originated.
Satin states the test the code makes (`SATIN-MST-007`) and adds no exemption with it: no deposit L1 derives carries that source hash.

**Why exempt the protocol's work from the per-transaction limits but count it?**
A per-transaction limit or detention must not stop an oracle write the block's transactions depend on once the block includes it; its usage is still state and data the block keeps, so it counts on the block's counters, and the block's packing budgets hold a Mega System Transaction as any transaction, as in Rex6.

**Why is a Mega System Transaction's regular gas bounded by the execution cap?**
Rex6 bounded a Mega System Transaction by its gas limit alone; under EIP-8037's pools every transaction runs on at most the execution cap of regular gas, the rest of its gas limit paying only state and history gas ([Two-Pool Gas](../evm/gas-model.md)), and a Mega System Transaction is no exception, so it can no longer spend a gas limit above the cap on computation, although no per-transaction limit or detention stops it.

**Why does a protocol transaction pay history gas?**
What a transaction appends to the chain's history is stored by every node, whoever sent it; a deposit and a Mega System Transaction therefore pay history gas as any transaction does, and the bound it sets on what one transaction appends holds for them too.
A pre-block system call appends no transaction to the history and is the protocol's own step, run before any transaction, so it stays exempt.

## Security Considerations

- A whitelist check that admitted another target would let the system key call arbitrary contracts fee-free and unlimited; adding an address to `MEGA_SYSTEM_TX_WHITELIST` changes which transactions are privileged and needs a new spec.
- A creation from the system address treated as a Mega System Transaction would deploy arbitrary code at no cost.
- A node that skipped the chain-id or nonce check would accept a replayed system transaction, rewriting the Oracle with stale values.
- A node that decided system origin from anything but the transaction's own fields would price and limit the same transaction differently in a simulation and in a block.

## Spec History

- [MiniRex](../../upgrades/minirex.md) — Introduced Mega System Transactions from a fixed system address.
- [Rex5](../../upgrades/rex5.md) — Resolved the system address from the SequencerRegistry per block, and restored the chain-id, nonce and EIP-3607 checks.
- [Rex6](../../upgrades/rex6.md) — Exempted system-originated transactions from the resource limits and detention; the Rex6 rules are specified in [Mega System Transactions](../../system-contracts/system-tx.md).
- [Satin](../../upgrades/satin.md) — Every other transaction from the system address invalid, a deposit from it a failed deposit, and history gas paid by the protocol's transactions, the pre-block calls exempt.
