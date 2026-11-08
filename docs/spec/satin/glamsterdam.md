---
description: Satin (unstable) — Satin and Glamsterdam. An informative map of Ethereum's Glamsterdam upgrade onto Satin — every EIP scheduled for it and Satin's relation to each, Satin's departures from the EIPs it adopts, and the MegaETH mechanisms with no Glamsterdam counterpart — each statement linking the Satin rules that are normative.
spec: Satin
maturity: unstable
---

# Satin and Glamsterdam

{% hint style="warning" %}
**Unstable** — Satin is under active development: every value and rule on this page may change before Satin is frozen.
{% endhint %}

Abstract: Satin takes part of Ethereum's Glamsterdam upgrade onto its Optimism Karst base and changes part of it, and most of its rules are MegaETH's own mechanisms with no Ethereum counterpart; this page shows at a glance which is which, for a reader who knows Glamsterdam.
It restates no rule: every statement names the Satin rule ids that are normative, and where this page and a rule differ, the rule holds.

## Scope

The base Satin builds on is Optimism Karst with its Ethereum base Osaka (`SATIN-BASE-001`, [Base Layer](base-layer.md)); a Glamsterdam EIP is part of Satin only where a Satin rule names it.
The Glamsterdam EIPs are those [EIP-7773](https://eips.ethereum.org/EIPS/eip-7773), the Glamsterdam meta EIP, lists as Scheduled for Inclusion, read on 9 November 2026 at its revision of 22 October 2026 ([commit `f1ade090fd`](https://github.com/ethereum/EIPs/commit/f1ade090fd315895461fc3e249cb1a675aeb55a9)), with the networking and informational EIPs it lists beside them.
An EIP Satin adopts is applied at the revision its rule pins: EIP-8037 as of [commit `c406bdb2ff`](https://github.com/ethereum/EIPs/commit/c406bdb2ffbf2fbf9d85698e97b3b2e8b6e79112) with the later commits `SATIN-POOL-002` names, its profile frozen at [commit `dbc6d457cb`](https://github.com/ethereum/EIPs/commit/dbc6d457cbf90d5f9d55552f3fd91d58b88cc898) (`SATIN-POOL-004`), and every other EIP at its file's revision current at that freeze point (`SATIN-SCHED-001`, `SATIN-POOL-020`, `SATIN-LOG-001`, `SATIN-BASE-004`, `SATIN-BASE-005`).

## The Glamsterdam EIPs

"Adopted as written" means at the pinned revision; "adopted with changes" names what changes; "not adopted" names the rule that says so, or the base layer's absence of the EIP; "outside the execution specification" is consensus-layer, networking or informational work with no rule of the execution layer.

| EIP | What it does | Satin's relation | Rules | Parameters that differ |
| --- | --- | --- | --- | --- |
| [EIP-2780](https://eips.ethereum.org/EIPS/eip-2780) | Decomposes the flat intrinsic cost into primitives priced by what a transaction consumes | Adopted as written, at `7243c92ba8`; its account-creation charges are state gas under Satin's EIP-8037 profile, and a deposit's created caller is charged as a further pre-frame charge, in an order Satin fixes | `SATIN-SCHED-001`, `SATIN-SCHED-006`, `SATIN-SCHED-008`, `SATIN-AUTH-015`, `SATIN-DEP-003` | None in its own entries |
| [EIP-7688](https://eips.ethereum.org/EIPS/eip-7688) | Moves consensus SSZ structures to progressive containers | Outside the execution specification (consensus layer) | None | None |
| [EIP-7708](https://eips.ethereum.org/EIPS/eip-7708) | Every ETH transfer emits a log | Adopted with changes, at `f7230c46a7`: only the `Transfer` log, no `Burn` log; a transfer log counts as data size and pays no history gas; a deposit's mint is not logged | `SATIN-LOG-001`, `SATIN-LOG-004`, `SATIN-LOG-005`, `SATIN-LOG-006` | `TRANSFER_LOG_SIZE` 160 bytes of data size |
| [EIP-7732](https://eips.ethereum.org/EIPS/eip-7732) | Enshrined proposer-builder separation | Outside the execution specification (consensus layer; MegaETH has no beacon chain) | None | None |
| [EIP-7778](https://eips.ethereum.org/EIPS/eip-7778) | Excludes refunds from block gas accounting | Not adopted: the block gas limit and the gas a block uses are the base layer's (Karst counts receipts after the refund); the ledgers Satin's block counters hold are taken before the refund | `SATIN-BASE-001`, `SATIN-BLK-009`, `SATIN-BLK-001`, `SATIN-POOL-019`, `SATIN-POOL-020` | None |
| [EIP-7843](https://eips.ethereum.org/EIPS/eip-7843) | `SLOTNUM` opcode | Adopted with changes, at `e44e1960a9`: `SLOTNUM` pushes zero (MegaETH has no slot), and is a volatile read | `SATIN-BASE-005`, `SATIN-DET-001` | The value is always 0 |
| [EIP-7928](https://eips.ethereum.org/EIPS/eip-7928) | Enforced block-level access lists | Not adopted (block access lists are not part of Satin's blocks); a stateless validator is given Satin's own witness | `SATIN-BASE-001`, `SATIN-WIT-001` | None |
| [EIP-7954](https://eips.ethereum.org/EIPS/eip-7954) | Raises the contract size limit to 64 KiB and the initcode limit to 128 KiB | Not adopted: MegaETH's own, larger limits apply | `SATIN-SIZE-001`, `SATIN-SIZE-002`, `SATIN-SIZE-003` | `MAX_CONTRACT_SIZE` 512 KiB, `MAX_INITCODE_SIZE` 1 MiB |
| [EIP-7976](https://eips.ethereum.org/EIPS/eip-7976) | Raises the calldata floor to 64 gas per byte | Adopted as written, at `c998ef94eb`, with EIP-7623's floor; a deposit is charged nothing by it, and a block counts history gas apart from the floor | `SATIN-SCHED-001`, `SATIN-SCHED-005`, `SATIN-POOL-020`, `SATIN-HIST-017`, `SATIN-DEP-009` | None |
| [EIP-7981](https://eips.ethereum.org/EIPS/eip-7981) | Prices access lists for their data | Adopted as written, at `747b78c0ed` | `SATIN-SCHED-001`, `SATIN-SCHED-003`, `SATIN-SCHED-005` | None |
| [EIP-7997](https://eips.ethereum.org/EIPS/eip-7997) | A minimal `CREATE2` factory shared by EVM chains | Adopted as a precondition: Satin deploys nothing, and the block in which Satin activates requires the factory at its address with its code hash | `SATIN-ACT-004`, `SATIN-ACT-005` | None |
| [EIP-8024](https://eips.ethereum.org/EIPS/eip-8024) | `DUPN`, `SWAPN` and `EXCHANGE` | Adopted as written, at `34b49095ca`; the label of a halt it causes is not specified | `SATIN-BASE-004`, `SATIN-OUT-018` | None |
| [EIP-8037](https://eips.ethereum.org/EIPS/eip-8037) | Separate, higher metering of state creation: regular gas and a state-gas reservoir | Adopted with changes, at `c406bdb2ff` with the later commits taken and declined, frozen at `dbc6d457cb`; Satin's departures are in the next table | `SATIN-POOL-001` to `SATIN-POOL-004`, `SATIN-POOL-022`, `SATIN-STATE-001`, `SATIN-HIST-012`, `SATIN-STATE-012` | Execution cap 200,000,000 (not `TX_MAX_GAS_LIMIT`); no `TX_MAX_TOTAL_GAS_LIMIT`; `COST_PER_STATE_BYTE` 1,530 times the SALT multiplier; reservoir share 98/100 |
| [EIP-8038](https://eips.ethereum.org/EIPS/eip-8038) | Raises the gas of state-access operations | Adopted as written, at `4c7e2487e4`, as part of the Amsterdam schedule, with the schedule's three Satin changes | `SATIN-SCHED-001` to `SATIN-SCHED-004` | None in its own entries |
| [EIP-8045](https://eips.ethereum.org/EIPS/eip-8045) | Excludes slashed validators from proposing | Outside the execution specification (consensus layer) | None | None |
| [EIP-8061](https://eips.ethereum.org/EIPS/eip-8061) | Raises the exit and consolidation churn | Outside the execution specification (consensus layer) | None | None |
| [EIP-8246](https://eips.ethereum.org/EIPS/eip-8246) | Removes the remaining `SELFDESTRUCT` burns | Not adopted: a balance can still be burned, silently | `SATIN-LOG-005` | None |
| [EIP-8282](https://eips.ethereum.org/EIPS/eip-8282) | Predeploys builder deposit and exit request contracts for EIP-7732 | Outside the execution specification (consensus layer and its request bus) | None | None |
| [EIP-7975](https://eips.ethereum.org/EIPS/eip-7975), [EIP-8070](https://eips.ethereum.org/EIPS/eip-8070), [EIP-8136](https://eips.ethereum.org/EIPS/eip-8136), [EIP-8159](https://eips.ethereum.org/EIPS/eip-8159), [EIP-8189](https://eips.ethereum.org/EIPS/eip-8189) | Networking: paginated receipts, sparse blobpool, cell deltas, block-access-list exchange, snap state healing | Outside the execution specification (networking) | None | None |
| [EIP-7904](https://eips.ethereum.org/EIPS/eip-7904), [EIP-8261](https://eips.ethereum.org/EIPS/eip-8261) | Informational: compute gas analysis, a gas limit schedule | Outside the execution specification (informational) | None | None |

The Osaka EIPs the base layer carries that Satin changes are in the next table too: [EIP-7825](https://eips.ethereum.org/EIPS/eip-7825)'s transaction gas cap is not applied (`SATIN-BASE-002`), and [EIP-7610](https://eips.ethereum.org/EIPS/eip-7610) is not applied (`SATIN-SD-016`).

## Satin's departures from the EIPs it adopts

| Departure | What Satin does | Instead of | Rules |
| --- | --- | --- | --- |
| Execution cap | A transaction's regular gas is held under 200,000,000; the rest of its gas limit is the state-gas reservoir; no separate compute ledger | EIP-7825's 16,777,216 cap on a transaction's gas limit, which EIP-8037 uses as `TX_MAX_GAS_LIMIT` | `SATIN-BASE-002`, `SATIN-POOL-005`, `SATIN-POOL-021` |
| No total transaction cap | A transaction's gas limit is bounded by its block's alone | EIP-8037's `TX_MAX_TOTAL_GAS_LIMIT` of commit `d7087803ca`, which Satin declines | `SATIN-BASE-003`, `SATIN-POOL-003` |
| The give-back rule | Every give-back of state or history gas credits a reservoir, never regular gas: a frame's regular gas never rises within the frame but by a child's unused regular gas; a revert keeps the frame's undone charges in its reservoir, a halt consumes what regular gas paid | EIP-8037 at `dbc6d457cb`, which refills regular gas first, up to what regular gas paid, and returns it to regular gas on a revert; the rule follows [ethereum/EIPs#12581](https://github.com/ethereum/EIPs/pull/12581) (open) | `SATIN-HIST-012`, `SATIN-POOL-008`, `SATIN-POOL-012`, `SATIN-POOL-014`, `SATIN-POOL-015`, `SATIN-POOL-022`, `SATIN-TAKE-002` |
| The legacy share | A state charge for a fresh slot, a new account or a created account made by an opcode or a keyless deployment takes `min(state_charge, max(0, PRE_FORK_COST − execution_charge))` from regular gas first: 10,000, 25,000 (16,000 for a `SELFDESTRUCT`'s beneficiary) and 20,000, flat | EIP-8037 at `dbc6d457cb`, which draws the reservoir first for every state charge; the share follows ethereum/EIPs#12581 | `SATIN-STATE-012`, `SATIN-POOL-008`, `SATIN-POOL-024` |
| SALT-scaled state gas | A state charge is the entry at `COST_PER_STATE_BYTE` times the multiplier of the SALT bucket the state lands in, read once per bucket per transaction | A single price per state byte | `SATIN-STATE-001`, `SATIN-STATE-002`, `SATIN-STATE-006`, `SATIN-STATE-010` |
| History gas | A third ledger: 88 gas per byte of the body, logs, write records and deployed code, drawing the reservoir first and given back like state gas; deposits and the protocol's own work exempt | No history price; logs and calldata are regular gas | `SATIN-HIST-001`, `SATIN-HIST-002`, `SATIN-HIST-016`, `SATIN-POOL-019`, `SATIN-POOL-022` |
| The reservoir share | A child receives 98/100 of its caller's remaining reservoir, the caller keeping the rest | EIP-8037's whole reservoir passed to the child | `SATIN-POOL-011`, `SATIN-FWD-005`, `SATIN-POOL-022` |
| The destruction-table refill | The first effective `SELFDESTRUCT` of an account created in the transaction refills the state gas of each part absent at the transaction's start and takes back its records, into the destroying frame's reservoir | EIP-8037's no refill for that destruction | `SATIN-SD-004`, `SATIN-SD-005`, `SATIN-SD-007`, `SATIN-POOL-022` |
| The Amsterdam schedule's three changes | State-gas entries rebuilt at `COST_PER_STATE_BYTE`; deposited code charged 88 history gas per byte; the forwarding reduction 98/100 | Amsterdam's entries, zero history gas for code, and EIP-150's 63/64 | `SATIN-SCHED-001`, `SATIN-FWD-001` |
| `SLOTNUM` | Pushes zero in every block | EIP-7843's slot number | `SATIN-BASE-005` |
| EIP-7708 | `Transfer` logs only; no `Burn` log, and EIP-8246 not applied | EIP-7708's further logs, EIP-8246's removal of burns | `SATIN-LOG-001`, `SATIN-LOG-005` |
| EIP-7610 | A creation does not collide on storage alone | EIP-7610's collision on non-empty storage | `SATIN-SD-016`, `SATIN-POOL-002` |
| ModExp's order | The minimum charge, then the formula price, then EIP-7823's bound, an over-bound input priced by its formula | EIP-7823's bound checked before the formula price | `SATIN-PCMP-007`, `SATIN-DET-023` |
| KZG point evaluation | A fixed 100,000 gas | EIP-4844's 50,000 | `SATIN-PCMP-001`, `SATIN-PCMP-006` |
| Contract sizes | 512 KiB of code and 1 MiB of initcode | EIP-170 and EIP-3860's sizes, and EIP-7954's | `SATIN-SIZE-001`, `SATIN-SIZE-002` |
| The registry read | Every transaction's validation reads the `SequencerRegistry`, whose account and slot are warm from its start | No such read | `SATIN-REG-002`, `SATIN-SCHED-013` |

## MegaETH mechanisms with no Glamsterdam counterpart

| Mechanism | What it is | Page | Rules |
| --- | --- | --- | --- |
| Resource limits | Data size, KV updates and state growth per transaction and per frame, with frame budgets | [Resource Limits](evm/resource-limits.md), [Resource Accounting](evm/resource-accounting.md) | `SATIN-LIM-001`, `SATIN-ACCT-012` |
| Limit stops | Every limit reverts only the frame that crosses it, with `MegaLimitExceeded` | [Limit Stops](evm/limit-stops.md), [Halts, Reverts and Stops](evm/outcomes.md) | `SATIN-STOP-001`, `SATIN-OUT-002` |
| Gas detention | After a volatile read, computation is bounded by withholding regular gas | [Gas Detention](evm/gas-detention.md) | `SATIN-DET-001`, `SATIN-DET-012` |
| History gas and the history allowance | The third ledger, and the 160 bytes a value call's frame may log without paying | [History Gas and the History Allowance](evm/history-gas.md) | `SATIN-HIST-001`, `SATIN-HIST-018` |
| SALT pricing | State gas scaled by SALT bucket capacity | [State Gas and SALT Pricing](evm/state-gas.md) | `SATIN-STATE-002`, `SATIN-STATE-010` |
| Write and take-back patterns | What each ledger and count does when a write is taken back | [Write and Take-Back Patterns](evm/take-backs.md) | `SATIN-TAKE-001`, `SATIN-TAKE-002` |
| Oracle | Storage the sequencer writes, read through an oracle service | [Oracle](system-contracts/oracle.md) | `SATIN-ORCL-001` |
| SequencerRegistry | The live system address and sequencer, and their rotation | [SequencerRegistry](system-contracts/sequencer-registry.md) | `SATIN-REG-001` |
| KeylessDeploy | Deployment of pre-EIP-155 transactions at their keyless address | [KeylessDeploy](system-contracts/keyless-deploy.md) | `SATIN-KEY-001` |
| MegaAccessControl | A frame switch that refuses volatile reads | [MegaAccessControl](system-contracts/mega-access-control.md) | `SATIN-MAC-001` |
| MegaLimitControl | The remaining compute a frame may still spend | [MegaLimitControl](system-contracts/mega-limit-control.md) | `SATIN-MLC-001` |
| High-precision timestamp | A microsecond timestamp served through the Oracle | [High-Precision Timestamp](system-contracts/high-precision-timestamp.md) | `SATIN-HPTS-001` |
| Call interception and the system contracts' addresses and code | How calls to the system contracts are answered | [Call Interception](system-contracts/interception.md), [System Contracts](system-contracts/overview.md) | `SATIN-ICPT-001`, `SATIN-SYSC-001` |
| Mega System Transactions | The sequencer's own legacy transactions, promoted to deposits | [Mega System Transactions](system-contracts/system-tx.md) | `SATIN-MST-001` |
| Deposits | OP Stack deposits, with failed deposits, and their Satin pricing and counts | [Deposit Transactions](block/deposits.md) | `SATIN-DEP-003`, `SATIN-DEP-004` |
| Transaction validation and refusals | What a node refuses before execution, and how a failed read is reported | [Transaction Validation and Refusals](block/transaction-validation.md) | `SATIN-VAL-001`, `SATIN-VAL-010` |
| The pre-block sequence | The system calls and reads before a block's first transaction | [System Calls and the Pre-Block Sequence](block/system-calls.md) | `SATIN-PBLK-001` |
| Block limits and packing | The block's data-size, KV and state-growth budgets | [Block Limits and Packing](block/block-limits.md) | `SATIN-BLK-001`, `SATIN-BLK-002` |
| The stateless witness | What a block exports so a stateless validator can replay it | [The Stateless Witness](block/stateless-witness.md) | `SATIN-WIT-001` |
| Activation | The chain configuration, the activation block and the Rex-era carry-over | [Activation and Rex-Era Carry-Over](block/activation.md) | `SATIN-ACT-001`, `SATIN-ACT-005` |

## Keeping this page current

When an EIP Satin adopts changes upstream, the revision its rule pins decides: Satin keeps the pinned text until a later spec moves the pin (`SATIN-POOL-004`).
Whether Satin follows a change Ethereum is discussing is decided by the monitoring of ethereum/EIPs, and is recorded in the rules first and on this page after: today the open pull requests [#12581](https://github.com/ethereum/EIPs/pull/12581) (reservoir-only refills and the legacy share, which Satin already takes in its own words), [#12582](https://github.com/ethereum/EIPs/pull/12582) (a state-gas allowance of call frames, not taken) and [#12573](https://github.com/ethereum/EIPs/pull/12573) (documenting gas that returns before the settlement and reservoir forwarding in EIP-8037).
When EIP-7773 adds or drops an EIP, the first table gains or loses its row.

## Spec History

- [Satin](../upgrades/satin.md) — Introduced this map of Glamsterdam onto Satin.
