---
description: Satin (unstable) — EIP-7702 Authorizations Before the First Frame. How a transaction's authorization list is decided before its first frame — the simulation that loads every gated authority, the totals held to the KV and state-growth limits, the all-or-nothing skip settled as a stop — and the charges, records and warmth of an applied list.
spec: Satin
maturity: unstable
---

# EIP-7702 Authorizations Before the First Frame

{% hint style="warning" %}
**Unstable** — Satin is under active development: every value and rule on this page may change before Satin is frozen.
{% endhint %}

Abstract: Before its first frame, an EIP-7702 transaction's authorization list is simulated in order to find the write records and new accounts it would keep; a list whose totals would cross the transaction's KV or state-growth limit is skipped whole and the first frame is stopped, and a list that fits is applied, charged and kept through any later stop of the first frame.

## Motivation

An authorization list is applied before any frame exists, so no frame budget holds it and no caller can catch a stop it causes.
A list of a thousand entries for new authorities adds a thousand accounts, which crosses the state-growth limit, and the state gas of 1,001 new authorities fits in a gas limit above the execution cap; applying such a list and then reverting it would cost the node the work and leave the limits meaningless, while applying part of it would make the result depend on where the node stopped.

Which authorities a list would create or change depends on the state — whether each authority exists, what code it holds, what its nonce is — so a node cannot decide the list without reading the authorities, and a stateless validator must be given every account that decision read.

## Specification

### The simulation

- `SATIN-AUTH-001` Before the first frame of an EIP-7702 transaction, a node MUST decide its authorization list by simulating EIP-7702 application in list order, whatever the length of the list.
  A node MUST NOT omit the simulation for a list too short to cross either limit.
  The simulation MUST write nothing and warm nothing.
- `SATIN-AUTH-002` An entry whose chain id is neither zero nor the chain's, whose nonce is `2^64 − 1`, or whose signature does not recover an authority MUST be skipped, and its authority's account MUST NOT be read.
- `SATIN-AUTH-003` Every other entry MUST load its authority's account with its code.
  An authority whose account holds code other than an EIP-7702 delegation indicator MUST be skipped, and its simulated nonce MUST NOT be bumped.
- `SATIN-AUTH-004` The entry's nonce MUST then be compared with the authority's effective nonce:
  - when an earlier entry of the list for the same authority was accepted, the simulated nonce after those acceptances;
  - otherwise, when the authority is the sender, the sender's nonce after validation's bump, so an authorization signed for the sender's nonce before the transaction does not match;
  - otherwise, the authority's current nonce.

  A nonce that differs MUST skip the entry; a nonce that matches accepts it, and the simulated nonce MUST then become one higher.
- `SATIN-AUTH-005` The simulation MUST walk the whole list and MUST NOT stop at the first entry that would cross a limit.
  Each distinct authority whose entry passed the chain-id, nonce and signature gates of `SATIN-AUTH-002` MUST be loaded once, and a later entry for that authority MUST use the simulated nonce and the code already loaded.
  Every authority so loaded is in the block's witness, whether or not the list is applied ([The Stateless Witness](../block/stateless-witness.md)).
- `SATIN-AUTH-006` A failure to read an authority the simulation consults is a database fault, and the transaction MUST have no outcome: when the node's database declares the error fatal the node MUST report an internal error, and any other database error MUST make the block invalid ([Halts, Reverts and Stops](outcomes.md)).
  The block MUST NOT be refused for the limit instead, also when an earlier prefix of the list would already have crossed.
- `SATIN-AUTH-007` The simulation MUST charge no gas, a cold access included; the intrinsic `PER_AUTH_BASE_COST` of every entry is already charged by validation, applied or not ([Gas Schedule and Intrinsic Gas](gas-schedule.md)).

### The list's totals

- `SATIN-AUTH-008` The totals the list would keep, were it applied, MUST be:
  - one write record for each distinct accepted authority other than the sender, whose account is a fixed record of the body (`SATIN-ACCT-008`), however many of its entries are accepted;
  - one unit of state growth for each distinct accepted authority whose account does not exist, however many of its entries are accepted;
  - the new-account state gas once for each such new authority.
- `SATIN-AUTH-009` Delegation-indicator state gas MUST be charged at most once per authority, and only when an accepted authorization writes a non-zero delegation designator, the authority holds no delegation indicator at the start of the transaction, and no earlier authorization in the list set one for it.
  An authority that holds an indicator at the start of the transaction is charged none, a clear and a later non-zero authorization included; a clear charges none; two accepted non-zero authorizations for an authority that holds none at the start charge it once.
  An authorization with a zero delegation target still bumps the nonce and can create the account, and charges no indicator.
  The indicator is not a unit of state growth.

### A list that does not fit

- `SATIN-AUTH-010` If the list's KV or state-growth total would exceed the transaction's KV-update or state-growth limit, given what the body and the counts before it left ([Resource Limits](resource-limits.md)), the node MUST apply none of the list, MUST charge none of its authorities' state gas or record history, and MUST stop the transaction's own frame before it runs, with `MegaLimitExceeded` of the crossed kind and that transaction limit ([Limit Stops](limit-stops.md)).
  No frame budget exists yet, so the stop names the transaction limit; when both would be crossed the kind is 1.
  Data size cannot be crossed here, since validation refuses a body that, with `WRITE_RECORD_SIZE` bytes for each authorization entry, exceeds the data-size limit ([Transaction Validation and Refusals](../block/transaction-validation.md)), and compute does not apply.
- `SATIN-AUTH-011` A skipped list MUST keep no authority account, no authority write record, no authority state gas and no authority history; no delegation is written, and no authority nonce is bumped beyond the sender's validation bump.
  The intrinsic regular gas, the body's history gas and the body's data size stay.
- `SATIN-AUTH-012` On a skip the authorities the simulation consulted MUST NOT be made warm, except one already warm from the transaction's start: the sender, the recipient of a call, the block beneficiary, an access-list address, a precompile, or the `SequencerRegistry`'s account ([Gas Schedule and Intrinsic Gas](gas-schedule.md)).
- `SATIN-AUTH-013` The skip MUST be all or nothing, including an authority that would have fitted by itself, and MUST be settled as a revert-class stop of the transaction's own frame, which settles as `SATIN-STOP-009` states ([Limit Stops](limit-stops.md)).

### A list that fits

- `SATIN-AUTH-014` A list that fits MUST be applied as EIP-7702 applies it, which warms every authority whose account the application loads: an entry skipped for its chain id, for a nonce of `2^64 − 1` or for a signature that does not recover an authority is not loaded and is not warmed; an entry skipped because its authority's code is not a delegation, or because its nonce does not match, is loaded before that check, and its authority is warmed.
- `SATIN-AUTH-015` The authorities' state gas, their `ACCOUNT_WRITE` ([Gas Schedule and Intrinsic Gas](gas-schedule.md)) and the history of their write records MUST be charged when the list is applied, and reduce what the first frame is given.
  If one of those charges cannot be paid, the transaction MUST take the pre-frame out-of-gas path of `SATIN-SCHED-009`: the authorizations are taken back, and for a transaction other than a deposit this is an out-of-gas halt, not a limit stop.
  The limit is decided before those charges, so a list that does not fit never takes that path.
- `SATIN-AUTH-016` When the list fits, a later stop or revert of the first frame MUST keep the authorizations, with their state gas, their write records and the history those records cost (`SATIN-STOP-011`).
- `SATIN-AUTH-017` The caller account a deposit creates is not an authorization: it MUST always be created and kept, and, being one account, it cannot by itself cross `TX_STATE_GROWTH_LIMIT` ([Deposit Transactions](../block/deposits.md)).
- `SATIN-AUTH-018` The list rule MUST be decided during execution, where the authorities are read; it is not a rejection a transaction pool can make before inclusion.

### Retired ids

None.

## Constants

| Constant                | Value   | Description                                                        |
| ----------------------- | ------- | ------------------------------------------------------------------ |
| `PER_AUTH_BASE_COST`    | 7,816   | Intrinsic regular gas of one authorization entry                    |
| `ACCOUNT_WRITE`         | 9,000   | EIP-8038 account write, charged per applied authority's first write |
| `WRITE_RECORD_SIZE`     | 40      | Data size of one write record                                      |
| `TX_KV_UPDATE_LIMIT`    | 500,000 | KV-update limit of one transaction                                 |
| `TX_STATE_GROWTH_LIMIT` | 1,000   | State-growth limit of one transaction                              |

## Rationale

**Why simulate the whole list before applying any of it?**
Whether the list fits is a property of the whole list: a later entry for the same authority neither adds an account nor a record, and an authority that already exists adds no growth.
Deciding before applying anything means a list that does not fit leaves nothing applied, and the node never has to undo part of a list.

**Why every list, and not only a long one?**
A list shorter than what the limits leave cannot cross them, so for the limit alone its simulation is redundant.
But the simulation also fixes which authority accounts the transaction loads: an application that runs out of gas part-way through the list stops loading there, while the simulation has already loaded every gated authority.
Running the simulation for every list makes the set of accounts a transaction loads, and so the witness a stateless validator is given, the same whatever the list's length and wherever an out-of-gas falls.

**Why all or nothing?**
That is Rex6's rule for this list.
A partial application would depend on the order of the entries and on where a node stopped, and the authorities of the entries applied first would keep a state the limit refused.

**Why a stop rather than a halt?**
Rex6 halted the transaction.
Under Satin a stop of the first frame does not revert what was applied before it, so applying the list and then stopping would keep more than the limit allows; skipping the list and stopping the first frame keeps nothing of the list, and settles the transaction as every other limit stop is settled, with its sender paying only for what ran.

**Why is the indicator charged at most once?**
The indicator is 23 bytes of code an authority holds once, however many authorizations in the list set it; a clear removes it, and an authority that held one before the transaction adds no new bytes.

## Security Considerations

- If a node applied a list and only then held it to the limits, a transaction could make the node apply and revert thousands of authorizations for the price of a stop.
- If a node stopped simulating at the first crossing, the accounts a transaction loads would depend on where the crossing falls, and a stateless validator given the building node's witness could fail to re-execute it.
- If a skipped list left its authorities warm, a later access by the transaction would be charged as warm on one node and cold on another.
- If a database fault while reading an authority were treated as a crossing, a node with a failing database would include a stopped transaction where a healthy node computes a different result.
- This page preserves the invariant that a transaction never keeps more write records or state growth from its authorization list than its limits allow, and that an applied list is kept whole or not at all.

## Spec History

- [Satin](../../upgrades/satin.md) — Kept Rex6's all-or-nothing skip of an authorization list that would cross the KV or state-growth limit (see [Rex6](../../upgrades/rex6.md)), settled it as a stop of the first frame instead of a halt, and charged an applied list's state gas, account writes and record history when it is applied.
