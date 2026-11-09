---
description: Satin (unstable) — EIP-7708 Transfer Logs. The Transfer log every movement of value to another account emits, the movements that log nothing, the burns that stay silent, and what a transfer log counts.
spec: Satin
maturity: unstable
---

# EIP-7708 Transfer Logs

{% hint style="warning" %}
**Unstable** — Satin is under active development: every value and rule on this page may change before Satin is frozen.
{% endhint %}

Abstract: Every movement of value to another account emits an [EIP-7708](https://eips.ethereum.org/EIPS/eip-7708) `Transfer` log from a fixed system address, in execution order among the contracts' own logs; a transfer log counts as data size and pays no history gas.

## Motivation

A value transfer made by an internal call, a creation's endowment or a `SELFDESTRUCT` leaves no trace in a receipt: an indexer that wants every movement of value has to trace every transaction, which on MegaETH's throughput is the most expensive thing an indexer can do.
ERC-20 transfers carry a `Transfer` event that indexers already read; value transfers carry nothing.

## Specification

- `SATIN-LOG-001` A node MUST apply EIP-7708's transfer log: every movement of value to another account — the transaction's value, a value `CALL`, a creation's endowment, a `SELFDESTRUCT` that moves a balance to another account — MUST emit `Transfer(address indexed from, address indexed to, uint256 value)` from `TRANSFER_LOG_ADDRESS`, with `TRANSFER_TOPIC` as its first topic, `from` and `to` as its second and third, and `value` as its data.
  The transfer log MUST be that of EIP-7708 as of [commit `f7230c46a7`](https://github.com/ethereum/EIPs/commit/f7230c46a743313957d8f38a159bda934cc735b2) (10 July 2026), the revision current when the EIP-8037 profile was frozen (`SATIN-POOL-004`), as this page restates it.
- `SATIN-LOG-002` The log MUST appear in the receipt in execution order among the contracts' own logs, where the value moves; a failed frame's transfer logs MUST be discarded with the rest of its logs.
- `SATIN-LOG-003` A `CALLCODE`, a call to the calling account itself, and a transaction's value sent to its own sender move nothing to another account and MUST NOT log.
- `SATIN-LOG-004` A deposit's value MUST be logged; its mint MUST NOT be.
- `SATIN-LOG-005` A node MUST NOT emit any other log any revision of EIP-7708 defines, a `Burn` log included, and MUST NOT apply [EIP-8246](https://eips.ethereum.org/EIPS/eip-8246): a balance can still be burned, and a burn MUST NOT log.
  Two burns remain, both silent: a `SELFDESTRUCT` to itself of an account created in the same transaction burns the balance at once, and an account destroyed in the transaction is removed at its end with whatever balance it then holds, a value it received after its destruction included, whose `CALL` logged the transfer ([SELFDESTRUCT and the Destruction Table](selfdestruct.md)).
- `SATIN-LOG-006` A transfer log MUST count `TRANSFER_LOG_SIZE` bytes of data size where the value moves — with the start of the frame that moves it, held to the limits with the start's records (`SATIN-LIM-013`), or with the `SELFDESTRUCT` that moves it — and MUST NOT be a write record, MUST NOT pay history gas, and MUST NOT draw on a history allowance ([History Gas and the History Allowance](history-gas.md)).
- `SATIN-LOG-007` A frame start that the caller's account refuses (`SATIN-LIM-015`) moves nothing and MUST log nothing.
  A creation with an endowment onto an occupied address moves nothing and MUST log nothing: the collision fails it before the endowment moves, and nothing of the log is counted or held to a limit (`SATIN-LIM-016`).

### Retired ids

None.

## Constants

| Constant               | Value                                                                | Description                                    |
| ---------------------- | -------------------------------------------------------------------- | ---------------------------------------------- |
| `TRANSFER_LOG_ADDRESS` | `0xfffffffffffffffffffffffffffffffffffffffe`                         | The address every transfer log is emitted from |
| `TRANSFER_TOPIC`       | `0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef` | `keccak256("Transfer(address,address,uint256)")` |
| `TRANSFER_LOG_SIZE`    | 160                                                                  | Data size of one transfer log (a `LOG3` of one word) |

## Rationale

**Why EIP-7708's log and no other?**
The `Transfer` signature is the one ERC-20 indexers already decode, so value movements show up in the same pipelines as token transfers.
Later revisions of EIP-7708 require EIP-8246, which removes burns and adds a `Burn` log; Satin keeps the two burns EIP-6780 leaves and keeps them silent, so a revision of the EIP that adds logs does not change Satin's receipts.

**Why does a transfer emit a log Rex6 did not?**
Rex6 logged only the `LOG` instructions contracts executed, so a value movement — a deposit's value, a value call, a creation's endowment, a destruction's balance — left no log; Satin adopts EIP-7708 at its pinned revision, so every movement leaves one.
The log is emitted from `TRANSFER_LOG_ADDRESS`, the address EIP-7708 names; that address holds no code and is not a system contract ([System Contracts](../system-contracts/overview.md)).

**Why data size and not history gas?**
A transfer log is the protocol's record of a movement the transaction already paid for in its value transfer's regular gas; charging history gas for it would make every value transfer dearer by the log's 160 bytes.
It is still bytes the block carries, so it counts toward the data-size limit.

**Why does the allowance not pay for it?**
The history allowance exists for the callee's own event; a transfer log costs no history gas, so letting it draw the allowance would only waste the allowance.

## Security Considerations

- If a node emitted a log for a movement that did not happen — a refused start, a collided creation — an indexer would record value that never moved.
- If a failed frame's transfer logs were kept, receipts would show transfers the state does not contain.
- If transfer logs were not counted as data size, a transaction could append unbounded logs through value calls at no data-size cost.
- If a node applied EIP-8246, burns would fail or log, and its receipts and state would differ from every other node's.

## Spec History

- [Satin](../../upgrades/satin.md) — Introduced EIP-7708 transfer logs; under Rex6 a value transfer emitted no log.
