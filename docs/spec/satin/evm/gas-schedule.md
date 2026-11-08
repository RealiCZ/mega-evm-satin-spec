---
description: Satin (unstable) — Gas Schedule and Intrinsic Gas. Stub of the Satin specification: the rules this page will specify.
spec: Satin
maturity: unstable
---

# Gas Schedule and Intrinsic Gas

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
This page is a stub. It lists what the page will specify; the specification text is written after the outline is reviewed.
{% endhint %}

Abstract: The Amsterdam gas schedule Satin runs with its two changes, the EIP-2780 intrinsic cost, the charges made before the first frame, the code-deposit charge order and the addresses warm from the start of a transaction.

## Specification

The rules this page will specify, by their proposed ids:

- `SATIN-SCHED-001` — The gas schedule is Amsterdam's (EIP-8038's state-access prices, EIP-2780's intrinsic decomposition, EIP-7976's calldata floor, EIP-7981's access-list floor) with two changes: the EIP-8037 state-gas entries rebuilt at the cost per state byte, and deposited code's history gas at one history byte.
- `SATIN-SCHED-002` — Every opcode's static gas is Amsterdam's: EXTCODESIZE and EXTCODECOPY pay 200, EIP-8038's two warm accesses.
- `SATIN-SCHED-003` — The regular-gas entries that differ from Osaka, each with its value (the entry table).
- `SATIN-SCHED-004` — A cold SSTORE pays 2,100 for its access with its static cost (EIP-8038 folds the warm base into a cold slot's access).
- `SATIN-SCHED-005` — The floor's base is the transaction's own decomposed base without its calldata, access-list, authorization and initcode costs (12,000, 15,000, 21,000 or 24,000), plus 64 gas per calldata byte, initcode included, and 64 per access-list byte (20 per address, 32 per key).
- `SATIN-SCHED-006` — The EIP-2780 intrinsic regular gas: TX_BASE_COST 12,000, plus 3,000 for a recipient other than the sender and 6,000 more with value, plus 12,000 and EIP-3860's initcode cost for a creation, plus calldata, access-list and per-authorization costs; a transfer to the sender itself pays the base alone.
- `SATIN-SCHED-007` — The 7,816 per authorization is charged by validation for every entry, applied or not; an authority that already exists is refunded nothing.
- `SATIN-SCHED-008` — The state-dependent parts (a recipient or created account that does not exist, an authority that does not exist, a delegation indicator, an authority's first write) are charged at the start of execution, priced as state gas.
- `SATIN-SCHED-009` — A transaction that cannot pay a charge made before its first frame (a deposit-like caller account, an authorization's charges, the pre-frame write-record history, the first frame's start charge) runs out of gas without running a frame; a list the KV or growth limit skips is not charged.
- `SATIN-SCHED-010` — On that path everything applied before the first frame is taken back but validation's changes to the sender and a deposit-like caller account; the intrinsic gas and the body's history stay charged, the rest of the regular budget is consumed, the reservoir left returns, and a creation's sender keeps its nonce bump.
- `SATIN-SCHED-011` — Deposited code is charged after the code passed its checks, in order: the regular per-byte cost (zero), the hashing cost at 6 gas per 32-byte word, the code's state gas, its history gas; a creation that cannot pay one runs out of gas and leaves no code.
- `SATIN-SCHED-012` — Precompiles, the block beneficiary and access-list addresses listed without keys are warm from the start (EIP-2929); Rex6's cold charge on their first CALL-family or SELFDESTRUCT-beneficiary touch does not apply.
- `SATIN-SCHED-013` — The SequencerRegistry's account and its _currentSystemAddress slot are warm from the start of every transaction.
- `SATIN-SCHED-014` — The sender and a call's recipient are warm from the start, as EIP-2929 leaves them.

## Spec History

- [Satin](../../upgrades/satin.md) — The reviewers' delta of Satin against Rex6.
