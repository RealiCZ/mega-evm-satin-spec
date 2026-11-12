---
description: Satin (unstable) — High-Precision Timestamp. The sub-second timestamp wrapper over the Oracle's storage: its address, code, interface, storage allocation and service guarantees, its reads following the Satin Oracle and detention rules.
spec: Satin
maturity: unstable
---

# High-Precision Timestamp

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
{% endhint %}

Abstract: The High-Precision Timestamp system contract, a wrapper that reads a microsecond timestamp out of the Oracle's storage: its address, code, interface, the Oracle slots allotted to it, the guarantees the timestamp service gives, and how its reads are answered and priced.

## Motivation

`block.timestamp` has a resolution of one second, and MegaETH produces several blocks a second, so blocks share a timestamp.
Contracts that order events in time — auction deadlines, time-weighted prices — need a finer clock.
The timestamp is served through the Oracle's storage; nodes and contracts must agree on the wrapper's address, its interface and the slots it reads, and on how those reads are answered, or the same call reads different times.

## Specification

- `SATIN-HPTS-001` The High-Precision Timestamp MUST be the account at `HIGH_PRECISION_TIMESTAMP_ADDRESS` holding the code `HIGH_PRECISION_TIMESTAMP_CODE_HASH` (see [System Contracts](overview.md)); it has no interceptor, and its interface, storage allocation and service are the following.
  - **Interface.**
    `timestamp() returns (uint256)` returns the value at Oracle slot `TIMESTAMP_BASE_SLOT`, read through the Oracle's `getSlot`, as a number of microseconds since the Unix epoch.
    `update(uint256 ts)` forwards to the Oracle's `setSlot`, which authorizes its immediate caller — the timestamp contract itself — and so commits only when the live system address is `HIGH_PRECISION_TIMESTAMP_ADDRESS`, and otherwise reverts.
    `ORACLE_CONTRACT_ADDRESS()` returns `ORACLE_CONTRACT_ADDRESS`, `ALLOCATION_START()` returns `TIMESTAMP_BASE_SLOT`, and `ALLOCATION_SIZE()` returns `TIMESTAMP_MAX_SLOTS` as a `uint32`.
  - **Storage allocation.** Of the Oracle's storage, slot `TIMESTAMP_BASE_SLOT` holds the current timestamp in microseconds, and the following slots up to `TIMESTAMP_BASE_SLOT + TIMESTAMP_MAX_SLOTS − 1` are reserved.
  - **Service.** For a transaction that reads the timestamp, the value the timestamp service gives is a per-transaction snapshot, and it MUST be:
    - expressed in microseconds;
    - at most `block.timestamp × MICROSECONDS_PER_SECOND`;
    - above `parent.timestamp × MICROSECONDS_PER_SECOND`, the parent block's timestamp in microseconds, when the block's timestamp is above its parent's, and `block.timestamp × MICROSECONDS_PER_SECOND` when the two timestamps are equal;
    - the same for every read the transaction makes;
    - at least the snapshot any earlier transaction was given, of the same block or of an earlier one.

    The snapshot MUST be persisted before the transaction that read it unless that transaction's own write explains it (see [Oracle](oracle.md), `SATIN-ORCL-012`), and the protocol MUST NOT require a timestamp write for a transaction that does not read the timestamp.
    A read made where the service is not asked (`SATIN-ORCL-005`) pushes the slot's value.
- `SATIN-HPTS-002` The wrapper's reads of the Oracle's storage are Oracle reads: an `SLOAD` in the Oracle's own frame, reached through `getSlot`, MUST be answered by the oracle service, charged as a cold access and held to gas detention as [Oracle](oracle.md) and [Gas Detention](../evm/gas-detention.md) specify, and a frame whose volatile-data access is off MUST be refused it (see [MegaAccessControl](mega-access-control.md)).

## Constants

| Constant                             | Value                                                                | Description                                              |
| ------------------------------------ | -------------------------------------------------------------------- | -------------------------------------------------------- |
| `HIGH_PRECISION_TIMESTAMP_ADDRESS`   | `0x6342000000000000000000000000000000000002`                         | The High-Precision Timestamp                             |
| `HIGH_PRECISION_TIMESTAMP_CODE_HASH` | `0x1b2df8ca5350cd7106d67ed95532584526f97a5ca267c8eef73a1831f53720f2` | Its code hash, the Oracle's address embedded             |
| `ORACLE_CONTRACT_ADDRESS`            | `0x6342000000000000000000000000000000000001`                         | The Oracle                                               |
| `TIMESTAMP_BASE_SLOT`                | 0                                                                    | The Oracle slot holding the timestamp                    |
| `TIMESTAMP_MAX_SLOTS`                | 8                                                                    | Oracle slots allotted to the timestamp service           |
| `MICROSECONDS_PER_SECOND`            | 1,000,000                                                            | Microseconds in a second                                 |

## Rationale

**Why a wrapper instead of a direct Oracle read?**
The wrapper's address, interface and slot allocation are part of what contracts depend on; fixing them keeps every contract reading the same slot the same way, whatever the Oracle stores elsewhere.

**Why microseconds?**
They resolve sub-second blocks and fit one storage word.

**Why a per-transaction snapshot?**
A transaction that reads the timestamp twice must see one time, and successive transactions must see time move forward, or an ordering a contract derives from the timestamp contradicts the block's.

**Why above the parent's timestamp, and never below an earlier snapshot?**
A transaction must not read a time before the block it follows, and time must not run backwards from one block to the next.
The Rex6 page stated only the upper bound and the order within a block; the timestamp service of the node Rex6 runs on also keeps each snapshot above the parent block's time and never below the last snapshot it gave, and Satin states both as the service's obligations.

## Security Considerations

- A node that answered the wrapper's read from the slot alone, ignoring the service, would read an older time than every other node.
- A timestamp service that returned decreasing values within a block or across blocks, or a value at or before the parent block's time, would let a later transaction appear to precede an earlier one to any contract that orders by it.
- The wrapper's reads are volatile; a node that did not detain them would let a transaction that read the time keep computing past the limit every other node applies.

## Spec History

- [MiniRex](../../upgrades/minirex.md) — Introduced the High-Precision Timestamp.
- [Rex6](../../upgrades/rex6.md) — The Rex6 contract is specified in [High-Precision Timestamp](../../system-contracts/high-precision-timestamp.md).
- [Satin](../../upgrades/satin.md) — The contract is unchanged; its reads follow the Satin Oracle read and detention rules, and the service's lower bound and its order across blocks are stated.
