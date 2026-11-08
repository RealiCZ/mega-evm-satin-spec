---
description: Satin (unstable) — State Gas and SALT Pricing. How a state charge is priced — EIP-8037's byte counts at MegaETH's cost per state byte, scaled by the multiplier of the SALT bucket the state lands in — where each state charge is made, how it is given back, and what a failed bucket read means.
spec: Satin
maturity: unstable
---

# State Gas and SALT Pricing

{% hint style="warning" %}
**Unstable** — Satin is under active development: every value and rule on this page may change before Satin is frozen.
{% endhint %}

Abstract: [State gas](../../glossary.md#state-gas) prices the state a transaction adds — a fresh storage slot, a new account, a created contract, its code, a delegation indicator — at `entry × m`: EIP-8037's byte count of the state at MegaETH's cost per state byte, times the multiplier of the [SALT bucket](../../glossary.md#salt-bucket) the state lands in.

## Motivation

State a transaction adds is kept by every node for as long as it exists, so its price has to reflect what it costs to hold, not what it costs to compute.
In SALT the cost of holding an entry grows with the bucket it lands in: a bucket that fills doubles, so a write into a crowded region of the state makes the node carry more than a write into a sparse one.

Under Rex6 state was priced `base × (multiplier − 1)`, so a slot or account in a minimum-size bucket cost no storage gas at all: most new state was free, and the price only appeared once the state was already crowded.
A price that reads the bucket again at each charge also lets a give-back return a different amount than the charge took, if the bucket changed in between.

## Specification

### The price of a state charge

- `SATIN-STATE-001` Every EIP-8037 state charge MUST be `entry × m`:
  - `entry` — the schedule's state-gas entry ([Gas Schedule and Intrinsic Gas](gas-schedule.md)): EIP-8037's byte count of the state times `COST_PER_STATE_BYTE`.
  - `m` — the multiplier of the SALT bucket the state lands in (`SATIN-STATE-002`).
- `SATIN-STATE-002` The multiplier of a bucket MUST be `m = floor(bucket_capacity / MIN_BUCKET_SIZE)`.
  - `bucket_capacity` — the capacity SALT holds for the bucket in the state the block executes on.
- `SATIN-STATE-003` The states a state charge prices, their byte counts, and the bucket each lands in MUST be:

  | State                                                                  | Bytes                          | `entry` at `m = 1` | Bucket                |
  | ---------------------------------------------------------------------- | ------------------------------ | ------------------ | --------------------- |
  | Fresh storage slot (`SSTORE`, original and present zero, new non-zero) | `SLOT_STATE_BYTES` = 64        | 97,920             | The slot's            |
  | New account                                                            | `ACCOUNT_STATE_BYTES` = 120    | 183,600            | The account's         |
  | Created contract account                                               | `ACCOUNT_STATE_BYTES` = 120    | 183,600            | The created account's |
  | Deployed code, per byte                                                | `CODE_STATE_BYTES` = 1         | 1,530              | The created account's |
  | EIP-7702 delegation indicator                                          | `DELEGATION_STATE_BYTES` = 23  | 35,190             | The authority's       |

- `SATIN-STATE-010` The SALT bucket an account or a storage slot lands in MUST be the bucket [SALT](https://github.com/megaeth-labs/salt)'s own definition assigns to its key: the mapping from an account or a slot to its bucket is an input to this specification, as the bucket capacities are, and is not restated here.
- `SATIN-STATE-005` `m` MUST scale state gas and nothing else: regular gas and history gas are never scaled.

### Where state is charged

- `SATIN-STATE-004` A state charge MUST be made where the state is added:
  - a fresh slot, by the `SSTORE` that fills it (`SATIN-STATE-008`);
  - a new account, by the `CALL` that moves value to an account empty under EIP-161, by a `SELFDESTRUCT` that moves a non-zero balance to a distinct account empty under EIP-161, by the transaction whose value goes to a recipient empty under EIP-161, by an applied EIP-7702 authorization whose authority the state holds no account for, by a deposit or a Mega System Transaction whose caller is empty under EIP-161 ([Deposit Transactions](../block/deposits.md)), and by a keyless deployment whose signer's account is empty under EIP-161 ([KeylessDeploy](../system-contracts/keyless-deploy.md));
  - a created account, by `CREATE`, `CREATE2` or a creation transaction, when the created address is empty under EIP-161, and by a keyless deployment's creation ([KeylessDeploy](../system-contracts/keyless-deploy.md));
  - deployed code, at the code deposit ([Gas Schedule and Intrinsic Gas](gas-schedule.md));
  - a delegation indicator, by the applied authorization that writes it ([EIP-7702 Authorizations Before the First Frame](authorizations.md)).

  When each of these is charged relative to the opcode's other charges is specified on [History Gas and the History Allowance](history-gas.md) and [Gas Schedule and Intrinsic Gas](gas-schedule.md); how it draws the pools is `SATIN-POOL-008` ([Two-Pool Gas](gas-model.md)).
- `SATIN-STATE-011` Every new-account and created-account charge of `SATIN-STATE-004`, and the state-growth rise that goes with it ([Resource Accounting](resource-accounting.md)), MUST be decided, when the charge is decided, by one of two predicates:
  - **existence**, for the authority of an applied EIP-7702 authorization alone: the authority is new when the state holds no account at its address; an account whose leaf the state holds is not new, an account empty under EIP-161 included ([EIP-7702 Authorizations Before the First Frame](authorizations.md));
  - **EIP-161 emptiness**, for every other site — a deposit's or Mega System Transaction's caller, a value call's recipient, a transaction's value recipient, a `SELFDESTRUCT`'s beneficiary, a created address and a keyless deployment's signer: the account is new when the state holds no account at the address, or the account it holds has nonce zero, zero balance and no code.

  At a site decided by emptiness, an account whose leaf is in the state but is empty under EIP-161 is charged and counted as an absent one.
  Apart from an authority's charge, the distinction between no account and an empty leaf is made only by the witness ([The Stateless Witness](../block/stateless-witness.md)) and by the destruction table ([SELFDESTRUCT and the Destruction Table](selfdestruct.md)).
- `SATIN-STATE-008` The only `SSTORE` that charges fresh-slot state gas MUST be one whose original value in the transaction is zero, whose present value is zero, and whose new value is not zero.
  The only `SSTORE` that gives it back MUST be one whose original value is zero, whose present value is not zero, and whose new value is zero, unless the slot's account is marked for deletion ([SELFDESTRUCT and the Destruction Table](selfdestruct.md)); the give-back MUST be the price the slot was charged, credited to the frame running that `SSTORE` whichever frame paid the charge, in the refill order of [History Gas and the History Allowance](history-gas.md) (`SATIN-HIST-007`).
  Every other `SSTORE` transition MUST charge no fresh-slot state gas and give none back.
  These are the same transitions as the state-growth change of an `SSTORE` ([Resource Accounting](resource-accounting.md)).
- The first effective `SELFDESTRUCT` of an account created in the same transaction gives back the state gas of each part the destruction table names; that rule is `SATIN-SD-005` ([SELFDESTRUCT and the Destruction Table](selfdestruct.md)).

### Reading a bucket

- `SATIN-STATE-006` A node MUST read a bucket's capacity at most once per transaction: every later state charge, and every give-back, in that bucket during the transaction MUST use the same `m`, so a give-back cancels its charge exactly.
- `SATIN-STATE-007` A bucket capacity below `MIN_BUCKET_SIZE`, or one the node cannot read, is a fault of the node, for a deposit as for any transaction: the transaction MUST NOT be priced at any multiplier and MUST NOT be settled, and the node MUST report an internal error.
  The transaction then has no outcome ([Halts, Reverts and Stops](outcomes.md)).
- `SATIN-STATE-009` A system-originated transaction and a system call ([Mega System Transactions and the Protocol's Own Transactions](../system-contracts/system-tx.md)) MUST be priced at `m = 1` and MUST NOT read a bucket capacity.
  A deposit that is not system-originated MUST be priced by its buckets, although it pays no history gas ([History Gas and the History Allowance](history-gas.md)).

At `m = 1` every state charge is the schedule's own number: a fresh slot or account in a minimum-size bucket pays its state gas.

### Retired ids

None.

## Constants

| Constant                 | Value | Description                                                         |
| ------------------------ | ----- | ------------------------------------------------------------------- |
| `COST_PER_STATE_BYTE`    | 1,530 | Gas per byte of new state (EIP-8037 `COST_PER_STATE_BYTE`)          |
| `MIN_BUCKET_SIZE`        | 256   | The smallest SALT bucket capacity, at which `m = 1`                 |
| `SLOT_STATE_BYTES`       | 64    | EIP-8037 byte count of a storage slot                               |
| `ACCOUNT_STATE_BYTES`    | 120   | EIP-8037 byte count of an account leaf, new or created              |
| `CODE_STATE_BYTES`       | 1     | EIP-8037 byte count per byte of deployed code                       |
| `DELEGATION_STATE_BYTES` | 23    | EIP-8037 byte count of an EIP-7702 delegation indicator             |

## Rationale

**Why `entry × m` instead of `base × (multiplier − 1)`?**
Rex6's formula priced a write into a minimum-size bucket at nothing, so almost all new state was free until a region was already crowded.
Multiplying the whole entry makes every new slot and account pay for the bytes EIP-8037 counts, and keeps the SALT scaling that charges a crowded region more.

**Why MegaETH's own cost per state byte?**
EIP-8037's byte counts measure what a leaf, a slot or an indicator occupies, and Satin keeps them; the price of a byte is a property of the chain that stores it, so MegaETH sets its own.
At 1,530 per byte the entries happen to equal Amsterdam's; they are rebuilt from the byte count so that a change of the byte price moves them all together.

**Why one multiplier per bucket per transaction?**
A give-back must cancel its charge exactly, or a slot written and cleared in one transaction would earn or lose gas.
Reading the bucket once fixes `m` for the whole transaction, and it bounds the bucket reads a transaction makes, which a stateless validator must be given.

**Why is a failed bucket read a fault and not an outcome?**
A bucket read failing is a defect of the node or of the witness it was given, not something the transaction did; settling the transaction at any price would make its outcome depend on the node's failure.
So the transaction gets no outcome, and the node reports the fault.

**Why reference SALT's mapping instead of restating it?**
The bucket a key lands in is SALT's own definition, as the capacities are SALT's state; this specification prices by the bucket SALT names, and two nodes that disagree on the mapping disagree on SALT itself.

**Why EIP-161 emptiness, and existence for an authority?**
Since EIP-161 Ethereum treats an empty account as a dead one: `CALL` charges its new-account cost for a value sent to an empty account, whether or not a leaf is stored for it, and Ethereum's Amsterdam specification decides a value call's, a `SELFDESTRUCT`'s and a creation's new account by that test.
Using it at every such site — a value call, a `SELFDESTRUCT`'s beneficiary, a transaction's recipient, a deposit's caller, a created address — keeps an empty leaf from being priced as new at one site and as existing at another, and keeps the state gas and the state-growth count of the same account in step.
EIP-7702 decides its authority differently, by whether the authority exists in the trie, and the Amsterdam specification charges an authority's new account by that test; Rex6 did the same, so an authority keeps it.
The witness still tells an empty leaf from no account, because a stateless validator must be able to rebuild the state root, and the destruction table still reads the leaf's presence at the transaction's start, because it gives back only what the transaction added.

## Security Considerations

- If a node read a bucket more than once in a transaction and the capacity differed, a give-back would not cancel its charge, and a transaction could mint gas by writing and clearing slots.
- If a node priced a failed or impossible capacity (below `MIN_BUCKET_SIZE`) at some multiplier, two nodes failing differently would settle the same transaction at different prices.
- If a node mapped keys to buckets with another function than SALT's, its prices would differ from the chain's on every state charge outside a minimum-size bucket.
- If the protocol's own transactions read buckets, a block's pre-block calls and its Mega System Transactions would depend on SALT reads a stateless validator is not given.
- If `m` scaled regular gas, the execution cap would bound less computation in crowded regions of the state than in sparse ones.

## Spec History

- [Satin](../../upgrades/satin.md) — Replaced the Rex6 dynamic storage gas `base × (multiplier − 1)` of the [Dual Gas Model](../../evm/dual-gas-model.md) with EIP-8037 state gas at `entry × m`, so new state in a minimum-size bucket is no longer free.
