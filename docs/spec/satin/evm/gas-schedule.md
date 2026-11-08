---
description: Satin (unstable) — Gas Schedule and Intrinsic Gas. The Amsterdam gas schedule with its three changes, the regular-gas entries that differ from Osaka, the EIP-2780 intrinsic regular gas and the floor, the charges made before the first frame and their out-of-gas path, the code-deposit charge order, and the addresses warm from a transaction's start.
spec: Satin
maturity: unstable
---

# Gas Schedule and Intrinsic Gas

{% hint style="warning" %}
**Unstable** — Satin is under active development: every value and rule on this page may change before Satin is frozen.
{% endhint %}

Abstract: The gas schedule every charge is priced from: Amsterdam's, with its state-gas entries rebuilt at MegaETH's cost per state byte and deposited code charged one history byte per byte; this page also specifies the intrinsic regular gas and the floor, which charges are made at the start of execution, what happens when one cannot be paid, the order of the code-deposit charges, and which addresses are warm from a transaction's start.

## Motivation

The Prague schedule prices state access and creation as one cost in one dimension: a fresh slot costs 20,000 of the same gas that pays for computation, and a value transfer that creates its recipient 25,000 more.
Once state is paid in its own dimension ([Two-Pool Gas](gas-model.md)), the regular part of those costs has to be the work they are (an access and a write), or new state is paid twice, once as computation and once as state.

Prague's intrinsic cost has the same problem: a flat 21,000 includes the recipient's access and a value transfer's writes whether or not the transaction makes them, and an EIP-7702 authorization costs 25,000 up front with 12,500 refunded when its authority already exists, so the up-front price is wrong for one of the two cases.
A charge that depends on state cannot be made correctly before the state is read.

## Specification

### The schedule

- `SATIN-SCHED-001` The gas schedule MUST be Amsterdam's — including [EIP-8038](https://eips.ethereum.org/EIPS/eip-8038)'s state-access prices, [EIP-2780](https://eips.ethereum.org/EIPS/eip-2780)'s decomposition of the intrinsic cost, [EIP-7976](https://eips.ethereum.org/EIPS/eip-7976)'s calldata floor and [EIP-7981](https://eips.ethereum.org/EIPS/eip-7981)'s access-list floor — with exactly three changes:
  - the EIP-8037 state-gas entries MUST be rebuilt at `COST_PER_STATE_BYTE` ([State Gas and SALT Pricing](state-gas.md));
  - the history gas of deposited code MUST be `COST_PER_HISTORY_BYTE` per byte ([History Gas and the History Allowance](history-gas.md)), where Amsterdam prices it at zero;
  - the forwarding reduction of a call or a creation MUST be the 98/100 cap of [Gas Forwarding](gas-forwarding.md) (`SATIN-FWD-001`), where Amsterdam keeps EIP-150's 63/64: a caller keeps `remaining × 2 / 100` of its regular gas instead of `remaining / 64`, so 1,000 regular gas forwards 980, not 985.

  Every other entry MUST be Amsterdam's: every regular-gas entry, the regular code-deposit cost, the EIP-7702 entries, and the entries Amsterdam introduced for EIP-8037, EIP-2780, EIP-7976 and EIP-7981.
  The regular gas of creating state is therefore the access and the write EIP-8038 prices, and the new state itself is paid in state gas alone.
  A node MUST apply EIP-8038 as of [commit `4c7e2487e4`](https://github.com/ethereum/EIPs/commit/4c7e2487e4da3131bcadc7399f8b153f5344c0b7) (18 September 2026), EIP-2780 as of [commit `7243c92ba8`](https://github.com/ethereum/EIPs/commit/7243c92ba812437c64bae9fc6524ee269b29daa9) (4 September 2026), EIP-7976 as of [commit `c998ef94eb`](https://github.com/ethereum/EIPs/commit/c998ef94eb16a6af8a9b8e2084f947b17ea14865) (7 July 2026) and EIP-7981 as of [commit `747b78c0ed`](https://github.com/ethereum/EIPs/commit/747b78c0edfdf04e9e2933ad1bec592d3318e1d9) (7 July 2026), each the revision current when the EIP-8037 profile was frozen (`SATIN-POOL-004`); every value of them a transaction's outcome depends on is restated on this page, so the pins are their provenance.
- `SATIN-SCHED-002` The static gas every opcode pays before its dynamic cost MUST be Amsterdam's: `EXTCODESIZE` and `EXTCODECOPY` pay `WARM_STORAGE_READ_COST` twice, one access for the account and one for its code, and every other opcode's static gas is the same in Osaka and Amsterdam.
- `SATIN-SCHED-003` The regular-gas, state-gas and history-gas entries below MUST have the values in the Value column; each differs from Osaka, or is one EIP-8038 restates at its Osaka value:

  | Entry                                                | Osaka  | Value   |
  | ---------------------------------------------------- | ------ | ------- |
  | Warm storage read                                    | 100    | 100     |
  | Cold account access, additional                      | 2,500  | 2,900   |
  | Cold storage access of an `SLOAD`, additional        | 2,000  | 2,000   |
  | Cold storage access of an `SSTORE`, additional       | 2,100  | 2,000   |
  | Value transfer of a call, with its 2,300 stipend     | 9,000  | 11,300  |
  | New account of a call                                | 25,000 | 0       |
  | New account of `SELFDESTRUCT`                        | 25,000 | 9,000   |
  | `SSTORE` static cost                                 | 100    | 100     |
  | `SSTORE` of a fresh slot, before the load cost       | 19,900 | 10,000  |
  | `SSTORE` reset, before the cold load                 | 2,800  | 10,000  |
  | `SSTORE` refund of a restored fresh slot             | 19,900 | 10,000  |
  | `SSTORE` refund of a restored reset                  | 2,800  | 10,000  |
  | `SSTORE` refund of a cleared slot                    | 4,800  | 11,616  |
  | `CREATE` and `CREATE2`                               | 32,000 | 12,000  |
  | `EXTCODESIZE` and `EXTCODECOPY`, static gas          | 100    | 200     |
  | Creation transaction (unused under EIP-2780)         | 32,000 | 12,000  |
  | Access-list address, with its 20 bytes at 64 gas     | 2,400  | 4,180   |
  | Access-list storage key, with its 32 bytes at 64 gas | 1,900  | 4,048   |
  | Code deposit, regular gas per byte                   | 200    | 0       |
  | Code deposit, state gas per byte                     | 0      | 1,530   |
  | Code deposit, history gas per byte                   | 0      | 88      |
  | Fresh-slot `SSTORE`, state gas                       | 0      | 97,920  |
  | New account, state gas                               | 0      | 183,600 |
  | Created account, state gas                           | 0      | 183,600 |
  | EIP-7702 delegation indicator, state gas             | 0      | 35,190  |
  | EIP-7702 authorization, intrinsic regular gas        | 25,000 | 7,816   |
  | EIP-7702 refund for an existing authority            | 12,500 | 0       |
  | Account write (EIP-2780)                             | 0      | 9,000   |
  | Creation access (EIP-2780)                           | 0      | 12,000  |
  | Floor cost per token                                 | 10     | 16      |
  | Floor base                                           | 21,000 | 12,000  |
  | Floor tokens per zero calldata byte                  | 1      | 4       |
  | Floor tokens per access-list byte                    | 0      | 4       |

  The state-gas entries are the price at `m = 1`; a state charge is scaled by its bucket's multiplier ([State Gas and SALT Pricing](state-gas.md)).
- `SATIN-SCHED-004` A cold `SSTORE` MUST pay `COLD_STORAGE_ACCESS` (2,100) for its access together with its static cost, as a cold `SLOAD` does: EIP-8038 folds the warm base into a cold slot's access.

### Intrinsic regular gas and the floor

- `SATIN-SCHED-006` The intrinsic regular gas of a transaction MUST be `TX_BASE_COST`, plus, for a call to an account other than the sender, `COLD_ACCOUNT_ACCESS` for the recipient's access and `TX_VALUE_COST` more when it carries value; plus, for a creation, `CREATE_ACCESS` and EIP-3860's initcode cost; plus the calldata cost, the access-list entries of `SATIN-SCHED-003`, and `PER_AUTH_BASE_COST` per authorization entry.
  A transaction to its own sender MUST pay `TX_BASE_COST` alone for its base, with or without value.
- `SATIN-SCHED-005` The floor's base MUST be the transaction's own decomposed base of `SATIN-SCHED-006` without its calldata, access-list, authorization and initcode costs: `TX_BASE_COST` for a transaction to its sender, `TX_BASE_COST + COLD_ACCOUNT_ACCESS` for a call to another account without value, `TX_BASE_COST + COLD_ACCOUNT_ACCESS + TX_VALUE_COST` for one with value, and `TX_BASE_COST + CREATE_ACCESS` for a creation.
  The floor MUST be that base plus `TOTAL_COST_FLOOR_PER_TOKEN × FLOOR_TOKENS_PER_BYTE` gas for every calldata byte, zero or non-zero, a creation's initcode included, and the same for every access-list byte, `ACCESS_LIST_ADDRESS_SIZE` bytes for an address and `ACCESS_LIST_SLOT_SIZE` for a storage key.
  How the floor sets the gas used is `SATIN-POOL-018` and `SATIN-POOL-020` ([Two-Pool Gas](gas-model.md)); how validation holds the gas limit to it is on [Transaction Validation and Refusals](../block/transaction-validation.md).
- `SATIN-SCHED-007` The `PER_AUTH_BASE_COST` of every authorization entry MUST be charged by the transaction's validation, as every intrinsic entry is, whether or not the authorization will apply; an authority that already exists MUST be refunded nothing when its authorization is applied.

### Charges made at the start of execution

- `SATIN-SCHED-008` The state-dependent parts of a transaction's cost MUST be charged at the start of its execution, before its first frame, as EIP-2780 and EIP-8037 specify, every state charge priced as [State Gas and SALT Pricing](state-gas.md) says and every new-account charge decided by the predicates of `SATIN-STATE-011` (an authority by existence, every other account by EIP-161 emptiness), in this order:
  1. for a deposit, a Mega System Transaction executed as one included, whose caller is empty under EIP-161: the new-account state gas of that account, exactly once (`SATIN-DEP-003`, [Deposit Transactions](../block/deposits.md));
  2. for each authorization the list applies, in list order ([EIP-7702 Authorizations Before the First Frame](authorizations.md)): the new-account state gas of an authority the state holds no account for, then `ACCOUNT_WRITE` for the authority's first write, then the delegation indicator's state gas at most once per authority;
  3. the history gas of the write records made outside every frame: the applied authorities' records and the record of the first frame's start ([History Gas and the History Allowance](history-gas.md));
  4. the new-account state gas of the transaction's recipient, when its value goes to a recipient empty under EIP-161, or of its created account, when the created address is empty under EIP-161.

  `ACCOUNT_WRITE` MUST NOT be charged for an authority whose account write the transaction has already paid: the sender, whose write validation pays in `TX_BASE_COST`; the recipient of a transaction that carries a non-zero value, whose write `TX_VALUE_COST` pays; and an authority an earlier applied authorization of the list already wrote.
  The recipient or the created address is read at step 4 and at no earlier step, so a transaction that cannot pay a charge of steps 1 to 3 loads nothing of it.
- `SATIN-SCHED-009` A transaction that cannot pay a charge of `SATIN-SCHED-008` — the account a deposit creates for its caller, an authorization's charges, the history of the records made outside a frame, or the charge for the first frame's start — MUST run out of gas without running a frame.
  An authorization list the KV or state-growth limit skips is charged nothing ([EIP-7702 Authorizations Before the First Frame](authorizations.md)), and this path does not apply to it.
- `SATIN-SCHED-010` On that path everything applied before the first frame MUST be taken back, except what validation did to the sender's account (its fee and a call's nonce bump) and the account a deposit created for its caller: the applied EIP-7702 authorizations with their nonce and delegation writes, the sender's own authorization included, their state gas and their write records.
  The intrinsic gas and the body's history gas MUST stay charged, the rest of the regular budget MUST be consumed, and the reservoir left MUST return to the sender; the sender of a creation keeps the nonce bump the creation would have made.
  A deposit that runs out of gas this way is a failed deposit instead, which uses its whole gas limit, the reservoir included ([Deposit Transactions](../block/deposits.md)).

### Code deposit

- `SATIN-SCHED-011` Once a creation's returned code passed its checks ([Contract Size Limits](contract-limits.md)), deposited code MUST be charged in this order: the regular code-deposit cost per byte (zero), the hashing cost of the code at `KECCAK256_WORD_COST` per 32-byte word, the code's state gas (`SATIN-STATE-003`), and its history gas (`SATIN-HIST-002`).
  A creation that cannot pay any of the four MUST run out of gas, and no code is deposited.
  The data size of the code is counted after every deposit charge is made and before the creation commits ([Resource Accounting](resource-accounting.md)).

### Addresses warm from the start

- `SATIN-SCHED-012` The addresses EIP-2929 and EIP-3651 make warm from the start of a transaction — the precompiles, the block beneficiary, and the addresses the transaction's access list names, those listed without storage keys included — MUST be charged as warm on every access, their first `CALL`-family access and their first access as a `SELFDESTRUCT` beneficiary included.
- `SATIN-SCHED-013` The `SequencerRegistry`'s account and its `_currentSystemAddress` slot MUST be warm from the start of every transaction, the slot as an access-list storage key is, because validation reads both for every transaction ([SequencerRegistry](../system-contracts/sequencer-registry.md)).
- `SATIN-SCHED-014` The sender, and the recipient of a call, MUST be warm from the start of the transaction, as EIP-2929 has them.

### Retired ids

None.

## Constants

| Constant                     | Value  | Description                                                                         |
| ---------------------------- | ------ | ----------------------------------------------------------------------------------- |
| `TX_BASE_COST`               | 12,000 | EIP-2780 base cost of every transaction                                              |
| `COLD_ACCOUNT_ACCESS`        | 3,000  | EIP-8038 cold account access, charged for a recipient other than the sender          |
| `TX_VALUE_COST`              | 6,000  | EIP-2780 surcharge of a call to another account that carries value                   |
| `CREATE_ACCESS`              | 12,000 | EIP-8038 creation access (`ACCOUNT_WRITE` plus `COLD_ACCOUNT_ACCESS`)                |
| `ACCOUNT_WRITE`              | 9,000  | EIP-8038 account write                                                               |
| `PER_AUTH_BASE_COST`         | 7,816  | Intrinsic regular gas of one EIP-7702 authorization entry                            |
| `WARM_STORAGE_READ_COST`     | 100    | Warm account or storage access                                                       |
| `COLD_STORAGE_ACCESS`        | 2,100  | Cold storage access, the warm base included                                          |
| `TOTAL_COST_FLOOR_PER_TOKEN` | 16     | Floor gas per token                                                                  |
| `FLOOR_TOKENS_PER_BYTE`      | 4      | Floor tokens per calldata byte, zero or non-zero, and per access-list byte           |
| `ACCESS_LIST_ADDRESS_SIZE`   | 20     | Bytes of an access-list address                                                      |
| `ACCESS_LIST_SLOT_SIZE`      | 32     | Bytes of an access-list storage key                                                  |
| `KECCAK256_WORD_COST`        | 6      | Hashing cost per 32-byte word of deposited code                                      |
| `COST_PER_STATE_BYTE`        | 1,530  | Gas per byte of new state ([State Gas and SALT Pricing](state-gas.md))               |
| `COST_PER_HISTORY_BYTE`      | 88     | Gas per history byte ([History Gas and the History Allowance](history-gas.md))       |

## Rationale

**Why Amsterdam's schedule?**
Amsterdam is the schedule EIP-8037 was written for: it splits every cost of creating state into the regular work EIP-8038 prices and the state EIP-8037 prices, and its intrinsic cost under EIP-2780 charges a recipient's access and a value's writes only where the transaction makes them.
Running EIP-8037 on Osaka's schedule would charge creating state twice.

**Why only three changes?**
The state-gas entries carry MegaETH's cost per state byte, because MegaETH's state is priced by its own measure and scaled by SALT; deposited code gets a history price, because every node keeps the code it receives; and the forwarding reduction is MegaETH's 98/100, which keeps more gas back at each level of a deep call stack than 63/64 does at MegaETH's block gas limits.
Every other entry is Amsterdam's, so an Ethereum tool that prices Amsterdam prices Satin's regular gas correctly.

**Why charge an authority's state at the start of execution?**
Whether an authority exists, and whether it already holds a delegation indicator, is a property of the state, which validation without state cannot read.
EIP-2780 therefore charges the state-independent part of an authorization (7,816) at validation and the rest when the list is applied; Satin keeps that split, and refunds nothing for an existing authority because nothing was charged for it.

**Why are preload-warm addresses warm on their first touch?**
Rex6 charged a cold access on the first `CALL`-family or `SELFDESTRUCT`-beneficiary touch of a precompile, the beneficiary or an access-list address, a MegaETH addition on Ethereum's warm set.
Satin restates execution on Ethereum's access rules, under which those addresses are warm from the start, and EIP-8038 prices them as such.

**Why are the registry's account and slot warm?**
Every transaction's validation reads them to find the live system address, so they are in the transaction's state before its first frame, like the beneficiary under EIP-3651; charging a later access to them as cold would charge for a load that already happened, and only for some envelopes.

## Security Considerations

- If a node charged an authority's new-account state gas at validation, a transaction could be refused or overcharged for an authority that exists; if it skipped the charge at execution, an authorization list could create accounts without paying for the state they add.
- If the pre-frame out-of-gas path kept the authorizations, a transaction that cannot pay for them would apply delegations for free; if it took back the sender's nonce bump or fee, a transaction could be replayed.
- If deposited code were committed before its four charges, a creation that cannot pay would leave code no gas paid for.
- If a node priced preload-warm addresses as cold on first touch, its gas used would differ from every other node's on the same transaction.
- This page preserves the invariant that every charge is made once: a part paid at validation is never charged again at execution, and a part charged at execution is never refunded at validation.

## Spec History

- [Satin](../../upgrades/satin.md) — Replaced the Prague schedule and the Rex6 intrinsic storage gas of the [Dual Gas Model](../../evm/dual-gas-model.md) with the Amsterdam schedule, EIP-2780 intrinsic gas and runtime authorization charges, and dropped the cold first touch of preload-warm addresses of [Compute Gas](../../evm/compute-gas.md).
