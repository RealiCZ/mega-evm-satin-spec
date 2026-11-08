# Satin Specification — Outline

Phase 1 of the Satin specification: the page list of the Satin section in reading order and, for every page, each rule it will specify with its sources.
No rule below is normative yet; each line names what the page will state, and where the sources leave behaviour undefined or disagree the line points at a question in [questions.md](questions.md).
Rule ids are the proposal of [rule-ids.md](rule-ids.md); they are not applied anywhere else yet.

## How to read the tables

- **Draft** — a line range of `docs/spec/upgrades/satin.md` as copied into this repository (the Satin draft at mega-evm `5e3f30ad`), as `satin.md §<n>` L<from>–L<to> for its numbered sections, or by the name of an unnumbered part (Summary, Node integrators, Safety and Compatibility). `none` means no line of the draft states the rule.
- **Rex page** — the Rex6-era page (frozen, under `docs/spec/`) and section the rule `replaces`, `changes` or `keeps`; `new` when no Rex page covers it.
- **Code (a)** — implementation (a), mega-evm `5e3f30ad` on MegaETH's revm 40 forks: `a:<path>` is `crates/mega-evm/src/<path>`.
- **Code (b)** — implementation (b), the `next/` workspace on evm2 at mega-evm `785182eb`: `b:<path>` is `next/mega-evm2/src/<path>`, `op:<path>` is `next/op-evm2/src/<path>`, and `evm2:<path>` is `crates/evm2/src/<path>` in the evm2 fork at `91518705`.
- A second backticked word after a path is an item in that file (a function, type or constant). `none` means the implementation has no code for the rule.
- **Note** — `undefined: Q…` where the sources leave the behaviour undefined; `disagreement: Q…` where the sources disagree. The id is a question in [questions.md](questions.md).

## Reading order

1. [Satin Specification](../docs/spec/satin/overview.md) — `docs/spec/satin/overview.md` (index page, no rules)
2. [Base Layer](../docs/spec/satin/base-layer.md) — `docs/spec/satin/base-layer.md` (`SATIN-BASE-…`, 10 rules)
3. [Satin EVM Overview](../docs/spec/satin/evm/overview.md) — `docs/spec/satin/evm/overview.md` (index page, no rules)
4. [Two-Pool Gas](../docs/spec/satin/evm/gas-model.md) — `docs/spec/satin/evm/gas-model.md` (`SATIN-POOL-…`, 22 rules)
5. [Gas Schedule and Intrinsic Gas](../docs/spec/satin/evm/gas-schedule.md) — `docs/spec/satin/evm/gas-schedule.md` (`SATIN-SCHED-…`, 14 rules)
6. [State Gas and SALT Pricing](../docs/spec/satin/evm/state-gas.md) — `docs/spec/satin/evm/state-gas.md` (`SATIN-STATE-…`, 10 rules)
7. [History Gas and the History Allowance](../docs/spec/satin/evm/history-gas.md) — `docs/spec/satin/evm/history-gas.md` (`SATIN-HIST-…`, 21 rules)
8. [Gas Forwarding](../docs/spec/satin/evm/gas-forwarding.md) — `docs/spec/satin/evm/gas-forwarding.md` (`SATIN-FWD-…`, 7 rules)
9. [Resource Limits](../docs/spec/satin/evm/resource-limits.md) — `docs/spec/satin/evm/resource-limits.md` (`SATIN-LIM-…`, 18 rules)
10. [Resource Accounting](../docs/spec/satin/evm/resource-accounting.md) — `docs/spec/satin/evm/resource-accounting.md` (`SATIN-ACCT-…`, 20 rules)
11. [EIP-7702 Authorizations Before the First Frame](../docs/spec/satin/evm/authorizations.md) — `docs/spec/satin/evm/authorizations.md` (`SATIN-AUTH-…`, 18 rules)
12. [SELFDESTRUCT and the Destruction Table](../docs/spec/satin/evm/selfdestruct.md) — `docs/spec/satin/evm/selfdestruct.md` (`SATIN-SD-…`, 20 rules)
13. [Limit Stops](../docs/spec/satin/evm/limit-stops.md) — `docs/spec/satin/evm/limit-stops.md` (`SATIN-STOP-…`, 21 rules)
14. [Gas Detention](../docs/spec/satin/evm/gas-detention.md) — `docs/spec/satin/evm/gas-detention.md` (`SATIN-DET-…`, 27 rules)
15. [Halts, Reverts and Stops](../docs/spec/satin/evm/outcomes.md) — `docs/spec/satin/evm/outcomes.md` (`SATIN-OUT-…`, 18 rules)
16. [EIP-7708 Transfer Logs](../docs/spec/satin/evm/transfer-logs.md) — `docs/spec/satin/evm/transfer-logs.md` (`SATIN-LOG-…`, 7 rules)
17. [Contract Size Limits](../docs/spec/satin/evm/contract-limits.md) — `docs/spec/satin/evm/contract-limits.md` (`SATIN-SIZE-…`, 6 rules)
18. [Precompiles](../docs/spec/satin/evm/precompiles.md) — `docs/spec/satin/evm/precompiles.md` (`SATIN-PCMP-…`, 8 rules)
19. [System Contracts](../docs/spec/satin/system-contracts/overview.md) — `docs/spec/satin/system-contracts/overview.md` (`SATIN-SYSC-…`, 4 rules)
20. [Call Interception](../docs/spec/satin/system-contracts/interception.md) — `docs/spec/satin/system-contracts/interception.md` (`SATIN-ICPT-…`, 6 rules)
21. [Oracle](../docs/spec/satin/system-contracts/oracle.md) — `docs/spec/satin/system-contracts/oracle.md` (`SATIN-ORCL-…`, 11 rules)
22. [High-Precision Timestamp](../docs/spec/satin/system-contracts/high-precision-timestamp.md) — `docs/spec/satin/system-contracts/high-precision-timestamp.md` (`SATIN-HPTS-…`, 2 rules)
23. [KeylessDeploy](../docs/spec/satin/system-contracts/keyless-deploy.md) — `docs/spec/satin/system-contracts/keyless-deploy.md` (`SATIN-KEY-…`, 18 rules)
24. [MegaAccessControl](../docs/spec/satin/system-contracts/mega-access-control.md) — `docs/spec/satin/system-contracts/mega-access-control.md` (`SATIN-MAC-…`, 7 rules)
25. [MegaLimitControl](../docs/spec/satin/system-contracts/mega-limit-control.md) — `docs/spec/satin/system-contracts/mega-limit-control.md` (`SATIN-MLC-…`, 4 rules)
26. [SequencerRegistry](../docs/spec/satin/system-contracts/sequencer-registry.md) — `docs/spec/satin/system-contracts/sequencer-registry.md` (`SATIN-REG-…`, 7 rules)
27. [Mega System Transactions and the Protocol's Own Transactions](../docs/spec/satin/system-contracts/system-tx.md) — `docs/spec/satin/system-contracts/system-tx.md` (`SATIN-MST-…`, 10 rules)
28. [Satin Transactions and Blocks Overview](../docs/spec/satin/block/overview.md) — `docs/spec/satin/block/overview.md` (index page, no rules)
29. [Transaction Validation and Refusals](../docs/spec/satin/block/transaction-validation.md) — `docs/spec/satin/block/transaction-validation.md` (`SATIN-VAL-…`, 9 rules)
30. [Deposit Transactions](../docs/spec/satin/block/deposits.md) — `docs/spec/satin/block/deposits.md` (`SATIN-DEP-…`, 13 rules)
31. [System Calls and the Pre-Block Sequence](../docs/spec/satin/block/system-calls.md) — `docs/spec/satin/block/system-calls.md` (`SATIN-PBLK-…`, 6 rules)
32. [Block Limits and Packing](../docs/spec/satin/block/block-limits.md) — `docs/spec/satin/block/block-limits.md` (`SATIN-BLK-…`, 13 rules)
33. [The Stateless Witness](../docs/spec/satin/block/stateless-witness.md) — `docs/spec/satin/block/stateless-witness.md` (`SATIN-WIT-…`, 17 rules)
34. [Activation and Rex-Era Carry-Over](../docs/spec/satin/block/activation.md) — `docs/spec/satin/block/activation.md` (`SATIN-ACT-…`, 10 rules)

34 pages, 384 rules.

## Satin

### Satin Specification (`satin/overview.md`)

The entry point of the Satin section: what Satin is, its maturity, its base layer, how the section is organized, and how its rules are identified.

Rex pages it draws on: `overview.md`, `hardfork-spec.md`, `evm/overview.md`.

An index page: it summarizes and links the pages of its group and specifies no rule of its own.

### Base Layer (`satin/base-layer.md`)

The base Satin builds on (Optimism Karst, Ethereum Osaka), the opcodes it adds, the inherited caps it does not apply, and the Karst block rules it keeps.

Rex pages it draws on: `overview.md`, `evm/overview.md`.

| Id | Rule | Draft | Rex page | Code (a) | Code (b) | Note |
| --- | --- | --- | --- | --- | --- | --- |
| `SATIN-BASE-001` | Every standard EVM, transaction and block rule the Satin section does not override is Optimism Karst's, the Optimism changes of Jovian and Karst and the Ethereum changes of Osaka included | `satin.md §1` L70–L71 | replaces overview.md "Why MegaETH Differs from Standard Ethereum" (Isthmus base); replaces evm/overview.md "Inheritance Boundary" | `a:evm/spec.rs` | `b:lib.rs` `satin_version`<br>`op:spec.rs` | undefined: QG-02 |
| `SATIN-BASE-002` | EIP-7825's per-transaction gas limit cap is not applied; a transaction's gas limit is bounded by the block's gas limit | `satin.md §1` L72–L73 | new | `a:evm/spec.rs` | `b:lib.rs` `satin_version` |  |
| `SATIN-BASE-003` | EIP-8037's TX_MAX_TOTAL_GAS_LIMIT (2^32 − 1) is not applied | `satin.md §1` L74; `satin.md §4` L155–L157, L236–L237 | new | `a:evm/spec.rs` | `b:lib.rs` `tx_total_gas_cap`<br>`evm2:ethereum/mod.rs` `tx_total_gas_cap` |  |
| `SATIN-BASE-004` | DUPN (0xE6), SWAPN (0xE7) and EXCHANGE (0xE8) of EIP-8024 are enabled | `satin.md §1` L76 | new | `a:evm/instructions.rs` `mega_instructions` | `b:lib.rs` `satin_table` | undefined: QG-02 |
| `SATIN-BASE-005` | SLOTNUM (0x4B) of EIP-7843 pushes the block's slot number, an unsigned 64-bit value supplied with the block; a block supplied no number runs with zero | `satin.md §1` L76–L78; `satin.md §22` L1402–L1403 | new | `a:evm/host.rs` `slot_num` | `b:lib.rs` `satin_table`<br>`b:detention.rs` `wrap_table` | undefined: QA-05 |
| `SATIN-BASE-006` | A block in which Satin, or an Optimism fork at or after Jovian, activates admits only deposits; a non-deposit transaction in it makes the block invalid | `satin.md §1` L80–L82; `satin.md §21` L1349, L1366 | new | `a:block/executor.rs` `with_no_user_tx_activation_block` | `b:block.rs` `only_deposits` | disagreement: QB-02 |
| `SATIN-BASE-007` | A fork activates in a block when it is active at the block's timestamp and not at the parent's, as the chain configuration schedules it; an unscheduled fork never activates | `satin.md §1` L81–L82 | new | `a:block/hardfork.rs` | none | disagreement: QC-06 |
| `SATIN-BASE-008` | A Mega System Transaction is refused in such a block, and the Satin activation block owes no Oracle write | `satin.md §1` L83 | new | `a:block/executor.rs` `run_transaction` | `b:block.rs` `run_transaction` |  |
| `SATIN-BASE-009` | Each non-deposit transaction's data-availability footprint (compressed size × the L1 block contract's footprint gas scalar) accumulates against the block gas limit and is reported as blob gas used; a transaction that does not fit is not included; no scalar in state means zero | `satin.md §1` L84–L86; `satin.md §21` L1347 | new | `a:block/limit.rs` `available_da_footprint` | `b:block.rs` `check_da_footprint`<br>`b:block.rs` `estimated_da_size` |  |
| `SATIN-BASE-010` | Non-deposit transactions are priced against the L1 block information the block's L1 attributes deposit wrote, as the state stands before the first non-deposit transaction other than a Mega System Transaction; the footprint scalar is read again for each non-deposit transaction, a Mega System Transaction included | `satin.md §1` L87–L88; `satin.md §22` L1404–L1411; `satin.md` Node integrators L1513–L1514 | new | `a:block/l1_block_info.rs` `read_l1_block_info` | `op:l1block.rs`<br>`b:block.rs` `run_transaction` |  |

## Execution

### Satin EVM Overview (`satin/evm/overview.md`)

An index of the Satin execution pages: the gas model, the resource limits, the stop rule, gas detention and the opcode-level changes.

Rex pages it draws on: `evm/overview.md`.

An index page: it summarizes and links the pages of its group and specifies no rule of its own.

### Two-Pool Gas (`satin/evm/gas-model.md`)

EIP-8037's regular gas and state-gas reservoir in Satin's profile: the execution cap, the three kinds of charge, how frames receive and return the reservoir, the transaction's settlement and its three gas ledgers.

Rex pages it draws on: `evm/dual-gas-model.md`, `evm/compute-gas.md`.

| Id | Rule | Draft | Rex page | Code (a) | Code (b) | Note |
| --- | --- | --- | --- | --- | --- | --- |
| `SATIN-POOL-001` | EIP-8037 applies as of commit c406bdb2ff, with Satin's parameters (the execution cap, the cost per state byte scaled by the bucket multiplier) | `satin.md §4` L146, L230–L231 | replaces evm/dual-gas-model.md "Total Gas" | `a:evm/schedule.rs` `satin_gas_params` | `b:lib.rs` `satin_version`<br>`evm2:interpreter/gas.rs` `GasTracker` | undefined: QG-01 |
| `SATIN-POOL-002` | Later EIP-8037 commits taken: the child-merge return (3ff5cff17a) as the reference implementation performs it, the first-frame failure outcome (9dcd72754f), no collision on storage (dbc6d457cb) | `satin.md §4` L147, L158–L162, L232–L235 | new | `a:limit/ledger.rs` `StartLedger` | `b:ledger.rs` `pop_child` |  |
| `SATIN-POOL-003` | Later EIP-8037 commits declined: the transaction gas cap (d7087803ca) and the commit of the pre-execution spill (9dcd72754f) | `satin.md §4` L147, L161, L236–L238 | new | `a:evm/spec.rs` | `b:lib.rs` `satin_version` |  |
| `SATIN-POOL-004` | Satin's EIP-8037 profile is frozen at commit dbc6d457cb (18 September 2026): a later change to EIP-8037 does not apply under Satin, whatever the EIP's status becomes | `satin.md §4` L163, L227–L228, L239–L240, L247–L249 | new | none | none |  |
| `SATIN-POOL-005` | The execution cap EXECUTION_CAP = 200,000,000; at the start of execution regular_budget = min(gas_limit, EXECUTION_CAP) − intrinsic_regular_gas and reservoir = max(0, gas_limit − EXECUTION_CAP) | `satin.md §4` L165–L176 | replaces evm/compute-gas.md "Limits"; replaces evm/resource-limits.md "Limit Set" (compute row) | `a:constants.rs` `TX_GAS_LIMIT_CAP` | `b:ledger.rs` `EXECUTION_CAP` |  |
| `SATIN-POOL-006` | The intrinsic state gas (the body's history gas) is taken from the reservoir first and only its excess from the regular budget | `satin.md §4` L177; `satin.md §7` L402 | new | `a:evm/history.rs` `tx_body_history_bytes`<br>`a:evm/execution.rs` | `b:tx.rs` `adjust_intrinsic_gas` |  |
| `SATIN-POOL-007` | A regular charge (every inherited opcode and intrinsic cost) draws only the regular budget | `satin.md §4` L180 | replaces evm/dual-gas-model.md "Compute Gas" | `a:evm/execution.rs` | `evm2:interpreter/gas.rs` `GasTracker` |  |
| `SATIN-POOL-008` | A state charge and a history charge draw the reservoir first and spill onto the regular budget only past it | `satin.md §4` L181; `satin.md §7` L428–L431 | new | `a:limit/ledger.rs` | `b:ledger.rs` `charge_history` |  |
| `SATIN-POOL-009` | GAS returns the regular budget the frame has left, not the reservoir | `satin.md §4` L182; `satin.md §12` L961 | new | `a:evm/execution.rs` | `evm2:interpreter/gas.rs` |  |
| `SATIN-POOL-010` | The transaction's own frame and a system call's outermost frame receive the whole reservoir | `satin.md §4` L185; `satin.md §9` L489 | new | `a:evm/execution.rs` | `b:tx.rs` `before_initial_frame` |  |
| `SATIN-POOL-011` | A child frame of the call opcodes, CREATE, CREATE2 or a keyless deployment receives reservoir_share = remaining − remaining × 2 / 100 of the caller's reservoir after every charge the caller makes for that start; the requested gas does not bound it; the caller keeps the rest | `satin.md §4` L186–L188; `satin.md §9` L490–L492 | new | `a:limit/ledger.rs` `reservoir_share` | `b:ledger.rs` `reservoir_share` |  |
| `SATIN-POOL-012` | Child-merge return on every start, answered or built: d = min(returned reservoir, caller's outstanding spill); the caller's regular gas rises by d, its spill falls by d, its reservoir rises by the returned reservoir less d; the reservoir the caller kept is never drawn; state and history charges share the spill | `satin.md §4` L148–L152, L189, L193–L194; `satin.md §9` L495–L499 | new | `a:limit/ledger.rs` `StartLedger` | `b:ledger.rs` `pop_child` |  |
| `SATIN-POOL-013` | A successful child's own spill is added to the caller's spill before the unwind; a reverted or halted child's is not | `satin.md §4` L153–L154 | new | `a:limit/ledger.rs` | `b:ledger.rs` `pop_child` |  |
| `SATIN-POOL-014` | A frame that reverts or halts gives back its state and history charges as EIP-8037 specifies (the reservoir-paid part to the reservoir, the spilled part to the regular budget); a revert returns the unspent regular gas to the caller, a halt consumes it, the returned spill included | `satin.md §4` L190–L192; `satin.md §9` L496–L497 | replaces evm/resource-accounting.md "Revert Behavior" (gas part) | `a:evm/execution.rs` | `evm2:interpreter/gas.rs` |  |
| `SATIN-POOL-015` | The caller's own charge for a leaf the child did not add is given back after the merge | `satin.md §4` L195; `satin.md §9` L500 | new | `a:limit/ledger.rs` | `b:lib.rs` `start_charge_or_hand_back` |  |
| `SATIN-POOL-016` | An authority charge made before the first frame is not committed out of the outstanding spill; the reservoir the first frame returns unwinds it with any other outstanding spill; a failure of the first frame returns no reservoir that charge drew | `satin.md §4` L158–L161, L234 | new | `a:evm/execution.rs` | `b:tx.rs` `before_initial_frame`<br>`b:tx.rs` `charge_tx_state` |  |
| `SATIN-POOL-017` | When the transaction ends the reservoir left returns to the sender, and so does the unspent regular gas unless the transaction's own frame halted, a revert and a limit stop included | `satin.md §4` L196–L197; `satin.md §11` L886 | new | `a:evm/execution.rs` | `b:tx.rs` `settle_transaction` |  |
| `SATIN-POOL-018` | The receipt's gas used is what the transaction spent from both pools after the inherited refund and floor rules; when the spend less the refund is below the floor, gas used is the floor, no refund is made, and the floor's excess is drawn from the unspent regular gas and the reservoir alike | `satin.md §4` L199–L200; `satin.md §7` L448 | new | `a:evm/result.rs` `MegaGasUsage` | `b:block.rs` `run_transaction` |  |
| `SATIN-POOL-019` | Three ledgers: regular = total − state − history, state = the state charges kept, history = the history charges kept, the body included; spilled state or history gas stays on its own ledger | `satin.md §4` L201–L207 | replaces evm/dual-gas-model.md "Total Gas" (compute and storage split) | `a:evm/result.rs` `MegaGasUsage` | `b:ledger.rs` `history`<br>`b:block.rs` `run_transaction` |  |
| `SATIN-POOL-020` | The EIP-7623 floor, as EIP-7976 and EIP-7981 amend it, is computed and validated as Amsterdam does; the block's execution ledger counts max(regular, floor), history gas taken out of regular before the floor applies | `satin.md §4` L208; `satin.md §7` L446–L448; `satin.md §20` L1272 | new | `a:evm/result.rs` `block_execution_gas` | `b:block.rs` `run_transaction` | undefined: QG-02 |
| `SATIN-POOL-021` | Satin has no separate compute-gas limit: compute is regular gas, bounded by the execution cap and by gas detention | `satin.md §4` L223; `satin.md §10` L529 | replaces evm/compute-gas.md (whole page); replaces evm/resource-limits.md "Limit Set" (compute row) | `a:block/limit.rs` `for_spec` | `b:ledger.rs` `Cfg` |  |
| `SATIN-POOL-022` | Satin's departures from EIP-8037: the reservoir share, history gas on the reservoir and the shared spill, the destruction-table refill | `satin.md §4` L241–L245 | new | none | none |  |

### Gas Schedule and Intrinsic Gas (`satin/evm/gas-schedule.md`)

The Amsterdam gas schedule Satin runs with its two changes, the EIP-2780 intrinsic cost, the charges made before the first frame, the code-deposit charge order and the addresses warm from the start of a transaction.

Rex pages it draws on: `evm/dual-gas-model.md`, `evm/compute-gas.md`.

| Id | Rule | Draft | Rex page | Code (a) | Code (b) | Note |
| --- | --- | --- | --- | --- | --- | --- |
| `SATIN-SCHED-001` | The gas schedule is Amsterdam's (EIP-8038's state-access prices, EIP-2780's intrinsic decomposition, EIP-7976's calldata floor, EIP-7981's access-list floor) with two changes: the EIP-8037 state-gas entries rebuilt at the cost per state byte, and deposited code's history gas at one history byte | `satin.md §5` L262–L267 | replaces evm/dual-gas-model.md (Prague schedule) | `a:evm/schedule.rs` `satin_gas_params` | `b:lib.rs` `satin_version` | undefined: QG-02 |
| `SATIN-SCHED-002` | Every opcode's static gas is Amsterdam's: EXTCODESIZE and EXTCODECOPY pay 200, EIP-8038's two warm accesses | `satin.md §5` L270 | new | `a:evm/schedule.rs` | `evm2:version/gas_params.rs` |  |
| `SATIN-SCHED-003` | The regular-gas entries that differ from Osaka, each with its value (the entry table) | `satin.md §5` L268–L269, L272–L309 | new | `a:evm/schedule.rs` `satin_gas_params` | `b:lib.rs` `satin_version`<br>`evm2:version/gas_params.rs` | undefined: QG-02 |
| `SATIN-SCHED-004` | A cold SSTORE pays 2,100 for its access with its static cost (EIP-8038 folds the warm base into a cold slot's access) | `satin.md §5` L310–L311 | new | `a:evm/schedule.rs` | `evm2:version/gas_params.rs` |  |
| `SATIN-SCHED-005` | The floor's base is the transaction's own decomposed base without its calldata, access-list, authorization and initcode costs (12,000, 15,000, 21,000 or 24,000), plus 64 gas per calldata byte, initcode included, and 64 per access-list byte (20 per address, 32 per key) | `satin.md §5` L313–L314 | new | `a:evm/validation.rs` `IntrinsicGas` | `b:tx.rs` `adjust_intrinsic_gas` |  |
| `SATIN-SCHED-006` | The EIP-2780 intrinsic regular gas: TX_BASE_COST 12,000, plus 3,000 for a recipient other than the sender and 6,000 more with value, plus 12,000 and EIP-3860's initcode cost for a creation, plus calldata, access-list and per-authorization costs; a transfer to the sender itself pays the base alone | `satin.md §5` L316–L317 | replaces evm/dual-gas-model.md "Transaction Intrinsic Costs" | `a:evm/validation.rs` `IntrinsicGas` | `b:tx.rs` `adjust_intrinsic_gas` |  |
| `SATIN-SCHED-007` | The 7,816 per authorization is charged by validation for every entry, applied or not; an authority that already exists is refunded nothing | `satin.md §5` L318; `satin.md §10` L806 | new | `a:evm/validation.rs` | `b:eip7702.rs` `prepare` |  |
| `SATIN-SCHED-008` | The state-dependent parts (a recipient or created account that does not exist, an authority that does not exist, a delegation indicator, an authority's first write) are charged at the start of execution, priced as state gas | `satin.md §5` L319 | new | `a:evm/execution.rs` | `b:tx.rs` `before_initial_frame`<br>`b:eip7702.rs` `execute` |  |
| `SATIN-SCHED-009` | A transaction that cannot pay a charge made before its first frame (a deposit-like caller account, an authorization's charges, the pre-frame write-record history, the first frame's start charge) runs out of gas without running a frame; a list the KV or growth limit skips is not charged | `satin.md §5` L322–L323 | new | `a:evm/execution.rs` | `b:tx.rs` `before_initial_frame` |  |
| `SATIN-SCHED-010` | On that path everything applied before the first frame is taken back but validation's changes to the sender and a deposit-like caller account; the intrinsic gas and the body's history stay charged, the rest of the regular budget is consumed, the reservoir left returns, and a creation's sender keeps its nonce bump | `satin.md §5` L324–L325 | new | `a:evm/execution.rs` | `b:tx.rs` `settle_transaction` |  |
| `SATIN-SCHED-011` | Deposited code is charged after the code passed its checks, in order: the regular per-byte cost (zero), the hashing cost at 6 gas per 32-byte word, the code's state gas, its history gas; a creation that cannot pay one runs out of gas and leaves no code | `satin.md §5` L328–L329; `satin.md §7` L424 | new | `a:evm/host.rs` | `b:lib.rs` `admit_code_deposit`<br>`evm2:evm/message_hooks.rs` `admit_code_deposit` |  |
| `SATIN-SCHED-012` | Precompiles, the block beneficiary and access-list addresses listed without keys are warm from the start (EIP-2929); Rex6's cold charge on their first CALL-family or SELFDESTRUCT-beneficiary touch does not apply | `satin.md §5` L331 | replaces evm/compute-gas.md "Inherited-Cost Exception: Preload-Warm Addresses" | `a:evm/execution.rs` | `evm2:interpreter/instructions/account_load.rs` |  |
| `SATIN-SCHED-013` | The SequencerRegistry's account and its _currentSystemAddress slot are warm from the start of every transaction | `satin.md §5` L332; `satin.md §17` L1180 | new | `a:system/sequencer_registry.rs` `live_system_address` | `b:tx.rs` `read_registry` |  |
| `SATIN-SCHED-014` | The sender and a call's recipient are warm from the start, as EIP-2929 leaves them | `satin.md §5` L333 | new | none | none |  |

### State Gas and SALT Pricing (`satin/evm/state-gas.md`)

How a state charge is priced: EIP-8037's byte counts at MegaETH's cost per state byte, scaled by the multiplier of the SALT bucket the state lands in, where each charge is made and how it is given back.

Rex pages it draws on: `evm/dual-gas-model.md`.

| Id | Rule | Draft | Rex page | Code (a) | Code (b) | Note |
| --- | --- | --- | --- | --- | --- | --- |
| `SATIN-STATE-001` | Every EIP-8037 state charge is entry × m, entry being EIP-8037's byte count times COST_PER_STATE_BYTE = 1,530 | `satin.md §6` L344–L346 | replaces evm/dual-gas-model.md "Storage Gas" (base × (multiplier − 1)) | `a:constants.rs` `COST_PER_STATE_BYTE`<br>`a:external/gas.rs` `BucketMultipliers` | `b:ledger.rs` `CPSB`<br>`b:lib.rs` `reprice` |  |
| `SATIN-STATE-002` | m = floor(bucket_capacity / MIN_BUCKET_SIZE), MIN_BUCKET_SIZE = 256 | `satin.md §6` L347 | replaces evm/dual-gas-model.md "Dynamic SALT Multiplier" | `a:external/gas.rs` `for_capacity`<br>`a:external/salt.rs` `MIN_BUCKET_SIZE` | `b:ledger.rs` `multiplier`<br>`b:ledger.rs` `MIN_BUCKET_SIZE` |  |
| `SATIN-STATE-003` | The state byte table (fresh slot 64, new account 120, created account 120, deployed code 1 per byte, delegation indicator 23) and the bucket each lands in | `satin.md §6` L349–L355 | new | `a:constants.rs` `SLOT_STATE_GAS`<br>`a:constants.rs` `ACCOUNT_STATE_GAS` | `b:lib.rs` `satin_version` |  |
| `SATIN-STATE-004` | A state charge is made where the state is added: the SSTORE that fills a fresh slot; the value CALL, the balance-moving SELFDESTRUCT, the transaction value or the applied authorization that creates an account; CREATE, CREATE2 or a creation transaction | `satin.md §6` L357 | new | `a:evm/host.rs`<br>`a:evm/execution.rs` | `b:lib.rs` `state_gas_price` |  |
| `SATIN-STATE-005` | m scales state gas and nothing else | `satin.md §6` L358 | new | none | none |  |
| `SATIN-STATE-006` | A bucket's multiplier is read at most once per transaction; every later charge and give-back in that bucket uses the same m | `satin.md §6` L359 | new | `a:external/gas.rs` `cached` | `b:ledger.rs` `multiplier` |  |
| `SATIN-STATE-007` | A capacity below MIN_BUCKET_SIZE, or one the node cannot read, is a fault of the node, a deposit included: the transaction is neither priced nor settled and the node reports an internal error | `satin.md §6` L360; `satin.md §21` L1358–L1359; `satin.md §22` L1417 | new | `a:external/gas.rs` `BucketError` | `b:ledger.rs` `SaltBelowMinimum` |  |
| `SATIN-STATE-008` | The only SSTORE that charges fresh-slot state gas has original zero, present zero, new non-zero; the only one that refills it has original zero, present non-zero, new zero, not on an account marked for deletion, at the price charged | `satin.md §6` L361–L364 | new | `a:evm/host.rs` | `b:lib.rs` `mega_sstore`<br>`b:lib.rs` `sstore_completed` |  |
| `SATIN-STATE-009` | The protocol's own transactions are priced at m = 1 without reading a bucket; a deposit that is not system-originated is priced by bucket | `satin.md §6` L367–L368; `satin.md §19` L1253 | new | `a:evm/context.rs` `is_system_originated` | `b:ledger.rs` `set_system_originated` |  |
| `SATIN-STATE-010` | The function that maps an account or a storage slot to its SALT bucket | none | new | `a:external/salt.rs` `bucket_id_for_account`<br>`a:external/hasher/mod.rs` | `b:ledger.rs` `bucket_for`<br>`b:salt_hash/mod.rs` | undefined: QA-04 |

### History Gas and the History Allowance (`satin/evm/history-gas.md`)

The third gas ledger: the price per byte of what a transaction appends to the chain's history, the byte table, when each history charge is made and given back, the exemptions, and the history allowance of a value call.

Rex pages it draws on: `evm/dual-gas-model.md`, `evm/gas-forwarding.md`.

| Id | Rule | Draft | Rex page | Code (a) | Code (b) | Note |
| --- | --- | --- | --- | --- | --- | --- |
| `SATIN-HIST-001` | COST_PER_HISTORY_BYTE = 88 gas per byte, never scaled by SALT | `satin.md §7` L381–L382 | replaces evm/dual-gas-model.md "Storage Gas" (logs, calldata, code deposit, intrinsic storage gas) | `a:constants.rs` `COST_PER_HISTORY_BYTE`<br>`a:evm/history.rs` `history_gas` | `b:ledger.rs` `CPHB` |  |
| `SATIN-HIST-002` | The byte table, shared with data size: TX_BODY_SIZE 310; calldata 1 per byte; access-list address 20; access-list key 32; authorization 101; log 32 + 32 per topic + data; write record 40; deployed code 1 per byte | `satin.md §7` L383–L394 | new | `a:limit/mod.rs` `AUTHORIZATION_SIZE`<br>`a:limit/mod.rs` `log_history_bytes` | `b:ledger.rs` `TX_BODY_SIZE`<br>`b:eip7702.rs` `AUTHORIZATION_SIZE`<br>`b:lib.rs` `mega_log` |  |
| `SATIN-HIST-003` | TX_BODY_SIZE is TX_BASE_SIZE 110 plus TX_FIXED_WRITE_RECORDS = 5 records (the sender and the four fee accounts), charged as an upper bound whether or not each is written; it covers the sender's account writes and the fee credits only | `satin.md §7` L396–L397 | new | `a:limit/mod.rs` `TX_BODY_SIZE`<br>`a:limit/mod.rs` `TX_FIXED_WRITE_RECORDS` | `b:ledger.rs` `TX_BODY_SIZE` |  |
| `SATIN-HIST-004` | The body is charged before execution as intrinsic state gas, not part of the intrinsic regular gas, and never reported on the state ledger | `satin.md §7` L402–L404 | new | `a:evm/history.rs` `transaction_body_bytes` | `b:tx.rs` `begin` |  |
| `SATIN-HIST-005` | The applied authorities' records and the first frame's start record are charged before the first frame; the authorities' records stay when the first frame fails; the start record comes back with that frame, once, also when the destruction table already took it back; an out-of-gas before the first frame keeps neither | `satin.md §7` L405–L412 | new | `a:evm/execution.rs` | `b:tx.rs` `before_initial_frame`<br>`b:eip7702.rs` `execute` |  |
| `SATIN-HIST-006` | A log, a storage write's record and a SELFDESTRUCT's records are charged by the opcode once it completed; what the opcode takes back is given back first, then what it makes is charged | `satin.md §7` L413 | new | `a:evm/host.rs` | `b:lib.rs` `sstore_completed`<br>`b:lib.rs` `mega_log`<br>`b:lib.rs` `mega_selfdestruct` |  |
| `SATIN-HIST-007` | A part the destruction table takes back is given back to the destroying frame even when another frame paid it; every other record to whoever paid it | `satin.md §7` L414–L415, L425–L426 | new | `a:limit/record.rs` `DestroyedParts` | `b:lib.rs` `mega_selfdestruct` |  |
| `SATIN-HIST-008` | An opcode that fails after its write was observed keeps nothing and is charged no history; a LOG observes its write after every inherited charge | `satin.md §7` L416 | new | `a:evm/host.rs` | `b:lib.rs` `mega_log` |  |
| `SATIN-HIST-009` | A call or creation charges its own frame for the records the frame it starts makes, after the forward is computed; a caller that cannot pay halts out of gas and the frame does not start; the price of a record the start takes back returns to the caller once the frame returned with its start kept | `satin.md §7` L417–L419 | new | `a:limit/ledger.rs`<br>`a:limit/record.rs` `StartRecords` | `b:lib.rs` `start_charge_or_hand_back`<br>`b:lib.rs` `count_start` |  |
| `SATIN-HIST-010` | A value CALL to an empty account charges in order: its regular gas (static 100, memory, value transfer, cold surcharge and the new account's regular gas, zero), the new account's state gas reservoir first, the 98/100 forward of the regular gas left, then the start records' history; the reservoir share follows the history charge | `satin.md §7` L420–L422 | new | `a:evm/execution.rs` | `b:lib.rs` `mega_call_impl` |  |
| `SATIN-HIST-011` | CREATE and CREATE2 charge the created account's state gas, when the address is empty, before computing the forward, and give the reservoir share after the start records' history | `satin.md §7` L423 | new | `a:evm/execution.rs` | `b:lib.rs` `mega_create_impl` |  |
| `SATIN-HIST-012` | Every give-back of state or history gas follows one refill order: the frame's regular gas first, up to the spill still outstanding on that frame, the rest to its reservoir | `satin.md §7` L428–L431 | new | `a:limit/ledger.rs` | `b:ledger.rs` `refill_history` |  |
| `SATIN-HIST-013` | A record an opcode commits is checked against the limits before its history is charged; a frame that cannot pay that history halts out of gas keeping neither the record nor its bytes | `satin.md §7` L433–L434 | new | `a:evm/host.rs` | `b:lib.rs` `sstore_completed` |  |
| `SATIN-HIST-014` | At a frame start the calling opcode pays for the records before the start and they are counted; the charge for a start a limit stops is given back when the stopped frame returns | `satin.md §7` L435 | new | `a:limit/ledger.rs` | `b:lib.rs` `start_charge_or_hand_back` |  |
| `SATIN-HIST-015` | The start records are charged as the state stands: a value the caller cannot fund, a creator nonce that cannot be bumped, or a call depth past the limit makes no record and is charged nothing | `satin.md §7` L436 | new | `a:limit/record.rs` `start_makes_no_records` | `b:lib.rs` `mega_create_impl` |  |
| `SATIN-HIST-016` | No history gas for an EIP-7708 transfer log, an Oracle hint's payload, or any byte of a deposit, a system-originated transaction or a system call (their deposited-code history is zero); the exemption is from history gas alone | `satin.md §7` L438–L444; `satin.md §19` L1254 | new | `a:evm/schedule.rs` `satin_gas_params_history_exempt`<br>`a:evm/context.rs` `prices_history` | `b:tx.rs` `prepare_deposit` |  |
| `SATIN-HIST-017` | The floor is still computed; it can raise the gas used of a transaction exempt from history gas, binds the block's execution figure, and where it binds is drawn from the whole gas limit; a deposit is charged nothing either way | `satin.md §7` L446–L448 | new | `a:evm/result.rs` `block_execution_gas` | `b:block.rs` `run_transaction` |  |
| `SATIN-HIST-018` | A value-transferring CALL or CALLCODE below the transaction's own frame grants the frame it starts a history allowance of HISTORY_ALLOWANCE_BYTES = 160 bytes (14,080 gas) | `satin.md §8` L458 | replaces evm/dual-gas-model.md "Storage Gas Stipend for Value Transfers"; replaces evm/gas-forwarding.md "Storage Gas Stipend Interaction" | `a:evm/history.rs` `HISTORY_ALLOWANCE_BYTES` | `b:ledger.rs` `HISTORY_ALLOWANCE_BYTES` |  |
| `SATIN-HIST-019` | Only a log's history charge in that frame draws the allowance, before the frame's gas; a write record never does | `satin.md §8` L459–L460 | new | `a:evm/history.rs` `history_allowance_gas` | `b:lib.rs` `mega_log` |  |
| `SATIN-HIST-020` | The allowance is not frame gas: it pays for nothing else, is never returned as gas and is on no ledger; the bytes it pays for still count as appended | `satin.md §8` L461–L462; `satin.md §9` L486 | new | `a:evm/history.rs` | `b:ledger.rs` `Entry` |  |
| `SATIN-HIST-021` | The transfer log of the value that granted the allowance does not draw on it | `satin.md §8` L463; `satin.md §14` L1051 | new | `a:limit/record.rs` `is_transfer_log` | `b:lib.rs` `mega_log` |  |

### Gas Forwarding (`satin/evm/gas-forwarding.md`)

How much regular gas a call or creation forwards (98/100 of the caller's remaining gas in place of 63/64), the value-transfer stipend, and how the forward differs from the reservoir share and the frame budget.

Rex pages it draws on: `evm/gas-forwarding.md`.

| Id | Rule | Draft | Rex page | Code (a) | Code (b) | Note |
| --- | --- | --- | --- | --- | --- | --- |
| `SATIN-FWD-001` | CALL, CALLCODE, DELEGATECALL, STATICCALL, CREATE and CREATE2 cap the regular gas they forward at parent_remaining_gas − parent_remaining_gas × 2 / 100 (integer division), in place of EIP-150's 63/64 | `satin.md §9` L473–L476, L479; `satin.md §4` L184 | keeps evm/gas-forwarding.md "Stable Forwarding Rule" | `a:evm/schedule.rs` `FORWARD_REDUCTION_QUOTIENT` | `b:lib.rs` `satin_version` |  |
| `SATIN-FWD-002` | parent_remaining_gas is the caller's regular gas after the opcode's charges before the forward, the 11,300 value transfer (which contains the 2,300 stipend) included | `satin.md §9` L477–L478 | new | `a:evm/schedule.rs` | `evm2:version/gas_params.rs` |  |
| `SATIN-FWD-003` | The child's regular gas is min(requested_gas, forwarded_gas_cap), plus the 2,300 stipend for a value-transferring CALL or CALLCODE only; the stipend is outside the cap and not taken from the caller | `satin.md §9` L480–L483, L485 | keeps evm/gas-forwarding.md "Value Transfer Stipend" | `a:evm/execution.rs` `value_call_stipend` | `evm2:interpreter/instructions/system.rs` |  |
| `SATIN-FWD-004` | CREATE and CREATE2 forward forwarded_gas_cap and add no stipend | `satin.md §9` L484 | keeps evm/gas-forwarding.md "Stable Forwarding Rule" | `a:evm/execution.rs` | `b:lib.rs` `mega_create_impl` |  |
| `SATIN-FWD-005` | The reservoir is not part of the cap; a call that forwards no regular gas still forwards the reservoir share | `satin.md §9` L488–L492 | new | `a:limit/ledger.rs` `reservoir_share` | `b:ledger.rs` `reservoir_share` |  |
| `SATIN-FWD-006` | The reservoir-share subtraction and the frame-budget multiplication are different integers (98 of 99 and the whole value below 50, against 97 of 99 and 0 of 1) | `satin.md §9` L501–L505, L511–L514; `satin.md §10` L609–L610 | new | `a:limit/ledger.rs` `reservoir_share`<br>`a:limit/mod.rs` `FRAME_DATA_SHARE_NUMERATOR` | `b:ledger.rs` `reservoir_share`<br>`b:ledger.rs` `push_child` |  |
| `SATIN-FWD-007` | A system-originated transaction and a system call are not exempt from the reservoir split | `satin.md §9` L515 | new | `a:evm/execution.rs` | `b:ledger.rs` `begin_system_call` |  |

### Resource Limits (`satin/evm/resource-limits.md`)

The three limited dimensions (data size, KV updates, state growth) per transaction and per frame, how frame budgets are derived and merged, the order in which one operation is held to them, and the rule that the limits are fixed per spec.

Rex pages it draws on: `evm/resource-limits.md`.

| Id | Rule | Draft | Rex page | Code (a) | Code (b) | Note |
| --- | --- | --- | --- | --- | --- | --- |
| `SATIN-LIM-001` | Three dimensions are limited per transaction, each with a frame budget: data size (bytes of the byte table) TX_DATA_LIMIT = 13,107,200; KV updates (write records) TX_KV_UPDATE_LIMIT = 500,000; state growth (new accounts and slots) TX_STATE_GROWTH_LIMIT = 1,000; compute is not a fourth limit | `satin.md §10` L528–L537 | replaces evm/resource-limits.md "Limit Set" and "Runtime Transaction-Level Limits" | `a:constants.rs` `TX_DATA_LIMIT`<br>`a:block/limit.rs` `for_spec` | `b:ledger.rs` `Cfg` | disagreement: QC-02 |
| `SATIN-LIM-002` | The transaction's own frame gets what the transaction has left in each dimension once the body and the pre-frame counts are counted | `satin.md §10` L581, L605–L606 | replaces evm/resource-limits.md "Per-Call-Frame Runtime Budgets" | `a:limit/ledger.rs` | `b:ledger.rs` `draw_first_frame` |  |
| `SATIN-LIM-003` | A child gets parent_remaining × FRAME_DATA_SHARE_NUMERATOR (98) / FRAME_DATA_SHARE_DENOMINATOR (100), rounded down, in each of the three dimensions; a CREATE or CREATE2 takes that share at the opcode | `satin.md §10` L582–L583, L601–L602, L607 | replaces evm/resource-limits.md "Per-Call-Frame Runtime Budgets" | `a:limit/mod.rs` `FRAME_DATA_SHARE_NUMERATOR`<br>`a:limit/mod.rs` `FRAME_DATA_SHARE_DENOMINATOR` | `b:ledger.rs` `push_child` |  |
| `SATIN-LIM-004` | A frame's net is signed (added, less given back, plus successful children's nets); its remaining is min(budget, max(0, budget − net)), so a negative net never raises what it forwards | `satin.md §10` L584–L587, L592–L593, L747–L748 | new | `a:limit/ledger.rs` | `b:ledger.rs` `Entry` |  |
| `SATIN-LIM-005` | The transaction's net is what sits on no frame (the body, the applied authorities' records, a deposit's caller, every admitted hint) plus the net of every frame on the stack; its remaining is the same clamp against the transaction limit | `satin.md §10` L588–L591 | new | `a:limit/limit.rs` | `b:ledger.rs` `Lite` |  |
| `SATIN-LIM-006` | A successful frame's signed net merges into its caller, whose remaining is computed again from its own budget; a failed frame's net and the credits inside it are discarded | `satin.md §10` L594–L599, L744–L746 | new | `a:limit/ledger.rs` | `b:ledger.rs` `pop_child` |  |
| `SATIN-LIM-007` | The KV and state-growth counts a transaction reports are max(net, 0) | `satin.md §10` L600, L749 | new | `a:limit/limit.rs` | `b:ledger.rs` `usage` |  |
| `SATIN-LIM-008` | A creator's nonce record, and its state growth when the bump creates the creator, are counted on the creator when the creation returns, held to the creator's budget, and survive the creation's failure; the creation's budget is the share taken before that record | `satin.md §10` L557–L558, L603–L604, L782–L784 | new | `a:evm/execution.rs` `hold_creator` | `b:satin_ext.rs` `hold_caller` |  |
| `SATIN-LIM-009` | Satin sets no further per-frame cap | `satin.md §10` L608 | new | `a:limit/mod.rs` `EvmTxRuntimeLimits` | `b:ledger.rs` `Cfg` | disagreement: QA-06 |
| `SATIN-LIM-010` | At one completed write or decided frame start, an operation crossing several dimensions stops on the first of data size (kind 0), KV updates (kind 1), state growth (kind 3); compute (kind 2) is decided at the regular charge, before the write is counted | `satin.md §10` L760–L764 | replaces evm/resource-limits.md (Rex6 dimension order) | `a:limit/mod.rs` | `b:ledger.rs` `KIND`<br>`b:ledger.rs` `hold_check` |  |
| `SATIN-LIM-011` | Within a dimension the frame budget is tested before the transaction limit: a crossed budget names the budget, otherwise a crossed transaction limit names that limit | `satin.md §10` L768–L771 | new | `a:limit/limit.rs` | `b:ledger.rs` `hold_check` |  |
| `SATIN-LIM-012` | No frame budget applies to an Oracle hint's bytes or to the authorization list; a framed write can cross the transaction's data-size limit alone after hints used it; KV and growth cannot cross the transaction limit without crossing the frame budget | `satin.md §10` L772–L777 | new | `a:limit/limit.rs` | `b:intercept.rs` `hint_before` |  |
| `SATIN-LIM-013` | A frame start is held to the limits once it is decided (the value moved; for a creation the nonce bumped and the account made), to what the start kept: its records, its state growth, its transfer log | `satin.md §10` L778–L779 | new | `a:limit/record.rs` `StartRecords` | `b:lib.rs` `count_start` |  |
| `SATIN-LIM-014` | A start answered with a failure (a precompile that fails after its value moved) counts nothing and is not stopped | `satin.md §10` L780 | new | `a:evm/execution.rs` | `b:lib.rs` `StartHooks` |  |
| `SATIN-LIM-015` | A start the caller's account refuses (a value it cannot fund, a creator nonce that cannot be bumped) counts nothing, is stopped by no limit and is charged nothing | `satin.md §10` L574, L781 | new | `a:limit/record.rs` `start_makes_no_records` | `b:tx.rs` `creation_nonce_unbumpable` | disagreement: QA-08 |
| `SATIN-LIM-016` | A creation onto an occupied address is not stopped for what its start would count; the creator's surviving nonce record is counted on the creator; the collision adds no state growth | `satin.md §10` L782–L784 | new | `a:evm/execution.rs` `hold_creator` | `b:lib.rs` `mega_create_impl` |  |
| `SATIN-LIM-017` | The transaction limits, the frame share, the detention caps and the block budgets are protocol values of the spec, the same on every chain, never chain configuration or values handed with a block | `satin.md §10` L844–L848; `satin.md §20` L1308–L1309 | new | `a:block/limit.rs` `for_spec` | `b:ledger.rs` `Cfg`<br>`b:block.rs` `BLOCK_BUDGETS` | disagreement: QC-02 |
| `SATIN-LIM-018` | An execution outside a block (a call, a gas estimate, a simulation) is expected to use the same per-transaction limits and caps; a node that does not acts on its own policy and keeps eth_call and eth_estimateGas consistent | `satin.md §10` L849–L850 | new | `a:evm/context.rs` `with_tx_runtime_limits` | none | disagreement: QG-06 |

### Resource Accounting (`satin/evm/resource-accounting.md`)

What each limited dimension counts: the data-size byte table and when each item is counted, write records (the KV count), and state growth with its SSTORE transition table.

Rex pages it draws on: `evm/resource-accounting.md`.

| Id | Rule | Draft | Rex page | Code (a) | Code (b) | Note |
| --- | --- | --- | --- | --- | --- | --- |
| `SATIN-ACCT-001` | Data size counts the byte table plus two items that pay no history: an EIP-7708 transfer log, TRANSFER_LOG_SIZE = 160, and an Oracle hint's payload length | `satin.md §10` L539 | replaces evm/resource-accounting.md "Data Size" | `a:limit/mod.rs` `TRANSFER_LOG_SIZE` | `b:ledger.rs` `TRANSFER_LOG_SIZE` |  |
| `SATIN-ACCT-002` | When each item is counted: the body before any frame; the applied authorities' records before the first frame; a start's records and transfer log at the start; a storage write's record, a log, a SELFDESTRUCT's records and transfer log once the opcode completed; deployed code after every deposit charge and before the creation commits; a hint before it is forwarded, on the transaction alone | `satin.md §10` L540 | new | `a:evm/host.rs`<br>`a:limit/record.rs` | `b:lib.rs` `sstore_completed`<br>`b:lib.rs` `count_start`<br>`b:intercept.rs` `hint_before` |  |
| `SATIN-ACCT-003` | A deposit's data size is counted like any transaction's; a deposit that fails keeps its body and its admitted hints | `satin.md §10` L541; `satin.md §11` L873 | new | `a:limit/limit.rs` | `b:tx.rs` `failed_deposit` |  |
| `SATIN-ACCT-004` | A write record is one account or storage write the transaction keeps: a slot's while its value differs from its original value in the transaction; an account's while its nonce, balance or code differs from what the transaction loaded (its original info at first load) | `satin.md §10` L543–L545 | replaces evm/resource-accounting.md "KV Updates" | `a:limit/record.rs` | `b:ledger.rs` `changed`<br>`evm2:evm/state/account.rs` `original` |  |
| `SATIN-ACCT-005` | The writes that make records: a value transfer's sender and recipient; a creation's created account and the creator's nonce; a SELFDESTRUCT's beneficiary and cleared account; an applied authority; the transaction's value recipient or created account; a created account is no exception | `satin.md §10` L546–L547 | new | `a:limit/record.rs` `Accounts` | `b:ledger.rs` `StartRecords` |  |
| `SATIN-ACCT-006` | A record is made where the write is and taken back where a write returns the account (a value transfer's return in the frame it starts, with its data size; a SELFDESTRUCT's where it completes); a slot written back gives its record back | `satin.md §10` L548, L552 | new | `a:limit/record.rs` `RecordDelta` | `b:ledger.rs` `set_slot_record` |  |
| `SATIN-ACCT-007` | A value-transferring CALLCODE, and a value CALL to the calling account itself, change no account and record none | `satin.md §10` L553 | new | `a:limit/record.rs` | `b:lib.rs` `count_start` |  |
| `SATIN-ACCT-008` | The sender's account is one of the body's fixed records and is never recorded again | `satin.md §10` L554 | new | `a:limit/record.rs` | `b:ledger.rs` `changed` |  |
| `SATIN-ACCT-009` | An applied EIP-7702 authority is changed by its nonce and delegation when applied; a later write to it adds nothing | `satin.md §10` L555 | new | `a:limit/record.rs` | `b:eip7702.rs` `execute` |  |
| `SATIN-ACCT-010` | The four fee accounts are in the body only for the settlement's fee credits; a write execution makes to one that is not the sender is recorded like any other | `satin.md §10` L556; `satin.md §7` L397 | replaces evm/resource-accounting.md "Post-Execution Fee-Reward Accounting" | `a:limit/record.rs` | `b:ledger.rs` `changed` |  |
| `SATIN-ACCT-011` | A successful frame's records and bytes merge into its caller's; a failed frame's are discarded and the records it took back stand again, the creator's nonce record excepted | `satin.md §10` L557 | new | `a:limit/ledger.rs` | `b:ledger.rs` `pop_child` |  |
| `SATIN-ACCT-012` | The KV count is the write-record count; each record weighs WRITE_RECORD_SIZE = 40 bytes of data size, counted and taken back with it; TX_KV_UPDATE_LIMIT is enforced on the count even though the data-size cap binds first at these constants; a record taken back cannot cross it | `satin.md §10` L559–L567 | new | `a:limit/mod.rs` `WRITE_RECORD_SIZE` | `b:ledger.rs` `WRITE_RECORD_SIZE` |  |
| `SATIN-ACCT-013` | State growth is the net count of new accounts and new slots kept: one unit per account-leaf or fresh-slot charge site, not per byte of code or indicator | `satin.md §10` L616–L619, L751–L754 | replaces evm/resource-accounting.md "State Growth" | `a:limit/limit.rs` | `b:ledger.rs` `Lite` |  |
| `SATIN-ACCT-014` | The rises: a fresh slot; a value CALL to an EIP-161-empty account; a SELFDESTRUCT moving a non-zero balance to a non-existent account; the recipient a transaction's value creates; an applied authorization that creates its authority; a creation onto an empty address; a keyless signer its creation's bump creates; a deposit-like transaction's created caller | `satin.md §10` L620–L628 | new | `a:limit/record.rs` | `b:lib.rs` `count_start`<br>`b:keyless.rs` `run` |  |
| `SATIN-ACCT-015` | Not rises: an existing account, a CALLCODE, a value call to the calling account, deployed code, the delegation indicator | `satin.md §10` L629 | new | `a:limit/record.rs` | `b:lib.rs` `count_start` |  |
| `SATIN-ACCT-016` | The SSTORE state-growth transition table (original, present, new) and its worked sequences | `satin.md §10` L630–L650 | new | `a:evm/host.rs` | `b:lib.rs` `mega_sstore` |  |
| `SATIN-ACCT-017` | The settlement's fee credits are neither rises nor EIP-8037 charge sites | `satin.md §10` L651–L654 | replaces evm/resource-accounting.md "Post-Execution Fee-Reward Accounting" | `a:limit/limit.rs` | `b:block.rs` `run_transaction` |  |
| `SATIN-ACCT-018` | Falls happen at the opcode that restores the state and cannot cross a limit; the only slot fall is original zero, present non-zero, new zero | `satin.md §10` L655–L657 | new | `a:evm/host.rs` | `b:lib.rs` `sstore_completed` |  |
| `SATIN-ACCT-019` | A rise that would take the signed net past the transaction limit or the frame budget is the crossing and is not kept | `satin.md §10` L750 | new | `a:limit/limit.rs` | `b:ledger.rs` `over` |  |
| `SATIN-ACCT-020` | A failed deposit that creates its caller counts one unit of growth on the transaction and the block counter, pays no state gas, and is not stopped; a deposit that succeeds or reverts makes the ordinary charged rise, kept through a stop of its first frame | `satin.md §10` L755–L758; `satin.md §21` L1341–L1342 | new | `a:limit/limit.rs` | `b:tx.rs` `failed_deposit` |  |

### EIP-7702 Authorizations Before the First Frame (`satin/evm/authorizations.md`)

How a transaction's authorization list is decided before its first frame: the simulation, the totals held to the KV and state-growth limits, the all-or-nothing skip, and the charges and warmth of an applied list.

Rex pages it draws on: `evm/resource-limits.md`, `evm/resource-accounting.md`, `upgrades/rex6.md`.

| Id | Rule | Draft | Rex page | Code (a) | Code (b) | Note |
| --- | --- | --- | --- | --- | --- | --- |
| `SATIN-AUTH-001` | Before the first frame the list is decided by simulating EIP-7702 application in list order; the simulation writes nothing and warms nothing | `satin.md §10` L786–L787 | replaces upgrades/rex6.md "EIP-7702 Authorization List Skip on Pre-Frame Limit Exceed" | `a:evm/execution.rs` | `b:eip7702.rs` `simulate` |  |
| `SATIN-AUTH-002` | An entry whose chain id is neither zero nor the chain's, whose nonce is 2^64 − 1, or whose signature recovers no authority is skipped without reading its authority | `satin.md §10` L788 | new | `a:evm/execution.rs` | `b:eip7702.rs` `simulate` |  |
| `SATIN-AUTH-003` | Every other entry loads its authority's account with its code; an account holding code other than a delegation is skipped and its simulated nonce is not bumped | `satin.md §10` L789–L790 | new | `a:evm/execution.rs` | `b:eip7702.rs` `simulate` | disagreement: QD-01 |
| `SATIN-AUTH-004` | The effective nonce: after earlier acceptances for the same authority, the simulated nonce; for the sender with none, its nonce after validation's bump; otherwise the account's nonce; a mismatch skips, a match applies and bumps the simulated nonce | `satin.md §10` L791–L797 | new | `a:evm/execution.rs` | `b:eip7702.rs` `simulate` |  |
| `SATIN-AUTH-005` | The simulation walks the whole list without stopping at a crossing; each distinct authority that passed the gates is loaded once, later entries using the simulated nonce and the loaded code | `satin.md §10` L798–L800 | new | `a:evm/execution.rs` | `b:eip7702.rs` `simulate` | disagreement: QD-01 |
| `SATIN-AUTH-006` | A failed read of an authority the simulation consults is a database fault: no outcome; a fatal database error is an internal error, any other makes the block invalid; never a refusal for the limit | `satin.md §10` L801–L804 | new | `a:block/executor.rs` `MegaBlockExecutionError` | `b:eip7702.rs` `execute` |  |
| `SATIN-AUTH-007` | The simulation charges no cold-access gas; the intrinsic 7,816 per entry is already charged for every entry | `satin.md §10` L805–L806 | new | `a:evm/validation.rs` | `b:eip7702.rs` `prepare` |  |
| `SATIN-AUTH-008` | The list's totals: one write record per distinct authority it would change other than the sender, one growth unit per distinct authority it would create, account-creation state gas once per new authority | `satin.md §10` L576, L807, L815–L816 | new | `a:evm/execution.rs` | `b:eip7702.rs` `Charges` |  |
| `SATIN-AUTH-009` | Delegation-indicator state gas at most once per authority: only for an accepted non-zero designator, with no indicator at the transaction's start and none set earlier in the list; a clear charges none; a zero target still bumps the nonce and can create the account; the indicator is not growth | `satin.md §10` L808–L814; `satin.md §5` L320 | new | `a:evm/execution.rs` | `b:eip7702.rs` `Charges` |  |
| `SATIN-AUTH-010` | If the KV or growth totals would exceed the transaction limit, none of the list applies and none of its state gas or history is charged, and the transaction's own frame is stopped before it runs with MegaLimitExceeded of the crossed kind and the transaction limit; both crossed names kind 1 | `satin.md §10` L817–L821 | new | `a:evm/execution.rs` | `b:eip7702.rs` `execute` |  |
| `SATIN-AUTH-011` | A skipped list keeps no authority account, record, state gas or history, writes no delegation and bumps no nonce beyond the sender's; the intrinsic regular gas, the body's history and data size stay | `satin.md §10` L822–L824; `satin.md §11` L894 | new | `a:evm/execution.rs` | `b:eip7702.rs` `execute` |  |
| `SATIN-AUTH-012` | On a skip the consulted authorities are not made warm, except one already warm from the transaction's start (sender, call recipient, beneficiary, access-list address, precompile, SequencerRegistry) | `satin.md §10` L825 | new | `a:evm/execution.rs` | `b:eip7702.rs` `execute` |  |
| `SATIN-AUTH-013` | The skip is all or nothing and is settled as a revert-class stop of the first frame | `satin.md §10` L827–L829 | replaces upgrades/rex6.md "EIP-7702 Authorization List Skip on Pre-Frame Limit Exceed" | `a:evm/execution.rs` | `b:eip7702.rs` `execute` |  |
| `SATIN-AUTH-014` | A list that fits is applied: EIP-7702 warms every authority the application loads; an entry skipped by its chain id, its 2^64 − 1 nonce or its signature is neither loaded nor warmed; one skipped for its code or its nonce is loaded and warmed | `satin.md §10` L830–L832 | new | `a:evm/execution.rs` | `b:eip7702.rs` `execute` |  |
| `SATIN-AUTH-015` | The authorities' state gas and record history are charged when the list is applied and reduce what the first frame is given; one that cannot be paid takes the pre-frame out-of-gas path (for a non-deposit an out-of-gas halt, not a stop); the limit is decided before those charges | `satin.md §10` L833–L836; `satin.md §5` L322 | new | `a:evm/execution.rs` | `b:eip7702.rs` `execute` |  |
| `SATIN-AUTH-016` | When the list fits, a later stop of the first frame keeps the authorizations, their state gas, records and history | `satin.md §10` L837; `satin.md §11` L893; `satin.md §7` L407 | new | `a:evm/execution.rs` | `b:eip7702.rs` `execute` |  |
| `SATIN-AUTH-017` | A deposit's created caller is not an authorization: it is always created and kept, and cannot alone cross the growth limit | `satin.md §10` L838–L839 | new | `a:evm/execution.rs` | `b:tx.rs` `prepare_deposit_inner` |  |
| `SATIN-AUTH-018` | The list rule is decided during execution where the accounts are read; it is not a pool rejection | `satin.md §10` L840–L841 | new | `a:evm/validation.rs` | `b:eip7702.rs` `execute` |  |

### SELFDESTRUCT and the Destruction Table (`satin/evm/selfdestruct.md`)

SELFDESTRUCT under EIP-6780 in Satin: the destruction table that refills the state gas and takes back the records of what a transaction created and destroys, the marked account afterwards, the beneficiary's rise, the order of a destruction's effects, and the creation-collision rule.

Rex pages it draws on: `evm/selfdestruct.md`.

| Id | Rule | Draft | Rex page | Code (a) | Code (b) | Note |
| --- | --- | --- | --- | --- | --- | --- |
| `SATIN-SD-001` | EIP-6780 semantics are inherited: a SELFDESTRUCT deletes an account only when the account was created in the same transaction | `satin.md §10` L701–L703 | keeps evm/selfdestruct.md "Stable Behavior" | `a:evm/host.rs` | `b:lib.rs` `mega_selfdestruct` |  |
| `SATIN-SD-002` | The first effective SELFDESTRUCT of an account created in the same transaction applies the destruction table to every part of it (leaf, code, slots), by its value at the transaction's start and before the destruction | `satin.md §10` L661–L667 | replaces evm/selfdestruct.md "State Growth Refund" | `a:limit/record.rs` `DestroyedParts` | `b:lib.rs` `mega_selfdestruct` |  |
| `SATIN-SD-003` | A slot's value at the transaction's start is its original value at first access; a slot first accessed after the creation reads zero; one accessed before keeps the value it held | `satin.md §10` L663–L665 | new | `a:limit/record.rs` | `b:lib.rs` `mega_selfdestruct` |  |
| `SATIN-SD-004` | The table's rows: account leaf (absent or present at the start), deployed code (absent then present, absent then absent, present unreachable), slot (zero then non-zero, zero then zero, non-zero then any) | `satin.md §10` L669–L678 | new | `a:limit/record.rs` `DestroyedParts` | `b:lib.rs` `mega_selfdestruct` |  |
| `SATIN-SD-005` | A refill is the price that part was charged (entry × that charge's multiplier) and goes to the destroying frame, also when another frame paid; the absent leaf's charge is this transaction's charge for that leaf | `satin.md §10` L680–L681; `satin.md §6` L365–L366 | new | `a:limit/record.rs` | `b:lib.rs` `mega_selfdestruct` |  |
| `SATIN-SD-006` | State growth falls for the absent leaf and for each zero-then-non-zero slot and nothing else; the leaf's fall stands even when the creation added no rise | `satin.md §10` L682–L684 | new | `a:limit/record.rs` | `b:lib.rs` `mega_selfdestruct` |  |
| `SATIN-SD-007` | A record the table takes back returns its data size to the destroying frame's budget and its history gas to that frame, and the KV count falls; for a succeeding transaction frame this is the record's history once, and the settlement does not give it back again | `satin.md §10` L549–L551, L685–L687; `satin.md §7` L410–L411 | new | `a:limit/ledger.rs` `Settlement` | `b:tx.rs` `settle_transaction` |  |
| `SATIN-SD-008` | Deployed code is not a record nor growth; code on the absent-then-present row returns its data size and history gas the same way | `satin.md §10` L688–L689 | new | `a:limit/record.rs` | `b:lib.rs` `mega_selfdestruct` |  |
| `SATIN-SD-009` | The give-back follows the refill order, is not an EIP-3529 refund, is credited with the completed write after every charge the opcode makes, and never raises the frame's remaining above its budget | `satin.md §10` L690–L695 | new | `a:limit/ledger.rs` | `b:ledger.rs` `refill_history` |  |
| `SATIN-SD-010` | When the destroying frame succeeds the give-back is unspent gas that returns up the chain; when it, or a frame containing it, fails, the mark and every effect of the table are discarded and records it took back stand again | `satin.md §10` L696–L699 | new | `a:limit/ledger.rs` | `b:ledger.rs` `pop_child` |  |
| `SATIN-SD-011` | A later SELFDESTRUCT of the same account while the mark stands applies the table for nothing | `satin.md §10` L700 | new | `a:limit/record.rs` | `b:ledger.rs` `is_destroyed` |  |
| `SATIN-SD-012` | A SELFDESTRUCT of an account not created in the transaction applies no table and does not mark the account | `satin.md §10` L701–L703 | new | `a:limit/record.rs` | `b:lib.rs` `mega_selfdestruct` |  |
| `SATIN-SD-013` | While the mark stands the account adds no growth and keeps no state gas: an SSTORE of its slots neither rises nor falls nor charges nor refills (its regular gas unchanged) | `satin.md §10` L704–L707 | new | `a:evm/host.rs` | `b:lib.rs` `mega_sstore` |  |
| `SATIN-SD-014` | Code deposited after a constructor destroyed its own account pays no state gas but its data size and history gas, which no later destruction takes back | `satin.md §10` L708–L710 | new | `a:evm/host.rs` | `b:lib.rs` `admit_code_deposit` |  |
| `SATIN-SD-015` | Value sent to the marked account is no rise and no record; the account is removed at the transaction's end with whatever it holds, and that removal takes nothing back again | `satin.md §10` L711–L715 | new | `a:limit/record.rs` | `b:ledger.rs` `is_destroyed` |  |
| `SATIN-SD-016` | A creation collides when the address holds non-empty code or a non-zero nonce, never on storage alone (EIP-7610 is not applied); what that means for the slots of such an address | `satin.md §10` L716–L725; `satin.md §4` L162 | new | `a:evm/execution.rs` | `evm2:interpreter/instructions/system.rs` |  |
| `SATIN-SD-017` | An EIP-161-empty account whose leaf the state holds (non-empty storage) is the present-leaf row: the creation may charge new-account state gas and count a rise, and the destruction refills and subtracts neither | `satin.md §10` L726–L728 | new | `a:limit/record.rs` | `b:lib.rs` `mega_selfdestruct` |  |
| `SATIN-SD-018` | A SELFDESTRUCT that moves a non-zero balance to a distinct non-existent account is a rise (a repeated destruction included), a zero balance is not; the rise is held only after the operation's give-back | `satin.md §10` L729–L735; `satin.md §6` L357 | replaces evm/selfdestruct.md "Beneficiary Account Creation" and "Beneficiary Balance Credit to an Existing Account" | `a:evm/host.rs` | `b:lib.rs` `mega_selfdestruct` |  |
| `SATIN-SD-019` | The order of a destruction: compute is decided first (a detention crossing applies nothing); then the table's give-back; then the positive effects in the order data size, KV updates, state growth (the records it makes, its transfer log, the beneficiary's growth); a crossing positive effect stops the frame and the operation keeps nothing | `satin.md §10` L736–L743 | replaces evm/selfdestruct.md "Running Out of Gas After Recording" | `a:evm/host.rs` | `b:lib.rs` `mega_selfdestruct` |  |
| `SATIN-SD-020` | A SELFDESTRUCT's volatile reads of either end are committed only after its last fallible step | `satin.md §12` L941 | new | `a:evm/instructions.rs` | `b:lib.rs` `beneficiary_read` |  |

### Limit Stops (`satin/evm/limit-stops.md`)

The revert-class stop: every resource limit and gas detention's compute limit stops the frame that crosses it with a revert its caller can catch; what the stop reverts and keeps, how a stopped transaction settles, and the revert data.

Rex pages it draws on: `evm/resource-limits.md`, `evm/compute-gas.md`, `glossary.md`.

| Id | Rule | Draft | Rex page | Code (a) | Code (b) | Note |
| --- | --- | --- | --- | --- | --- | --- |
| `SATIN-STOP-001` | Every limit (the transaction's data-size, KV and growth limits, a frame's budget in those, gas detention's compute limit) stops the frame that crosses it with a revert, never a halt | `satin.md §11` L862; `satin.md §10` L611 | replaces evm/resource-limits.md "Outcomes"; replaces evm/compute-gas.md "Exceed Behavior" | `a:limit/mod.rs` `MegaLimitExceeded` | `b:ledger.rs` `stop_frame`<br>`b:ledger.rs` `limit_exceeded_output` |  |
| `SATIN-STOP-002` | A limit stop exists in exactly four dimensions: data size (0), KV updates (1), compute under detention (2), state growth (3); nothing else is a limit stop | `satin.md §11` L863–L864 | new | `a:limit/mod.rs` `LimitKind` | `b:ledger.rs` `KIND` |  |
| `SATIN-STOP-003` | The stop applies only to a transaction that passes validation and pays every pre-frame charge; any other reports no stop (a rejection, or a failed deposit whose body stays counted) | `satin.md §11` L871–L873 | new | `a:evm/result.rs` `limit_stop` | `b:ledger.rs` `Settlement` |  |
| `SATIN-STOP-004` | The crossing frame reverts with MegaLimitExceeded(uint8 kind, uint64 limit) as its output; the crossing write or charge is not made; every write and log of the frame is reverted as a REVERT reverts them | `satin.md §11` L876–L877 | new | `a:limit/mod.rs` `MegaLimitExceeded` | `b:ledger.rs` `revert_with` |  |
| `SATIN-STOP-005` | The caller resumes as after any revert: the call fails, its return data is the stop's revert data, and the gas the frame had (before the crossing charge, for detention) returns to it, reservoir included | `satin.md §11` L878 | new | `a:evm/execution.rs` | `b:ledger.rs` `pop_child` |  |
| `SATIN-STOP-006` | What the frame counted is discarded with it, but for one case: when a hint the frame admitted filled room a take-back freed, the frame it returns into returns the transaction's data-size stop before running another instruction | `satin.md §11` L879–L881 | new | `a:limit/limit.rs` | `b:ledger.rs` `note_stop`<br>`b:lib.rs` `stop_on_resume` |  |
| `SATIN-STOP-007` | A caller that carries on is held to what the transaction has left, and a crossing of its own stops it in turn | `satin.md §11` L882–L883 | new | `a:limit/limit.rs` | `b:ledger.rs` `hold_check` |  |
| `SATIN-STOP-008` | A caller that catches the stop runs on; a transaction whose frames catch every stop below its own frame can succeed | `satin.md §11` L884 | new | none | none |  |
| `SATIN-STOP-009` | A stop of the transaction's own frame is the transaction's result and settles like an EIP-8037 revert (writes and logs reverted, the first frame's value and record included; the sender pays the intrinsic gas, the body's history, the kept pre-frame charges and what ran; the unspent regular gas and the reservoir return); failed receipt; counts toward the block's counters | `satin.md §11` L885–L887 | new | `a:evm/execution.rs` | `b:tx.rs` `settle_transaction` |  |
| `SATIN-STOP-010` | A deposit whose own frame is stopped settles as a revert, not as a failed deposit | `satin.md §11` L888 | new | `a:evm/execution.rs` | `b:tx.rs` `execute_deposit_inner` |  |
| `SATIN-STOP-011` | A stop of the transaction's own frame does not revert what was applied before the first frame: the sender's nonce and fees; a deposit's mint and created caller with its state gas; the admitted authorizations with their writes, state gas, records and history | `satin.md §11` L890–L894 | new | `a:evm/execution.rs` | `b:tx.rs` `settle_transaction`<br>`b:eip7702.rs` `execute` |  |
| `SATIN-STOP-012` | An Oracle hint a frame admitted stays counted as data size through any stop; a hint that would itself cross is neither forwarded nor counted | `satin.md §11` L896–L897 | new | `a:system/oracle.rs` `intercept` | `b:intercept.rs` `hint_before` |  |
| `SATIN-STOP-013` | A frame whose start crosses a limit is stopped before it runs an instruction, with what its start moved reverted (the value, the transfer log, a created account) | `satin.md §11` L901 | new | `a:evm/execution.rs` | `b:ledger.rs` `draw_first_frame`<br>`b:lib.rs` `StartHooks` |  |
| `SATIN-STOP-014` | A frame answered with a success without running (an account with no code, a precompile that answers) has its answer replaced by the stop on the untouched forward; one answered with a failure is not replaced; a precompile whose price crosses gas detention moves nothing and is held to the price alone, its result the compute stop | `satin.md §11` L902–L904 | new | `a:evm/frame.rs` `synthetic_call_result` | `b:lib.rs` `StartHooks` |  |
| `SATIN-STOP-015` | A stopped creation keeps its creator's nonce bump, whose record is counted on the creator when the creation returns, the creator held to its limits before it runs on | `satin.md §11` L905 | new | `a:evm/execution.rs` `hold_creator` | `b:satin_ext.rs` `hold_caller` |  |
| `SATIN-STOP-016` | A frame answered without running whose answer is rewritten to the stop has what its start moved reverted | `satin.md §11` L906 | new | `a:evm/frame.rs` | `b:detention.rs` `crossing_answer` |  |
| `SATIN-STOP-017` | Nothing counted before the first frame crosses the data-size limit; KV and growth can cross there only on the authorization list, which is then skipped | `satin.md §11` L907–L908 | new | `a:limit/limit.rs` | `b:tx.rs` `adjust_intrinsic_gas` |  |
| `SATIN-STOP-018` | The revert data: kind 0, 1 and 3 carry the crossed frame budget, or the transaction limit when no budget was crossed; kind 2 carries the compute limit of the binding read | `satin.md §11` L912–L920, L923–L925 | new | `a:limit/mod.rs` `MegaLimitExceeded` | `b:ledger.rs` `limit_exceeded_output` |  |
| `SATIN-STOP-019` | The kind discriminants are Rex6's | `satin.md §11` L921 | keeps glossary.md "Call-frame-local exceed" (kind values) | `a:limit/mod.rs` `LimitKind` | `b:ledger.rs` `KIND` |  |
| `SATIN-STOP-020` | Only a limit stop carries MegaLimitExceeded; other refusals carry their own errors (VolatileDataAccessDisabled, the system contracts' and keyless deployment's errors), a call past the depth limit or with an unfundable value fails with empty return data, and a halt has none | `satin.md §11` L922 | new | `a:access/detention.rs` `volatile_data_access_disabled_revert_data` | `b:satin_ext.rs` `disabled_revert` |  |
| `SATIN-STOP-021` | The revert data alone does not identify a stop: the stop of a transaction is the crossing that produced the result of its own frame, which execution reports | `satin.md §11` L926; `satin.md` Node integrators L1533–L1538 | new | `a:evm/result.rs` `limit_stop` | `b:ledger.rs` `Settlement` |  |

### Gas Detention (`satin/evm/gas-detention.md`)

Gas detention on withheld gas: what is volatile, how compute is measured, the limit a read sets, how a frame's regular gas is split into spendable and withheld parts, the crossing, and the precompile and interceptor cases.

Rex pages it draws on: `evm/gas-detention.md`, `evm/compute-gas.md`.

| Id | Rule | Draft | Rex page | Code (a) | Code (b) | Note |
| --- | --- | --- | --- | --- | --- | --- |
| `SATIN-DET-001` | Volatile data: the block environment (NUMBER, TIMESTAMP, COINBASE, PREVRANDAO, GASLIMIT, BASEFEE, BLOBBASEFEE, SLOTNUM, BLOCKHASH); the beneficiary's account through the account opcodes, the call opcodes and the delegate they follow, SELFDESTRUCT at either end, a sender, recipient or delegating recipient, an applied authority or a keyless signer that is the beneficiary; the Oracle's storage through SLOAD in the Oracle's frame | `satin.md §12` L939 | replaces evm/gas-detention.md "Volatile Data Categories" | `a:access/volatile.rs` `VolatileDataAccess`<br>`a:access/mod.rs` | `b:detention.rs` `wrap_table`<br>`b:satin_ext.rs` `access` |  |
| `SATIN-DET-002` | BLOBHASH is not volatile | `satin.md §12` L940 | replaces evm/gas-detention.md "Volatile Data Categories" (BLOBHASH) | `a:access/volatile.rs` | `b:detention.rs` `wrap_table` |  |
| `SATIN-DET-003` | A read is marked where the value is loaded and only once the opcode completed; a load that fails, and a read whose opcode then fails, mark nothing | `satin.md §12` L941 | new | `a:evm/instructions.rs` | `b:detention.rs` `commit_read` |  |
| `SATIN-DET-004` | Every BLOCKHASH is a read of the block environment, whatever its operand | `satin.md §12` L942 | new | `a:evm/instructions.rs` | `b:detention.rs` `Volatile` |  |
| `SATIN-DET-005` | A call to the EIP-2935 history contract is a block-environment read; an SLOAD of the storage the EIP-2935 and EIP-4788 pre-block calls write is not volatile | `satin.md §12` L943 | new | `a:evm/instructions.rs` | `b:detention.rs` `Volatile` |  |
| `SATIN-DET-006` | A CREATE or CREATE2 is never marked as a read nor refused, even with the beneficiary as creator or created address | `satin.md §12` L944 | new | `a:evm/instructions.rs` | `b:lib.rs` `before_account_load` | disagreement: QC-03 |
| `SATIN-DET-007` | A frame running as the beneficiary marks the beneficiary's account by its own SELFBALANCE, SELFDESTRUCT and the other reads | `satin.md §12` L945 | new | `a:evm/instructions.rs` | `b:lib.rs` `mega_selfbalance` |  |
| `SATIN-DET-008` | A transaction whose sender, recipient or applied authority is the beneficiary is detained from its start | `satin.md §12` L939; `satin.md §13` L1032 | new | `a:access/detention.rs` `Detention` | `b:tx.rs` `before_initial_frame`<br>`b:eip7702.rs` `execute` | disagreement: QC-03 |
| `SATIN-DET-009` | Compute is every regular charge the frames make, whoever funds it: the running frame's regular gas spent plus every suspended caller's, each less what it forwarded, less spilled state and history gas, less what halting frames burned | `satin.md §12` L947 | replaces evm/compute-gas.md "Measurement Window" and "Opcode Metering Classes" | `a:access/detention.rs` `regular_spent` | `b:detention.rs` `compute`<br>`b:detention.rs` `regular_spent` |  |
| `SATIN-DET-010` | What a callee runs on a value call's 2,300 stipend counts as compute, and the stipend never lowers compute when it returns | `satin.md §12` L948–L950 | new | `a:access/detention.rs` | `b:detention.rs` `caller_contribution` |  |
| `SATIN-DET-011` | What a halting frame burns is not compute; a precompile that runs out of gas burns its forward without counting it, unless it is the crossing | `satin.md §12` L951–L952 | new | `a:access/detention.rs` | `b:detention.rs` `before_commit` |  |
| `SATIN-DET-012` | A read sets limit = compute_at_read + cap, BLOCK_ENV_ACCESS_COMPUTE_GAS = 20,000,000 for the block environment and the beneficiary, ORACLE_ACCESS_COMPUTE_GAS = 20,000,000 for the Oracle; the limit only goes down | `satin.md §12` L953–L954 | replaces evm/gas-detention.md "Cap Selection" | `a:constants.rs` `BLOCK_ENV_ACCESS_COMPUTE_GAS`<br>`a:constants.rs` `ORACLE_ACCESS_COMPUTE_GAS` | `b:ledger.rs` `Cfg`<br>`b:detention.rs` `DetentionState` | disagreement: QC-02 |
| `SATIN-DET-013` | The caps are protocol values fixed per spec, both below 199,987,900, the most compute a transaction can spend | `satin.md §12` L955–L956 | new | `a:constants.rs` `MAX_TX_COMPUTE_GAS` | `b:ledger.rs` `Cfg` | disagreement: QC-02 |
| `SATIN-DET-014` | Once a limit is set every frame's regular gas is split into a spendable part (limit − compute, or zero) and a withheld part, at the read's completion, at every frame start or resume, and after an SSTORE | `satin.md §12` L957–L959 | replaces evm/gas-detention.md "Execution Semantics" | `a:access/detention.rs` | `b:detention.rs` `hold`<br>`b:detention.rs` `after_sstore`<br>`b:detention.rs` `on_resume` |  |
| `SATIN-DET-015` | Only a regular charge is limited to the spendable part; every other reader of the frame's gas (GAS, the forward and its clamp, the SSTORE minimum-gas check, the cold-load checks, a child's returned gas, the settlement) sees both parts | `satin.md §12` L960–L961, L965 | new | `a:access/detention.rs` | `b:detention.rs` `reserve_for`<br>`evm2:evm/config.rs` `gas_reserve` |  |
| `SATIN-DET-016` | At the settlement the withheld part is unspent gas returned to the sender and not part of the gas used that caps the EIP-3529 refund; a failed deposit returns none of it | `satin.md §12` L962–L963 | replaces evm/gas-detention.md "Refund Semantics" | `a:evm/execution.rs` | `b:tx.rs` `settle_transaction` |  |
| `SATIN-DET-017` | A forward and a spill of state or history gas draw the withheld part first | `satin.md §12` L964 | new | `a:access/detention.rs` | `b:detention.rs` `draw_withheld`<br>`b:detention.rs` `draw_reserve` |  |
| `SATIN-DET-018` | The crossing: a regular charge the spendable part cannot pay but the frame's whole regular gas can is not made, the gas is put back, and the frame is stopped with MegaLimitExceeded(2, limit); what was spent before stays spent; the caller gets back everything the frame had, the withheld part included | `satin.md §12` L966–L968 | new | `a:access/detention.rs` `ComputeStop` | `b:detention.rs` `before_commit`<br>`evm2:interpreter/gas.rs` `record_failed_charge` |  |
| `SATIN-DET-019` | At the crossing the transaction's compute is at most the limit; a caller the stop returns into is held to what the limit leaves; what halting frames burn adds nothing, so compute since a read is at most its cap | `satin.md §12` L969–L971 | new | `a:access/detention.rs` | `b:detention.rs` `on_resume` |  |
| `SATIN-DET-020` | A regular charge beyond the frame's whole regular gas, and every other out-of-gas, halts as without the read | `satin.md §12` L972 | new | `a:access/detention.rs` | `b:detention.rs` `before_commit` |  |
| `SATIN-DET-021` | A precompile call's own regular charges come first; a call forwarded more than the frame's allowance is decided from the precompile's price: within the allowance it runs on its whole forward, past the allowance and within the forward it does not run and is the crossing, past the forward it runs and fails | `satin.md §12` L973–L975; `satin.md §10` L765–L767 | new | `a:evm/precompiles.rs` `PricedPrecompiles` | `b:detention.rs` `hold_precompile`<br>`b:detention.rs` `precompile_price` | disagreement: QC-05 |
| `SATIN-DET-022` | The value has not moved when the price is consulted, so the crossing is kind 2 whatever records the value transfer would have made | `satin.md §12` L976; `satin.md §10` L765 | new | `a:evm/precompiles.rs` | `b:detention.rs` `hold_precompile` |  |
| `SATIN-DET-023` | Every precompile of the Satin set has a price; an input over a size limit is priced at zero | `satin.md §12` L977 | new | `a:evm/precompiles.rs` | `b:detention.rs` `precompile_price`<br>`evm2:precompiles/modexp.rs` | disagreement: QE-01 |
| `SATIN-DET-024` | An input priced between the allowance and the forward that would fail a later check is the crossing too; a call refused on its caller's account runs no precompile and is answered as without the read | `satin.md §12` L978–L979 | new | `a:evm/precompiles.rs` | `b:detention.rs` `hold_precompile` |  |
| `SATIN-DET-025` | A system contract's intercepted answer that spent more regular gas than the allowance is the crossing, and its whole regular spend is the one charge that crossed (none of it billed) | `satin.md §12` L980–L982 | new | `a:system/intercept.rs` | `b:detention.rs` `hold_charge` |  |
| `SATIN-DET-026` | A system-originated transaction and a system call are never detained | `satin.md §12` L985–L986; `satin.md §19` L1256 | replaces evm/gas-detention.md "Transaction Boundary" (exemptions) | `a:access/detention.rs` | `b:ledger.rs` `set_system_originated` |  |
| `SATIN-DET-027` | A precompile a node adds or replaces is outside the Satin set and outside the specification | `satin.md §12` L988–L991; `satin.md` Node integrators L1488–L1490 | new | `a:evm/precompiles.rs` | `b:lib.rs` `precompile_map` | disagreement: QG-04 |

### Halts, Reverts and Stops (`satin/evm/outcomes.md`)

The one rule that decides how a frame and a transaction end under Satin: which crossings revert and can be caught, which endings halt, which transactions are rejected or become failed deposits, and which faults give a transaction no outcome at all.

Rex pages it draws on: `evm/resource-limits.md`, `evm/compute-gas.md`, `evm/gas-detention.md`.

| Id | Rule | Draft | Rex page | Code (a) | Code (b) | Note |
| --- | --- | --- | --- | --- | --- | --- |
| `SATIN-OUT-001` | The outcome classes of a transaction: rejected before inclusion; included as a failed deposit; executed to a success, a revert, a halt or a limit stop of its own frame; or no outcome when the node meets a fault | `satin.md §11` L862–L873; `satin.md §21` L1327–L1360 | replaces evm/resource-limits.md "Outcomes" | `a:evm/result.rs` `MegaTransactionOutcome` | `b:ledger.rs` `Settlement`<br>`op:handler.rs` |  |
| `SATIN-OUT-002` | The revert-or-halt rule: every resource limit and gas detention's compute limit reverts only the frame that crosses it, and its caller can catch the stop; no limit halts a transaction | `satin.md §11` L862, L884 | replaces evm/resource-limits.md "Outcomes"; replaces evm/compute-gas.md "Exceed Behavior" | `a:limit/mod.rs` `MegaLimitExceeded` | `b:ledger.rs` `stop_frame` |  |
| `SATIN-OUT-003` | Exception: initcode over MAX_INITCODE_SIZE (a creation transaction rejected, a creation opcode halting the creating frame, a keyless deployment refused with InitCodeTooLarge) and deployed code over MAX_CONTRACT_SIZE (the creation halts) | `satin.md §11` L866; `satin.md §3` L129–L130; `satin.md §15` L1080 | replaces evm/contract-limits.md (rejection wording) | `a:evm/spec.rs` | `b:lib.rs` `satin_version`<br>`b:keyless.rs` `run` |  |
| `SATIN-OUT-004` | Exception: an OP precompile input over its size limit halts the call before any gas check, consuming its forward | `satin.md §11` L867; `satin.md §2` L115 | new | `a:evm/precompiles.rs` | `op:precompiles.rs` |  |
| `SATIN-OUT-005` | Exception: a failed deposit uses its whole gas limit and reports no stop | `satin.md §11` L868; `satin.md §21` L1338–L1341 | new | `a:evm/execution.rs` | `b:tx.rs` `failed_deposit` |  |
| `SATIN-OUT-006` | Exception: a pre-frame charge the transaction cannot pay runs out of gas without running a frame (a non-deposit is included out of gas; a deposit becomes a failed deposit) | `satin.md §11` L869; `satin.md §5` L322–L326 | new | `a:evm/execution.rs` | `b:tx.rs` `before_initial_frame` |  |
| `SATIN-OUT-007` | A real out-of-gas, a precompile given less than its price, an invalid opcode, and every other exceptional halt of the base layer still halt and consume the frame's gas; a regular charge beyond the frame's whole gas halts even under detention; a creation that cannot pay a code-deposit charge runs out of gas and leaves no code | `satin.md §11` L910; `satin.md §12` L972; `satin.md §1` L70–L71; `satin.md §5` L328–L329 | new | `a:evm/execution.rs` | `evm2:interpreter/gas.rs` |  |
| `SATIN-OUT-008` | A refused volatile read reverts the frame with VolatileDataAccessDisabled(uint8); it is not a limit stop | `satin.md §13` L1007; `satin.md §11` L922 | new | `a:access/detention.rs` `volatile_data_access_disabled_revert_data` | `b:lib.rs` `settle_refusal` |  |
| `SATIN-OUT-009` | A system contract's own refusal (for example NonZeroTransfer() or NotIntercepted()) reverts with its own error and is not a limit stop; a keyless deployment's rule refusal reverts the call (its state and history gas given back, its regular gas spent); an out-of-gas step halts the call | `satin.md §15` L1071–L1072; `satin.md §11` L922 | new | `a:system/keyless/dispatch.rs` | `b:keyless.rs` `run` |  |
| `SATIN-OUT-010` | A call past the call-depth limit, or with a value its caller cannot fund, fails with empty return data and counts nothing | `satin.md §11` L922; `satin.md §10` L781 | new | `a:evm/execution.rs` | `b:lib.rs` `mega_call_impl` |  |
| `SATIN-OUT-011` | A precompile that fails consumes all the gas forwarded to it | `satin.md §2` L115–L117; `satin.md §10` L780 | new | `a:evm/precompiles.rs` | `b:lib.rs` `kzg100k` |  |
| `SATIN-OUT-012` | A creation opcode in a static frame, or short of its operands, halts; under detention the initcode cost and memory a CREATE2 charges before its salt can be the crossing (a revert) where the underflow would halt | `satin.md §3` L131–L133 | new | `a:evm/execution.rs` | `evm2:interpreter/instructions/system.rs` |  |
| `SATIN-OUT-013` | A halt of the transaction's own frame: failed receipt, the unspent regular gas consumed, the reservoir returned; for a deposit a failed deposit | `satin.md §4` L196–L198; `satin.md §11` L888; `satin.md §21` L1341 | new | `a:evm/execution.rs` | `b:tx.rs` `settle_transaction`<br>`op:handler.rs` |  |
| `SATIN-OUT-014` | A revert or a limit stop of the transaction's own frame: failed receipt, the unspent regular gas and the reservoir returned | `satin.md §4` L197; `satin.md §11` L885–L887; `satin.md §21` L1357 | new | `a:evm/execution.rs` | `b:tx.rs` `settle_transaction` |  |
| `SATIN-OUT-015` | A failed bucket-capacity read or database read is never an outcome: the transaction is not settled and the node reports an internal error or an invalid block by the error's cause | `satin.md §21` L1358–L1360; `satin.md §6` L360 | new | `a:block/executor.rs` `MegaBlockExecutionError` | `b:ledger.rs` `SaltBelowMinimum`<br>`b:tx.rs` `host_error` |  |
| `SATIN-OUT-016` | A transaction that fails validation: a non-deposit is rejected; a deposit (a system deposit refused under Regolith and one whose body is over the data-size limit included) is a failed deposit; a Mega System Transaction is a legacy transaction until it passes its own checks | `satin.md §11` L872; `satin.md §21` L1338–L1340 | new | `a:system/tx.rs` `validate_and_promote` | `b:tx.rs` `prepare_legacy` |  |
| `SATIN-OUT-017` | What a tracer is shown for a first frame whose runtime gas phase cannot be paid (one halted root frame, or none) | none | new | none | `b:tx.rs` `settle_first_frame`<br>`b:eip7702.rs` `execute` | undefined: QA-01 |
| `SATIN-OUT-018` | The halt reason named for a failed DUP, DUPN, SWAPN or EXCHANGE | none | new | `a:evm/instructions.rs` | `evm2:interpreter/instructions/stack.rs` `InvalidImmediateEncoding` | undefined: QA-02 |

### EIP-7708 Transfer Logs (`satin/evm/transfer-logs.md`)

The Transfer log every movement of value to another account emits, which movements log nothing, the burns that stay silent, and what a transfer log counts.

| Id | Rule | Draft | Rex page | Code (a) | Code (b) | Note |
| --- | --- | --- | --- | --- | --- | --- |
| `SATIN-LOG-001` | EIP-7708 applies: every movement of value to another account (the transaction's value, a value CALL, a creation's endowment, a SELFDESTRUCT that moves a balance) emits Transfer(address indexed from, address indexed to, uint256 value) from 0xff…fe with topic 0xddf252ad… | `satin.md §14` L1042–L1044 | new | `a:limit/record.rs` `emits_transfer_logs` | `evm2:constants.rs` `EIP7708_TRANSFER_TOPIC`<br>`b:lib.rs` `satin_version` | undefined: QG-02 |
| `SATIN-LOG-002` | The log appears in the receipt in execution order among the contracts' own logs; a failed frame's transfer logs are discarded with its other logs | `satin.md §14` L1045 | new | `a:limit/record.rs` | `evm2:evm/mod.rs` |  |
| `SATIN-LOG-003` | A CALLCODE, a call to the caller itself and a transaction's value sent to its own sender move nothing to another account and emit no log | `satin.md §14` L1046 | new | `a:limit/record.rs` `is_transfer_log` | `b:lib.rs` `count_start` |  |
| `SATIN-LOG-004` | A deposit's value is logged; its mint is not | `satin.md §14` L1047 | new | `a:limit/record.rs` | `op:handler.rs` |  |
| `SATIN-LOG-005` | Only EIP-7708's Transfer log applies: EIP-8246 is not applied, a balance can still be burned, and a burn never logs (a same-transaction account's SELFDESTRUCT to itself; an account destroyed in the transaction removed at its end) | `satin.md §14` L1048–L1049 | new | `a:limit/record.rs` | `b:lib.rs` `mega_selfdestruct` |  |
| `SATIN-LOG-006` | A transfer log is data size, TRANSFER_LOG_SIZE = 160, counted where the value moves (with the frame start that moves it, or with the SELFDESTRUCT); it is not a write record, pays no history gas and draws no history allowance | `satin.md §14` L1050–L1051 | new | `a:limit/mod.rs` `TRANSFER_LOG_SIZE` | `b:ledger.rs` `TRANSFER_LOG_SIZE`<br>`b:ledger.rs` `StartRecords` |  |
| `SATIN-LOG-007` | A frame start the caller's account refuses moves and logs nothing; a creation with an endowment onto an occupied address moves and logs nothing and counts nothing | `satin.md §14` L1052–L1053 | new | `a:limit/record.rs` `start_makes_no_records` | `b:lib.rs` `mega_create_impl` |  |

### Contract Size Limits (`satin/evm/contract-limits.md`)

The deployed-code and initcode size limits, how crossing them ends a creation, and the order in which the creation opcodes make their checks and charges.

Rex pages it draws on: `evm/contract-limits.md`.

| Id | Rule | Draft | Rex page | Code (a) | Code (b) | Note |
| --- | --- | --- | --- | --- | --- | --- |
| `SATIN-SIZE-001` | Deployed code is at most MAX_CONTRACT_SIZE = 524,288 bytes | `satin.md §3` L127 | keeps evm/contract-limits.md (value unchanged) | `a:constants.rs` `MAX_CONTRACT_SIZE` | `b:lib.rs` `satin_version` |  |
| `SATIN-SIZE-002` | Initcode is at most MAX_INITCODE_SIZE = 1,048,576 bytes, twice the code limit | `satin.md §3` L128 | changes evm/contract-limits.md (548,864 bytes under Rex6) | `a:constants.rs` `MAX_INITCODE_SIZE` | `b:lib.rs` `satin_version` |  |
| `SATIN-SIZE-003` | Initcode over the limit halts the creating frame at the creation opcode, deployed code over the limit halts the creation, each consuming the halting frame's gas; neither is a limit stop | `satin.md §3` L129–L130; `satin.md §11` L866 | changes evm/contract-limits.md (halt instead of rejection wording) | `a:evm/spec.rs` | `evm2:interpreter/instructions/system.rs` |  |
| `SATIN-SIZE-004` | A non-deposit creation transaction whose initcode is over the limit is rejected at validation | `satin.md §11` L866 | new | `a:evm/validation.rs` | `evm2:ethereum/mod.rs` |  |
| `SATIN-SIZE-005` | The creation opcodes' check and charge order: the static context; the value, offset and size operands and the size's range; the initcode size; EIP-3860's initcode cost; the offset's range and the memory (neither for empty initcode); for CREATE2 the salt, then 12,000 and the hashing cost; for CREATE 12,000; Satin adds no charge ahead of these | `satin.md §3` L131–L132 | replaces evm/contract-limits.md "Creation-Opcode Halt Ordering" and "Zero-Length Init Code in CREATE2" | `a:evm/execution.rs` | `evm2:interpreter/instructions/system.rs` `create2_pops_its_salt_after_the_init_code_and_memory_charges` |  |
| `SATIN-SIZE-006` | So a creation in a static frame fails before reading operands, and a CREATE2 short of its salt pays the initcode cost and the memory first, which under detention can be the crossing | `satin.md §3` L133 | new | `a:evm/execution.rs` | `evm2:interpreter/instructions/system.rs` |  |

### Precompiles (`satin/evm/precompiles.md`)

The Satin precompile set: Optimism Karst's, with KZG point evaluation at MegaETH's price, and the input size limits the OP specification sets.

Rex pages it draws on: `evm/precompiles.md`.

| Id | Rule | Draft | Rex page | Code (a) | Code (b) | Note |
| --- | --- | --- | --- | --- | --- | --- |
| `SATIN-PCMP-001` | The precompile set is Karst's, with KZG point evaluation (0x0A) at a fixed 100,000 gas; every precompile not listed is as Karst defines it | `satin.md §2` L102–L106, L113 | changes evm/precompiles.md (Isthmus set) | `a:evm/precompiles.rs` `satin_precompiles` | `b:lib.rs` `precompile_map`<br>`op:precompiles.rs` |  |
| `SATIN-PCMP-002` | ModExp (0x05) runs on the Osaka schedule (EIP-7823 and EIP-7883) | `satin.md §2` L107 | keeps evm/precompiles.md (ModExp) | `a:evm/precompiles.rs` | `evm2:precompiles/modexp.rs` |  |
| `SATIN-PCMP-003` | P256VERIFY (0x100) costs 6,900 gas (EIP-7951) | `satin.md §2` L108 | changes evm/precompiles.md (3,450 under Rex6) | `a:evm/precompiles.rs` | `evm2:precompiles/secp256r1.rs` `P256VERIFY_BASE_GAS_FEE_OSAKA` | undefined: QG-02 |
| `SATIN-PCMP-004` | Input limits: BN254 pairing (0x08) 57,600 bytes; BLS12-381 G1 MSM (0x0C) 288,960; G2 MSM (0x0E) 278,784; pairing (0x0F) 156,672 | `satin.md §2` L109–L112 | changes evm/precompiles.md (Isthmus limits) | `a:evm/precompiles.rs` | `op:precompiles.rs` `KARST_MAX_INPUT_SIZE`<br>`op:precompiles.rs` `JOVIAN_G1_MSM_MAX_INPUT_SIZE` |  |
| `SATIN-PCMP-005` | An input over a size limit fails the call before any gas check, a call forwarded no gas included, and consumes the forward | `satin.md §2` L115 | new | `a:evm/precompiles.rs` | `op:precompiles.rs` |  |
| `SATIN-PCMP-006` | KZG point evaluation: a call given less than 100,000 fails with an out-of-gas before any verification; a success is charged exactly 100,000; a failure with at least 100,000 consumes the whole forward | `satin.md §2` L116–L117 | keeps evm/precompiles.md (KZG) | `a:evm/precompiles.rs` `GAS_COST` | `b:lib.rs` `kzg100k` |  |
| `SATIN-PCMP-007` | ModExp's EIP-7823 bound is checked after its 500 minimum price and before its formula price | `satin.md §12` L977 (silent on the order) | new | `a:evm/precompiles.rs` | `evm2:precompiles/modexp.rs` `ModexpEip7823LimitSize` | disagreement: QE-01 |
| `SATIN-PCMP-008` | A call to a precompile address is dispatched and priced by the called address, whatever code that address holds | `satin.md §12` L975 (implied) | new | `a:evm/precompiles.rs` `PricedPrecompiles` | `b:detention.rs` `precompile_price_of` | disagreement: QC-05 |

## System contracts

### System Contracts (`satin/system-contracts/overview.md`)

The registry of MegaETH system contracts under Satin: their addresses, the rule that their bytecode is the Rex-era bytecode, and how they differ from precompiles.

Rex pages it draws on: `system-contracts/overview.md`.

| Id | Rule | Draft | Rex page | Code (a) | Code (b) | Note |
| --- | --- | --- | --- | --- | --- | --- |
| `SATIN-SYSC-001` | Six system contracts at fixed addresses under 0x6342…: the Oracle, the High-Precision Timestamp, KeylessDeploy, MegaAccessControl, MegaLimitControl and the SequencerRegistry | `satin.md §18` L1218; `satin.md §15` L1066 | keeps system-contracts/overview.md "Stable Registry" | `a:system/mod.rs`<br>`a:system/predeploys.rs` `SYSTEM_CONTRACT_ADDRESSES` | `b:ledger.rs` `SEQUENCER_REGISTRY`<br>`b:keyless.rs` `KEYLESS`<br>`b:intercept.rs` `LIMIT_CONTROL`<br>`b:satin_ext.rs` `ACCESS_CONTROL` |  |
| `SATIN-SYSC-002` | Their bytecode and ABI are Rex6's, but for the four errors IKeylessDeploy no longer declares | `satin.md §15` L1131–L1135; `satin.md §13` L1028; `satin.md` Safety and Compatibility L1566 | keeps system-contracts/overview.md "Backward Compatibility Rule" | `a:system/predeploys.rs` `system_contract_specs` | none |  |
| `SATIN-SYSC-003` | Satin deploys, upgrades and seeds no system contract; its activation block checks that they are present | `satin.md §18` L1222–L1228; `satin.md` Node integrators L1523–L1526 | replaces system-contracts/overview.md "Deployment Semantics" | `a:system/predeploys.rs` `check_system_contract` | none | disagreement: QC-01 |
| `SATIN-SYSC-004` | A system contract is an account with code, not a precompile; an intercepted method is answered by the node, everything else runs the contract's bytecode | none | keeps system-contracts/overview.md "Distinction from Precompiles" and "Call Interception" | `a:system/intercept.rs` `intercept` | `b:intercept.rs` `is_intercepted` | undefined: QA-10 |

### Call Interception (`satin/system-contracts/interception.md`)

How the node answers a call to a system contract's intercepted method before a frame is built, what falls through to bytecode, and how an interceptor's answer is settled and detained.

Rex pages it draws on: `system-contracts/interception.md`.

| Id | Rule | Draft | Rex page | Code (a) | Code (b) | Note |
| --- | --- | --- | --- | --- | --- | --- |
| `SATIN-ICPT-001` | A CALL or STATICCALL to a system contract with an interceptor whose selector names an intercepted method is answered before a frame is built; DELEGATECALL, CALLCODE and an unknown selector run the contract's bytecode | `satin.md §16` L1155 | keeps system-contracts/interception.md "Interception Point", "Matching", "Fall-Through to Bytecode" | `a:system/intercept.rs` `intercept`<br>`a:system/intercept.rs` `peek_selector` | `b:intercept.rs` `is_intercepted` |  |
| `SATIN-ICPT-002` | The interceptors' call-depth gate | none | keeps system-contracts/interception.md "Call-Depth Gate" | `a:system/intercept.rs` | `b:intercept.rs` `answer_before` | undefined: QA-10 |
| `SATIN-ICPT-003` | An intercepted MegaAccessControl or MegaLimitControl method carrying value reverts with NonZeroTransfer() | none | keeps system-contracts/interception.md "Interception Outcomes" | `a:system/intercept.rs` `reject_non_zero_transfer` | `b:intercept.rs` `non_zero_transfer` | undefined: QA-10 |
| `SATIN-ICPT-004` | An interceptor's answer returns to the caller as a frame's result on the gas the caller forwarded, its reservoir share returned by the child-merge rule | `satin.md §4` L148, L192 | keeps system-contracts/interception.md "Gas Semantics" | `a:evm/frame.rs` `synthetic_call_result` | `b:lib.rs` `StartHooks` |  |
| `SATIN-ICPT-005` | Under gas detention an answer whose regular spend exceeds the frame's allowance is the crossing, none of it billed | `satin.md §12` L980–L982 | new | `a:system/intercept.rs` | `b:detention.rs` `hold_charge` |  |
| `SATIN-ICPT-006` | KeylessDeploy is recognized by depth, scheme, target and selector, whatever code the state holds at its address | `satin.md §15` L1066–L1067 | replaces system-contracts/interception.md (keyless as an interceptor) | `a:system/keyless/dispatch.rs` `is_dispatched` | `b:keyless.rs` `is_dispatched` |  |

### Oracle (`satin/system-contracts/oracle.md`)

The Oracle under Satin: how an SLOAD in its own frame answers from the oracle service, what such a read costs, and when a sendHint reaches the service and what it counts.

Rex pages it draws on: `system-contracts/oracle.md`.

| Id | Rule | Draft | Rex page | Code (a) | Code (b) | Note |
| --- | --- | --- | --- | --- | --- | --- |
| `SATIN-ORCL-001` | Address 0x6342…0001, version 2.0.0 bytecode; its read, restricted-write and auxiliary interfaces and its storage layout are Rex6's | `satin.md §18` L1223; `satin.md §17` L1188 | keeps system-contracts/oracle.md "Address", "Bytecode", "Public Read Interface", "Restricted Write Interface", "Auxiliary Interface", "Versioning" | `a:system/oracle.rs` `ORACLE_CONTRACT_ADDRESS` | `b:ledger.rs` `ORACLE`<br>`b:tx.rs` `ORACLE` |  |
| `SATIN-ORCL-002` | An SLOAD in the Oracle's own frame loads the slot, then asks the oracle service; the service's value wins over whatever the slot holds, the frame's own earlier write included; with no value the slot's present value answers | `satin.md §16` L1146–L1147 | replaces system-contracts/oracle.md "Storage Access Semantics" | `a:external/oracle.rs`<br>`a:evm/host.rs` | `b:lib.rs` `mega_sload` |  |
| `SATIN-ORCL-003` | Every such read is charged as a cold access (2,100), however often the slot was read, and the slot is loaded whichever source answers | `satin.md §16` L1148 | replaces system-contracts/oracle.md "Gas and Detention Semantics" | `a:evm/host.rs` | `b:lib.rs` `mega_sload` |  |
| `SATIN-ORCL-004` | A frame whose regular gas, withheld part included, cannot pay the cold access reads and asks nothing; a refused read asks nothing | `satin.md §16` L1149 | new | `a:evm/host.rs` | `b:lib.rs` `mega_sload` |  |
| `SATIN-ORCL-005` | A system call never asks the service: its read answers the chain's value and records no answer; a Mega System Transaction still asks | `satin.md §16` L1150; `satin.md §18` L1230–L1232 | new | `a:evm/host.rs` | `b:ledger.rs` `begin_system_call`<br>`b:lib.rs` `mega_sload` |  |
| `SATIN-ORCL-006` | A sendHint reaches the service synchronously only when forwarded gas, carrying no value, from a frame whose volatile-data access is on; otherwise it is dropped and counts nothing; the call runs the Oracle's bytecode either way | `satin.md §16` L1151–L1153 | replaces system-contracts/oracle.md "Hint Forwarding" | `a:system/oracle.rs` `intercept` | `b:intercept.rs` `hint_before`<br>`b:satin_ext.rs` `is_send_hint` |  |
| `SATIN-ORCL-007` | The service is handed the hint's topic, its data and the address of the calling frame (the sender for a sendHint that is the transaction's own call) | `satin.md §16` L1154 | new | `a:system/oracle.rs` `intercept` | `b:satin_ext.rs` `decode_hint` |  |
| `SATIN-ORCL-008` | Only a CALL or STATICCALL to the Oracle is a sendHint; a CALLCODE or DELEGATECALL of the method reaches no service and counts nothing | `satin.md §16` L1155 | new | `a:system/intercept.rs` `intercept` | `b:intercept.rs` `is_intercepted` |  |
| `SATIN-ORCL-009` | An admitted hint counts the call's whole input length as data size on the transaction, before decoding, and pays no history; a top-level sendHint counts its input twice; the count stays whatever happens afterwards, an undecodable input included | `satin.md §16` L1156–L1159; `satin.md §11` L896 | new | `a:system/oracle.rs` `intercept` | `b:intercept.rs` `hint_before` |  |
| `SATIN-ORCL-010` | A hint whose length would take the transaction over its data-size limit is neither forwarded nor counted and the call is answered with the stop without running bytecode; the block counts none of its bytes; the check is against the transaction limit alone | `satin.md §16` L1160–L1163 | new | `a:system/oracle.rs` `intercept` | `b:intercept.rs` `hint_before` |  |
| `SATIN-ORCL-011` | The Oracle authorizes writes on the sender alone, so no transaction from the system address other than a Mega System Transaction reaches it | `satin.md §17` L1188 | keeps system-contracts/oracle.md "Restricted Write Interface" | `a:system/oracle.rs` | none |  |

### High-Precision Timestamp (`satin/system-contracts/high-precision-timestamp.md`)

The High-Precision Timestamp contract, unchanged from the Rex era: its address, interface and storage layout, whose reads follow the Satin Oracle and detention rules.

Rex pages it draws on: `system-contracts/high-precision-timestamp.md`.

| Id | Rule | Draft | Rex page | Code (a) | Code (b) | Note |
| --- | --- | --- | --- | --- | --- | --- |
| `SATIN-HPTS-001` | Address, interface, storage layout and service semantics as under Rex6; bytecode unchanged | `satin.md §18` L1218, L1223; `satin.md` Safety and Compatibility L1566 | keeps system-contracts/high-precision-timestamp.md (whole page) | `a:system/timestamp.rs` | none |  |
| `SATIN-HPTS-002` | Its reads of the Oracle's storage are Oracle reads under the Satin rules (service answer, cold price, detention) | `satin.md §16` L1146–L1148; `satin.md §12` L939 | new | `a:system/timestamp.rs` | `b:lib.rs` `mega_sload` | undefined: QA-10 |

### KeylessDeploy (`satin/system-contracts/keyless-deploy.md`)

Keyless deployment (Nick's method) as a native creation: which calls are deployments, the fifteen steps the call makes, the creation it starts, the signer's nonce rule, the answer, and what a limit does to a deployment.

Rex pages it draws on: `system-contracts/keyless-deploy.md`.

| Id | Rule | Draft | Rex page | Code (a) | Code (b) | Note |
| --- | --- | --- | --- | --- | --- | --- |
| `SATIN-KEY-001` | Address 0x6342…0003; bytecode and code hash unchanged; the interface declares the errors without the four removed | `satin.md §15` L1066, L1131–L1135 | changes system-contracts/keyless-deploy.md "Address", "Bytecode", "Interface" | `a:system/keyless/mod.rs`<br>`a:system/keyless/error.rs` | `b:keyless.rs` `KEYLESS` |  |
| `SATIN-KEY-002` | A keylessDeploy(bytes,uint256) call that is the transaction's own frame (depth 0, CALL, the address, the selector) deploys the carried creation as an ordinary creation frame, a child of the call, whatever code the state holds there | `satin.md §15` L1066–L1067 | replaces system-contracts/keyless-deploy.md "Interception Scope" and "Sandbox Execution Model" | `a:system/keyless/dispatch.rs` `is_dispatched` | `b:keyless.rs` `is_dispatched`<br>`b:keyless.rs` `mega_keyless` |  |
| `SATIN-KEY-003` | A keylessDeploy call a contract makes runs the bytecode: NotIntercepted() without value, an empty revert with value | `satin.md §15` L1068 | new | `a:system/keyless/dispatch.rs` | `b:keyless.rs` `before` |  |
| `SATIN-KEY-004` | A rule's refusal reverts the call with its error (state and history gas given back, regular gas spent); an out-of-gas step halts the call | `satin.md §15` L1070–L1072 | new | `a:system/keyless/dispatch.rs` `ready` | `b:keyless.rs` `run` |  |
| `SATIN-KEY-005` | The fifteen steps in order (100,000 overhead; no value; decoding; nonce 0; initcode size; gasLimitOverride covers the signed limit; recovery with a low or high s; signer nonce at most 1; EIP-3607 unless disabled; an empty signer's state gas; the forward covers; no code at the deploy address; balance covers the value; CREATE's charges and records; the forward still covers) | `satin.md §15` L1074–L1090 | replaces system-contracts/keyless-deploy.md "Accepted Inner Transaction Format", "Validation Rules", "Deploy-Address Occupancy Read" | `a:system/keyless/dispatch.rs` `ready`<br>`a:system/keyless/tx.rs`<br>`a:system/keyless/mod.rs` `KEYLESS_DEPLOY_OVERHEAD_GAS` | `b:keyless.rs` `run`<br>`b:keyless.rs` `OVERHEAD` | disagreement: QC-04 |
| `SATIN-KEY-006` | Steps 1 to 13 keep Rex6's order, so a call several rules refuse reports the Rex6 error | `satin.md §15` L1092 | keeps system-contracts/keyless-deploy.md "Validation Rules" (order) | `a:system/keyless/dispatch.rs` | `b:keyless.rs` `run` |  |
| `SATIN-KEY-007` | The signer and deploy-address reads load the accounts warm (the deploy address without its code), uncharged; no charge depends on their warmth | `satin.md §15` L1093–L1094 | new | `a:system/keyless/dispatch.rs` | `b:keyless.rs` `run` |  |
| `SATIN-KEY-008` | Step 12 checks code alone: an address holding a nonce but no code passes, and the creation then collides there and fails (ExecutionHalted) | `satin.md §15` L1095–L1096 | new | `a:system/keyless/dispatch.rs` | `b:keyless.rs` `run` |  |
| `SATIN-KEY-009` | A creation at the deploy address that returns empty code is refused its empty deposit and reverts (EmptyCodeDeployed), as is a constructor that destroyed its own account | `satin.md §15` L1097–L1101, L1117 | new | `a:system/keyless/settle.rs` `refuses_empty_deposit` | `b:keyless.rs` `refuses_empty_deposit` |  |
| `SATIN-KEY-010` | A signer that is the beneficiary is detained at the signer read, after step 7 and before step 8, with the call's 100,000 as the read's compute | `satin.md §15` L1102 | new | `a:system/keyless/dispatch.rs` | `b:keyless.rs` `run` |  |
| `SATIN-KEY-011` | The creation starts by the signer at the deploy address one level below the call, forwarding min(gasLimitOverride, remaining gas) with the withheld part drawn first and no 98/100 cap, the reservoir share of what step 14 left and the child share of the three budgets; ORIGIN and GASPRICE are the transaction's own | `satin.md §15` L1103–L1109; `satin.md §9` L493–L494 | replaces system-contracts/keyless-deploy.md "Sandbox Execution Model" and "State Merge Semantics" | `a:system/keyless/dispatch.rs` `start` | `b:keyless.rs` `run` |  |
| `SATIN-KEY-012` | The signer's nonce record, and its growth when the bump creates the signer, are counted on the call at its settlement | `satin.md §15` L1107 | new | `a:system/keyless/settle.rs` `settle` | `b:keyless.rs` `run` |  |
| `SATIN-KEY-013` | The signer's nonce: from 0 the bump stays; from 1, when the creation's bump is the last nonce change, it is taken back whether the deployment succeeded or failed, the record counted after and its history given back when none stands; a signer whose own code spent a nonce keeps every bump | `satin.md §15` L1110–L1115 | new | `a:system/keyless/settle.rs` `settle` | `b:keyless.rs` `run` |  |
| `SATIN-KEY-014` | The answer (gasUsed, deployedAddress, errorData): the deploy address and empty errorData when it holds code afterwards; otherwise the zero address and ExecutionReverted, ExecutionHalted or EmptyCodeDeployed | `satin.md §15` L1116–L1117 | replaces system-contracts/keyless-deploy.md "Result Semantics" and "Error Classes" | `a:system/keyless/settle.rs` `answer` | `b:keyless.rs` `return_with` |  |
| `SATIN-KEY-015` | gasUsed is what the creation spent from both pools, no intrinsic gas, before the EIP-3529 refund, net of every give-back inside it; the call's own charges of steps 1 and 14 are not in it; never less than the regular gas the creation spent | `satin.md §15` L1118–L1119 | replaces system-contracts/keyless-deploy.md "Result Semantics" (gasUsed) | `a:system/keyless/settle.rs` `answer` | `b:keyless.rs` `run` |  |
| `SATIN-KEY-016` | A limit the creation crosses stops the creation and the call answers ExecutionReverted with the stop's data; a limit the call's own charges or the signer's nonce record cross stops the call, taking the deployment back; that stop is the transaction's | `satin.md §15` L1120–L1130 | new | `a:system/keyless/settle.rs` `settle` | `b:keyless.rs` `run` |  |
| `SATIN-KEY-017` | The four Rex-era errors are not declared and never produced; AddressMismatch() and NoContractCreated() remain as unreachable answers | `satin.md §15` L1131–L1134 | changes system-contracts/keyless-deploy.md "Error Classes" | `a:system/keyless/error.rs` | `b:keyless.rs` `err` |  |
| `SATIN-KEY-018` | With value, the 100,000 overhead is decided under detention first (a crossing stops the call with none of it billed), then NoEtherTransfer() is answered before anything moves | `satin.md §15` L1076–L1077; `satin.md §12` L981–L982 | new | `a:system/keyless/dispatch.rs` | `b:keyless.rs` `before`<br>`b:detention.rs` `hold_charge` |  |

### MegaAccessControl (`satin/system-contracts/mega-access-control.md`)

Switching volatile-data access off for a call subtree under Satin: where a read is refused, what a refused read pays, and the access types its error carries.

Rex pages it draws on: `system-contracts/mega-access-control.md`.

| Id | Rule | Draft | Rex page | Code (a) | Code (b) | Note |
| --- | --- | --- | --- | --- | --- | --- |
| `SATIN-MAC-001` | Address 0x6342…0004; interface, errors and the scope of disableVolatileDataAccess(), enableVolatileDataAccess() and isVolatileDataAccessDisabled() unchanged; bytecode unchanged | `satin.md §13` L1002, L1028 | keeps system-contracts/mega-access-control.md "Address", "Bytecode", "Interface", "Interception Scope", "Execution-Local Policy State", "Value Transfer Policy", "Lifetime" | `a:system/control.rs` `ACCESS_CONTROL_ADDRESS` | `b:satin_ext.rs` `ACCESS_CONTROL`<br>`b:satin_ext.rs` `access_control_answer` |  |
| `SATIN-MAC-002` | disableVolatileDataAccess() switches access off once its answer is settled; an answer detention turns into the compute stop leaves the switch as it was | `satin.md §13` L1003 | changes system-contracts/mega-access-control.md "disableVolatileDataAccess" | `a:access/detention.rs` `disable_access` | `b:satin_ext.rs` `access_control_answer` |  |
| `SATIN-MAC-003` | A read is refused where the opcode loads the value, after its operands (an opcode failing on its operands fails as with access on); a read on a full stack is refused rather than overflowing; BLOCKHASH is refused as BLOCKHASH (7) whatever its operand | `satin.md §13` L1004–L1006 | new | `a:evm/instructions.rs` | `b:lib.rs` `refuses_load`<br>`evm2:interpreter/instructions/account_load.rs` |  |
| `SATIN-MAC-004` | A refused read reverts the frame with VolatileDataAccessDisabled(accessType) on the gas it had after the opcode's static gas (2, 5, 20, 100, 200 or 5,000 by opcode); what it charged after the static gas and before the load is given back | `satin.md §13` L1007–L1009 | new | `a:access/detention.rs` `volatile_data_access_disabled_revert_data` | `b:lib.rs` `refusal_gas`<br>`b:lib.rs` `settle_refusal` |  |
| `SATIN-MAC-005` | The accessType values (0 NUMBER, 1 TIMESTAMP, 2 COINBASE, 4 GASLIMIT, 5 BASEFEE, 6 PREVRANDAO, 7 BLOCKHASH, 8 BLOBBASEFEE, 10 beneficiary, 11 Oracle, 12 SLOTNUM), ABI-encoded as uint8; 3 and 9 never produced; 12 outside the contract's enum | `satin.md §13` L1010–L1027 | new | `a:access/volatile.rs` `VolatileDataAccess`<br>`a:system/control.rs` `SLOT_NUM_ACCESS_TYPE` | `b:satin_ext.rs` `access` |  |
| `SATIN-MAC-006` | A CREATE or CREATE2 is not refused in a frame whose access is off | `satin.md §12` L944 | new | `a:evm/instructions.rs` | `b:lib.rs` `before_account_load` |  |
| `SATIN-MAC-007` | A call's EIP-7702 delegate that is the beneficiary is refused at its own load | `satin.md §12` L939 | new | `a:evm/instructions.rs` | `b:lib.rs` `mega_call_impl` |  |

### MegaLimitControl (`satin/system-contracts/mega-limit-control.md`)

The remainingComputeGas() query under Satin: what it answers once compute is regular gas and detention withholds gas.

Rex pages it draws on: `system-contracts/mega-limit-control.md`.

| Id | Rule | Draft | Rex page | Code (a) | Code (b) | Note |
| --- | --- | --- | --- | --- | --- | --- |
| `SATIN-MLC-001` | Address 0x6342…0005, interface, bytecode, interception scope and value policy unchanged | `satin.md §13` L1028 | keeps system-contracts/mega-limit-control.md "Address", "Bytecode", "Interface", "Interception Scope", "Value Transfer Policy" | `a:system/limit_control.rs` `LIMIT_CONTROL_ADDRESS` | `b:intercept.rs` `LIMIT_CONTROL` | undefined: QA-10 |
| `SATIN-MLC-002` | remainingComputeGas() answers the lesser of the calling frame's own regular gas with the gas the call forwarded counted back, and, once a read set a limit, what the limit leaves the transaction, read when the call reaches the interceptor | `satin.md §13` L1030 | replaces system-contracts/mega-limit-control.md "remainingComputeGas" | `a:system/limit_control.rs` `intercept` | `b:intercept.rs` `remaining_compute_gas` |  |
| `SATIN-MLC-003` | The answer is regular gas only; the reservoir is not in it | `satin.md §13` L1031 | new | `a:system/limit_control.rs` | `b:intercept.rs` `remaining_compute_gas` |  |
| `SATIN-MLC-004` | A transaction that calls the contract directly hears its own frame's regular gas, or less when detained from its start | `satin.md §13` L1032 | new | `a:system/limit_control.rs` | `b:intercept.rs` `remaining_compute_gas` |  |

### SequencerRegistry (`satin/system-contracts/sequencer-registry.md`)

The SequencerRegistry under Satin: the Rex-era contract, read by every transaction for the live system address, its role changes applied by the pre-block step.

Rex pages it draws on: `system-contracts/sequencer-registry.md`, `system-contracts/system-tx.md`.

| Id | Rule | Draft | Rex page | Code (a) | Code (b) | Note |
| --- | --- | --- | --- | --- | --- | --- |
| `SATIN-REG-001` | Address 0x6342…0006, version 2.0.0 bytecode, storage layout, interface, read methods, change scheduling, two-step admin transfer, no interception: Rex6's | `satin.md §17` L1178; `satin.md §18` L1223 | keeps system-contracts/sequencer-registry.md "Address", "Bytecode", "Storage Layout", "Interface", "Read Methods", "Change Scheduling", "Two-Step Admin Transfer", "Interception" | `a:system/sequencer_registry.rs` `SEQUENCER_REGISTRY_ADDRESS` | `b:ledger.rs` `SEQUENCER_REGISTRY`<br>`b:tx.rs` `SEQUENCER_REGISTRY_CODE_HASH` |  |
| `SATIN-REG-002` | Every transaction reads the registry when validated: its account and, from the transaction's own state, its _currentSystemAddress slot; with the version 2.0.0 code hash and a non-zero slot the slot names the live system address; the code is compared by hash, never loaded or run | `satin.md §17` L1177–L1179 | replaces system-contracts/system-tx.md "Resolution" | `a:system/sequencer_registry.rs` `live_system_address`<br>`a:system/sequencer_registry.rs` `load_system_address` | `b:tx.rs` `read_registry`<br>`b:tx.rs` `live_system_address` |  |
| `SATIN-REG-003` | The account and the slot are warm for the rest of the transaction; the read is not charged, writes nothing, and lands in the transaction's returned state | `satin.md §17` L1180–L1182 | new | `a:system/sequencer_registry.rs` | `b:tx.rs` `read_registry` |  |
| `SATIN-REG-004` | An absent registry, other code, or a zero slot names no live system address | `satin.md §17` L1184–L1185 | new | `a:system/sequencer_registry.rs` `live_system_address` | `b:tx.rs` `live_system_address` |  |
| `SATIN-REG-005` | A role change is scheduled for a later block only and applied by that block's pre-block call; an applyPendingChanges() inside a block finds nothing due | `satin.md §17` L1192 | keeps system-contracts/sequencer-registry.md "Change Scheduling" and "Pre-Block Apply" | `a:system/sequencer_registry.rs` `transact_apply_pending_changes` | `b:block.rs` `registry_due` |  |
| `SATIN-REG-006` | The registry's roles are what it holds, seeded by the legacy forks; Satin reads none of their configuration keys | `satin.md` Node integrators L1526 | replaces system-contracts/sequencer-registry.md "Deploy-Time Seeding" | `a:block/genesis.rs` | none |  |
| `SATIN-REG-007` | A registry read the node fails to make gives the transaction no outcome | `satin.md §17` L1193 | new | `a:system/sequencer_registry.rs` | `b:tx.rs` `host_error` |  |

### Mega System Transactions and the Protocol's Own Transactions (`satin/system-contracts/system-tx.md`)

Which transactions are Mega System Transactions, how one is validated and promoted to a deposit, which transactions are system-originated, and what that exempts them from.

Rex pages it draws on: `system-contracts/system-tx.md`.

| Id | Rule | Draft | Rex page | Code (a) | Code (b) | Note |
| --- | --- | --- | --- | --- | --- | --- |
| `SATIN-MST-001` | The system shape is tested on the transaction's own fields: type 0x0, a call (not a creation) to an address on MEGA_SYSTEM_TX_WHITELIST (the Oracle) | `satin.md §17` L1176 | replaces system-contracts/system-tx.md "Identification" and "Stable Whitelist" | `a:system/tx.rs` `has_system_transaction_shape`<br>`a:system/tx.rs` `MEGA_SYSTEM_TX_WHITELIST` | `b:tx.rs` `classify`<br>`b:block.rs` `is_system_transaction` |  |
| `SATIN-MST-002` | A transaction of the system shape whose caller is the live system address is a Mega System Transaction | `satin.md §17` L1183 | new | `a:system/tx.rs` `classify_system_transaction` | `b:tx.rs` `classify` |  |
| `SATIN-MST-003` | A transaction from the live system address without the system shape is invalid, whatever its type: a non-deposit is rejected, a deposit is a failed deposit (one carrying the promotion's source hash included) | `satin.md §17` L1186–L1187; `satin.md §21` L1332 | new | `a:system/tx.rs` `SYSTEM_ADDRESS_WITHOUT_SYSTEM_SHAPE` | `b:tx.rs` `SYSTEM_ADDRESS_WITHOUT_SYSTEM_SHAPE` |  |
| `SATIN-MST-004` | A transaction from any other address, a retired system address included, is an ordinary transaction | `satin.md §17` L1189 | new | `a:system/tx.rs` | `b:tx.rs` `classify` |  |
| `SATIN-MST-005` | A Mega System Transaction is validated before promotion, a failure being a rejection: it carries the chain's id, its nonce is the system address's, and the system address has no code (EIP-3607); it then executes as a deposit | `satin.md §17` L1190–L1191; `satin.md §21` L1335, L1340 | replaces system-contracts/system-tx.md "Processing Semantics" | `a:system/tx.rs` `validate_and_promote` | `b:tx.rs` `prepare_legacy`<br>`b:tx.rs` `check_system_sender` |  |
| `SATIN-MST-006` | The promotion stamps the source hash keccak256("MEGA_SYSTEM_TRANSACTION") | `satin.md §19` L1247 | new | `a:system/tx.rs` `MEGA_SYSTEM_TRANSACTION_SOURCE_HASH` | `b:tx.rs` `MEGA_SYSTEM_TRANSACTION_SOURCE_HASH` |  |
| `SATIN-MST-007` | A transaction is system-originated when it is a Mega System Transaction before or after promotion, when its caller is 0xff…fe, or when it is a deposit carrying the promotion's source hash, decided from its own fields wherever it is executed | `satin.md §19` L1247–L1249 | replaces system-contracts/system-tx.md "System-Originated Transaction Metering Exemption" | `a:system/tx.rs` `is_system_originated`<br>`a:system/tx.rs` `originates_from_the_protocol` | `b:ledger.rs` `set_system_originated` |  |
| `SATIN-MST-008` | A system-originated transaction and every system call are priced at m = 1 without reading a bucket, pay no history gas, are stopped by no per-transaction limit or frame budget, are not detained, and still have their usage counted | `satin.md §19` L1251–L1257 | new | `a:evm/context.rs` `is_system_originated` | `b:ledger.rs` `set_system_originated`<br>`b:ledger.rs` `begin_system_call` |  |
| `SATIN-MST-009` | A system-originated transaction's usage is reported and counts toward the block's counters; the pre-block calls count toward neither the counters nor the limits | `satin.md §19` L1259 | new | `a:block/executor.rs` | `b:block.rs` `commit_transaction_outcome` |  |
| `SATIN-MST-010` | A user's deposit is not system-originated | `satin.md §19` L1261 | new | `a:system/tx.rs` `is_system_originated` | `b:tx.rs` `prepare_deposit` |  |

## Transactions and blocks

### Satin Transactions and Blocks Overview (`satin/block/overview.md`)

An index of the Satin pages on transaction validation, deposits, the pre-block system calls, the block's limits, the stateless witness and activation.

Rex pages it draws on: `evm/resource-limits.md`.

An index page: it summarizes and links the pages of its group and specifies no rule of its own.

### Transaction Validation and Refusals (`satin/block/transaction-validation.md`)

The checks a transaction is held to before inclusion, their order and the error each names, the chain-id rule, and what a pool can check without state.

Rex pages it draws on: `evm/resource-limits.md`, `evm/dual-gas-model.md`, `upgrades/rex5.md`.

| Id | Rule | Draft | Rex page | Code (a) | Code (b) | Note |
| --- | --- | --- | --- | --- | --- | --- |
| `SATIN-VAL-001` | A transaction is rejected when its body, with WRITE_RECORD_SIZE bytes for every authorization entry (applied or not), exceeds the transaction data-size limit, unless it is system-originated | `satin.md §4` L211–L212; `satin.md §21` L1329 | replaces evm/resource-limits.md "Pre-Execution Limits" | `a:limit/mod.rs` `TX_BODY_OVER_DATA_SIZE_LIMIT`<br>`a:evm/validation.rs` | `b:tx.rs` `adjust_intrinsic_gas` |  |
| `SATIN-VAL-002` | A transaction is rejected when its gas limit is below its intrinsic regular gas plus its body's history gas (CallGasCostMoreThanGasLimit), when its floor exceeds its gas limit (GasFloorMoreThanGasLimit), or when its gas limit exceeds EXECUTION_CAP while its intrinsic regular gas or floor exceeds the cap (GasFloorMoreThanGasLimit) | `satin.md §4` L213–L215; `satin.md §21` L1330–L1331 | replaces upgrades/rex5.md "14. Final Mega-Side Gas Validation Ordering" | `a:evm/validation.rs` `IntrinsicGas` | `b:tx.rs` `adjust_intrinsic_gas` |  |
| `SATIN-VAL-003` | The checks' order, the first failure naming the error: the body against the data-size limit before any gas; the gas limit against the intrinsic regular gas alone; the floor; the execution cap; the gas limit against the intrinsic regular gas plus the body's history | `satin.md §4` L217–L218 | new | `a:evm/validation.rs` `validate_transaction_stateless` | `b:tx.rs` `adjust_intrinsic_gas` | undefined: QA-03 |
| `SATIN-VAL-004` | A transaction that passes validation cannot cross the data-size limit before its first frame | `satin.md §4` L220–L221 | new | `a:limit/limit.rs` | `b:tx.rs` `adjust_intrinsic_gas` |  |
| `SATIN-VAL-005` | A transaction is rejected when sent from the live system address without the system shape | `satin.md §21` L1332; `satin.md §17` L1186 | new | `a:system/tx.rs` `SYSTEM_ADDRESS_WITHOUT_SYSTEM_SHAPE` | `b:tx.rs` `SYSTEM_ADDRESS_WITHOUT_SYSTEM_SHAPE` |  |
| `SATIN-VAL-006` | A transaction is rejected when it carries a chain id that is not the chain's, or is a typed transaction without one; a legacy transaction without a chain id is valid unless it is a Mega System Transaction; the check holds whatever the node's configuration says | `satin.md §21` L1333–L1334 | replaces upgrades/rex5.md "13. System Transaction Chain-Id and Nonce Validation" | `a:evm/validation.rs` | `b:lib.rs` `satin_version` |  |
| `SATIN-VAL-007` | A transaction is rejected when it is a Mega System Transaction failing the chain-id, nonce or EIP-3607 check, or when it fails any inherited validation | `satin.md §21` L1335–L1336 | new | `a:system/tx.rs` `validate_and_promote` | `b:tx.rs` `check_system_sender` | undefined: QA-03 |
| `SATIN-VAL-008` | A deposit is never rejected for a validation failure: it is included as a failed deposit; a read the node fails to make is not a validation check | `satin.md §21` L1338–L1339; `satin.md §4` L219 | new | `a:evm/execution.rs` | `b:tx.rs` `prepare_deposit` |  |
| `SATIN-VAL-009` | What a transaction pool can decide without state, and what it cannot (whether a recipient, created account or authority is new; the start records' history) | `satin.md` Node integrators L1491–L1505 | new | `a:evm/validation.rs` `validate_transaction_stateless` | none | disagreement: QG-05 |

### Deposit Transactions (`satin/block/deposits.md`)

Deposits under Satin: what they pay and are held to, the account a deposit creates for its caller, when a deposit becomes a failed deposit and what a failed deposit keeps.

Rex pages it draws on: `system-contracts/system-tx.md`, `upgrades/rex5.md`.

| Id | Rule | Draft | Rex page | Code (a) | Code (b) | Note |
| --- | --- | --- | --- | --- | --- | --- |
| `SATIN-DEP-001` | A deposit pays no history gas, its body, calldata and deposited code included | `satin.md §7` L442–L444; `satin.md §19` L1261 | new | `a:evm/context.rs` `prices_history` | `b:tx.rs` `prepare_deposit` |  |
| `SATIN-DEP-002` | A deposit that is not system-originated is priced by bucket, held to every per-transaction limit and frame budget, and detained | `satin.md §7` L444; `satin.md §6` L368; `satin.md §19` L1261 | new | `a:evm/context.rs` | `b:tx.rs` `prepare_deposit_inner` |  |
| `SATIN-DEP-003` | A deposit-like transaction whose caller does not exist is charged that account's new-account state gas exactly once, before the first frame; the account is always created and kept and is one unit of state growth | `satin.md §5` L321; `satin.md §10` L628, L838–L839 | replaces upgrades/rex5.md "17. Deposit Caller New-Account Accounting" | `a:evm/execution.rs` | `b:tx.rs` `prepare_deposit_inner` |  |
| `SATIN-DEP-004` | A deposit that fails a validation check, cannot pay a charge made before its first frame, or whose own frame halts is a failed deposit: its sender's nonce is bumped, its mint credited, its whole gas limit (reservoir included) used, and nothing else applied | `satin.md §21` L1338, L1341; `satin.md §4` L198; `satin.md §5` L326; `satin.md §11` L888 | new | `a:evm/execution.rs` | `b:tx.rs` `failed_deposit`<br>`op:handler.rs` |  |
| `SATIN-DEP-005` | A failed deposit reports its whole gas limit as regular gas and no state or history gas on any ledger; its created caller carries no state gas and counts one unit of growth on the transaction and the block | `satin.md §21` L1341–L1342; `satin.md §10` L755–L757 | new | `a:evm/result.rs` | `b:tx.rs` `failed_deposit` |  |
| `SATIN-DEP-006` | A failed deposit keeps the data size of its body and of the hints it admitted, and returns no withheld gas, unspent gas or reservoir | `satin.md §10` L541; `satin.md §11` L873; `satin.md §12` L963; `satin.md §4` L198 | new | `a:limit/limit.rs` | `b:tx.rs` `failed_deposit` |  |
| `SATIN-DEP-007` | A deposit that succeeds, reverts or is stopped by a limit settles as an ordinary transaction (a stop is a revert, not a failed deposit) | `satin.md §4` L198; `satin.md §11` L888 | new | `a:evm/execution.rs` | `b:tx.rs` `execute_deposit_inner` |  |
| `SATIN-DEP-008` | A deposit from the live system address, and one handed to the node already carrying the promotion's source hash, is a failed deposit; a system deposit is refused under Regolith and fails | `satin.md §17` L1186–L1187; `satin.md §11` L872; `satin.md §1` L83 | new | `a:system/tx.rs` `classify_system_transaction` | `b:tx.rs` `prepare_deposit` |  |
| `SATIN-DEP-009` | Where the floor binds, a deposit is charged nothing; only its receipt's and the block's figures move | `satin.md §7` L447–L448 | new | `a:evm/result.rs` | `op:handler.rs` |  |
| `SATIN-DEP-010` | A deposit creating from a sender whose nonce cannot be bumped (2^64 − 1) succeeds with nothing created and nothing counted | `satin.md §10` L781 | new | `a:evm/execution.rs` | `b:tx.rs` `creation_nonce_unbumpable`<br>`b:tx.rs` `unbumpable_creation` |  |
| `SATIN-DEP-011` | A failed deposit whose mint would overflow its sender's balance | `satin.md §21` L1338 (silent) | new | `a:evm/execution.rs` | `b:tx.rs` `failed_deposit` | undefined: QE-03 |
| `SATIN-DEP-012` | Whether a deposit that fails before its first frame loads its recipient | `satin.md §5` L322; `satin.md §21` L1338; `satin.md §22` L1391, L1440 (implied) | new | `a:evm/execution.rs` | `b:tx.rs` `prepare_deposit`<br>`b:tx.rs` `park_start` | undefined: QE-02 |
| `SATIN-DEP-013` | A deposit carrying a gas price | none | new | `a:evm/execution.rs` | `b:tx.rs` `prepare_deposit` | undefined: QA-07 |

### System Calls and the Pre-Block Sequence (`satin/block/system-calls.md`)

The gas a system call runs on, the calls a block makes before its transactions and their order, the Oracle rule inside a system call, and how a failed pre-block call ends the block.

Rex pages it draws on: `upgrades/rex5.md`, `system-contracts/sequencer-registry.md`.

| Id | Rule | Draft | Rex page | Code (a) | Code (b) | Note |
| --- | --- | --- | --- | --- | --- | --- |
| `SATIN-PBLK-001` | A system call runs on at most SYSTEM_CALL_REGULAR_GAS_LIMIT = 30,000,000 of regular gas, the rest of its gas limit being its reservoir; GAS inside reads at most 30,000,000; a transaction, a Mega System Transaction included, is not a system call | `satin.md §18` L1206–L1208 | replaces upgrades/rex5.md "26. EIP-2935 / EIP-4788 Pre-Block System Call Gas Floor" | `a:evm/execution.rs` `SYSTEM_CALL_REGULAR_GAS_LIMIT` | `evm2:evm/system.rs` `SYSTEM_CALL_GAS_LIMIT` |  |
| `SATIN-PBLK-002` | Each pre-block call runs from 0xff…fe on PRE_BLOCK_CALL_GAS_LIMIT = 31,566,720 (30,000,000 regular and a reservoir of sixteen fresh slots at m = 1), whatever the block's gas limit; state gas the reservoir cannot pay spills | `satin.md §18` L1210–L1213 | new | `a:constants.rs` `PRE_BLOCK_CALL_GAS_LIMIT` | `evm2:evm/system.rs` `SYSTEM_MAX_SSTORES_PER_CALL`<br>`b:block.rs` `system_call` |  |
| `SATIN-PBLK-003` | Before its transactions a block, in order: makes the EIP-2935 call; makes the EIP-4788 call (a block without a parent beacon block root is invalid); in Satin's activation block only, checks the predeploys; reads whether the SequencerRegistry has a role change due and if so calls applyPendingChanges(); reads the L1 block contract's account and five fee slots | `satin.md §18` L1215–L1220 | replaces upgrades/rex5.md "4. Pre-Block Role Change" | `a:block/executor.rs`<br>`a:block/eips.rs` `transact_beacon_root_contract_call` | `b:block.rs` `apply_pre_execution_changes` | disagreement: QC-01 |
| `SATIN-PBLK-004` | Whether a role change is due, read from the registry's pending slots | `satin.md §18` L1219 | keeps system-contracts/sequencer-registry.md "Pre-Block Apply" | `a:system/sequencer_registry.rs` `is_apply_pending_changes_due` | `b:block.rs` `registry_due` | undefined: QA-09 |
| `SATIN-PBLK-005` | A system call never asks the oracle service: an SLOAD in the Oracle's frame reads the chain's value, priced as an Oracle read, and records no answer; the rule ends with the call | `satin.md §18` L1230–L1232 | new | `a:evm/host.rs` | `b:ledger.rs` `begin_system_call` |  |
| `SATIN-PBLK-006` | A pre-block call that does not succeed makes the block invalid before its state is used; a database error the database declares fatal is an internal error; a database error in the activation check, the due-change read or the L1 info read is always an internal error | `satin.md §18` L1234–L1237; `satin.md §21` L1364 | new | `a:block/executor.rs` `MegaBlockExecutionError` | `b:block.rs` `system_call`<br>`b:block.rs` `apply_pre_execution_changes` |  |

### Block Limits and Packing (`satin/block/block-limits.md`)

What a block counts of its transactions, the three packing budgets and the transactions they never refuse, the block gas limit, and what a builder may do as policy that a validator never applies.

Rex pages it draws on: `evm/resource-limits.md`.

| Id | Rule | Draft | Rex page | Code (a) | Code (b) | Note |
| --- | --- | --- | --- | --- | --- | --- |
| `SATIN-BLK-001` | A block counts per transaction its regular gas (as max(regular, floor)), state gas, history gas, history bytes, data size, KV updates and state growth | `satin.md §20` L1272 | replaces evm/resource-limits.md "Runtime Block-Level Limits" | `a:block/limit.rs` `BlockUsage` | `b:block.rs` `BlockLimiter` |  |
| `SATIN-BLK-002` | Three counts are limited, each checked before the next transaction runs: BLOCK_DATA_LIMIT = 13,107,200, BLOCK_KV_UPDATE_LIMIT = 500,000, BLOCK_STATE_GROWTH_LIMIT = 1,000 | `satin.md §20` L1273–L1280 | replaces evm/resource-limits.md "Runtime Block-Level Limits" | `a:constants.rs` `BLOCK_DATA_LIMIT`<br>`a:block/limit.rs` `for_spec` | `b:block.rs` `BLOCK_BUDGETS` |  |
| `SATIN-BLK-003` | The transaction that moves a counter to or past its limit is included and a later ordinary transaction is skipped before it runs; a node may report the skip in the order data size, KV updates, state growth; a skip leaves no field in the block | `satin.md §20` L1274, L1282–L1287 | new | `a:block/limit.rs` `pre_execution_check` | `b:block.rs` `pre_execution_check` |  |
| `SATIN-BLK-004` | A builder that executes several candidates before committing one holds each to the counters, the block gas limit and the DA footprint again at commit; a validator's second check finds what its first found | `satin.md §20` L1289 | replaces evm/resource-limits.md "Two-Phase Block Building Workflow" | `a:block/executor.rs` `commit_transaction_outcome` | `b:block.rs` `commit_transaction_outcome` |  |
| `SATIN-BLK-005` | A builder does not commit a candidate whose sender's nonce or balance another commit moved since it executed; any other stale read is the builder's to handle | `satin.md §20` L1290–L1291; `satin.md` Node integrators L1527–L1529 | new | `a:block/executor.rs` `commit_transaction_outcome` | `b:block.rs` `commit_transaction_outcome` |  |
| `SATIN-BLK-006` | A deposit and a Mega System Transaction are never refused by the three budgets or by building policy and count toward each; the block decides this before the transaction runs from its envelope and the live system address | `satin.md §20` L1292–L1299; `satin.md` Node integrators L1530–L1532 | new | `a:block/limit.rs` `pre_execution_check` | `b:block.rs` `run_transaction`<br>`b:block.rs` `is_system_transaction` |  |
| `SATIN-BLK-007` | A Mega System Transaction is still held to the block gas limit and, its envelope being legacy, to the DA footprint | `satin.md §20` L1300–L1301 | new | `a:block/limit.rs` | `b:block.rs` `run_transaction` |  |
| `SATIN-BLK-008` | Execution, state and history gas have no block limit beyond the block gas limit; history bytes are reported and not limited | `satin.md §20` L1302–L1306 | new | `a:block/limit.rs` | `b:block.rs` `BlockLimiter` |  |
| `SATIN-BLK-009` | A transaction's declared gas limit fits in what the block has left | `satin.md §20` L1307; `satin.md §21` L1346 | new | `a:block/limit.rs` `available_gas` | `b:block.rs` `pre_execution_check` |  |
| `SATIN-BLK-010` | The three packing budgets are protocol values fixed per spec; a validator holds a block to them and no other value | `satin.md §20` L1308–L1309 | new | `a:block/limit.rs` `for_spec` | `b:block.rs` `BLOCK_BUDGETS` |  |
| `SATIN-BLK-011` | A builder may pack tighter as policy (a per-transaction declared-gas, encoded-size or DA limit, block encoded-size or DA budgets, packing budgets below the protocol's), never refusing a deposit or a Mega System Transaction; a validator never applies a policy | `satin.md §20` L1310–L1315; `satin.md §21` L1353–L1355; `satin.md §1` L75 | new | `a:block/limit.rs` `BlockLimits` | `b:block.rs` `pre_execution_check` |  |
| `SATIN-BLK-012` | Satin sets no limit on a transaction's or block's encoded size | `satin.md §20` L1316 | new | `a:block/limit.rs` | none |  |
| `SATIN-BLK-013` | A transaction is skipped for the block (and may be included later) when its gas limit or DA footprint does not fit, when the block reached a packing budget and it is neither a deposit nor a Mega System Transaction, or when it is a non-deposit in a deposit-only block; a block holding a transaction it should have skipped is invalid | `satin.md §21` L1344–L1351, L1362–L1366 | new | `a:block/limit.rs` `pre_execution_check` | `b:block.rs` `run_transaction` |  |

### The Stateless Witness (`satin/block/stateless-witness.md`)

What a stateless validator re-executing a block is given: the accounts, slots, code, block hashes, SALT capacities and oracle answers the block read, where each read lands, and the check a replay must pass.

| Id | Rule | Draft | Rex page | Code (a) | Code (b) | Note |
| --- | --- | --- | --- | --- | --- | --- |
| `SATIN-WIT-001` | A block's witness holds every account and slot the block loads (pre-block steps and included transactions) as held before the block, absent accounts as absent with no slots, empty slots of held accounts as zero, with every such account's pre-block code; every hash BLOCKHASH read; every exported SALT bucket's capacity; the oracle answers the included transactions recorded, in block order | `satin.md §22` L1380–L1387 | new | `a:evm/state.rs` | `b:ledger.rs` `Lite` |  |
| `SATIN-WIT-002` | A transaction loads every account and slot its execution reads (validation, fee settlement, every frame, reverted, halted and failed-deposit ones included); a failed frame's writes are taken back, not its reads | `satin.md §22` L1388–L1389 | new | `a:evm/execution.rs` | `b:tx.rs` `read_registry` |  |
| `SATIN-WIT-003` | The L1 block info a transaction is priced against is loaded by the pre-block phase for the whole block | `satin.md §22` L1390 | new | `a:block/l1_block_info.rs` | `b:block.rs` `apply_pre_execution_changes` |  |
| `SATIN-WIT-004` | A read gas or a limit skipped loads nothing, except an authority the authorization preflight consulted | `satin.md §22` L1391; `satin.md §10` L826 | new | `a:evm/execution.rs` | `b:eip7702.rs` `simulate` | disagreement: QD-01 |
| `SATIN-WIT-005` | Execution reports its loads in the states the block commits (each pre-block step's, each transaction's returned state, naming every account and slot loaded, written or not), independent of how the node caches state | `satin.md §22` L1392–L1394 | new | `a:block/eips.rs` | `b:block.rs` `commit_transaction_outcome` |  |
| `SATIN-WIT-006` | A slot of an account the chain does not hold before the block is not recorded; a validator answers it with zero | `satin.md §22` L1395 | new | `a:evm/state.rs` | none |  |
| `SATIN-WIT-007` | The code in the witness is the chain's before the block, not the code a returned state carries | `satin.md §22` L1396 | new | `a:evm/state.rs` | none |  |
| `SATIN-WIT-008` | Where each read lands: a transaction's returned state (sender, recipient or created address, every frame's loads, the fee recipients, the registry's account and slot, consulted authorities, a keyless signer and deploy address); the pre-block states, one per step in order, each committed whole and collected as committed | `satin.md §22` L1397–L1400; `satin.md` Node integrators L1515–L1518 | new | `a:block/executor.rs`<br>`a:block/eips.rs` | `b:block.rs` `system_call` |  |
| `SATIN-WIT-009` | BLOCKHASH reads outside the journal and is exported; SALT capacities and oracle answers are read outside the database and exported or recorded | `satin.md §22` L1401 | new | `a:evm/state.rs` `BlockHashRecord` | `b:ledger.rs` `Lite` |  |
| `SATIN-WIT-010` | A validator is given beside the witness: the header, the chain configuration, the parent hash, the parent beacon block root, the extra data, the deposit-only flag, whether Satin activates, and the slot number the building node supplied | `satin.md §22` L1402–L1403 | new | `a:block/executor.rs` `MegaBlockExecutionCtx` | `b:block.rs` `BlockExecutor` | undefined: QA-05 |
| `SATIN-WIT-011` | The L1 block info: the contract at 0x4200…0015, slots 1, 3, 7, 8 and, only when the Ecotone scalars are empty, 5; read on the block's state; the pre-block phase reads the account and all five slots and commits them as a read-only state after every other step; a state without the contract records it absent; one that cannot serve them fails the block as an internal error | `satin.md §22` L1404–L1411; `satin.md §18` L1220, L1237 | new | `a:block/l1_block_info.rs` `L1_BLOCK_INFO_SLOTS` | `b:block.rs` `L1_BLOCK_INFO_SLOTS`<br>`b:block.rs` `apply_pre_execution_changes` |  |
| `SATIN-WIT-012` | The reads a validator makes again are skipped again on replay and need not be carried | `satin.md §22` L1412–L1413 | new | `a:evm/state.rs` | none |  |
| `SATIN-WIT-013` | The SALT bucket export: the buckets answered with a valid capacity during the block, emptied at the block's start, failed lookups excluded; the witness proves every bucket in it; several executions take the union; pre-block calls and system transactions add none | `satin.md §22` L1414–L1421 | new | `a:evm/state.rs` `BucketRecord` | `b:ledger.rs` `Lite` |  |
| `SATIN-WIT-014` | The block-hash export: every hash BLOCKHASH was served, emptied at the block's start | `satin.md §22` L1422–L1424 | new | `a:evm/state.rs` `BlockHashRecord` | `b:ledger.rs` `Lite` |  |
| `SATIN-WIT-015` | The oracle records: each read a transaction makes through the service, with its answer (none allowed), in order on its outcome; a node takes the included transactions' records in block order; a validator either answers from them or runs no service and reads the Oracle's slots, with the conditions under which that reproduces the block | `satin.md §22` L1425–L1438 | new | `a:evm/state.rs` `OracleReadRecord` | `b:ledger.rs` `Lite` |  |
| `SATIN-WIT-016` | A block replayed on exactly its witness produces the same receipts, state changes, gas ledgers, logs and block counters and reads nothing outside it; its exports are a subset of the building node's | `satin.md §22` L1439–L1441 | new | `a:evm/state.rs` | none |  |
| `SATIN-WIT-017` | An address the state holds no account for is answered as no account, never as an empty account | `satin.md` Node integrators L1519–L1522 | new | `a:evm/state.rs` | `evm2:evm/state/account.rs` `original` |  |

### Activation and Rex-Era Carry-Over (`satin/block/activation.md`)

When Satin takes effect, the chain configuration key that schedules it and the base forks it requires, the checks its activation block makes, and what it carries over from the Rex era unchanged.

Rex pages it draws on: `hardfork-spec.md`, `upgrades/overview.md`, `system-contracts/overview.md`.

| Id | Rule | Draft | Rex page | Code (a) | Code (b) | Note |
| --- | --- | --- | --- | --- | --- | --- |
| `SATIN-ACT-001` | Satin follows Rex6 on the spec ladder; a block from satinTime on executes Satin, every earlier block the spec its timestamp resolves to | `satin.md` Safety and Compatibility L1563–L1564; `satin.md` Summary L31 | keeps hardfork-spec.md "Hardfork vs Spec" | `a:block/hardfork.rs`<br>`a:evm/spec.rs` | `b:lib.rs` `MegaSpec` | disagreement: QF-01 |
| `SATIN-ACT-002` | The chain configuration carries Satin as one key, satinTime (a JSON number up to 2^64 − 1, or the arbitrary-precision object form); Satin carries no parameter; no key names a limit or the registry's roles; another key starting with satin is refused; a duplicated key is read as its last copy; the format is provisional | `satin.md` Node integrators L1539–L1553 | new | `a:block/genesis.rs` `SatinChainConfig`<br>`a:block/genesis.rs` `SATIN_TIME_KEY` | none | disagreement: QG-05 |
| `SATIN-ACT-003` | Every base fork (Ethereum Shanghai to Osaka, Optimism Regolith to Karst) is active by satinTime, and Jovian, Karst and Osaka activate no earlier than satinTime; a node refuses a configuration that breaks either | `satin.md` Node integrators L1555–L1559 | new | `a:block/hardfork.rs` `ScheduleError` | none | disagreement: QB-01 |
| `SATIN-ACT-004` | Satin's activation block admits only deposits and checks the predeploys before its transactions | `satin.md §1` L80; `satin.md §18` L1218 | new | `a:block/executor.rs` `with_satin_activation_block` | `b:block.rs` `only_deposits` | disagreement: QB-02 |
| `SATIN-ACT-005` | The activation check: the six system contracts in address order, then the EIP-7997 CREATE2 factory at 0x4e59b448…, each holding exactly the code Satin expects (Oracle and SequencerRegistry at 2.0.0, the others at Rex6's bytecode, the factory's code hash 0x2fa86add…); nonces, balances and storage unchecked; any other state makes the block invalid; the reads are read-only entries; no other block reads the seven | `satin.md §18` L1221–L1228; `satin.md §21` L1365 | replaces system-contracts/overview.md "Deployment Semantics" | `a:system/predeploys.rs` `check_system_contract`<br>`a:system/predeploys.rs` `CREATE2_FACTORY_CODE_HASH` | none | disagreement: QC-01 |
| `SATIN-ACT-006` | Satin deploys, upgrades and seeds nothing: the chain holds the six contracts at the versions the legacy forks left (Rex5 deployed the SequencerRegistry and upgraded the Oracle to 2.0.0, Rex6 upgraded the SequencerRegistry to 2.0.0) and the factory from genesis, so a chain runs a Rex6 block before satinTime | `satin.md §18` L1222; `satin.md` Node integrators L1523–L1526; `satin.md` Safety and Compatibility L1566 | new | `a:system/predeploys.rs` `system_contract_specs` | none |  |
| `SATIN-ACT-007` | Satin starts from the L1 block contract the Rex era left, OP's L1Block 1.6.0 (Isthmus) with zero DA footprint and operator fee scalars, and does not upgrade it | `satin.md §1` L89–L90 | new | `a:block/l1_block_info.rs` | `op:l1block.rs` |  |
| `SATIN-ACT-008` | State and contracts from earlier specs keep working: Satin changes nothing about blocks under earlier specs, and contracts deployed earlier run under the Satin rules | `satin.md` Safety and Compatibility L1563–L1564 | changes hardfork-spec.md "Backward Compatibility" | none | none | disagreement: QF-06 |
| `SATIN-ACT-009` | Part of the execution configuration is fixed by the spec whatever a node supplies: the Satin gas schedule, EIP-8037, EIP-2780 and EIP-7708 on, the 200,000,000 execution cap, the chain-id check on, the two code-size limits, the byte prices (no build that reads them at run time), and the limits; a node that reads the configuration before executing reads these values, not its own | `satin.md` Node integrators L1483–L1487 | new | `a:evm/spec.rs`<br>`a:evm/prices.rs`<br>`a:block/limit.rs` `for_spec` | `b:lib.rs` `satin_version`<br>`b:ledger.rs` `Cfg` | disagreement: QG-04 |
| `SATIN-ACT-010` | Whether a block admits only deposits, and whether Satin activates in it, are worked out from the chain configuration and the parent's timestamp for every block built or validated and given to the executor and to a stateless validator; the derivation node and builders enforce deposit-only activation blocks for Satin and every later MegaETH fork; an execution not told the first runs the block as one that admits non-deposit transactions, and one not told the second checks no predeploy | `satin.md` Node integrators L1506–L1512 | new | `a:block/executor.rs` `MegaBlockExecutionCtx`<br>`a:block/hardfork.rs` | `b:block.rs` `only_deposits` | disagreement: QB-02 |

## Coverage of the draft's 22 sections

Every numbered section of the draft, with the rules above that cite it (first ten listed).

| Section | Rules citing it |
| --- | --- |
| `satin.md §1` Base Layer | 15: `SATIN-BASE-001`, `SATIN-BASE-002`, `SATIN-BASE-003`, `SATIN-BASE-004`, `SATIN-BASE-005`, `SATIN-BASE-006`, `SATIN-BASE-007`, `SATIN-BASE-008`, `SATIN-BASE-009`, `SATIN-BASE-010`, and 5 more |
| `satin.md §2` Precompiles | 8: `SATIN-OUT-004`, `SATIN-OUT-011`, `SATIN-PCMP-001`, `SATIN-PCMP-002`, `SATIN-PCMP-003`, `SATIN-PCMP-004`, `SATIN-PCMP-005`, `SATIN-PCMP-006` |
| `satin.md §3` Contract Size Limits | 7: `SATIN-OUT-003`, `SATIN-OUT-012`, `SATIN-SIZE-001`, `SATIN-SIZE-002`, `SATIN-SIZE-003`, `SATIN-SIZE-005`, `SATIN-SIZE-006` |
| `satin.md §4` Two-Pool Gas | 36: `SATIN-BASE-003`, `SATIN-POOL-001`, `SATIN-POOL-002`, `SATIN-POOL-003`, `SATIN-POOL-004`, `SATIN-POOL-005`, `SATIN-POOL-006`, `SATIN-POOL-007`, `SATIN-POOL-008`, `SATIN-POOL-009`, and 26 more |
| `satin.md §5` Gas Schedule and Intrinsic Gas | 21: `SATIN-SCHED-001`, `SATIN-SCHED-002`, `SATIN-SCHED-003`, `SATIN-SCHED-004`, `SATIN-SCHED-005`, `SATIN-SCHED-006`, `SATIN-SCHED-007`, `SATIN-SCHED-008`, `SATIN-SCHED-009`, `SATIN-SCHED-010`, and 11 more |
| `satin.md §6` State Gas and SALT Pricing | 13: `SATIN-STATE-001`, `SATIN-STATE-002`, `SATIN-STATE-003`, `SATIN-STATE-004`, `SATIN-STATE-005`, `SATIN-STATE-006`, `SATIN-STATE-007`, `SATIN-STATE-008`, `SATIN-STATE-009`, `SATIN-SD-005`, and 3 more |
| `satin.md §7` History Gas | 28: `SATIN-POOL-006`, `SATIN-POOL-008`, `SATIN-POOL-018`, `SATIN-POOL-020`, `SATIN-SCHED-011`, `SATIN-HIST-001`, `SATIN-HIST-002`, `SATIN-HIST-003`, `SATIN-HIST-004`, `SATIN-HIST-005`, and 18 more |
| `satin.md §8` History Allowance | 4: `SATIN-HIST-018`, `SATIN-HIST-019`, `SATIN-HIST-020`, `SATIN-HIST-021` |
| `satin.md §9` Gas Forwarding | 14: `SATIN-POOL-010`, `SATIN-POOL-011`, `SATIN-POOL-012`, `SATIN-POOL-014`, `SATIN-POOL-015`, `SATIN-HIST-020`, `SATIN-FWD-001`, `SATIN-FWD-002`, `SATIN-FWD-003`, `SATIN-FWD-004`, and 4 more |
| `satin.md §10` Resource Limits | 88: `SATIN-POOL-021`, `SATIN-SCHED-007`, `SATIN-FWD-006`, `SATIN-LIM-001`, `SATIN-LIM-002`, `SATIN-LIM-003`, `SATIN-LIM-004`, `SATIN-LIM-005`, `SATIN-LIM-006`, `SATIN-LIM-007`, and 78 more |
| `satin.md §11` The Revert-Class Stop | 45: `SATIN-POOL-017`, `SATIN-ACCT-003`, `SATIN-AUTH-011`, `SATIN-AUTH-016`, `SATIN-STOP-001`, `SATIN-STOP-002`, `SATIN-STOP-003`, `SATIN-STOP-004`, `SATIN-STOP-005`, `SATIN-STOP-006`, and 35 more |
| `satin.md §12` Gas Detention on Withheld Gas | 38: `SATIN-POOL-009`, `SATIN-SD-020`, `SATIN-DET-001`, `SATIN-DET-002`, `SATIN-DET-003`, `SATIN-DET-004`, `SATIN-DET-005`, `SATIN-DET-006`, `SATIN-DET-007`, `SATIN-DET-008`, and 28 more |
| `satin.md §13` Volatile-Data Access Control and remainingComputeGas() | 12: `SATIN-DET-008`, `SATIN-OUT-008`, `SATIN-SYSC-002`, `SATIN-MAC-001`, `SATIN-MAC-002`, `SATIN-MAC-003`, `SATIN-MAC-004`, `SATIN-MAC-005`, `SATIN-MLC-001`, `SATIN-MLC-002`, and 2 more |
| `satin.md §14` EIP-7708 Transfer Logs | 8: `SATIN-HIST-021`, `SATIN-LOG-001`, `SATIN-LOG-002`, `SATIN-LOG-003`, `SATIN-LOG-004`, `SATIN-LOG-005`, `SATIN-LOG-006`, `SATIN-LOG-007` |
| `satin.md §15` Native Keyless Deployment | 23: `SATIN-OUT-003`, `SATIN-OUT-009`, `SATIN-SYSC-001`, `SATIN-SYSC-002`, `SATIN-ICPT-006`, `SATIN-KEY-001`, `SATIN-KEY-002`, `SATIN-KEY-003`, `SATIN-KEY-004`, `SATIN-KEY-005`, and 13 more |
| `satin.md §16` Oracle Storage Reads and Hints | 11: `SATIN-ICPT-001`, `SATIN-ORCL-002`, `SATIN-ORCL-003`, `SATIN-ORCL-004`, `SATIN-ORCL-005`, `SATIN-ORCL-006`, `SATIN-ORCL-007`, `SATIN-ORCL-008`, `SATIN-ORCL-009`, `SATIN-ORCL-010`, and 1 more |
| `satin.md §17` The Live System Address | 16: `SATIN-SCHED-013`, `SATIN-ORCL-001`, `SATIN-ORCL-011`, `SATIN-REG-001`, `SATIN-REG-002`, `SATIN-REG-003`, `SATIN-REG-004`, `SATIN-REG-005`, `SATIN-REG-007`, `SATIN-MST-001`, and 6 more |
| `satin.md §18` System Calls and Pre-Block Calls | 16: `SATIN-SYSC-001`, `SATIN-SYSC-003`, `SATIN-ORCL-001`, `SATIN-ORCL-005`, `SATIN-HPTS-001`, `SATIN-REG-001`, `SATIN-PBLK-001`, `SATIN-PBLK-002`, `SATIN-PBLK-003`, `SATIN-PBLK-004`, and 6 more |
| `satin.md §19` The Protocol's Own Transactions | 10: `SATIN-STATE-009`, `SATIN-HIST-016`, `SATIN-DET-026`, `SATIN-MST-006`, `SATIN-MST-007`, `SATIN-MST-008`, `SATIN-MST-009`, `SATIN-MST-010`, `SATIN-DEP-001`, `SATIN-DEP-002` |
| `satin.md §20` Block Limits | 14: `SATIN-POOL-020`, `SATIN-LIM-017`, `SATIN-BLK-001`, `SATIN-BLK-002`, `SATIN-BLK-003`, `SATIN-BLK-004`, `SATIN-BLK-005`, `SATIN-BLK-006`, `SATIN-BLK-007`, `SATIN-BLK-008`, and 4 more |
| `satin.md §21` Transaction and Block Refusals | 27: `SATIN-BASE-006`, `SATIN-BASE-009`, `SATIN-STATE-007`, `SATIN-ACCT-020`, `SATIN-OUT-001`, `SATIN-OUT-005`, `SATIN-OUT-013`, `SATIN-OUT-014`, `SATIN-OUT-015`, `SATIN-OUT-016`, and 17 more |
| `satin.md §22` The Stateless Witness | 20: `SATIN-BASE-005`, `SATIN-BASE-010`, `SATIN-STATE-007`, `SATIN-DEP-012`, `SATIN-WIT-001`, `SATIN-WIT-002`, `SATIN-WIT-003`, `SATIN-WIT-004`, `SATIN-WIT-005`, `SATIN-WIT-006`, and 10 more |
