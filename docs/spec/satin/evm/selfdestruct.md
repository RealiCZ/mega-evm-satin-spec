---
description: Satin (unstable) — SELFDESTRUCT and the Destruction Table. SELFDESTRUCT under EIP-6780: the destruction table that refills the state gas and takes back the records of what a transaction created and destroys, the marked account afterwards, the beneficiary's rise, the order of a destruction's effects, and the creation-collision rule.
spec: Satin
maturity: unstable
---

# SELFDESTRUCT and the Destruction Table

{% hint style="warning" %}
**Unstable** — Satin is under active development: every value and rule on this page may change before Satin is frozen.
{% endhint %}

Abstract: `SELFDESTRUCT` deletes an account only when the account was created in the same transaction (EIP-6780); the first such destruction applies the destruction table to every part of the account — its leaf, its code and its slots — giving back the state gas, the state growth, the write records and the code's data size and history gas of each part the transaction made, and marking the account so nothing further is charged or counted for it.

## Motivation

A contract created and destroyed in one transaction leaves no state behind, yet the transaction paid state gas for its leaf, its code and its slots, counted them as state growth, and made write records for them.
If none of that is given back, a factory pattern that creates and destroys a helper contract pays for state no node stores and is stopped by a state-growth limit for growth the block never keeps.
If it is given back carelessly, a destruction can give back what another transaction or an earlier part of the state paid, or give the same part back twice, and a transaction could earn gas by destroying.

## Specification

### EIP-6780 and the first effective destruction

- `SATIN-SD-001` `SELFDESTRUCT` MUST follow [EIP-6780](https://eips.ethereum.org/EIPS/eip-6780): it moves the account's balance to its beneficiary, and it deletes the account only when the account was created in the same transaction.
- `SATIN-SD-012` A `SELFDESTRUCT` of an account that was not created in the transaction MUST NOT apply the destruction table and MUST NOT mark the account: it subtracts nothing, refills nothing and takes nothing back, and EIP-6780 does not delete the account.
- `SATIN-SD-002` The first effective `SELFDESTRUCT` of an account created in the same transaction MUST apply the table of `SATIN-SD-004` to every part of that account — its leaf, its deployed code and each of its slots — by the part's value at the transaction's start and its value before the destruction, and MUST mark the account as destroyed.
- `SATIN-SD-003` A slot's value at the transaction's start MUST be its original value in the transaction, the value it held when the transaction first accessed it.
  A slot of the created account that the transaction first accesses after the creation reads zero, whatever the state held there, and so has an original of zero; a slot the transaction accessed before the creation keeps the value it held then as its original.

### The table

- `SATIN-SD-004` The destruction MUST apply, to each part, the effect of its row:

  | Part          | At the transaction's start | Before   | Effect                                                                                                                                                         |
  | ------------- | -------------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
  | Account leaf  | absent                     | present  | Refill the leaf's state gas; state growth −1; take the account's write record back                                                                            |
  | Account leaf  | present                    | present  | Nothing: the leaf existed before the transaction, and its write record stands                                                                                  |
  | Deployed code | absent                     | present  | Refill the code's state gas; take back its data size and its history gas                                                                                       |
  | Deployed code | absent                     | absent   | Nothing                                                                                                                                                        |
  | Deployed code | present                    | present  | Not reached: non-empty code at the start collides with the creation (`SATIN-SD-016`)                                                                           |
  | Slot          | zero                       | non-zero | Refill the slot's state gas; state growth −1; take the slot's write record back                                                                                |
  | Slot          | zero                       | zero     | Nothing: the slot is already clear                                                                                                                             |
  | Slot          | non-zero                   | any      | Nothing of the refill or the fall; the write record of a slot the transaction loaded stands, and the deletion makes it when that slot still holds its original value; a slot the transaction did not load has no record |

  Every part is deleted with the account.
- `SATIN-SD-005` A refill MUST be the price that part was charged — its schedule entry times the bucket multiplier of that charge ([State Gas and SALT Pricing](state-gas.md)) — and MUST go to the destroying frame, also when another frame paid it.
  On the absent-leaf row the leaf's charge is the one this transaction made for that leaf: at the value transfer that funded the address, at a `SELFDESTRUCT` that paid it, at the transaction's own value, or at the creation when the created address was empty.
- `SATIN-SD-006` State growth MUST fall for the absent leaf and for each slot on the zero-then-non-zero row, and for nothing else in the table.
  The fall of the absent leaf stands also when the creation itself added no rise, as when the transaction funded the address and then created onto it.
  An address that held a balance before the transaction is on the present-leaf row: the creation adds no rise for that leaf, the destruction subtracts none, and the write record the nonce bump made stands.
- `SATIN-SD-007` A write record the table takes back MUST return its data size to the destroying frame's budget and its history gas to the destroying frame, and the KV count falls by that record.
  When the destroying frame is the transaction's own frame and that frame succeeds, this return is the record's history gas once, and the settlement MUST NOT give that charge back again (`SATIN-HIST-005`).
- `SATIN-SD-008` Deployed code is neither a write record nor a unit of state growth; code on the absent-then-present row MUST return its data size and its history gas as a record taken back does.
- `SATIN-SD-009` The give-back MUST follow the refill order of `SATIN-HIST-012` and is a give-back of state or history gas, as a slot written back to zero is, not an EIP-3529 refund.
  It MUST be credited with the completed write, after every charge the opcode makes: a charge the frame cannot pay halts the opcode first, and the give-back is not credited.
  It MUST NOT raise the destroying frame's remaining in any dimension above the budget the frame was given (`SATIN-LIM-004`).
- `SATIN-SD-010` When the destroying frame succeeds, the give-back is unspent gas of that frame and returns up the chain with it.
  When the destroying frame fails, or a frame containing it fails, the mark and every effect of the table MUST be discarded: the charges stand, or come back by the ordinary rule for that failure, and a record the table took back stands again; the discarded give-back is not a further one.

### The marked account

- `SATIN-SD-011` A later `SELFDESTRUCT` of the same account while the mark stands MUST apply the table for nothing: it subtracts nothing, refills nothing and takes nothing back.
- `SATIN-SD-013` From the first effective destruction until the end of the transaction, while the mark stands, the account MUST add nothing further to state growth and keep no further state gas: an `SSTORE` of one of its slots neither rises nor falls and neither charges nor refills fresh-slot state gas, its regular gas being unchanged.
  A write to the account or to one of its slots makes no record.
- `SATIN-SD-014` Code deposited after a constructor destroyed its own account, on the absent-then-absent row, MUST NOT be charged state gas; its data size and history gas MUST be charged as any deposited code's, and no later destruction takes them back.
- `SATIN-SD-015` Value sent to the marked account MUST NOT be a rise and MUST make no write record.
  The account still exists until the transaction ends, and MUST then be removed with the balance it holds ([EIP-7708 Transfer Logs](transfer-logs.md)); its logs and the transfer log of the balance moved stay counted and charged.
  The removal MUST NOT take a record back again, and MUST NOT take the code's data size or history gas back again.

### Collisions and empty leaves

- `SATIN-SD-016` A creation MUST collide when the created address holds non-empty code or a nonce other than zero, and MUST NOT collide on storage alone: [EIP-7610](https://eips.ethereum.org/EIPS/eip-7610) is not applied.
  A creation can therefore land on an address with nonce zero, empty code and storage.
  A slot of such an address that the transaction first accesses once the account is created reads zero and is on a zero row; a slot the state held that the transaction never accessed makes no record when the account is destroyed; a slot the transaction accessed before the creation keeps the value it held, and the destruction deletes it with the account as an ordinary deletion, which makes its write record while it still holds that value.
- `SATIN-SD-017` An account that is empty under EIP-161 while its leaf is in the state the transaction loaded — nonce zero, balance zero, empty code, storage that is not empty — MUST be the present-leaf row: the creation charges new-account state gas and counts a rise, the address being empty under EIP-161 (`SATIN-STATE-004`, `SATIN-ACCT-014`), and the destruction MUST NOT refill that charge or subtract that rise.
  An address the state holds no account for is absent, never an empty account.

### The beneficiary and the order of a destruction

- `SATIN-SD-018` A `SELFDESTRUCT` that moves a non-zero balance to a distinct account that does not exist MUST be a rise of state growth and MUST be charged new-account state gas ([State Gas and SALT Pricing](state-gas.md)), a repeated destruction included; a zero balance creates no account and is not a rise.
  That rise MUST be held to the limits only after the operation's give-back, which cannot cross a limit.
  A frame exactly at its state-growth budget that destroys an account created in the transaction, with N new slots, while moving a non-zero balance to a new beneficiary, subtracts `1 + N` when the leaf was absent at the transaction's start and N when it was present, before it adds the beneficiary.
- `SATIN-SD-019` A `SELFDESTRUCT` MUST proceed in this order:
  1. its charges: its regular gas, at which compute is decided — a regular charge that crosses gas detention stops the frame there, and the operation applies none of the table and no beneficiary ([Gas Detention](gas-detention.md)) — and the new-account state gas of a beneficiary it creates; a charge the frame cannot pay halts the opcode before anything below;
  2. the table's give-back: the state-growth falls, the state-gas refills, the write records, and the deployed code's data size and history gas;
  3. its positive effects, held in the dimension order data size, KV updates, state growth (`SATIN-LIM-010`): the records it makes — the account it clears, when that account was not created in the transaction and this write makes its record; a loaded pre-existing slot of an account the table covers, when the deletion makes that slot's record; and its beneficiary — and its transfer log, then the beneficiary's state growth;
  4. the history of the records it makes (`SATIN-HIST-013`).

  When a positive effect crosses a limit, the frame stops and the operation keeps nothing: the table's effects, the beneficiary and the transfer log are discarded with it.
- `SATIN-SD-020` A `SELFDESTRUCT`'s volatile reads of either end — the destroyed account or the beneficiary being the block beneficiary ([Gas Detention](gas-detention.md)) — MUST be marked only after its last step that can fail.

### Retired ids

None.

## Constants

This page defines no constants of its own; the prices and sizes it gives back are those of [State Gas and SALT Pricing](state-gas.md) and [History Gas and the History Allowance](history-gas.md).

## Rationale

**Why refill state gas EIP-8037 leaves charged?**
EIP-8037 specifies that a destruction of a same-transaction account produces no state-gas refill.
Satin refills it, because a part the transaction made does not remain for any node to store: keeping the charge would make state gas price state that does not exist, and the state-growth count, which falls, and the state gas, which would not, would disagree.
Rex6 refunded none of its storage gas; Satin's table restores the alignment between what a transaction keeps and what it pays.

**Why only parts absent at the transaction's start?**
A part that existed before the transaction was paid for by whoever created it, in another transaction; giving it back would pay this transaction for state it did not add.
Reading each part's value at the transaction's start, rather than at the creation, also makes a slot accessed before the creation an ordinary deletion.

**Why give everything back to the destroying frame?**
The frame that destroys the account is the one whose action removes the state, and it may be a different frame from the one that paid; giving each part back to its payer would credit frames that have already returned.
A failure of the destroying frame discards the give-back with the mark, so no frame is credited for a destruction that did not happen.

**Why no storage collision?**
EIP-7610 refuses a creation onto non-empty storage, and Ethereum's clients apply it retroactively.
The engine reads storage slot by slot and cannot see storage it has not loaded, so it cannot tell a collision with storage alone; execution that has always applied EIP-161 and EIP-6780 does not produce such an address, but it can be in the state a block is given, and the rows of the table say what happens to its slots.

**Why hold the beneficiary only after the give-back?**
A destruction that frees growth and creates a beneficiary in the same opcode keeps the net; holding the rise before the falls would stop a frame at its budget for growth it does not keep.

## Security Considerations

- If a node refilled parts that existed at the transaction's start, a transaction could destroy a contract it created onto a funded address and be paid for a leaf another transaction bought.
- If the mark did not stop further charges and counts, a transaction could fill a destroyed account's slots, have them refilled again, and mint gas.
- If a failure of the destroying frame kept the give-back, a callee could destroy, collect the refill, and revert, keeping the gas while the account survives.
- If a node answered an address it holds no account for as an empty account, it would put that leaf on the present row, refill nothing, and execute a different chain from a node that answers it absent.
- If the give-back could raise a frame's remaining above its budget, a destruction could enlarge the budgets of the frames started after it.
- This page preserves the invariant that a transaction's state gas, state growth and write records for an account it creates and destroys return to what they would be had it never created the account, except for code deposited after the destruction.

## Spec History

- [Satin](../../upgrades/satin.md) — Kept EIP-6780 destruction of Rex6's [SELFDESTRUCT](../../evm/selfdestruct.md) and replaced its state-growth refund with the destruction table, which refills state gas and takes back records, data size and history gas of every part the transaction made.
