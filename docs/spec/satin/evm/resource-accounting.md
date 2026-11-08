---
description: Satin (unstable) — Resource Accounting. Stub of the Satin specification: the rules this page will specify.
spec: Satin
maturity: unstable
---

# Resource Accounting

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
This page is a stub. It lists what the page will specify; the specification text is written after the outline is reviewed.
{% endhint %}

Abstract: What each limited dimension counts: the data-size byte table and when each item is counted, write records (the KV count), and state growth with its SSTORE transition table.

## Specification

The rules this page will specify, by their proposed ids:

- `SATIN-ACCT-001` — Data size counts the byte table plus two items that pay no history: an EIP-7708 transfer log, TRANSFER_LOG_SIZE = 160, and an Oracle hint's payload length.
- `SATIN-ACCT-002` — When each item is counted: the body before any frame; the applied authorities' records before the first frame; a start's records and transfer log at the start; a storage write's record, a log, a SELFDESTRUCT's records and transfer log once the opcode completed; deployed code after every deposit charge and before the creation commits; a hint before it is forwarded, on the transaction alone.
- `SATIN-ACCT-003` — A deposit's data size is counted like any transaction's; a deposit that fails keeps its body and its admitted hints.
- `SATIN-ACCT-004` — A write record is one account or storage write the transaction keeps: a slot's while its value differs from its original value in the transaction; an account's while its nonce, balance or code differs from what the transaction loaded (its original info at first load).
- `SATIN-ACCT-005` — The writes that make records: a value transfer's sender and recipient; a creation's created account and the creator's nonce; a SELFDESTRUCT's beneficiary and cleared account; an applied authority; the transaction's value recipient or created account; a created account is no exception.
- `SATIN-ACCT-006` — A record is made where the write is and taken back where a write returns the account (a value transfer's return in the frame it starts, with its data size; a SELFDESTRUCT's where it completes); a slot written back gives its record back.
- `SATIN-ACCT-007` — A value-transferring CALLCODE, and a value CALL to the calling account itself, change no account and record none.
- `SATIN-ACCT-008` — The sender's account is one of the body's fixed records and is never recorded again.
- `SATIN-ACCT-009` — An applied EIP-7702 authority is changed by its nonce and delegation when applied; a later write to it adds nothing.
- `SATIN-ACCT-010` — The four fee accounts are in the body only for the settlement's fee credits; a write execution makes to one that is not the sender is recorded like any other.
- `SATIN-ACCT-011` — A successful frame's records and bytes merge into its caller's; a failed frame's are discarded and the records it took back stand again, the creator's nonce record excepted.
- `SATIN-ACCT-012` — The KV count is the write-record count; each record weighs WRITE_RECORD_SIZE = 40 bytes of data size, counted and taken back with it; TX_KV_UPDATE_LIMIT is enforced on the count even though the data-size cap binds first at these constants; a record taken back cannot cross it.
- `SATIN-ACCT-013` — State growth is the net count of new accounts and new slots kept: one unit per account-leaf or fresh-slot charge site, not per byte of code or indicator.
- `SATIN-ACCT-014` — The rises: a fresh slot; a value CALL to an EIP-161-empty account; a SELFDESTRUCT moving a non-zero balance to a non-existent account; the recipient a transaction's value creates; an applied authorization that creates its authority; a creation onto an empty address; a keyless signer its creation's bump creates; a deposit-like transaction's created caller.
- `SATIN-ACCT-015` — Not rises: an existing account, a CALLCODE, a value call to the calling account, deployed code, the delegation indicator.
- `SATIN-ACCT-016` — The SSTORE state-growth transition table (original, present, new) and its worked sequences.
- `SATIN-ACCT-017` — The settlement's fee credits are neither rises nor EIP-8037 charge sites.
- `SATIN-ACCT-018` — Falls happen at the opcode that restores the state and cannot cross a limit; the only slot fall is original zero, present non-zero, new zero.
- `SATIN-ACCT-019` — A rise that would take the signed net past the transaction limit or the frame budget is the crossing and is not kept.
- `SATIN-ACCT-020` — A failed deposit that creates its caller counts one unit of growth on the transaction and the block counter, pays no state gas, and is not stopped; a deposit that succeeds or reverts makes the ordinary charged rise, kept through a stop of its first frame.

## Spec History

- [Satin](../../upgrades/satin.md) — The reviewers' delta of Satin against Rex6.
