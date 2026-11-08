---
description: Satin (unstable) — Resource Accounting. What each limited dimension counts — the data-size items and when each is counted, write records (the KV count) and how they are made and taken back, and state growth with its rises, its falls and the SSTORE transition table.
spec: Satin
maturity: unstable
---

# Resource Accounting

{% hint style="warning" %}
**Unstable** — Satin is under active development: every value and rule on this page may change before Satin is frozen.
{% endhint %}

Abstract: The counts the [resource limits](resource-limits.md) hold: data size, the bytes of the byte table plus transfer logs and Oracle hints; KV updates, the [write records](../../glossary.md#write-record) a transaction keeps; and state growth, the net count of new accounts and new storage slots it keeps.

## Motivation

A limit is only as good as what it counts.
Counting every write operation, as Rex6's KV count did, counts a slot written ten times ten times although the block keeps one change, counts a write and its exact undo although the block keeps none, and counts the sender and the fee recipients after the result, where the count can no longer stop anything.
Counting state growth without its falls stops a transaction that creates and removes a slot as if it had kept it, and counting it without a rule for each `SSTORE` transition lets two nodes disagree on a slot that goes from zero to non-zero and back.

## Specification

### Data size

- `SATIN-ACCT-001` Data size MUST count the byte table of [History Gas and the History Allowance](history-gas.md) (`SATIN-HIST-002`), plus two items that pay no history gas: an EIP-7708 transfer log, counted as `TRANSFER_LOG_SIZE` bytes ([EIP-7708 Transfer Logs](transfer-logs.md)), and an Oracle hint's input, counted by its length ([Oracle](../system-contracts/oracle.md)).
- `SATIN-ACCT-002` Each item MUST be counted at this point:
  - the body, before any frame;
  - the applied authorities' records, before the first frame ([EIP-7702 Authorizations Before the First Frame](authorizations.md));
  - a frame start's records and transfer log, when the start is decided (`SATIN-LIM-013`);
  - a storage write's record, a log, and a `SELFDESTRUCT`'s records and transfer log, once the opcode completed;
  - deployed code, once every deposit charge is made and before the creation commits ([Gas Schedule and Intrinsic Gas](gas-schedule.md));
  - an Oracle hint's input, before the hint is forwarded, on the transaction and on no frame's budget; a hint that would cross the transaction's data-size limit is neither counted nor forwarded ([Oracle](../system-contracts/oracle.md)).
- `SATIN-ACCT-003` A deposit's data size MUST be counted as any transaction's, and a deposit that fails MUST keep what it counted: its body and the hints it admitted.

### Write records

- `SATIN-ACCT-004` A write record MUST be one account or storage write the transaction keeps.
  A storage slot's record MUST exist while the slot's value differs from its original value in the transaction: the slot's first change makes it, and writing the slot back to its original value takes it back.
  An account's record MUST exist while the account's nonce, balance or code differs from what the transaction loaded — its information at its first load in the transaction: a write that changes an unchanged account makes the record, a write that returns a changed account to what was loaded takes it back, and a write to an account that already differs adds nothing.
- `SATIN-ACCT-005` These writes MUST be held to `SATIN-ACCT-004`: a value transfer's sender and recipient, on the balances the transfer leaves them; a creation's created account, which the creation leaves changed by its nonce, and the creator's nonce it bumps; a `SELFDESTRUCT`'s beneficiary and the account it clears; an applied EIP-7702 authority; and the transaction's value recipient or created account.
  A created account is no exception: an address the transaction changed before a creation lands on it — a value transfer funded it, or a `SELFDESTRUCT` paid it — differs already, and the creation adds no record for it.
- `SATIN-ACCT-006` A record MUST be made where the write is, and taken back where a write returns the account or slot: a value transfer that returns an account to what the transaction loaded takes the record back in the frame the transfer starts, with its data size, and its history gas comes back to the caller once that frame returned with its start kept (`SATIN-HIST-009`); a `SELFDESTRUCT` whose move returns an account takes the record back where the opcode completed; a slot written back to its original value gives its record back.
  N value transfers from one frame to the same recipient keep one record for the recipient and one for the sender; a transfer and its exact return keep none; a recipient that passes on exactly what it received keeps none of its own; a frame that funds an address and then creates at it keeps two records, its own and the address's.
- `SATIN-ACCT-007` A value-transferring `CALLCODE`, which moves the value from the calling account to that same account, and a value-transferring `CALL` to the calling account itself MUST change no account and record none.
- `SATIN-ACCT-008` The sender's account is one of the body's fixed records (`SATIN-HIST-003`), which are data size and history bytes only and MUST NOT count as KV updates, and it MUST NOT be recorded again: validation changes it before execution, by its fee and a call's nonce, and a creation transaction's first frame by its nonce, so no write execution makes to it — a frame running as the sender, a value transfer or a `SELFDESTRUCT` that moves value to it, a keyless deployment whose signer is the sender — changes it from what the transaction loaded.
- `SATIN-ACCT-009` An applied EIP-7702 authority is changed by its nonce and its delegation when it is applied: a write to it afterwards, the transaction's own value to it included, MUST add no record.
- `SATIN-ACCT-010` The four fee accounts are in the body only for the fee credits the settlement makes, and are unchanged until execution writes them: a write execution makes to a fee account that is not the sender — a value transfer to it, a `SELFDESTRUCT` that moves a balance to it, an applied EIP-7702 authority that is one of them — MUST be recorded like a write to any other account.
- `SATIN-ACCT-011` A successful frame's records and bytes MUST merge into its caller's; a failed frame's MUST be discarded, the records it took back standing again, except that a creator's nonce record is the creating frame's and survives the creation's failure (`SATIN-LIM-008`).
- `SATIN-ACCT-012` The KV count MUST be the write-record count, held to `TX_KV_UPDATE_LIMIT`; the five fixed records of the body (`SATIN-HIST-003`) are not in it.
  Every record MUST weigh `WRITE_RECORD_SIZE` bytes of data size, counted and taken back with it, so `KV × WRITE_RECORD_SIZE ≤ data size` at every point.
  The KV check MUST be made although, at these constants, `TX_KV_UPDATE_LIMIT` records weigh more than `TX_DATA_LIMIT` bytes; a record taken back cannot cross it.
  Logs, deployed code, transfer logs and Oracle hints are not records.

### State growth

- `SATIN-ACCT-013` State growth MUST be the net count of new accounts and new storage slots the transaction keeps: each rise is one unit at an account-leaf or fresh-slot state charge site ([State Gas and SALT Pricing](state-gas.md)), not one unit per byte of deployed code or of a delegation indicator, whose bytes state gas still prices.
- `SATIN-ACCT-014` The rises MUST be exactly:
  - a fresh slot, at the `SSTORE` transition of `SATIN-ACCT-016` that rises;
  - a value `CALL` to an account empty under EIP-161;
  - a `SELFDESTRUCT` that moves a non-zero balance to a distinct account empty under EIP-161 ([SELFDESTRUCT and the Destruction Table](selfdestruct.md));
  - the recipient of a transaction's value, when it is empty under EIP-161;
  - an applied EIP-7702 authorization whose authority is empty under EIP-161;
  - a `CREATE`, a `CREATE2`, a creation transaction or a keyless creation, when the created address is empty under EIP-161;
  - a keyless signer's account, when the creation's nonce bump creates it, counted on the keyless call ([KeylessDeploy](../system-contracts/keyless-deploy.md));
  - the caller account of a deposit, a Mega System Transaction executed as a deposit included, when that caller is empty under EIP-161, once (`SATIN-ACCT-020`, `SATIN-DEP-003`).

  Each is decided by the predicate of `SATIN-STATE-011`: the account is empty under EIP-161 — no account, or nonce zero, zero balance and no code.
- `SATIN-ACCT-015` An account that is not empty under EIP-161 MUST NOT be a rise, and neither MUST a `CALLCODE`, a value call to the calling account itself, deployed code, or a delegation indicator.
  An account whose leaf is in the state but is empty under EIP-161 is the exception to existence: at the sites of `SATIN-ACCT-014` it MUST be a rise as an absent account is, although the witness answers it as a leaf (`SATIN-WIT-017`).
- `SATIN-ACCT-016` An `SSTORE` MUST change state growth by this table alone, whose columns are the slot's original value in the transaction, its present value, and the value written:

  | Original | Present  | New      | State growth |
  | -------- | -------- | -------- | ------------ |
  | zero     | zero     | zero     | none         |
  | zero     | zero     | non-zero | +1           |
  | zero     | non-zero | zero     | −1           |
  | zero     | non-zero | non-zero | none         |
  | non-zero | zero     | zero     | none         |
  | non-zero | zero     | non-zero | none         |
  | non-zero | non-zero | zero     | none         |
  | non-zero | non-zero | non-zero | none         |

  The transitions are those of the fresh-slot state charge and give-back (`SATIN-STATE-008`).
  A no-op writes the present value and changes nothing.
  A slot written from zero to a non-zero value and then to another non-zero value rose once; written from zero to non-zero and back to zero, its net is zero; written from zero to non-zero, back to zero and to non-zero again, it rose, fell and rose.
  A slot whose original value is not zero changes nothing on any transition.
  While its account is marked for deletion, an `SSTORE` of its slots changes nothing ([SELFDESTRUCT and the Destruction Table](selfdestruct.md)).
- `SATIN-ACCT-017` The fee credits the settlement writes MUST NOT be rises and are not EIP-8037 charge sites.
- `SATIN-ACCT-018` A fall MUST happen at the opcode that restores the state, and a fall cannot cross a limit.
  The only slot fall is the table's row of original zero, present non-zero and new zero; the other falls are the destruction table's ([SELFDESTRUCT and the Destruction Table](selfdestruct.md)).
- `SATIN-ACCT-019` A rise that would take the signed net past the transaction limit or the frame budget is the crossing, and that rise MUST NOT be kept ([Limit Stops](limit-stops.md)).
- `SATIN-ACCT-020` A failed deposit whose caller was empty under EIP-161 when the deposit was executed MUST count that account as one unit of state growth on the transaction's reported usage and on the block's counter, MUST NOT be charged state gas for it, and MUST NOT be stopped by the limit, the deposit having already failed ([Deposit Transactions](../block/deposits.md)).
  A deposit that runs to a success or a revert and creates its caller makes the ordinary charged rise of one, and a stop of its first frame keeps that account ([Limit Stops](limit-stops.md)).

### Retired ids

None.

## Constants

| Constant                | Value      | Description                                                    |
| ----------------------- | ---------- | -------------------------------------------------------------- |
| `TRANSFER_LOG_SIZE`     | 160        | Data size of one EIP-7708 transfer log (a `LOG3` of one word)  |
| `WRITE_RECORD_SIZE`     | 40         | Data size of one write record                                  |
| `TX_KV_UPDATE_LIMIT`    | 500,000    | KV-update limit of one transaction ([Resource Limits](resource-limits.md)) |
| `TX_DATA_LIMIT`         | 13,107,200 | Data-size limit of one transaction ([Resource Limits](resource-limits.md)) |

## Rationale

**Why count write records instead of write operations?**
What a block keeps of a transaction is the net change: one entry per account or slot left different from what the transaction found.
Counting that change, and taking it back when a write is undone, makes the KV count, the data size and the history gas of a record all the same thing, so a limit on one is a limit on what a node stores.

**Why are the sender and the fee accounts fixed records of the body?**
Rex6 counted the caller as an update that could not be discarded and each fee recipient after the result, where the count could not stop anything.
The body bounds those five writes before execution, and a write execution itself makes to a fee account is counted where it happens, so every count can still stop the frame that made it.

**Why keep the KV check when data size binds first?**
At 40 bytes per record, 500,000 records weigh more than the 13,107,200-byte data-size limit, so today the data-size check stops first.
Dropping the KV check because of that comparison would retire the KV limit the moment the byte weight or the data-size limit changed.

**Why signed state growth?**
A transaction that creates a slot and clears it keeps no state, and a destruction of an account the transaction created removes what it added; counting only rises would stop such a transaction for state the block never holds.

**Why does a failed deposit count its caller?**
A failed deposit still creates its caller's account, which the block keeps; without the count a block of such deposits could add state past the block's state-growth limit while reporting none.

## Security Considerations

- If a node counted writes per frame rather than per transaction, a contract could be stopped for a write its frames undo, and two nodes deduplicating differently would stop different transactions.
- If a failed frame's take-backs stood, a callee could write and fail to free room its caller then used twice.
- If the fee credits were counted as rises or records after the result, the counts a block reports would depend on the settlement order and could not be held to the limits.
- If a node used another `SSTORE` table for state growth than for the fresh-slot charge, a slot could be counted as new without paying for it, or pay without being counted.
- This page preserves the invariant that `KV × WRITE_RECORD_SIZE ≤ data size` at every point of a transaction.

## Spec History

- [Satin](../../upgrades/satin.md) — Replaced the Rex6 KV-update count and state-growth rules of [Resource Accounting](../../evm/resource-accounting.md) with write records (one per kept account or slot change, 40 bytes of data size each), signed state growth with the `SSTORE` transition table, and dropped the post-execution fee-reward accounting.
