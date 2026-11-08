---
description: Satin (unstable) — History Gas and the History Allowance. Stub of the Satin specification: the rules this page will specify.
spec: Satin
maturity: unstable
---

# History Gas and the History Allowance

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
This page is a stub. It lists what the page will specify; the specification text is written after the outline is reviewed.
{% endhint %}

Abstract: The third gas ledger: the price per byte of what a transaction appends to the chain's history, the byte table, when each history charge is made and given back, the exemptions, and the history allowance of a value call.

## Specification

The rules this page will specify, by their proposed ids:

- `SATIN-HIST-001` — COST_PER_HISTORY_BYTE = 88 gas per byte, never scaled by SALT.
- `SATIN-HIST-002` — The byte table, shared with data size: TX_BODY_SIZE 310; calldata 1 per byte; access-list address 20; access-list key 32; authorization 101; log 32 + 32 per topic + data; write record 40; deployed code 1 per byte.
- `SATIN-HIST-003` — TX_BODY_SIZE is TX_BASE_SIZE 110 plus TX_FIXED_WRITE_RECORDS = 5 records (the sender and the four fee accounts), charged as an upper bound whether or not each is written; it covers the sender's account writes and the fee credits only.
- `SATIN-HIST-004` — The body is charged before execution as intrinsic state gas, not part of the intrinsic regular gas, and never reported on the state ledger.
- `SATIN-HIST-005` — The applied authorities' records and the first frame's start record are charged before the first frame; the authorities' records stay when the first frame fails; the start record comes back with that frame, once, also when the destruction table already took it back; an out-of-gas before the first frame keeps neither.
- `SATIN-HIST-006` — A log, a storage write's record and a SELFDESTRUCT's records are charged by the opcode once it completed; what the opcode takes back is given back first, then what it makes is charged.
- `SATIN-HIST-007` — A part the destruction table takes back is given back to the destroying frame even when another frame paid it; every other record to whoever paid it.
- `SATIN-HIST-008` — An opcode that fails after its write was observed keeps nothing and is charged no history; a LOG observes its write after every inherited charge.
- `SATIN-HIST-009` — A call or creation charges its own frame for the records the frame it starts makes, after the forward is computed; a caller that cannot pay halts out of gas and the frame does not start; the price of a record the start takes back returns to the caller once the frame returned with its start kept.
- `SATIN-HIST-010` — A value CALL to an empty account charges in order: its regular gas (static 100, memory, value transfer, cold surcharge and the new account's regular gas, zero), the new account's state gas reservoir first, the 98/100 forward of the regular gas left, then the start records' history; the reservoir share follows the history charge.
- `SATIN-HIST-011` — CREATE and CREATE2 charge the created account's state gas, when the address is empty, before computing the forward, and give the reservoir share after the start records' history.
- `SATIN-HIST-012` — Every give-back of state or history gas follows one refill order: the frame's regular gas first, up to the spill still outstanding on that frame, the rest to its reservoir.
- `SATIN-HIST-013` — A record an opcode commits is checked against the limits before its history is charged; a frame that cannot pay that history halts out of gas keeping neither the record nor its bytes.
- `SATIN-HIST-014` — At a frame start the calling opcode pays for the records before the start and they are counted; the charge for a start a limit stops is given back when the stopped frame returns.
- `SATIN-HIST-015` — The start records are charged as the state stands: a value the caller cannot fund, a creator nonce that cannot be bumped, or a call depth past the limit makes no record and is charged nothing.
- `SATIN-HIST-016` — No history gas for an EIP-7708 transfer log, an Oracle hint's payload, or any byte of a deposit, a system-originated transaction or a system call (their deposited-code history is zero); the exemption is from history gas alone.
- `SATIN-HIST-017` — The floor is still computed; it can raise the gas used of a transaction exempt from history gas, binds the block's execution figure, and where it binds is drawn from the whole gas limit; a deposit is charged nothing either way.
- `SATIN-HIST-018` — A value-transferring CALL or CALLCODE below the transaction's own frame grants the frame it starts a history allowance of HISTORY_ALLOWANCE_BYTES = 160 bytes (14,080 gas).
- `SATIN-HIST-019` — Only a log's history charge in that frame draws the allowance, before the frame's gas; a write record never does.
- `SATIN-HIST-020` — The allowance is not frame gas: it pays for nothing else, is never returned as gas and is on no ledger; the bytes it pays for still count as appended.
- `SATIN-HIST-021` — The transfer log of the value that granted the allowance does not draw on it.

## Spec History

- [Satin](../../upgrades/satin.md) — The reviewers' delta of Satin against Rex6.
