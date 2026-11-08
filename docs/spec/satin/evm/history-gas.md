---
description: Satin (unstable) — History Gas and the History Allowance. The third gas ledger: the price per byte of what a transaction appends to the chain's history, the byte table, when each history charge is made and given back, the give-back rule, the exemptions, the floor, and the 160-byte history allowance of a value call.
spec: Satin
maturity: unstable
---

# History Gas and the History Allowance

{% hint style="warning" %}
**Unstable** — Satin is under active development: every value and rule on this page may change before Satin is frozen.
{% endhint %}

Abstract: [History gas](../../glossary.md#history-gas) prices, at a flat price per byte, the bytes a transaction appends to the chain's history — its body, its logs, its [write records](../../glossary.md#write-record) and its deployed code; this page specifies the byte table, when each charge is made and given back, which transactions and items are exempt, and the [history allowance](../../glossary.md#history-allowance) a value call grants the frame it starts.

## Motivation

Every node receives, stores and serves every block's transactions, receipts, logs and state diffs, whatever their computation cost.
Priced as computation, a log or a byte of calldata costs a few gas per byte, which does not cover what the network carries for it; priced as state, it would be scaled by SALT, although history does not land in a bucket.
Rex6 approximated these costs with surcharges: ten times the standard log and calldata cost, 10,000 gas per byte of deployed code, and 39,000 intrinsic storage gas per transaction, none of which counted the bytes actually appended.

A value transfer that triggers a `receive()` hook must also be able to emit an event even when its caller forwards only the 2,300-gas stipend, which a per-byte price above a few gas makes impossible without an allowance.

## Specification

### The price and the byte table

- `SATIN-HIST-001` History gas MUST be `COST_PER_HISTORY_BYTE` gas per byte of the byte table, and MUST NOT be scaled by SALT.
- `SATIN-HIST-002` The bytes MUST be those of this table, which is also the table the data-size limit counts ([Resource Accounting](resource-accounting.md)), so an item's history bytes are its own data size:

  | Item                                      | Bytes                                                              |
  | ----------------------------------------- | ------------------------------------------------------------------ |
  | Transaction body                          | `TX_BODY_SIZE`                                                     |
  | Calldata (a creation's initcode included) | 1 per byte, zero or non-zero                                       |
  | Access-list address                       | `ACCESS_LIST_ADDRESS_SIZE`                                         |
  | Access-list storage key                   | `ACCESS_LIST_SLOT_SIZE`                                            |
  | EIP-7702 authorization                    | `AUTHORIZATION_SIZE`                                               |
  | Log                                       | `LOG_BASE_SIZE`, plus `LOG_TOPIC_SIZE` per topic, plus its data length |
  | Write record                              | `WRITE_RECORD_SIZE`                                                |
  | Deployed code                             | 1 per byte                                                         |

- `SATIN-HIST-003` `TX_BODY_SIZE` MUST be `TX_BASE_SIZE` for the envelope plus `TX_FIXED_WRITE_RECORDS` write records of `WRITE_RECORD_SIZE` bytes: the sender's account, and the settlement writes of the four accounts a transaction's fees are credited to (the block beneficiary, the L1 fee vault, the base fee vault and the operator fee vault).
  It is an upper bound, charged whether or not every fee account is written.
  It covers every account write to the sender, and of the fee accounts only the fee credits; a storage write to the sender's slots, and a write execution makes to a fee account that is not the sender, are records of their own ([Resource Accounting](resource-accounting.md)).
  The five fixed records are bytes of the body alone: they MUST count as data size and pay history gas with the body, and MUST NOT count as KV updates, so a transaction that keeps no write of its own reports zero KV updates, and the body takes nothing of the transaction's KV-update limit ([Resource Accounting](resource-accounting.md)).

### When each charge is made

- `SATIN-HIST-004` The body — `TX_BODY_SIZE`, the calldata, the access list and the authorization entries — MUST be charged before execution as the intrinsic state gas ([Two-Pool Gas](gas-model.md)): the reservoir pays it first and the regular budget its excess.
  It MUST NOT be part of the intrinsic regular gas the execution cap is validated against, a gas limit that cannot cover it makes the transaction invalid ([Transaction Validation and Refusals](../block/transaction-validation.md)), and it MUST NOT be reported on the state ledger.
- `SATIN-HIST-005` The records of the applied EIP-7702 authorities, and the record the transaction's own frame makes at its start (its value's recipient or its created account), MUST be charged before the first frame.
  A list the KV or state-growth limit skips has no authority records, and that history is not charged ([EIP-7702 Authorizations Before the First Frame](authorizations.md)).
  The authorities' records are the transaction's own: their history MUST be kept when the first frame fails or is stopped.
  The first frame's record is that frame's: its history gas MUST come back, into the transaction's reservoir, when that frame fails or is stopped.
  When the destruction table takes that record back inside a first frame that then succeeds, the charge has already come back with the table, and the settlement MUST NOT give it back a second time; when that first frame then fails, the table's give-back is discarded with the table, and the settlement MUST give the charge back once.
  A transaction that runs out of gas before its first frame keeps neither ([Gas Schedule and Intrinsic Gas](gas-schedule.md)).
- `SATIN-HIST-006` A log, a storage write's record, and the records of a `SELFDESTRUCT` (the account it clears and its beneficiary) MUST be charged by the opcode once it completed.
  A record the opcode takes back — a slot written back to its original value, an account a `SELFDESTRUCT` returns to what the transaction loaded, each part the destruction table takes back — MUST be given back by the opcode then, before what it makes is charged.
- `SATIN-HIST-007` A part the destruction table takes back MUST be given back into the reservoir of the destroying frame, including when another frame paid it, and a failure of that frame discards the give-back (`SATIN-SD-010`, [SELFDESTRUCT and the Destruction Table](selfdestruct.md)).
  Every other give-back of history gas, and every give-back of state gas but the destruction table's, MUST go into the reservoir of the frame that makes it, at the price the record or the state was charged, by the rule of `SATIN-HIST-012`, whichever frame paid the charge: a slot written back to its original value, and an account a `SELFDESTRUCT` returns to what the transaction loaded, give back to the frame running the opcode; an account a value transfer returns to what the transaction loaded gives back to the caller of that start once the frame returned with its start kept (`SATIN-HIST-009`); a start's records and state gas that a failed or stopped child discards give back to its caller when the child returns (`SATIN-HIST-014`, `SATIN-POOL-015`).
  A failed frame's own charges, its records and logs among them, are given back by its rollback (`SATIN-POOL-014`), and a give-back the failed frame received is undone with it: the record it took back stands again, and its charge stays where it was paid.
  The frame that makes a give-back decides only whose reservoir holds it: a frame can pay state and history charges, while it runs, with gas an ancestor paid for records or state the frame takes back, at most the price of those records and that state, but it cannot compute with that gas (`SATIN-POOL-007`, `SATIN-POOL-009`); what it does not spend returns up the chain with its reservoir when it succeeds.
- `SATIN-HIST-008` An opcode that fails after its write was observed — an `SSTORE` or a `SELFDESTRUCT` that cannot pay a regular charge it makes after its load — MUST keep nothing and MUST be charged no history.
  A `LOG` observes its write after every regular charge of the inherited opcode, so only the limits and its history charge can fail it after its write was observed.
- `SATIN-HIST-013` A record an opcode commits — a storage write, a log, a `SELFDESTRUCT`'s records — MUST be held to the limits ([Resource Limits](resource-limits.md)) before its history is charged, so a record a limit refuses is not charged.
  A frame that cannot pay that history charge MUST halt out of gas, keeping neither the record nor its bytes.
- `SATIN-HIST-009` A `CALL`, `CALLCODE`, `CREATE` or `CREATE2` MUST charge its own frame for the records the frame it starts makes — the accounts a value transfer changes from what the transaction loaded; a creation's created account, unless the transaction changed it already, and the creator's nonce record when the bump changes the creator's account from what the transaction loaded ([Resource Accounting](resource-accounting.md)) — after the regular gas it forwards is computed, so the forward is not reduced by them.
  A caller that cannot pay MUST halt out of gas, and the frame MUST NOT start.
  The price of a record the start takes back — an account the transfer returns to what the transaction loaded — MUST be given back to the caller once the frame returned with its start kept.
- `SATIN-HIST-014` At a frame start the order is the reverse of an opcode's: the calling opcode MUST pay for the start's records before the frame starts, and they are then held to the limits, so a caller that cannot pay runs out of gas first; the charge for a start a limit stops MUST be given back when the stopped frame returns.
- `SATIN-HIST-015` The opcode MUST charge the records a start makes as the state stands when it runs: a value the caller cannot fund makes no record and is charged no history; a creation whose creator's nonce cannot be bumped, whose endowment the creator cannot fund, or which is past the call-depth limit starts no frame and is charged no history and no state gas, the creation opcode refusing it before it charges for the start and before it reads the created address.
  The refusal takes back none of the opcode's regular charges made before it — a call's static cost, memory, value-transfer cost and cold access, a creation's static cost, initcode cost and memory — and a regular charge that crosses gas detention stops the frame before the refusal is reached ([Gas Detention](gas-detention.md)).
  A value `CALL` to an account empty under EIP-161 that its caller cannot fund, or that is past the call-depth limit, MUST still charge the new account's state gas, its legacy share included, at step 2 of `SATIN-HIST-010`, before the refusal, and that charge MUST be given back into the caller's reservoir when the call returns refused (`SATIN-POOL-015`); a caller that cannot pay it runs out of gas.
- `SATIN-HIST-010` A value `CALL` to an account empty under EIP-161 MUST charge its caller in this order:
  1. its regular gas: the access's static cost, memory, the value transfer, then the cold surcharge with the new account's regular gas, which is zero ([Gas Schedule and Intrinsic Gas](gas-schedule.md));
  2. the new account's state gas: its legacy share from regular gas (`SATIN-STATE-012`), then the reservoir, then the rest from regular gas;
  3. the forward of the regular gas left ([Gas Forwarding](gas-forwarding.md));
  4. the history of the start's records.

  The legacy share, and a state charge's part the reservoir cannot pay, therefore shrink the forward, and the records' history does not; the forward is regular gas only.
  The child MUST be given its reservoir share after the history charge, from the reservoir that charge left the caller (`SATIN-POOL-011`).
- `SATIN-HIST-011` A `CREATE` or `CREATE2` MUST charge the created account's state gas, its legacy share included (`SATIN-STATE-012`), when the account at the created address is empty under EIP-161 (no account, or nonce zero, zero balance and no code), before it computes the forward, and MUST give the creation its reservoir share after the history of the start's records, as a call does.
- Deployed code is charged at the deposit, in the order of `SATIN-SCHED-011` ([Gas Schedule and Intrinsic Gas](gas-schedule.md)).

### The give-back rule

- `SATIN-HIST-012` Every give-back of state gas or of history gas — a refill (a slot written back, an account returned to what the transaction loaded, a record taken back), the destruction table's, a start's charge given back when the start fails or is refused, a failed frame's rollback — MUST credit the reservoir of the frame that receives it (`SATIN-HIST-007`, `SATIN-SD-005`, `SATIN-POOL-015`, `SATIN-POOL-014`) and MUST NOT credit its regular gas, whichever pool paid the charge, a legacy share included.
  A frame's regular gas MUST NOT rise within the frame except by the unused regular gas a child returns (`SATIN-POOL-012`); a give-back of a charge regular gas paid leaves that gas spent and puts its price into the reservoir, where it can pay later state and history charges, and what is left of it returns to the sender at the settlement (`SATIN-POOL-017`).
  An exceptional halt consumes the halting frame's regular gas, with the part of its charges that regular gas paid, and restores its reservoir to what it received (`SATIN-POOL-014`).

### Exemptions and the floor

- `SATIN-HIST-016` These MUST NOT pay history gas:
  - an [EIP-7708 transfer log](transfer-logs.md), which is data size only;
  - an Oracle hint's payload, which goes to the oracle service and not into a block ([Oracle](../system-contracts/oracle.md));
  - any byte of a deposit, of a system-originated transaction, or of a system call ([Mega System Transactions and the Protocol's Own Transactions](../system-contracts/system-tx.md)); for these the deposited-code history gas MUST be zero too.

  The exemption is from history gas alone: a deposit that is not system-originated MUST still be priced by bucket ([State Gas and SALT Pricing](state-gas.md)), held to every per-transaction limit, and detained ([Gas Detention](gas-detention.md)).
- `SATIN-HIST-017` The EIP-7623 floor MUST still be computed and validated for every transaction ([Gas Schedule and Intrinsic Gas](gas-schedule.md)).
  It can raise the gas used of a transaction exempt from history gas, and it bounds the figure a block counts on its execution ledger, `max(regular, floor)` (`SATIN-POOL-020`).
  Where it binds, the gas used is the floor, drawn from the whole gas limit, the reservoir included (`SATIN-POOL-018`); a deposit, which paid nothing, MUST be charged nothing either way, and only its receipt's and the block's figures move.

### The history allowance

- `SATIN-HIST-018` A value-transferring `CALL` or `CALLCODE` below the transaction's own frame MUST grant the frame it starts a history allowance of `HISTORY_ALLOWANCE_BYTES × COST_PER_HISTORY_BYTE` gas.
  No other start grants one: not the transaction's own frame, a `DELEGATECALL`, a `STATICCALL`, a creation, or a call without value.
- `SATIN-HIST-019` A log's history charge in that frame MUST draw `min(history_charge, allowance_left)` from the allowance first, and the frame's gas MUST pay the rest; the allowance MUST be reduced by what it paid.
  - `history_charge` — the log's history gas (`SATIN-HIST-002`).
  - `allowance_left` — what the frame's allowance has left before the log.

  Only a log's history charge draws on the allowance: a write record's history charge MUST NOT draw on it.
  A value call whose child has only the stipend and no reservoir, and whose child emits an empty `LOG0` (2,816 gas of history), therefore pays that log from the allowance and succeeds.
- `SATIN-HIST-020` The allowance MUST NOT enter the frame's gas: it MUST NOT pay for computation or state, it is never returned as gas, and what it pays for is on no gas ledger.
  The history bytes it pays for still count as bytes the transaction appended, and as data size.
- `SATIN-HIST-021` The transfer log of the value that granted the allowance MUST NOT draw on it ([EIP-7708 Transfer Logs](transfer-logs.md)).

### The history bytes a transaction reports

- `SATIN-HIST-022` The history bytes a transaction reports, which the block counts ([Block Limits and Packing](../block/block-limits.md)), MUST be the bytes of the byte table (`SATIN-HIST-002`) the transaction keeps — its body, its kept write records, its kept logs and its deposited code — whether history gas or a history allowance paid them, net of every take-back.
  A transaction exempt from history gas by `SATIN-HIST-016` — a deposit, a system-originated transaction, a system call — MUST report zero history bytes, although its data size still counts those bytes ([Resource Accounting](resource-accounting.md)).
  EIP-7708 transfer logs and Oracle hint payloads are not history bytes.
  A deposit with empty calldata that makes no write reports 310 bytes of data size and zero history bytes; an ordinary transaction whose value call's child emits a `LOG0` the allowance pays reports that log's 32 bytes among its history bytes.

### Retired ids

None.

## Constants

| Constant                   | Value | Description                                                                        |
| -------------------------- | ----- | ---------------------------------------------------------------------------------- |
| `COST_PER_HISTORY_BYTE`    | 88    | Gas per history byte                                                               |
| `TX_BODY_SIZE`             | 310   | Bytes of a transaction body: `TX_BASE_SIZE + TX_FIXED_WRITE_RECORDS × WRITE_RECORD_SIZE` |
| `TX_BASE_SIZE`             | 110   | Bytes of a transaction's envelope                                                  |
| `TX_FIXED_WRITE_RECORDS`   | 5     | Write records in every body: the sender and the four fee accounts                  |
| `WRITE_RECORD_SIZE`        | 40    | Bytes of one write record                                                          |
| `ACCESS_LIST_ADDRESS_SIZE` | 20    | Bytes of an access-list address                                                    |
| `ACCESS_LIST_SLOT_SIZE`    | 32    | Bytes of an access-list storage key                                                |
| `AUTHORIZATION_SIZE`       | 101   | Bytes of an EIP-7702 authorization entry                                           |
| `LOG_BASE_SIZE`            | 32    | Bytes of a log before its topics and data                                          |
| `LOG_TOPIC_SIZE`           | 32    | Bytes per log topic                                                                |
| `HISTORY_ALLOWANCE_BYTES`  | 160   | History bytes a value call's frame may log without paying: 14,080 gas              |

## Rationale

**Why a flat price per byte?**
What a node carries for history is proportional to the bytes appended, not to where they land, so the price is per byte and is not scaled by SALT.
At 88 gas per byte, the history gas of a byte is above the floor's 64 gas per calldata byte, so the floor never raises the gas used of a transaction that pays history gas.

**Why write records rather than KV updates?**
A write record is one account or slot a transaction keeps changed, which is what the state diff a node stores and serves carries.
Pricing each kept record at its 40 bytes ties the price to what the block holds: a slot written back to its original value, or an account returned to what was loaded, leaves nothing to carry and gets its price back.

**Why does a give-back go to the frame that makes it, and not to the frame that paid?**
A give-back is made by an opcode, and only the frame running that opcode is there to receive it: the frame that paid may be suspended above, or may have returned already, and crediting it would mean reaching into another frame's gas while a different frame runs.
EIP-8037 refills its own state gas in the running frame too, so a slot's state and history give-backs land in the same frame.
Since a give-back credits a reservoir only (`SATIN-HIST-012`), the frame decides only whose reservoir holds the gas: a callee can pay state and history, while it runs, with gas an ancestor paid for the records it takes back, bounded by their price, but cannot compute with it, and what it does not spend returns up the chain.
The destruction table is the exception that still goes to the destroying frame for a different reason: the parts it gives back may have been paid by frames that have all returned.

**Why does a give-back credit the reservoir and never regular gas?**
Under EIP-8037 at the pinned commit a refill goes to regular gas first, up to what regular gas paid, so `GAS` can rise within a frame; on MegaETH, where a transaction at or below the execution cap has no reservoir, that is every give-back, and history gas makes every log and write record part of it.
A contract that records a failure after a failed call only when it holds more gas than a starved call could leave it relies on spent gas staying spent, as it always did under Rex6; the reservoir-only rule keeps that true for regular gas, at no cost to the sender, whose unused reservoir returns at the settlement ([Two-Pool Gas](gas-model.md)).

**Why is the body an upper bound?**
The sender's account and the four fee credits are written by the settlement, after the result is final, where a charge could no longer change the outcome.
Charging their five records up front, in the body, bounds them before execution and keeps every charge where it can still be refused.

**Why does the history allowance replace the storage gas stipend?**
Rex6 granted a value call's callee 23,000 gas of storage-gas allowance, drawn by every storage-gas surcharge.
Under Satin new state is paid from the reservoir, which a callee always receives a share of, so only history is left for an allowance to cover; 160 bytes is one three-topic event with one word of data, what a `receive()` hook reached through the 2,300-gas stipend needs to log a transfer.

**Why are the protocol's own transactions and deposits exempt?**
A deposit is derived from L1 and has already paid L1 for its bytes, and the protocol's own transactions are the chain's bookkeeping; charging them would only move gas between protocol accounts.

## Security Considerations

- If a node charged a record's history after a limit refused it, a stopped frame would pay for bytes the block does not keep; if it held the record to the limits after charging, a frame could be charged for a write that never happens.
- If a give-back credited regular gas, a frame's `GAS` would rise by state and history gas the frame or another frame had spent: a slot cleared after a failed call, or an intermediary's revert, would hand back to the running frame regular gas that a contract checking its gas after a failed call assumes is gone; and a frame could turn reservoir it was given into regular gas, and compute past the regular budget its caller forwarded.
- If a node credited a give-back to the frame that paid instead of the frame that makes it, the reservoirs of the frames would differ from every other node's while they run, and so would whether a later state or history charge fits in a frame's reservoir or spills onto its regular gas.
- If a failed frame kept a give-back it received, a callee could take back a record its caller paid for, collect the gas and revert, leaving the record standing and the gas spent twice.
- If the allowance entered the frame's gas, a value call could compute on 14,080 gas its caller never forwarded, and repeated calls could amplify computation without paying for it.
- If the settlement gave the first frame's record back after the destruction table had already given it back, the transaction would be credited the same history twice.
- This page preserves the invariant that a transaction's history ledger equals `COST_PER_HISTORY_BYTE` times the history bytes it keeps, less those an exemption or the allowance paid.

## Spec History

- [Satin](../../upgrades/satin.md) — Introduced history gas at 88 per byte for the body, logs, write records and deployed code, in place of the Rex6 log, calldata and code-deposit storage gas and the 39,000 intrinsic storage gas of the [Dual Gas Model](../../evm/dual-gas-model.md), and replaced the 23,000-gas [storage gas stipend](../../evm/gas-forwarding.md) with a 160-byte history allowance.
