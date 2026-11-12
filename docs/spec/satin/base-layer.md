---
description: Satin (unstable) — Base Layer. Optimism Karst (Ethereum Osaka) as Satin's base, the opcodes Satin adds, the inherited transaction gas caps it does not apply, and the Karst block rules it keeps.
spec: Satin
maturity: unstable
---

# Base Layer

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
{% endhint %}

Abstract: The base Satin builds on, Optimism Karst with its Ethereum base Osaka; the opcodes Satin enables that Osaka does not have; the inherited per-transaction gas caps Satin does not apply; the Karst block rules — deposit-only activation blocks, the data-availability footprint, and pricing against the block's L1 information — as they apply to MegaETH blocks; and the value transfers whose overflow lies outside the specification.

## Motivation

A MegaETH node executes standard EVM, transaction and block rules for everything MegaETH does not change, and two nodes that take those rules from different bases execute different chains.
The Rex-era specs build on Optimism Isthmus (Ethereum Prague).
Optimism Karst carries Jovian's and Karst's block rules (deposit-only activation blocks, the data-availability footprint limit, the operator fee) and Osaka's EVM changes; a node that ran MegaETH's rules on Isthmus would miss those, and one that applied Karst's inherited transaction caps would refuse MegaETH's large transactions: EIP-7825 caps a transaction's gas limit at 16,777,216, and EIP-8037 caps a transaction's total gas at 2^32 − 1, while a MegaETH transaction's gas limit is bounded only by its block's.

## Specification

The rules of this page apply to every block from Satin's activation on (see [Activation and Rex-Era Carry-Over](block/activation.md)).

### The base

- `SATIN-BASE-001` Every standard EVM, transaction and block rule that the Satin section does not override MUST be Optimism Karst's, including the Optimism changes of Jovian and Karst and the Ethereum changes of Osaka (for example `CLZ` of [EIP-7939](https://eips.ethereum.org/EIPS/eip-7939)).
  Satin follows the Optimism forks it requires — Karst, Jovian and their predecessors — with their whole transaction and block rule set, the data-availability footprint gas scalar, the blob gas used a block reports and the fee rules among them, and not rule by rule.
  Where a page of the Satin section states a rule, that rule MUST be applied in place of the base layer's.

### Inherited caps not applied

- `SATIN-BASE-002` A node MUST NOT apply the per-transaction gas limit cap of [EIP-7825](https://eips.ethereum.org/EIPS/eip-7825).
  A transaction's gas limit MUST be bounded by what its block's gas limit has left (see [Block Limits and Packing](block/block-limits.md)); its regular gas is bounded by the execution cap (see [Two-Pool Gas](evm/gas-model.md)).
  A block builder MAY refuse a larger declared gas limit as building policy, which a node validating a block MUST NOT apply (see [Block Limits and Packing](block/block-limits.md)).
- `SATIN-BASE-003` A node MUST NOT apply the [EIP-8037](https://eips.ethereum.org/EIPS/eip-8037) per-transaction cap `TX_MAX_TOTAL_GAS_LIMIT` on a transaction's total gas.

### Opcodes

- `SATIN-BASE-004` A node MUST enable `DUPN` (`DUPN_OPCODE`), `SWAPN` (`SWAPN_OPCODE`) and `EXCHANGE` (`EXCHANGE_OPCODE`) as [EIP-8024](https://eips.ethereum.org/EIPS/eip-8024) as of [commit `34b49095ca`](https://github.com/ethereum/EIPs/commit/34b49095ca5f7343045da279f04e7ecd1e451393) (10 June 2026) defines them, the revision current when the EIP-8037 profile was frozen (see [Two-Pool Gas](evm/gas-model.md)).
- `SATIN-BASE-005` A node MUST enable `SLOTNUM` (`SLOTNUM_OPCODE`) of [EIP-7843](https://eips.ethereum.org/EIPS/eip-7843) as of [commit `e44e1960a9`](https://github.com/ethereum/EIPs/commit/e44e1960a9328282af8dd884837c2302f6a45c3d) (17 September 2026), and `SLOTNUM` MUST push zero in every block.
  `SLOTNUM` is a read of the block environment: it is a volatile read for [gas detention](evm/gas-detention.md), and a frame whose volatile-data access is off is refused it (see [MegaAccessControl](system-contracts/mega-access-control.md)).

### Deposit-only activation blocks

- `SATIN-BASE-006` A block in which Satin activates, or in which an Optimism fork at or after Jovian in the Optimism fork order activates, MUST contain only deposit transactions.
  A non-deposit transaction in such a block MUST make the block invalid.
  The rule covers Jovian, Karst and every later Optimism fork the chain configuration schedules.
- `SATIN-BASE-007` A fork MUST be taken to activate in a block when the chain configuration schedules it, it is active at the block's timestamp, and it is not active at the parent block's timestamp.
  A fork the chain configuration does not schedule MUST NOT be taken to activate in any block.
- `SATIN-BASE-008` A Mega System Transaction is a legacy transaction, so a block that admits only deposits MUST NOT contain one either.
  The block in which Satin activates therefore carries no Mega System Transaction, and no Oracle read in it asks the oracle service (see [Oracle](system-contracts/oracle.md), `SATIN-ORCL-005`).
  A deposit can still write the Oracle in that block through code running at the live system address, as the Oracle's bytecode allows (`SATIN-ORCL-011`).

### The data-availability footprint

- `SATIN-BASE-009` A non-deposit transaction's data-availability footprint MUST be its estimated compressed size, as the Optimism Fjord specification estimates it, times the data-availability footprint gas scalar the L1 block contract (`L1_BLOCK_ADDRESS`) holds when the transaction is about to run; with no contract or no scalar in state the scalar MUST be taken as zero.
  A Mega System Transaction is a non-deposit transaction and has a footprint; a deposit has none.
  The footprints of a block's non-deposit transactions MUST accumulate against the block's gas limit: the sum MUST NOT exceed the block's gas limit, and the block MUST report the sum as its blob gas used.
  A transaction whose footprint does not fit in what the block's gas limit has left for footprints MUST NOT be included in the block (see [Block Limits and Packing](block/block-limits.md)).

### Pricing against the L1 block information

- `SATIN-BASE-010` Every non-deposit transaction that pays an L1 fee — every non-deposit transaction but a Mega System Transaction, which pays no fee (`SATIN-MST-005`) — MUST be priced against the L1 block information the block's own L1 attributes deposit wrote.
  That information MUST be what the L1 block contract holds on the state left by the transactions before the block's first non-deposit transaction other than a Mega System Transaction, and it MUST hold for every later transaction of the block.
  The data-availability footprint gas scalar is the exception: it MUST be read from the contract again before each non-deposit transaction, a Mega System Transaction included.
  The contract's slots are read as the base layer's fee computation and footprint read them, when they need them; that every slot either read makes is in the block's witness is specified in [The Stateless Witness](block/stateless-witness.md) (`SATIN-WIT-011`).

### Outside the specification

- `SATIN-BASE-011` A state from which a transaction's execution reaches a value transfer that would push the recipient's balance above 2^256 − 1 is an invalid prestate, and the execution of such a transaction lies outside this specification, whatever it would do next.
  This holds for every value transfer: a transaction's value, a deposit's included, a `CALL`'s value, a `SELFDESTRUCT`'s balance sent to its beneficiary, and a creation's endowment of the account it creates.
  A deposit's mint that would overflow its sender's balance is the same case, stated in [Deposit Transactions](block/deposits.md) (`SATIN-DEP-011`).

## Constants

| Constant                 | Value                                        | Description                                                         |
| ------------------------ | -------------------------------------------- | ------------------------------------------------------------------- |
| `DUPN_OPCODE`            | `0xE6`                                       | EIP-8024 `DUPN`                                                     |
| `SWAPN_OPCODE`           | `0xE7`                                       | EIP-8024 `SWAPN`                                                    |
| `EXCHANGE_OPCODE`        | `0xE8`                                       | EIP-8024 `EXCHANGE`                                                 |
| `SLOTNUM_OPCODE`         | `0x4B`                                       | EIP-7843 `SLOTNUM`                                                  |
| `TX_MAX_TOTAL_GAS_LIMIT` | 2^32 − 1                                     | EIP-8037's cap on a transaction's total gas, which is not applied   |
| `L1_BLOCK_ADDRESS`       | `0x4200000000000000000000000000000000000015` | The OP Stack L1 block contract, which holds the block's L1 information |

## Rationale

**Why Karst rather than Isthmus?**
Karst is the Optimism base that carries the Osaka EVM and the Jovian and Karst block rules the OP Stack runs on.
Restating MegaETH's rules on it keeps a Satin node an OP Stack node for every rule MegaETH does not change, instead of a fork of an older base.

**Why take the base forks' rule set whole?**
Rex6 runs on Isthmus; Satin takes Karst, Jovian and their predecessors with every transaction and block rule they bring, the ones that change what a Rex6 block computes included — a Mega System Transaction's data-availability footprint, the blob gas used a block reports, the operator fee — rather than adopting them one by one.
A node that took some of a base fork's rules and not others would be no OP Stack node, and every such choice would be one more rule MegaETH must specify and maintain against the base.

**Why drop EIP-7825 and EIP-8037's transaction caps?**
Both exist to bound the work of one Ethereum transaction.
On MegaETH that bound is the execution cap on regular gas, 200,000,000, and the per-transaction resource limits; the rest of a large gas limit can pay only state and history gas.
Keeping a 16,777,216 or a 2^32 − 1 cap on the gas limit would refuse transactions the execution cap already bounds.

**Why does `SLOTNUM` push zero?**
EIP-7843 defines the slot number from the beacon chain's slot, which MegaETH does not have; the OP Stack has no slot either and supplies zero.
A fixed zero keeps the opcode a function of nothing a validator must be given, and it stays a volatile read so that a contract that branches on it is treated as one that reads the block environment.

**Why is the footprint scalar read before each transaction?**
The Karst rule reads the scalar per transaction, and a Mega System Transaction can sit between two user transactions; reading it again for each one keeps the footprint of every transaction the one the state before it implies.
The other L1 fields are fixed for the block once its L1 attributes deposit and the deposits before the first user transaction have run.

**Why is a value transfer that overflows its recipient's balance outside the specification?**
No chain can reach it: all the ether in existence is about 1.2 × 10^26 wei, far below 2^256, and every balance is part of it.
Implementations differ on it — one saturates the recipient's balance, one wraps it, one fails the call — and defining one would bind every node to a behaviour no block can exercise; a deposit's mint is outside the specification for the same reason (`SATIN-DEP-011`).

**Why do the footprint and the operator fee cost nothing at activation?**
Satin starts from the L1 block contract the Rex era left, whose footprint and operator fee scalars are zero (see [Activation and Rex-Era Carry-Over](block/activation.md)); both take effect once that contract is upgraded and the scalars are set, which Satin itself does not do.

## Security Considerations

- A node that applies EIP-7825's or EIP-8037's transaction cap refuses transactions every other node includes, and so builds or validates a different chain.
- A node that skips the deposit-only rule accepts an activation block a correct node refuses: the fork's own upgrade transactions, which are deposits, would then run behind user transactions on a state the fork did not expect.
- A node that reads the L1 information before the block's L1 attributes deposit ran prices the block's transactions against the previous L1 origin, so its fees, and the balances that pay them, differ from every other node's.
- A node that does not count Mega System Transactions towards the data-availability footprint admits a block whose footprint exceeds its gas limit.
- A node that pushes anything but zero for `SLOTNUM` computes another state for any contract that reads it.

## Spec History

- [Rex6](../upgrades/rex6.md) — The Rex era builds on Optimism Isthmus (Ethereum Prague); `DUPN`, `SWAPN`, `EXCHANGE` and `SLOTNUM` are undefined there.
- [Satin](../upgrades/satin.md) — Optimism Karst (Ethereum Osaka) as the base, four added opcodes, no EIP-7825 or EIP-8037 transaction cap; a value transfer that would overflow its recipient's balance outside the specification.
