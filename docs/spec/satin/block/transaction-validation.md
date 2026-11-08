---
description: Satin (unstable) — Transaction Validation and Refusals. The checks a transaction is held to before inclusion, their order and the error each names, the chain-id rule, and how a deposit that fails one is included instead.
spec: Satin
maturity: unstable
---

# Transaction Validation and Refusals

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
{% endhint %}

Abstract: The checks a transaction must pass before it can be included in a block — the body's data size, the intrinsic gas with the body's history gas, the calldata floor, the execution cap, the system-address shape and the chain id — the order in which Satin's own checks are made and the error each names, and the rule that a deposit failing a check is included as a failed deposit rather than rejected.

## Motivation

A transaction a node rejects never reaches a block; one it includes changes state and pays for what it ran.
Two nodes that refuse different transactions build or accept different blocks, and a transaction pool that refuses for another reason than block execution keeps transactions no block can hold, or drops ones it could.
Beyond the base layer's checks, a transaction can carry a body too large for the transaction's data-size limit, a gas limit that cannot pay the history gas of its body, or a gas limit above the execution cap with intrinsic gas that does not fit under it; and a transaction signed for another chain, or a typed transaction without a chain id, can be replayed on MegaETH unless its chain id is checked.

## Specification

### What a transaction is rejected for

- `SATIN-VAL-001` A transaction MUST be rejected when its body, with `WRITE_RECORD_SIZE` bytes for every entry of its authorization list, exceeds the transaction's data-size limit (see [Resource Limits](../evm/resource-limits.md)), unless it is system-originated (see [Mega System Transactions](../system-contracts/system-tx.md)).
  Every entry counts, whether its authorization will apply or not.
  The body's size is the one [Resource Accounting](../evm/resource-accounting.md) counts as data size.
- `SATIN-VAL-002` A transaction MUST be rejected:
  - when its gas limit is below its intrinsic regular gas plus the history gas of its body (`CallGasCostMoreThanGasLimit`);
  - when its floor — the [EIP-7623](https://eips.ethereum.org/EIPS/eip-7623) floor as Amsterdam computes it — exceeds its gas limit (`GasFloorMoreThanGasLimit`);
  - when its gas limit exceeds `EXECUTION_CAP` while its intrinsic regular gas or its floor exceeds `EXECUTION_CAP` (`GasFloorMoreThanGasLimit`).

  The intrinsic regular gas and the floor are those of [Gas Schedule and Intrinsic Gas](../evm/gas-schedule.md); the body's history gas is that of [History Gas](../evm/history-gas.md).
- `SATIN-VAL-005` A transaction whose caller is the live system address and that does not have the system shape MUST be rejected, unless it is a deposit (see [Mega System Transactions](../system-contracts/system-tx.md), `SATIN-MST-003`).
- `SATIN-VAL-006` A transaction MUST be rejected when it carries a chain id that is not the chain's, or when it is a typed transaction (any type but legacy and deposit) and carries none.
  A legacy transaction without a chain id (pre-[EIP-155](https://eips.ethereum.org/EIPS/eip-155)) is valid, unless it is a Mega System Transaction, which MUST carry one (`SATIN-MST-005`).
  A node MUST make this check whatever its configuration says.
- `SATIN-VAL-007` A transaction MUST be rejected when it is a Mega System Transaction that fails its chain-id, nonce or EIP-3607 check (`SATIN-MST-005`), and when it fails any validation of the base layer (see [Base Layer](../base-layer.md)).

### Order

- `SATIN-VAL-003` Satin's own checks MUST be made in this order, and the first that fails names the transaction's refusal:
  1. the body with its authorization records against the data-size limit, before any gas is looked at — an invalid transaction whose reason is that the body and authorization records exceed the transaction data-size limit;
  2. the gas limit against the intrinsic regular gas alone — `CallGasCostMoreThanGasLimit`, carrying the intrinsic regular gas;
  3. the floor against the gas limit — `GasFloorMoreThanGasLimit`;
  4. the execution cap — `GasFloorMoreThanGasLimit`, carrying the larger of the intrinsic regular gas and the floor, against `EXECUTION_CAP`;
  5. the gas limit against the intrinsic regular gas plus the body's history gas — `CallGasCostMoreThanGasLimit`, carrying that sum.

  So a gas limit that covers the intrinsic regular gas but neither the floor nor the body's history gas is refused for the floor.
  Where a transaction also fails a check of the base layer, or the system-shape or chain-id check, which of the failures the node reports is not specified: only that the transaction is refused.
- `SATIN-VAL-004` The body and the records of the authorities a transaction applies are all the data size it counts before its first frame, so a transaction that passes validation MUST NOT be stopped by the data-size limit before its first frame.

### Deposits and faults

- `SATIN-VAL-008` A deposit MUST NOT be rejected for failing a validation check: a deposit that fails any check of this page, or of the base layer, MUST be included as a failed deposit instead (see [Deposit Transactions](deposits.md)).
  A Mega System Transaction is a legacy transaction until it has passed its own chain-id, nonce and EIP-3607 checks, so failing one of those is a rejection; once it has passed them it runs as a deposit, and a check it fails after that includes it as a failed deposit.
  A read the node fails to make — a database read, a bucket-capacity read, the registry read — is not a validation check, for a deposit as for any transaction: the transaction gets no outcome, as [Halts, Reverts and Stops](../evm/outcomes.md) specifies, and the node reports it as `SATIN-VAL-010` classifies it.
- `SATIN-VAL-010` A read a node fails to make for a transaction MUST be reported by its cause, and the transaction MUST NOT be settled, as a failed deposit or otherwise:
  - a failed bucket-capacity read, always as an internal error of the node (`SATIN-STATE-007`);
  - a failed database read the transaction's execution makes — in its validation, the registry read of `SATIN-REG-002` among them, in a frame, in the authorization list's simulation or application, or in a charge made before the first frame — as an internal error when the node's database declares the error fatal, and otherwise as an invalid block, as for a pre-block call (`SATIN-PBLK-006`);
  - a failed read the block's execution makes for the transaction outside its execution — the live system address the block reads to decide whether the transaction is a Mega System Transaction (`SATIN-BLK-006`), the sender's account before the transaction runs, the L1 block contract's account and the footprint gas scalar before a non-deposit transaction — always as an internal error, as the activation check's is.

  A node that meets such a failure reaches no verdict on the block except the invalid block of the second case, and cannot execute the block past that transaction.

### Retired rule ids

- `SATIN-VAL-009` Retired, removed: what a transaction pool can decide without state is node documentation, outside the specification.

## Constants

| Constant            | Value       | Description                                                              |
| ------------------- | ----------- | ------------------------------------------------------------------------ |
| `WRITE_RECORD_SIZE` | 40          | Data-size bytes of one write record (see [Resource Accounting](../evm/resource-accounting.md)) |
| `EXECUTION_CAP`     | 200,000,000 | The most regular gas a transaction runs on (see [Two-Pool Gas](../evm/gas-model.md)) |

## Rationale

**Why count every authorization entry against the body?**
Each authorization that applies makes a write record before the first frame; counting one for every entry, applied or not, makes the check decidable without state, so a pool can make it, and keeps a transaction that passes from crossing the data-size limit before its first frame.

**Why check the body before any gas?**
The body's size is known before anything is priced, and its refusal does not depend on the gas limit.
At the spec's prices the calldata floor and the execution cap already hold a body with its records well under the data-size limit, so the check refuses no transaction the gas checks admit; it is kept so that the limit holds whatever the prices become.

**Why the floor before the history?**
The base layer checks the intrinsic gas, then the floor; Satin adds the body's history gas as a separate, last check, so the reason a transaction names for a refusal does not change with the history price.

**Why fix only the order of Satin's own checks?**
The order names the error a pool reports for a transaction Satin refuses; the base layer's checks around them differ in order between implementations, and a transaction failing two checks at once is refused either way.

**Why is the chain-id check on?**
Rex6 ran with the check off, so a transaction signed for another chain, or a typed transaction without a chain id, was valid on MegaETH.
A pre-EIP-155 legacy transaction stays valid, as it is on Ethereum, so that Nick's-method deployments and other pre-signed transactions remain possible; a Mega System Transaction, which needs replay protection, must carry one.

**Why is pool behaviour not specified?**
What a pool can check without state follows from these rules; how a pool reports or orders transactions does not decide any block, and is node documentation.
Validation that reads no state cannot tell whether a recipient, a created account or an authority is new: those charges are made when the transaction runs, and a gas limit that cannot pay them runs out of gas rather than being refused.

## Security Considerations

- A node that does not reject a transaction whose body exceeds the data-size limit lets it be included and then fail on every node that does; the block is then invalid for those nodes.
- A node that leaves the chain-id check off accepts transactions replayed from other chains.
- A node that rejects a deposit for a validation failure instead of including it as a failed deposit refuses a transaction the L1 derivation requires the block to hold, and so cannot build or validate that block.
- A node that treats a failed state read as a validation failure includes as failed, or rejects, a transaction every other node executes.

## Spec History

- [Rex5](../../upgrades/rex5.md) — Ordered the Mega-side gas validation.
- [Rex6](../../upgrades/rex6.md) — The chain-id check is off in every configuration; the Rex6 limits are specified in [Resource Limits](../../evm/resource-limits.md).
- [Satin](../../upgrades/satin.md) — The body's data-size check, the history-inclusive intrinsic check, the execution-cap check, and the chain-id check on.
