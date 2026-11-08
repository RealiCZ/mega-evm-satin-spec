---
description: Satin (unstable) — Write and Take-Back Patterns. Every pattern in which a transaction makes a write and takes it back — a slot written 0 → x → 0 and its relatives, an account returned to what was loaded, a created account destroyed, a delegation set and cleared, logs, frame starts, failed and stopped frames and deposits — with what regular gas and the EIP-3529 refund counter, state gas, history gas, state growth, KV updates and data size each do, the frame a give-back goes to, and the order.
spec: Satin
maturity: unstable
---

# Write and Take-Back Patterns

{% hint style="warning" %}
**Unstable** — Satin is under active development: every value and rule on this page may change before Satin is frozen.
{% endhint %}

Abstract: A transaction can make a write and take it back — write a slot and write it back, move value and move it back, create an account and destroy it, or fail the frame that wrote; this page states, for every such pattern, what each gas ledger and each resource count does, to which frame each give-back goes, and in what order, gathering in one place what the pages of the charges and counts specify.

## Motivation

A write that is taken back touches six figures at once: the regular gas of the opcodes and the EIP-3529 refund counter, the state gas of new state, the history gas of a [write record](../../glossary.md#write-record), and the data-size, KV-update and state-growth counts the [resource limits](resource-limits.md) hold.
Each figure has its own rule on its own page, and the rules differ in which frame they credit: a slot written back gives its gas to the frame that writes it back, a destruction gives to the destroying frame, a failed frame's rollback gives to the failed frame itself, and a refused or stopped start gives back to its caller.
Read one page at a time, the combination is easy to get wrong — a give-back credited to the frame that paid, a record taken back twice, a refund counted as a give-back — and any such slip changes a frame's `GAS`, its forwards and whether a later charge fits, which changes the transaction's path.

## Specification

The rules of this page apply to every transaction and every system call.
A deposit, a system-originated transaction and a system call pay no history gas, so every history charge and give-back below is zero for them (`SATIN-HIST-016`); a system-originated transaction and a system call are priced at `m = 1` and held to no limit, their counts still being made (`SATIN-STATE-009`, `SATIN-LIM-001`).
Each row of a table is a pattern of writes; the rules each row follows from are named in its first cell, and the row restates them for that pattern.
A table is one rule, and a row is cited as `SATIN-TAKE-<NNN>/<row>`, the row named by its first cell's label.

### The ledgers and the frame credited

- `SATIN-TAKE-001` For every pattern of the tables below, a node MUST charge, give back and count as the pattern's row states, in the order the row states, on each of these:
  - **regular gas and the EIP-3529 refund counter** — the regular charges of the opcodes ([Gas Schedule and Intrinsic Gas](gas-schedule.md)), and the refund counter the inherited `SSTORE` rules raise and lower, which is capped and applied only when the transaction settles (`SATIN-POOL-018`);
  - **state gas** — a state charge and its refill ([State Gas and SALT Pricing](state-gas.md)), at the bucket multiplier `m` fixed for the transaction (`SATIN-STATE-006`);
  - **history gas** — a history charge and its give-back ([History Gas and the History Allowance](history-gas.md));
  - **state growth**, **KV updates** and **data size** — the three counts of [Resource Accounting](resource-accounting.md), on the net of the frame named.
- `SATIN-TAKE-002` A give-back of state gas or history gas MUST go to the frame that makes it — the frame running the opcode that takes the record or the state back, or the caller of a start when that start returns — in that frame's refill order: its regular gas first, up to its outstanding spill, and the rest to its reservoir (`SATIN-HIST-007`, `SATIN-HIST-012`).
  The two exceptions are the destruction table, whose give-back goes to the destroying frame (`SATIN-SD-005`, `SATIN-SD-007`), and the rollback of a failed frame, which gives the failed frame's own charges back inside that frame (`SATIN-POOL-014`).
  A frame can therefore spend, while it runs, gas an ancestor paid for what the frame takes back, up to the price of those records and that state; that gas returns up the chain with the frame's unspent gas when the frame succeeds, and is undone by the frame's rollback when it fails (`SATIN-TAKE-004`).
- `SATIN-TAKE-003` A give-back of state or history gas MUST NOT be an EIP-3529 refund: it is credited at once, to the frame of `SATIN-TAKE-002`, is not capped, and does not change the refund counter; the refund counter MUST change only by the inherited `SSTORE` rules, a frame's changes to it merging into its caller's when it succeeds and being discarded when it fails.
- `SATIN-TAKE-004` Every count a frame makes, a fall and a take-back included, MUST be on that frame's own net: it merges into the caller's net when the frame succeeds and is discarded when it fails, and a record the failed frame took back stands again (`SATIN-ACCT-011`, `SATIN-LIM-006`).
  A count made outside every frame — the body, the applied authorities' records, the caller a deposit creates, an admitted Oracle hint — is on the transaction's net and is not discarded by a frame's failure (`SATIN-LIM-005`).
  The rollback of a failed frame (`SATIN-POOL-014`) MUST undo the give-backs the frame received together with the charges it made: it leaves the frame exactly the reservoir it received when it started and its regular gas less the regular charges it made, whatever state and history charges and give-backs happened in between; regular gas a give-back credited and the frame then spent on a regular charge stays spent, as any regular charge does, and a halt then consumes the regular gas left.

In the tables, `m` is the multiplier of the bucket the state lands in, and "spill-first" is the refill order of `SATIN-TAKE-002`.
Regular gas is stated for a warm access; a cold one adds the cold surcharge the schedule names.

### Storage slot

- `SATIN-TAKE-005` A storage slot written by `SSTORE` and taken back MUST be accounted as this table states, the first value of a pattern being the slot's original value in the transaction (`SATIN-SD-003`), each `SSTORE` in the order: the `SSTORE` minimum-gas check, the regular charge with the refund counter's change and the fresh-slot state charge or refill, then the limits on the record in the order data size, KV updates, state growth (`SATIN-LIM-010`), then the history give-back of a record taken back, then the history charge of a record made (`SATIN-HIST-006`, `SATIN-HIST-013`):

| Pattern | Regular gas and EIP-3529 refund | State gas | History gas | State growth | KV updates | Data size | Frame credited | Order |
| ------- | ------------------------------- | --------- | ----------- | ------------ | ---------- | --------- | -------------- | ----- |
| zero-back: `0 → x → 0` (`SATIN-STATE-008`, `SATIN-ACCT-004`, `SATIN-ACCT-016`) | First write `WARM_STORAGE_READ_COST + SSTORE_WRITE_COST`; second `WARM_STORAGE_READ_COST` and refund `+SSTORE_RESTORE_REFUND` | `+SLOT_STATE_GAS × m`, then the refill `−SLOT_STATE_GAS × m` | `+RECORD_HISTORY_GAS`, then `−RECORD_HISTORY_GAS` | +1, then −1 | +1, then −1 | `+WRITE_RECORD_SIZE`, then `−WRITE_RECORD_SIZE` | The frame running the second `SSTORE`, spill-first | Second `SSTORE`: its regular charge, refund and refill, then the limits, then the history give-back |
| restore: `x → y → x`, `x ≠ 0` (`SATIN-ACCT-004`, `SATIN-ACCT-016`) | First `WARM_STORAGE_READ_COST + SSTORE_WRITE_COST`; second `WARM_STORAGE_READ_COST` and refund `+SSTORE_RESTORE_REFUND` | None | `+RECORD_HISTORY_GAS`, then `−RECORD_HISTORY_GAS` | None | +1, then −1 | `+WRITE_RECORD_SIZE`, then `−WRITE_RECORD_SIZE` | The frame running the second `SSTORE`, spill-first | Second `SSTORE`: its regular charge and refund, then the limits, then the history give-back |
| clear-back: `x → 0 → x`, `x ≠ 0` (`SATIN-ACCT-004`, `SATIN-ACCT-016`) | First `WARM_STORAGE_READ_COST + SSTORE_WRITE_COST` and refund `+SSTORE_CLEAR_REFUND`; second `WARM_STORAGE_READ_COST` and refund `−SSTORE_CLEAR_REFUND + SSTORE_RESTORE_REFUND` | None | `+RECORD_HISTORY_GAS`, then `−RECORD_HISTORY_GAS` | None | +1, then −1 | `+WRITE_RECORD_SIZE`, then `−WRITE_RECORD_SIZE` | The frame running the second `SSTORE`, spill-first | Second `SSTORE`: its regular charge and refund, then the limits, then the history give-back |
| rewrite: `0 → x → y`, `y ≠ 0` (`SATIN-STATE-008`, `SATIN-ACCT-016`) | First `WARM_STORAGE_READ_COST + SSTORE_WRITE_COST`; second `WARM_STORAGE_READ_COST`, no refund | `+SLOT_STATE_GAS × m` once; the second write charges and refills nothing | `+RECORD_HISTORY_GAS` once | +1 once | +1 once | `+WRITE_RECORD_SIZE` once | No give-back | First `SSTORE`: its regular and state charges, then the limits, then the history charge |
| again: `0 → x → 0 → x` (`SATIN-STATE-008`, `SATIN-ACCT-016`) | `WARM_STORAGE_READ_COST + SSTORE_WRITE_COST`, `WARM_STORAGE_READ_COST` with refund `+SSTORE_RESTORE_REFUND`, `WARM_STORAGE_READ_COST + SSTORE_WRITE_COST`; the refund stays | Charged, refilled, charged | Charged, given back, charged | +1, −1, +1 | +1, −1, +1 | `WRITE_RECORD_SIZE` added, taken back, added | The frame running the second `SSTORE`, for its give-backs | Each `SSTORE` in the order of zero-back or rewrite |
| rolled-back: a write the writing frame's revert or halt discards (`SATIN-POOL-014`, `SATIN-ACCT-011`) | The `SSTORE`'s regular gas stays spent; a revert returns the frame's unspent regular gas to its caller, a halt consumes it; the frame's refund-counter changes are discarded | Given back by the rollback: the part the reservoir paid to the reservoir, the spilled part to regular gas, which a halt consumes | As state gas | Discarded with the frame | Discarded; a record the frame took back stands again | Discarded | The failed frame itself, by its rollback | At the failing frame's end |
| descendant: a write a frame made that a descendant running on the same storage takes back — by `DELEGATECALL`, or by a call back into the writing contract (`SATIN-HIST-007`, `SATIN-TAKE-002`) | The descendant pays `WARM_STORAGE_READ_COST`; its refund `+SSTORE_RESTORE_REFUND` (or the clear-back change) is on its own counter, merged into the writer's when it succeeds | A fresh slot (zero original): the writer paid the charge and the descendant receives the refill; a non-zero original: none | The writer paid the charge; the descendant receives the give-back | A fresh slot: −1 on the descendant's net, which can be negative; a non-zero original: none | −1 on the descendant's net | `−WRITE_RECORD_SIZE` on the descendant's net | The descendant, spill-first; when it fails, its give-backs are discarded, the record stands again and the writer's charges stay paid | In the descendant's `SSTORE`, as zero-back; merged or discarded at its return |
| ancestor: a write a descendant made and merged by succeeding, taken back by an ancestor (`SATIN-HIST-007`) | The ancestor's `SSTORE` and refund, as the first rows | A fresh slot: the ancestor receives the refill; a non-zero original: none | The ancestor receives the give-back | A fresh slot: −1 on the ancestor's net; a non-zero original: none | −1 on the ancestor's net | `−WRITE_RECORD_SIZE` on the ancestor's net | The ancestor, spill-first | In the ancestor's `SSTORE`, as zero-back |
| refused: a write whose record crosses a limit (`SATIN-HIST-013`, `SATIN-STOP-004`) | The regular charge stays spent; the frame is stopped and reverts with the gas it has left | The fresh-slot charge, made before the limits, is given back by the stopped frame's rollback | Not charged | Not counted | Not counted | Not counted | The stopped frame, by its rollback | The regular and state charges, then the limit that crosses; no history |

  Example (descendant): a contract P whose slot 0 holds 7 writes 8, paying `RECORD_HISTORY_GAS` (3,520) for the record, then makes a `DELEGATECALL` to C with no reservoir.
  C emits an empty `LOG0`, whose 2,816 of history gas spill onto C's regular gas, and writes slot 0 back to 7: the 3,520 go to C, 2,816 unwinding C's spill and 704 entering C's reservoir, so a `GAS` C runs next reads 2,816 more than before the write; C's refund counter rises by `SSTORE_RESTORE_REFUND`, its KV net is −1, and its data-size net is −8: −40 for the record taken back and +32 for the `LOG0`.
  When C returns successfully, its unspent gas and its 704 of reservoir return to P and its nets merge, so P's record and its price are gone.
  When C reverts instead, the slot is 8 again and P's record and its 3,520 stand; C's rollback (`SATIN-TAKE-004`) leaves C the reservoir it received, zero, and its regular gas less its regular charges alone: the 704 leave with the rollback, and the 2,816 the give-back credited to C's regular gas are the `LOG0`'s spill, which the rollback would have returned to it anyway, so nothing is returned to P twice.

### Account

- `SATIN-TAKE-006` An account's nonce, balance or code written and taken back MUST be accounted as this table states, an account's record existing while it differs from what the transaction loaded (`SATIN-ACCT-004`); the sender, whose account is a fixed record of the body, makes none (`SATIN-ACCT-008`):

| Pattern | Regular gas and EIP-3529 refund | State gas | History gas | State growth | KV updates | Data size | Frame credited | Order |
| ------- | ------------------------------- | --------- | ----------- | ------------ | ---------- | --------- | -------------- | ----- |
| sent-back: value sent from P to Q and sent back from Q to P, both existing and neither the sender (`SATIN-ACCT-006`, `SATIN-HIST-009`) | Each call's regular charges, `VALUE_TRANSFER_COST` among them; no refund | None | The first call charges P `2 × RECORD_HISTORY_GAS` after its forward; the second makes no record and gives `2 × RECORD_HISTORY_GAS` back | None | +2 on the first start, −2 on the second | `+2 × WRITE_RECORD_SIZE + TRANSFER_LOG_SIZE`, then `−2 × WRITE_RECORD_SIZE + TRANSFER_LOG_SIZE`: both transfer logs stay | Q, the caller of the second start, spill-first, once that start's frame returned with its start kept; if that frame fails, the records stand again and nothing is given back | First start: its regular charges, the forward, then the records' history; the give-back at the second start's return, after the reservoir join of `SATIN-POOL-012` |
| destruct-back: an account a `SELFDESTRUCT` returns to what the transaction loaded, of an account not created in the transaction (`SATIN-HIST-006`, `SATIN-SD-012`) | The `SELFDESTRUCT`'s regular charge; no refund | None | `RECORD_HISTORY_GAS` given back for each account the move returns to what was loaded, before the history of a record the move makes is charged | None | −1 for each account returned | `−WRITE_RECORD_SIZE` for each account returned, `+TRANSFER_LOG_SIZE` for the move | The frame running the `SELFDESTRUCT`, spill-first | `SATIN-SD-019`: its charges, then the records it takes back, then its positive effects held to the limits, then the history of the records it makes |
| failed-new: a value `CALL` to an account empty under EIP-161 whose child reverts or halts (`SATIN-HIST-010`, `SATIN-POOL-015`, `SATIN-HIST-014`) | The call's regular charges stay spent | `+ACCOUNT_STATE_GAS × m` charged to the caller before the forward, given back to the caller after the reservoir the child returns was joined (`SATIN-POOL-012`) | The start's records charged to the caller after the forward, given back to the caller when the child returns failed | +1 on the start, discarded | The start's records, discarded | The start's records and transfer log, discarded | The caller, spill-first | `SATIN-HIST-010` at the call; at the return the reservoir join, then the state give-back, then the records' give-back |
| self: a value `CALLCODE`, or a value `CALL` to the calling account itself (`SATIN-ACCT-007`, `SATIN-LOG-003`) | The call's regular charges | None | None | None | None | None: no record and no transfer log | No give-back | None |
| keyless-back: a keyless deployment from signer nonce 1 whose creation's bump is set back (`SATIN-KEY-013`) | The call's regular charges | Step 10 charged nothing (the signer is not empty) | Step 14's charge for the signer's record given back when the set-back leaves the signer as loaded | None | The signer's record: none when the set-back leaves the account as loaded | None for the signer's record | The keyless call, spill-first | At the creation's return, by the nonce rule of `SATIN-KEY-013`, before the call answers |

  Example (sent-back): P, a contract, calls Q with 1 wei and Q calls P back with 1 wei.
  The first call charges P 7,040 of history after its forward and counts two records and a transfer log on its start: KV +2, data size +240.
  The second start, made by Q, takes both records back: KV −2 and data size −80 + 160 on that start, and once P's re-entered frame returns successfully Q is given 7,040; Q has no outstanding spill, so they enter Q's reservoir, which returns to P with Q's unspent gas, where they unwind P's spill first.

### Created account and the destruction table

- `SATIN-TAKE-007` An account created in the transaction and destroyed by its first effective `SELFDESTRUCT`, and a creation that fails, MUST be accounted as this table states, the destruction table's give-back going to the destroying frame whichever frame paid, and following `SATIN-SD-019`'s order: the opcode's charges, the table's give-back, the positive effects held to the limits, the history of the records the opcode makes:

| Pattern | Regular gas and EIP-3529 refund | State gas | History gas | State growth | KV updates | Data size | Frame credited | Order |
| ------- | ------------------------------- | --------- | ----------- | ------------ | ---------- | --------- | -------------- | ----- |
| absent-leaf: an account absent at the transaction's start, created and destroyed (`SATIN-SD-004`, `SATIN-SD-005`, `SATIN-SD-006`, `SATIN-SD-007`) | The `SELFDESTRUCT`'s regular charge; the refund counter is not touched by the table | Refill of the leaf's charge `ACCOUNT_STATE_GAS × m` | `RECORD_HISTORY_GAS` given back for the account's record | −1 | −1 | `−WRITE_RECORD_SIZE` | The destroying frame, spill-first | `SATIN-SD-019` step 2 |
| funded-then-created: an address the transaction funded, then created onto and destroyed (`SATIN-SD-005`, `SATIN-SD-006`) | As absent-leaf | Refill of the charge the funding transfer made for the leaf | The address's one record given back | −1, although the creation added no rise | −1 | `−WRITE_RECORD_SIZE` | The destroying frame, spill-first | `SATIN-SD-019` step 2 |
| present-leaf: a leaf in the state at the transaction's start — funded before, or empty under EIP-161 with storage (`SATIN-SD-006`, `SATIN-SD-017`) | As absent-leaf | No refill: a funded leaf was charged nothing; an empty leaf was charged at the creation (`SATIN-STATE-011`), and that charge stays | The record the nonce bump made stands | No fall: a funded leaf added no rise; an empty leaf's rise stays | The record stands | Stands | No give-back for the leaf | None for the leaf |
| code: deployed code of the destroyed account (`SATIN-SD-004`, `SATIN-SD-008`) | None | Refill `CODE_STATE_GAS × code length × m` | `COST_PER_HISTORY_BYTE × code length` given back | None | None: code is no record | `−code length` | The destroying frame, spill-first | `SATIN-SD-019` step 2 |
| fresh-slot: a slot whose original value is zero, non-zero before the destruction (`SATIN-SD-003`, `SATIN-SD-004`) | None; the refund counter's changes of earlier `SSTORE`s stand | Refill `SLOT_STATE_GAS × m` | `RECORD_HISTORY_GAS` given back | −1 | −1 | `−WRITE_RECORD_SIZE` | The destroying frame, spill-first | `SATIN-SD-019` step 2 |
| loaded-slot: a slot whose original value is not zero, which only a slot loaded before the creation has (`SATIN-SD-003`, `SATIN-SD-004`, `SATIN-SD-019`) | None | None | A changed slot's record stands; a slot still at its original value has its record made by the deletion, `+RECORD_HISTORY_GAS` on the destroying frame | None | Stands, or +1 when the deletion makes it | Stands, or `+WRITE_RECORD_SIZE` | The destroying frame pays a record the deletion makes | `SATIN-SD-019` steps 3 and 4 for a record the deletion makes |
| discarded: the destroying frame, or a frame containing it, fails (`SATIN-SD-010`) | As the failure's rollback | The refills are discarded with the mark; the charges stand, or come back by the failure's own rule | As state gas | The falls are discarded | Every record the table took back stands again | The give-backs are discarded | No frame keeps the table's give-back | At the failing frame's end |
| marked: a later `SELFDESTRUCT` of the marked account, an `SSTORE` of one of its slots, value sent to it (`SATIN-SD-011`, `SATIN-SD-013`, `SATIN-SD-015`) | The opcode's regular gas is unchanged | Nothing charged or refilled | No record; logs and transfer logs still charged and counted | Nothing | Nothing | Logs and transfer logs only | No give-back | None |
| after-destroy: code deposited after the constructor destroyed its own account (`SATIN-SD-014`) | The deposit's regular charges | None | `COST_PER_HISTORY_BYTE × code length` charged and never given back | None | None | `+code length`, never taken back | No give-back | `SATIN-SCHED-011`: the deposit's charges, then its data size |
| first-frame: a creation transaction whose own frame destroys the created account (`SATIN-HIST-005`, `SATIN-SD-007`) | As absent-leaf | As absent-leaf | The first frame's start record, charged before the first frame, is given back once: by the table when the first frame succeeds, by the settlement when it fails | As absent-leaf | As absent-leaf | As absent-leaf | The transaction's own frame | The table's give-back in the first frame, or the settlement's |
| failed-create: a `CREATE` or `CREATE2` whose child reverts or halts (`SATIN-POOL-015`, `SATIN-HIST-014`, `SATIN-LIM-008`) | The creation's regular charges stay spent | `ACCOUNT_STATE_GAS × m`, charged when the address was empty under EIP-161, given back to the creator after `SATIN-POOL-012` | The created account's record's history given back to the creator; the creator's nonce record and its history are kept | The created account's rise is discarded | The created account's record is discarded; the creator's nonce record is counted on the creator | Likewise | The creator, spill-first | At the return: the reservoir join, the state give-back, the records' give-back, then the creator's nonce record counted |
| collision: a creation onto an address with code or a nonce (`SATIN-SD-016`, `SATIN-LIM-016`) | The creation's regular charges and its forward are spent | None: the address was not empty | The created account's record's history given back to the creator; the creator's nonce record and its history kept | None | The created account's record discarded; the creator's nonce record counted on the creator | Likewise; no transfer log | The creator, spill-first, for the created account's record | As failed-create |

  Example (absent-leaf, code, fresh-slot): P creates C at an empty address in a bucket with `m = 1`; C's constructor writes two fresh slots and C deploys 100 bytes of code; later, called by P, C destroys itself holding no balance.
  The creation and the constructor charged 183,600 + 2 × 97,920 + 100 × 1,530 = 532,440 of state gas and 3 × 3,520 + 100 × 88 = 19,360 of history gas, and counted state growth +3, KV +3 and data size +220; P's nonce record, counted on P, stays.
  The destruction gives C's frame 532,440 of state gas and 19,360 of history gas back, spill-first, and counts −3, −3 and −220 on C's net, so a successful return leaves the transaction as if C had never been created, but for P's nonce record and the regular gas spent.

### Delegation indicator

- `SATIN-TAKE-008` An authorization list's writes, and their fate when the first frame fails or a charge before it cannot be paid, MUST be accounted as this table states, every charge being made on the transaction outside every frame in the order of `SATIN-SCHED-008`:

| Pattern | Regular gas and EIP-3529 refund | State gas | History gas | State growth | KV updates | Data size | Frame credited | Order |
| ------- | ------------------------------- | --------- | ----------- | ------------ | ---------- | --------- | -------------- | ----- |
| set-then-clear: two accepted authorizations for one authority holding no indicator at the start, a non-zero target and then the zero one (`SATIN-AUTH-009`, `SATIN-SCHED-008`) | `ACCOUNT_WRITE` once, for the first write, unless the transaction already paid it; no refund for any authority (`SATIN-SCHED-007`) | `DELEGATION_STATE_GAS × m` once at the first; the clear charges none and gives none back; `ACCOUNT_STATE_GAS × m` once when the authority is empty under EIP-161 | One record, `RECORD_HISTORY_GAS`, unless the authority is the sender | +1 once when empty under EIP-161 | +1 once, the sender excepted | `+WRITE_RECORD_SIZE` once | No give-back | `SATIN-SCHED-008` step 2 for each entry, then step 3 |
| reset: an authority holding an indicator at the start, cleared and set again (`SATIN-AUTH-009`) | `ACCOUNT_WRITE` once | None for the indicator | One record | None | +1 | `+WRITE_RECORD_SIZE` | No give-back | `SATIN-SCHED-008` step 2, then step 3 |
| first-frame-fails: the first frame reverts, halts or is stopped after the list applied (`SATIN-AUTH-016`, `SATIN-STOP-011`, `SATIN-HIST-005`, `SATIN-POOL-016`) | The first frame's regular gas returns, or a halt consumes it | The authorities' state gas is kept; the first frame's failure returns no reservoir those charges drew | The authorities' records' history is kept; the first frame's start record's history comes back | The authorities' units are kept | The authorities' records are kept | Kept | The transaction, at its settlement | At the settlement |
| skipped: a list whose KV or state-growth total would cross the transaction limit (`SATIN-AUTH-010`, `SATIN-AUTH-011`) | The intrinsic gas stays | None charged | None charged; the body's stays | None | None | The body's stays | No give-back: nothing was charged | Decided before any charge of the list (`SATIN-AUTH-010`) |
| pre-frame-out-of-gas: a charge before the first frame that cannot be paid after part of the list applied (`SATIN-SCHED-009`, `SATIN-SCHED-010`) | The intrinsic gas stays; the rest of the regular budget is consumed | Every authority's charge taken back; the reservoir left returns to the sender | The authorities' records taken back; the body's stays | Taken back | Taken back | The body's stays | The sender, at the settlement | At the charge that cannot be paid; nothing runs after it |

  Example (set-then-clear): a list whose two entries are signed by A, empty under EIP-161 and not the sender, the first delegating to D at nonce 0 and the second clearing at nonce 1.
  The first entry charges `ACCOUNT_STATE_GAS`, `ACCOUNT_WRITE` and `DELEGATION_STATE_GAS`; the second charges nothing and gives the indicator's 35,190 back to no one; the list keeps one record for A, one unit of state growth, and leaves A with nonce 2 and no code.

### Logs and transfer logs

- `SATIN-TAKE-009` A log and a transfer log MUST be accounted as this table states; neither is a write record, and neither is taken back by a later write:

| Pattern | Regular gas and EIP-3529 refund | State gas | History gas | State growth | KV updates | Data size | Frame credited | Order |
| ------- | ------------------------------- | --------- | ----------- | ------------ | ---------- | --------- | -------------- | ----- |
| log-reverted: a log in a frame that then reverts or halts, or whose caller later fails (`SATIN-HIST-006`, `SATIN-POOL-014`) | The log's regular charges stay spent | None | Given back by the rollback of the frame that fails | None | None | Discarded | The failing frame, by its rollback | Charged once the `LOG` completed and its bytes passed the limits; given back at the failing frame's end |
| log-allowance: a log the frame's history allowance paid, in a frame that then fails (`SATIN-HIST-019`, `SATIN-HIST-020`) | As log-reverted | None | None: the allowance is not gas, so nothing returns to any frame | None | None | Discarded | No give-back | The allowance first, then the frame's gas |
| transfer-failed: the transfer log of a value call whose child fails (`SATIN-LOG-002`, `SATIN-LOG-006`) | None of its own | None | None: a transfer log pays none | None | None | `TRANSFER_LOG_SIZE` discarded with the start | No give-back | Counted with the start, discarded at the child's failed return |
| transfer-back: the transfer logs of a value sent and sent back (`SATIN-LOG-001`, `SATIN-ACCT-006`) | None of their own | None | None | None | None | `2 × TRANSFER_LOG_SIZE`, both kept while the records are taken back | No give-back | Each counted with its start |

  Example (log-reverted): a frame emits `LOG2` with 64 bytes of data — 32 + 2 × 32 + 64 = 160 bytes, 14,080 of history gas, data size +160 — and then reverts: the 14,080 come back to that frame by its rollback, spill-first as charged, and the 160 bytes are discarded; had the frame been a value call's child, its history allowance would have paid the 14,080 and nothing would come back.

### Frame-start records

- `SATIN-TAKE-010` The records, state and transfer log a frame start makes MUST be accounted as this table states, the caller paying the start's records' history after the forward and the start being counted once it is decided (`SATIN-HIST-009`, `SATIN-HIST-014`, `SATIN-LIM-013`):

| Pattern | Regular gas and EIP-3529 refund | State gas | History gas | State growth | KV updates | Data size | Frame credited | Order |
| ------- | ------------------------------- | --------- | ----------- | ------------ | ---------- | --------- | -------------- | ----- |
| start-stopped: a start a limit stops (`SATIN-HIST-014`, `SATIN-STOP-013`, `SATIN-POOL-015`) | The opcode's regular charges stay spent; the forward returns untouched | A new-account or created-account charge is given back to the caller | The start's records' history is given back to the caller when the stopped frame returns | Not kept | Not kept | Not kept: value, transfer log and created account are reverted | The caller, spill-first | At the stopped frame's return: the reservoir join, the state give-back, then the records' give-back |
| answer-stopped: a start answered without a frame — no code, a precompile's success — whose start crosses (`SATIN-STOP-014`, `SATIN-STOP-016`) | The answer is replaced by the stop on the untouched forward | As start-stopped | As start-stopped | Not kept | Not kept | Not kept | The caller, spill-first | As start-stopped |
| refused: a start the caller's account refuses — a value it cannot fund, a creation whose nonce cannot be bumped, whose endowment it cannot fund, or past the call-depth limit (`SATIN-HIST-015`, `SATIN-LIM-015`) | The opcode's regular charges before the refusal stay spent | A value `CALL` to an account empty under EIP-161 is charged `ACCOUNT_STATE_GAS × m` and given it back at the return; a refused creation charges none | None: no record is made | None | None | None: no transfer log | The caller, for the state charge, spill-first | The opcode's regular charges and the state charge, then the refusal; the state give-back at the return |
| precompile-failed: a precompile that fails after its value moved (`SATIN-LIM-014`) | The forward is consumed | As failed-new for an empty recipient | The start's records' history is given back to the caller | None | None | None | The caller, spill-first | At the failed answer's return |
| start-returns: a start whose value returns accounts to what the transaction loaded (`SATIN-ACCT-006`, `SATIN-HIST-009`) | The call's regular charges | None | No charge for the records it takes back; their price is given back to the caller once the frame returned with its start kept | None | Each record taken back, on the started frame's net | `−WRITE_RECORD_SIZE` each, on the started frame's net, `+TRANSFER_LOG_SIZE` | The caller, spill-first | The take-back counted when the start is decided; the history given back once the frame returned with its start kept |
| tx-start: the record of the transaction's own frame's start, its value's recipient or its created account (`SATIN-HIST-005`, `SATIN-SCHED-008`) | None of its own | The recipient's or created account's state gas is the first frame's, given back when it fails (`SATIN-POOL-015`) | Charged before the first frame; comes back when the first frame fails or is stopped | The first frame's | The first frame's | The first frame's | The transaction, at its settlement | `SATIN-SCHED-008` step 3; given back at the settlement |

  Example (start-stopped): P calls Q, empty under EIP-161, with 1 wei, and the start crosses P's KV budget.
  P was charged `ACCOUNT_STATE_GAS × m` before the forward and `2 × RECORD_HISTORY_GAS` after it; the stopped frame returns `MegaLimitExceeded(1, budget)` with the forward untouched, and P is given both charges back, spill-first, with nothing counted and no transfer log kept.

### Failed and stopped frames

- `SATIN-TAKE-011` A frame that fails MUST be accounted as this table states, whatever writes and take-backs it made:

| Pattern | Regular gas and EIP-3529 refund | State gas | History gas | State growth | KV updates | Data size | Frame credited | Order |
| ------- | ------------------------------- | --------- | ----------- | ------------ | ---------- | --------- | -------------- | ----- |
| reverted: a frame below the transaction's own reverts (`SATIN-POOL-014`, `SATIN-TAKE-004`) | Its unspent regular gas, the returned spill included, returns to the caller; its refund-counter changes are discarded | Every charge it made and merged is given back: the reservoir part to its reservoir, which is again the share it received, the spilled part to its regular gas; a give-back it received is discarded | As state gas | Its net is discarded | Its net is discarded; records it took back stand again | Its net is discarded | The failed frame, by its rollback; the caller then joins its reservoir by `SATIN-POOL-012` | At the frame's end; the caller then joins its reservoir (`SATIN-POOL-012`) |
| halted: an exceptional halt (`SATIN-POOL-014`, `SATIN-OUT-007`) | Its regular gas, the returned spill included, is consumed; the refund-counter changes are discarded | As reverted; its reservoir share returns to the caller | As reverted | Discarded | Discarded | Discarded | As reverted, but no regular gas returns | As reverted |
| stopped: a limit stop, or gas detention's crossing (`SATIN-STOP-004`, `SATIN-STOP-005`, `SATIN-DET-018`) | As reverted; for gas detention, the frame's gas is put back to what it was before the crossing charge | As reverted | As reverted | As reverted; the crossing write is not counted | As reverted | As reverted | As reverted | At the crossing, then as reverted |
| creator-survives: the creator's nonce record across a failed creation (`SATIN-LIM-008`, `SATIN-STOP-015`) | None | None | Kept | A creator account the bump creates is kept | Counted on the creator | Counted on the creator | No give-back | Counted on the creator at the creation's return |
| hint-survives: an Oracle hint the failed frame admitted (`SATIN-STOP-012`, `SATIN-ORCL-009`) | None | None | None | None | None | Stays counted on the transaction | No give-back | Counted when the hint is admitted |
| own-frame: the transaction's own frame fails (`SATIN-POOL-017`, `SATIN-STOP-009`, `SATIN-POOL-015`) | Unspent regular gas returns to the sender, unless the frame halted | The recipient's or created account's state gas charged before the frame is given back to the transaction, spill-first; the reservoir left returns to the sender | The first frame's start record comes back (`SATIN-HIST-005`) | What was counted before the first frame stays | Likewise | Likewise | The sender, at the settlement | At the settlement |

  Example (reverted, halted): a child receives a reservoir share of 100,000 and 50,000 of regular gas, and writes a fresh slot at `m = 1`: 97,920 from the reservoir, then 3,520 of history, 2,080 from the reservoir and 1,440 spilled onto regular gas.
  When it reverts, its reservoir is 100,000 again and its regular gas is 1,440 higher, all of which returns to the caller; when it halts, the 100,000 still return and its regular gas, those 1,440 included, is consumed.

### Deposits

- `SATIN-TAKE-012` A deposit MUST be accounted as this table states; a deposit pays no history gas, so every history give-back of the tables above is zero for it (`SATIN-HIST-016`), and it reports zero history bytes (`SATIN-HIST-022`):

| Pattern | Regular gas and EIP-3529 refund | State gas | History gas | State growth | KV updates | Data size | Frame credited | Order |
| ------- | ------------------------------- | --------- | ----------- | ------------ | ---------- | --------- | -------------- | ----- |
| failed-deposit: a deposit that fails validation, cannot pay a charge made before its first frame, or whose own frame halts (`SATIN-DEP-004`, `SATIN-DEP-005`, `SATIN-DEP-006`, `SATIN-ACCT-020`) | The whole gas limit, reported as regular gas; no refund | None, a created caller's included | None | +1 for a caller empty under EIP-161, uncharged; everything else taken back | Every record taken back: zero | The body and the admitted hints stay; everything else taken back | No give-back: nothing returns to the sender, the reservoir and the withheld gas included | At the deposit's end, in place of the settlement |
| deposit-reverted: a deposit whose own frame reverts or is stopped (`SATIN-STOP-010`, `SATIN-STOP-011`, `SATIN-DEP-003`) | As any revert of the own frame | The created caller's `ACCOUNT_STATE_GAS × m` is kept; the frame's charges come back by its rollback | None | The created caller's +1 is kept; the frame's net is discarded | The frame's net is discarded | The body and hints stay; the frame's net is discarded | The sender, at the settlement | As own-frame |

  Example (failed-deposit): a deposit with a gas limit of 1,000,000 from a sender empty under EIP-161, whose first frame halts after its caller's 183,600 of state gas was paid, reports 1,000,000 of regular gas, no state and no history gas, one unit of state growth, zero KV updates, the data size of its body and calldata, and zero history bytes; its sender keeps the nonce bump and the mint.

### Retired ids

None.

## Constants

| Constant                  | Value   | Description                                                                                     |
| ------------------------- | ------- | ----------------------------------------------------------------------------------------------- |
| `COST_PER_HISTORY_BYTE`   | 88      | Gas per history byte ([History Gas and the History Allowance](history-gas.md))                  |
| `WRITE_RECORD_SIZE`       | 40      | Bytes of one write record                                                                       |
| `RECORD_HISTORY_GAS`      | 3,520   | History gas of one write record, `WRITE_RECORD_SIZE × COST_PER_HISTORY_BYTE`                    |
| `TRANSFER_LOG_SIZE`       | 160     | Data size of one EIP-7708 transfer log ([EIP-7708 Transfer Logs](transfer-logs.md))             |
| `SLOT_STATE_GAS`          | 97,920  | State gas of a fresh storage slot at `m = 1` ([State Gas and SALT Pricing](state-gas.md))       |
| `ACCOUNT_STATE_GAS`       | 183,600 | State gas of a new or created account at `m = 1`                                                |
| `CODE_STATE_GAS`          | 1,530   | State gas per byte of deployed code at `m = 1`                                                  |
| `DELEGATION_STATE_GAS`    | 35,190  | State gas of an EIP-7702 delegation indicator at `m = 1`                                        |
| `WARM_STORAGE_READ_COST`  | 100     | `SSTORE` static cost, a warm slot's access ([Gas Schedule and Intrinsic Gas](gas-schedule.md))  |
| `SSTORE_WRITE_COST`       | 10,000  | Regular gas of an `SSTORE` of a fresh slot or a reset, before its load cost                     |
| `SSTORE_RESTORE_REFUND`   | 10,000  | Refund of an `SSTORE` that restores a fresh slot or a reset to its original value               |
| `SSTORE_CLEAR_REFUND`     | 11,616  | Refund of an `SSTORE` that clears a slot whose original value is not zero                       |
| `VALUE_TRANSFER_COST`     | 11,300  | Regular gas of a call's value transfer, its stipend included                                    |
| `ACCOUNT_WRITE`           | 9,000   | EIP-8038 account write of an authority                                                          |

## Rationale

**Why gather the patterns on one page?**
The rules that make a write and take it back are spread over the pages of the charges and counts they own, and each is right on its own; what an implementer has to get right is their combination, which no single page shows.
One table per kind of write, with a column per figure, makes every combination explicit and lets a fixture name the pattern it exercises.

**Why does a give-back go to the frame that makes it?**
A give-back is made by an opcode, and only the frame running it can receive gas at that moment: the frame that paid may be suspended above it, or may already have returned.
EIP-8037's own state-gas refill credits the running frame, so a slot's state and history give-backs land together; the destruction table differs because the parts it gives back may have been paid by frames that have all returned.

**Why is a give-back not an EIP-3529 refund?**
A refund is capped at a fifth of the gas used and settles only at the end, so it cannot cancel the charge it answers; a give-back of state or history gas is the charge undone, and it has to be exact and immediate, or a slot written and cleared would cost or earn gas.

## Security Considerations

- If a node credited a give-back to the frame that paid, the running frame would see less gas than every other node's, and a forward, a `GAS` reading or a charge that fits on one node would fail on another.
- If a failed frame kept a give-back it received, a callee could take back a record its caller paid for, collect the gas and revert, so the record stands while the gas has been spent twice.
- If a give-back counted as an EIP-3529 refund, its cap would leave part of a charge unanswered, and a slot written and written back would cost more than leaving it alone.
- If a take-back were counted on the frame that made the write instead of the frame that undoes it, a failed undo would leave the record taken back, and a transaction could keep a write without its count.
- This page preserves the invariant that a pattern whose writes all end as they began leaves no state gas, no history gas, no state growth, no KV update and no record bytes on any ledger, its regular gas and the transfer logs it emitted excepted.

## Spec History

- [Satin](../../upgrades/satin.md) — Introduced history gas, write records and the destruction table, whose write and take-back patterns this page gathers; Rex6 refunded none of its storage gas ([Dual Gas Model](../../evm/dual-gas-model.md)).
