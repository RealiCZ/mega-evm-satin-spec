---
description: Satin (unstable) — Block Limits and Packing. What a block counts of its transactions, the three packing budgets and the transactions they never refuse, the block gas limit, and what a builder may do as policy that a validator never applies.
spec: Satin
maturity: unstable
---

# Block Limits and Packing

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
{% endhint %}

Abstract: What a block counts of each transaction; the three counts — data size, KV updates and state growth — that are packing budgets, checked before each transaction runs; the deposits and Mega System Transactions those budgets never refuse; the block gas limit; when a transaction is skipped for a block; how a builder that executes candidates before committing them commits one; and the building policy a builder may apply and a validator never does.

## Motivation

A single block must not carry more data, more storage writes or more new state than nodes can absorb at MegaETH's block rate, whatever the gas its transactions pay; state gas prices new state, but at `m = 1` a thousand new slots cost 97,920,000 gas, which a large block gas limit easily covers.
The block must also always be able to hold the transactions it cannot refuse: deposits, which L1 derivation requires, and the sequencer's own oracle updates, without which the block's transactions read values the chain cannot reproduce.
And a builder that executes transactions ahead of committing them must not commit an outcome computed on a state that another commit since changed.

## Specification

### What a block counts

- `SATIN-BLK-001` A block MUST count, for each transaction it includes, the transaction's regular gas as `max(regular, floor)`, its state gas, its history gas, its history bytes (`SATIN-HIST-022`: zero for a transaction exempt from history gas), its data size, its KV updates and its state growth, as the transaction reports them (see [Two-Pool Gas](../evm/gas-model.md), [History Gas](../evm/history-gas.md) and [Resource Accounting](../evm/resource-accounting.md)).

### The packing budgets

- `SATIN-BLK-002` Three of those counts are limited, each checked before the next transaction runs: data size against `BLOCK_DATA_LIMIT`, KV updates (write records) against `BLOCK_KV_UPDATE_LIMIT`, and state growth (new accounts and new slots) against `BLOCK_STATE_GROWTH_LIMIT`.
- `SATIN-BLK-003` A block reaches a limit when its counter is at or above it.
  The transaction that moves a counter from below its limit to the limit, or past it, MUST be included; once a limit is reached, every later transaction that is neither a deposit nor a Mega System Transaction MUST be skipped before it runs.
  When more than one limit is reached, a node MAY report the skip in the order data size, KV updates, state growth; two nodes need not name the same one, and a skip leaves no field in the block.
- `SATIN-BLK-006` A deposit (a transaction whose envelope is a deposit) and a Mega System Transaction MUST NOT be refused by any of the three budgets, nor by any building policy, and MUST count toward each.
  The block MUST decide this before the transaction runs, from the transaction's envelope and the live system address the block's state names (see [SequencerRegistry](../system-contracts/sequencer-registry.md)): a legacy transaction of the system shape sent from that address is a Mega System Transaction here; a transaction from that address of another shape is treated as any other transaction, and is invalid (see [Mega System Transactions](../system-contracts/system-tx.md)).
- `SATIN-BLK-007` A Mega System Transaction MUST still be held to the block gas limit and, its envelope being legacy, to the block's data-availability footprint (see [Base Layer](../base-layer.md)), which it counts toward; the exemption is from the three packing budgets and from building policy alone.
- `SATIN-BLK-008` Execution gas, state gas and history gas MUST have no block limit beyond the block gas limit, and history bytes MUST be reported and not limited.
- `SATIN-BLK-010` The three packing budgets are protocol values fixed by the spec, the same on every chain; no chain configuration carries them, and a node validating a block MUST hold the block to these values and to no other.
- `SATIN-BLK-012` A transaction's and a block's encoded size MUST NOT be limited by these rules; a block-size rule of the base layer, where a chain adopts one, is the node's to apply and is not one of these limits.

### The block gas limit and skipping

- `SATIN-BLK-009` A transaction's declared gas limit MUST fit in what the block's gas limit has left, as the base layer defines it.
- `SATIN-BLK-013` A transaction MUST be skipped for the current block, and MAY be included in a later one, when:
  - its declared gas limit does not fit in the block's remaining gas;
  - its data-availability footprint does not fit in what the block's gas limit has left for footprints (see [Base Layer](../base-layer.md));
  - it is neither a deposit nor a Mega System Transaction and the block has reached one of its packing budgets;
  - it is not a deposit and the block admits only deposits (see [Base Layer](../base-layer.md)).

  A block that contains a transaction these rules skip MUST be invalid.

### Committing a candidate

- `SATIN-BLK-004` A builder that executes several candidate transactions before it commits one MUST hold each candidate, when it commits it, to the block's packing budgets, the block gas limit and the data-availability footprint again, on the block as it then stands; a candidate that no longer fits MUST NOT be committed.
  A validator commits every transaction before it executes the next, so for it the second check finds what the first found.
- `SATIN-BLK-005` Such a builder MUST NOT commit a candidate whose sender's nonce or balance — the system address's, for a Mega System Transaction — another commit changed after the candidate executed; the refusal is a fault of the builder's ordering, neither a verdict on the block nor on the transaction, which the builder executes again.
  Any other state a candidate read and a later commit changed is the builder's to account for, by executing the candidate again; a candidate that read the Oracle before a Mega System Transaction that writes it, and is committed after that transaction, commits the value it read.

### Building policy

- `SATIN-BLK-011` A block builder MAY pack tighter than these rules, as building policy: it MAY refuse a transaction for its declared gas limit, its encoded size or its data-availability size, hold the block to an encoded-size or data-availability budget, and hold any of the three packing budgets below the protocol's value, never above it; and it MAY pack fewer transactions than the budgets allow by not selecting them.
  A building policy MUST NOT refuse a deposit or a Mega System Transaction: none of its per-transaction limits or budgets applies to either, and a policy's cap on a packing budget does not.
  A deposit counts toward the block's encoded size and not toward its data-availability size; a Mega System Transaction counts toward both.
  A node validating a block MUST NOT apply a building policy, and a block is not invalid for a transaction a building policy would have skipped.

## Constants

| Constant                   | Value      | Description                                                 |
| -------------------------- | ---------- | ----------------------------------------------------------- |
| `BLOCK_DATA_LIMIT`         | 13,107,200 | The block's data-size budget, in bytes (12 MiB + 512 KiB)   |
| `BLOCK_KV_UPDATE_LIMIT`    | 500,000    | The block's KV-update budget, in write records              |
| `BLOCK_STATE_GROWTH_LIMIT` | 1,000      | The block's state-growth budget, in new accounts and slots  |

## Rationale

**Why are the budgets checked before a transaction runs, not after?**
A block cannot know what a transaction will count before it runs, and refusing a transaction after it ran would waste the work; including the transaction that reaches a budget and skipping the next keeps the budget a bound that is overshot by at most one transaction's counts, which the per-transaction limits bound in turn.

**Why do deposits and Mega System Transactions count but are never refused?**
A deposit is derived from L1 and must be included; a Mega System Transaction is the sequencer's own oracle update, which the block's other transactions may depend on.
Rex6 skipped every later candidate, deposits included, once a counter reached its limit; a budget the block's other transactions used up must not keep either out.
The exemption covers KV updates and state growth for the same reason it covers data size: refusing one for any budget would make the same transaction valid on one budget and skippable on another.

**Why does state gas not replace the state-growth budget?**
At `m = 1`, 1,000 new slots cost 97,920,000 state gas; a block gas limit above that does not stop the 1,001st slot, and the count is what bounds state per block.

**Why are the budgets protocol values?**
A validator must hold every block to the same values; a budget a configuration could set would make the same block valid on one chain's nodes and invalid on another's.

**Why does a validator never apply a building policy?**
A policy decides which transactions a builder packs, not what a packed block computes; a validator that applied one would reject blocks built under a looser one, which are valid.

**Why refuse a stale commit?**
Committing a candidate whose sender's nonce or balance changed would write the sender's account over what the other commit did: the nonce would go backwards or the balance would be wrong.
Other stale reads change the candidate's result but not the consistency of the state, so they are the builder's to resolve.

## Security Considerations

- A node that refuses a deposit for a packing budget cannot build or validate the block the derivation requires.
- A node that refuses a Mega System Transaction for a budget lets the block's other transactions crowd out the oracle update they read, so their reads cannot be reproduced.
- A node that does not count deposits and Mega System Transactions toward the budgets lets a block exceed them by their counts.
- A validator that applies a builder's policy rejects valid blocks.
- A builder that commits a stale candidate writes an inconsistent sender account into the block.

## Spec History

- [Rex6](../../upgrades/rex6.md) — Block limits on data size, KV updates and state growth that skip every later candidate, deposits included; specified in [Resource Limits](../../evm/resource-limits.md).
- [Satin](../../upgrades/satin.md) — The three limits as packing budgets that never refuse a deposit or a Mega System Transaction; building policy separated from validation.
