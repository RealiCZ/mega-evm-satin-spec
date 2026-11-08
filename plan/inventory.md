# Satin Specification — Source Inventory

Phase 1 of the Satin specification.
This file lists every source a Satin rule comes from and what each covers, so that the Satin section (`docs/spec/satin/`) can be written from them and checked against them.
The rules themselves, page by page, are in [outline.md](outline.md); what the sources leave open is in [questions.md](questions.md).

## 1. The sources

| Source | Revision | What it is | How the plan cites it |
| --- | --- | --- | --- |
| The Satin draft | `docs/spec/upgrades/satin.md` of mega-evm `5e3f30ad` (the head of pull request #409), copied into this repository unchanged | A delta against Rex6 written for reviewers, 1,592 lines, 22 numbered sections | `satin.md §<n>` L<from>–L<to> (line numbers of the copied file) |
| The published specification | `docs/spec/` of mega-evm `main` at `d4c913c5`, copied into this repository unchanged | The Rex6-era gitbook: concept pages, system contracts, upgrade pages, glossary, writing rules | `docs/spec/<page>` and its section heading |
| Implementation (a) | mega-evm `5e3f30ad`: `crates/mega-evm/src/` (pull requests #386 and #409), on MegaETH's forks of revm 40.0.3 and op-revm 20.0.0 | The Satin engine on revm | `a:<path>` = `crates/mega-evm/src/<path>` |
| Implementation (b) | mega-evm `785182eb`: the `next/` workspace — `next/mega-evm2/src/` (the engine), `next/op-evm2/src/` (a vendored OP layer) — on the evm2 fork at `91518705` | The Satin engine rebuilt on evm2 | `b:<path>` = `next/mega-evm2/src/<path>`; `op:<path>` = `next/op-evm2/src/<path>`; `evm2:<path>` = `crates/evm2/src/<path>` of the fork |
| The revert-or-halt rule | The maintainers' Satin review guidelines | The rule every limit-stop site is reviewed against, with its exceptions | Section 4 below |
| The cross-checks of (a) and (b) | Three rounds of two-sided differential review of (b) against (a), each difference judged against the draft | Where an implementation and the draft disagree, and the decisions taken | Section 8 below and [questions.md](questions.md) |

Only one of the two implementations will ship; both are judged against the Satin specification, and a place where either differs from it is a question, not a rule.

## 2. The Satin draft, section by section

Line ranges are of `docs/spec/upgrades/satin.md` in this repository. "Satin pages" are the pages of the Satin section that will specify the section's rules.

| Section | Lines | What it covers | Satin pages |
| --- | --- | --- | --- |
| Frontmatter, title, unstable hint | L1–L13 | Description; the claim that the page is normative while the concept pages describe Rex6 | none (layout: [questions.md](questions.md) QF-04) |
| Summary | L15–L57 | The restatement on Karst, the three ledgers, the limits and the stop, the change list; Satin follows Rex6 and a Rex6 rule not carried over does not apply (L31–L32) | `satin/overview.md`, `satin/block/activation.md` |
| `satin.md §1` Base Layer: Optimism Karst (Ethereum Osaka) | L61–L90 | Karst base; no EIP-7825 or EIP-8037 total cap; DUPN, SWAPN, EXCHANGE, SLOTNUM; deposit-only activation blocks; DA footprint; L1 block info pricing; the L1Block contract carried over | `satin/base-layer.md`, `satin/block/activation.md` |
| `satin.md §2` Precompiles | L92–L117 | Karst set, KZG at 100,000, P256VERIFY 6,900, OP input limits, failure consumes the forward | `satin/evm/precompiles.md` |
| `satin.md §3` Contract Size Limits | L119–L133 | 512 KiB code, 1 MiB initcode, halts not stops, the creation opcodes' check order | `satin/evm/contract-limits.md` |
| `satin.md §4` Two-Pool Gas (EIP-8037) | L135–L249 | EIP-8037 base commit and later commits taken or declined, the child-merge return, the execution cap, the three kinds of charge, frames and the reservoir share, settlement, the three ledgers, validation, the EIP-8037 profile (L225–L249) | `satin/evm/gas-model.md`, `satin/block/transaction-validation.md` |
| `satin.md §5` Gas Schedule and Intrinsic Gas | L251–L333 | Amsterdam schedule with two changes, the entry table (L272–L309), the floor, EIP-2780 intrinsic gas, the pre-frame charges and their out-of-gas path, the code-deposit order, the warm set | `satin/evm/gas-schedule.md`, `satin/block/deposits.md` |
| `satin.md §6` State Gas and SALT Pricing | L335–L370 | `entry × m`, the byte table, charge sites, one multiplier per bucket per transaction, the bucket fault, the SSTORE transitions, the protocol's own transactions at `m = 1` | `satin/evm/state-gas.md` |
| `satin.md §7` History Gas | L372–L448 | 88 per byte, the byte table, the body, when each history charge is made and given back, the refill order, the limit-then-charge order, the exemptions, the floor | `satin/evm/history-gas.md` |
| `satin.md §8` History Allowance | L450–L463 | 160 bytes for a value call's frame, drawn only by logs | `satin/evm/history-gas.md` |
| `satin.md §9` Gas Forwarding | L465–L515 | 98/100 forward, the stipend, the reservoir share, the keyless forward, the two 98/100 integers | `satin/evm/gas-forwarding.md` |
| `satin.md §10` Resource Limits | L517–L850 | The three dimensions and limits (L528–L537), data size (L539–L541), write records (L542–L578), frame budgets (L579–L615), state growth with the SSTORE table (L616–L657), the destruction table (L659–L758), order at one site (L760–L777), a frame start (L778–L784), authorizations before the first frame (L785–L843), limits fixed per spec (L844–L850) | `satin/evm/resource-limits.md`, `satin/evm/resource-accounting.md`, `satin/evm/selfdestruct.md`, `satin/evm/authorizations.md` |
| `satin.md §11` The Revert-Class Stop | L852–L926 | Every limit stops with a revert; what is not a stop; what the stop reverts, keeps and reports; enforcement before a start runs; the revert data | `satin/evm/limit-stops.md`, `satin/evm/outcomes.md` |
| `satin.md §12` Gas Detention on Withheld Gas | L928–L991 | What is volatile, compute, the limit, withheld gas, the crossing, precompiles, interceptor answers, exemptions | `satin/evm/gas-detention.md` |
| `satin.md §13` Volatile-Data Access Control and `remainingComputeGas()` | L993–L1032 | Where a read is refused and what it pays, the access types, `remainingComputeGas()` | `satin/system-contracts/mega-access-control.md`, `satin/system-contracts/mega-limit-control.md` |
| `satin.md §14` EIP-7708 Transfer Logs | L1034–L1053 | Transfer logs, what logs nothing, silent burns, their data size | `satin/evm/transfer-logs.md` |
| `satin.md §15` Native Keyless Deployment | L1055–L1135 | Recognition, the fifteen steps (L1074–L1090), the creation, the signer's nonce, the answer, limits, the interface | `satin/system-contracts/keyless-deploy.md` |
| `satin.md §16` Oracle Storage Reads and Hints | L1137–L1163 | The service answer over the slot, the cold price, hints and what they count | `satin/system-contracts/oracle.md` |
| `satin.md §17` The Live System Address | L1165–L1193 | The system shape, the registry read by every transaction, Mega System Transactions and their validation | `satin/system-contracts/sequencer-registry.md`, `satin/system-contracts/system-tx.md` |
| `satin.md §18` System Calls and Pre-Block Calls | L1195–L1237 | The 30,000,000 split, the pre-block budget and sequence, the activation check, the Oracle in a system call, failure | `satin/block/system-calls.md`, `satin/block/activation.md` |
| `satin.md §19` The Protocol's Own Transactions | L1239–L1261 | What is system-originated and what that exempts | `satin/system-contracts/system-tx.md` |
| `satin.md §20` Block Limits | L1263–L1316 | What a block counts, the three packing budgets, exempt transactions, building policy | `satin/block/block-limits.md` |
| `satin.md §21` Transaction and Block Refusals | L1318–L1366 | Rejection, failed deposits, skips, failed receipts, node faults, invalid blocks | `satin/block/transaction-validation.md`, `satin/block/deposits.md`, `satin/evm/outcomes.md` |
| `satin.md §22` The Stateless Witness | L1368–L1441 | Witness contents, where reads land, the L1 block info read, SALT and block-hash exports, oracle records, the check | `satin/block/stateless-witness.md` |
| Developer Impact | L1443–L1477 | Gas figures and behaviour changes for contract authors; informative | none (informative) |
| Node integrators | L1479–L1559 | The fixed execution configuration, precompile replacement, pool checks, activation-block flags, L1 info handover, witness collection, absent accounts, predeploys, delayed commits, MST packing, reporting a stop, the chain configuration key | `satin/block/*` where a rule is stated (see [questions.md](questions.md) QG-04, QG-05) |
| Safety and Compatibility | L1561–L1575 | Earlier blocks unchanged, contracts and bytecode kept, limits fixed per spec | `satin/block/activation.md` |
| References | L1577–L1592 | EIPs and commits | none |

## 3. The published specification, page by page

Every page of `docs/spec/` at `main` `d4c913c5` is copied unchanged, except the roster pages and the writing rules, which this repository updates.
"Under Satin" says whether the page's rules apply to Satin unchanged, change, or are replaced; the Satin section restates each rule Satin keeps (a Satin page never relies on a Rex-era page for a rule).

| Page | Spec | Under Satin | Satin page | Notes |
| --- | --- | --- | --- | --- |
| `docs/spec/overview.md` | Rex6 | Changes (roster page, updated here) | `satin/overview.md` | Satin added to the progression and summary; the backward-compatibility hint left as it is ([QF-06](questions.md#qf-06)) |
| `docs/spec/hardfork-spec.md` | Rex6 | Changes (roster page, updated here) | `satin/block/activation.md` | Progression, base layer and maturity sentences updated; SATIN summary added |
| `docs/spec/glossary.md` | Rex6 | Changes (updated here) | all | Progression line; six Satin terms the draft links to (state gas, history gas, execution cap, reservoir, write record, history allowance) |
| `docs/spec/SUMMARY.md` | n/a | Changes (updated here) | all | The Satin part and `upgrades/satin.md` |
| `docs/spec/AGENTS.md` | n/a | Changes (updated here) | all | The Satin section rules (option B) |
| `docs/spec/.gitbook.yaml` | n/a | Applies unchanged | n/a | |
| `docs/spec/evm/overview.md` | Rex6 | Replaced | `satin/evm/overview.md` | Inheritance boundary moves to `satin/base-layer.md` |
| `docs/spec/evm/dual-gas-model.md` | Rex6 | Replaced | `satin/evm/gas-model.md`, `satin/evm/gas-schedule.md`, `satin/evm/state-gas.md`, `satin/evm/history-gas.md` | Compute and storage gas give way to regular, state and history gas |
| `docs/spec/evm/compute-gas.md` | Rex6 | Replaced | `satin/evm/gas-detention.md` (compute), `satin/evm/gas-schedule.md` (warm set) | No compute-gas ledger or limit under Satin; compute is regular gas |
| `docs/spec/evm/resource-limits.md` | Rex6 | Replaced | `satin/evm/resource-limits.md`, `satin/evm/limit-stops.md`, `satin/evm/outcomes.md`, `satin/block/block-limits.md`, `satin/block/transaction-validation.md` | Compute limit removed; halts become stops |
| `docs/spec/evm/resource-accounting.md` | Rex6 | Replaced | `satin/evm/resource-accounting.md` | KV updates become write records; fee-reward accounting dropped |
| `docs/spec/evm/gas-detention.md` | Rex6 | Replaced | `satin/evm/gas-detention.md` | Withheld gas instead of a detained compute limit; BLOBHASH no longer volatile |
| `docs/spec/evm/gas-forwarding.md` | Rex6 | Changes | `satin/evm/gas-forwarding.md` | 98/100 and the stipend kept; the reservoir share added; the storage-gas stipend interaction replaced |
| `docs/spec/evm/contract-limits.md` | Rex6 | Changes | `satin/evm/contract-limits.md` | Initcode 1,048,576; the creation-opcode order restated |
| `docs/spec/evm/precompiles.md` | Rex6 | Changes | `satin/evm/precompiles.md` | Karst set: P256VERIFY 6,900 and smaller OP input limits |
| `docs/spec/evm/selfdestruct.md` | Rex6 | Changes | `satin/evm/selfdestruct.md` | EIP-6780 kept; the destruction table replaces the state-growth refund |
| `docs/spec/system-contracts/overview.md` | Rex6 | Changes | `satin/system-contracts/overview.md`, `satin/block/activation.md` | Registry kept; Satin deploys nothing |
| `docs/spec/system-contracts/oracle.md` | Rex6 | Changes | `satin/system-contracts/oracle.md` | Contract kept; reads answer from the service at a cold price; hint conditions changed |
| `docs/spec/system-contracts/high-precision-timestamp.md` | Rex6 | Applies unchanged | `satin/system-contracts/high-precision-timestamp.md` | Its Oracle reads follow the Satin Oracle rules |
| `docs/spec/system-contracts/keyless-deploy.md` | Rex6 | Replaced | `satin/system-contracts/keyless-deploy.md` | Native creation instead of a sandbox; four errors removed from the interface |
| `docs/spec/system-contracts/mega-access-control.md` | Rex6 | Changes | `satin/system-contracts/mega-access-control.md` | Contract kept; refusal point, refusal gas and access type 12 |
| `docs/spec/system-contracts/mega-limit-control.md` | Rex6 | Changes | `satin/system-contracts/mega-limit-control.md` | Contract kept; `remainingComputeGas()` redefined |
| `docs/spec/system-contracts/sequencer-registry.md` | Rex6 | Changes | `satin/system-contracts/sequencer-registry.md` | Contract kept; read by every transaction; seeding is the legacy forks' |
| `docs/spec/system-contracts/interception.md` | Rex6 | Changes | `satin/system-contracts/interception.md` | Matching kept; answers detained; keyless recognized by its own rule |
| `docs/spec/system-contracts/system-tx.md` | Rex6 | Changes | `satin/system-contracts/system-tx.md` | Live system address; MST validation; system-originated exemptions restated |
| `docs/spec/upgrades/overview.md` | n/a | Changes (roster page, updated here) | n/a | Satin entry, not yet scheduled |
| `docs/spec/upgrades/minirex.md` | n/a | Applies unchanged (history) | n/a | |
| `docs/spec/upgrades/rex.md` | n/a | Applies unchanged (history) | n/a | |
| `docs/spec/upgrades/rex1.md` | n/a | Applies unchanged (history) | n/a | |
| `docs/spec/upgrades/rex2.md` | n/a | Applies unchanged (history) | n/a | |
| `docs/spec/upgrades/rex3.md` | n/a | Applies unchanged (history) | n/a | |
| `docs/spec/upgrades/rex4.md` | n/a | Applies unchanged (history) | n/a | |
| `docs/spec/upgrades/rex5.md` | n/a | Applies unchanged (history) | n/a | Several of its items are the origin of rules Satin restates (system-transaction validation, pre-block gas, deposit caller accounting) |
| `docs/spec/upgrades/rex6.md` | n/a | Applies unchanged (history) | n/a | Every "Previous behavior" of the draft is this spec's |
| `docs/spec/upgrades/satin.md` | n/a | Added from `5e3f30ad` unchanged | all | The reviewers' delta; see [QF-04](questions.md#qf-04) |

`upgrades/rex7.md` is not on `main` at `d4c913c5`: it was removed there before the Satin draft (see [QF-01](questions.md#qf-01)).

The draft at `5e3f30ad` also edits sixteen of the pages above (among them `keyless-deploy.md`, `gas-detention.md`, `resource-limits.md`, `precompiles.md`, `selfdestruct.md`, `mega-access-control.md` and the roster pages).
Under option B those edits are not applied to the Rex-era pages: their Satin content goes to the Satin section instead.
The roster pages here take the draft's Satin summaries in shortened form; its change to `overview.md`'s reference-implementation table is not taken ([QF-07](questions.md#qf-07)).

## 4. The revert-or-halt rule and its exceptions

**The rule.** A crossing of a resource limit reverts only the frame that crosses it, and that frame's caller may catch the stop.
Under Satin this holds for every limit: the transaction's data-size, KV-update and state-growth limits, a frame's budget in those dimensions, and gas detention's compute limit (`satin.md §11` L862–L863, L884).
No limit halts a transaction; a stop of the transaction's own frame is its result and settles like an EIP-8037 revert (`satin.md §11` L885–L888).
The maintainers' review guidelines hold every site of the engines to it, including the sites that report a stop (a stop is read from the execution's report, never from the output bytes: `satin.md` Node integrators L1533–L1538).

**The exceptions** — endings that are not limit stops, and refusals that are not reverts of the crossing frame:

| Exception | What happens | Draft | Outline |
| --- | --- | --- | --- |
| Initcode over `MAX_INITCODE_SIZE` | A creation transaction is rejected; a creation opcode halts the creating frame; a keyless deployment is refused with `InitCodeTooLarge` | `satin.md §11` L866; `satin.md §3` L129–L130; `satin.md §15` L1082 | `SATIN-OUT-003`, `SATIN-SIZE-003`, `SATIN-SIZE-004` |
| Deployed code over `MAX_CONTRACT_SIZE` | The creation halts | `satin.md §11` L866; `satin.md §3` L129 | `SATIN-OUT-003`, `SATIN-SIZE-003` |
| An OP precompile input over its size limit | The call halts before any gas check, consuming its forward | `satin.md §11` L867; `satin.md §2` L115 | `SATIN-OUT-004`, `SATIN-PCMP-005` |
| A failed deposit | Whole gas limit used, mint credited, nonce bumped, no stop reported | `satin.md §11` L868; `satin.md §21` L1338–L1341 | `SATIN-OUT-005`, `SATIN-DEP-004` |
| A pre-frame charge the transaction cannot pay | Out of gas without running a frame; a deposit becomes a failed deposit | `satin.md §11` L869; `satin.md §5` L322–L326 | `SATIN-OUT-006`, `SATIN-SCHED-009` |
| A transaction that fails validation | Rejected, or a failed deposit; no stop | `satin.md §11` L871–L873 | `SATIN-OUT-016`, `SATIN-STOP-003` |
| A real out-of-gas, a precompile given less than its price, an invalid opcode | Halt, consuming the frame's gas | `satin.md §11` L910 | `SATIN-OUT-007` |
| Under detention, a charge beyond the frame's whole regular gas | Halt, as without the read; only a charge the withheld part could pay is the crossing | `satin.md §12` L966–L972 | `SATIN-DET-018`, `SATIN-DET-020` |
| CREATE2 short of its salt under detention | The initcode cost and memory charged first can be the crossing (a revert) where the stack underflow would halt | `satin.md §3` L131–L133 | `SATIN-SIZE-006`, `SATIN-OUT-012` |
| A refused volatile read | Reverts with `VolatileDataAccessDisabled(uint8)`, not a stop | `satin.md §13` L1007; `satin.md §11` L922 | `SATIN-OUT-008`, `SATIN-MAC-004` |
| A keyless rule refusal | The call reverts with the rule's error; an out-of-gas step halts the call | `satin.md §15` L1070–L1072 | `SATIN-OUT-009`, `SATIN-KEY-004` |
| A call past the depth limit or with an unfundable value | Fails with empty return data | `satin.md §11` L922; `satin.md §10` L781 | `SATIN-OUT-010` |
| A hint sent into room a take-back freed | The frame the failed frame returns into returns the data-size stop before its next instruction, whether the frame below reverted, halted or was stopped | `satin.md §11` L879–L881 | `SATIN-STOP-006` |
| A failed bucket or database read | No outcome: an internal error or an invalid block, never a halt or revert | `satin.md §21` L1358–L1360 | `SATIN-OUT-015` |
| A failed precompile answer at a frame start | Not replaced by a stop; consumes its forward | `satin.md §11` L903; `satin.md §10` L780 | `SATIN-STOP-014`, `SATIN-LIM-014` |

The outline's page "Halts, Reverts and Stops" (`satin/evm/outcomes.md`) will state the rule and every exception in one place, each pointing to the page that owns its detail.

## 5. Rex-era carry-over Satin must keep

Satin does not start from zero: the chain it activates on ran the Rex-era specs, and Satin deploys, upgrades and seeds nothing (`satin.md §18` L1222–L1228; Node integrators L1523–L1526).

### System contracts

| Contract | Address | Version Satin expects | Bytecode source | Notes |
| --- | --- | --- | --- | --- |
| Oracle | `0x6342000000000000000000000000000000000001` | 2.0.0 (upgraded in place by Rex5) | `crates/system-contracts/artifacts/Oracle-2.0.0.json` at `5e3f30ad` | Writes authorized on the sender (the system address) |
| High-Precision Timestamp | `0x6342000000000000000000000000000000000002` | Rex6's bytecode, the Oracle's address embedded | `a:system/timestamp.rs` | Reads the Oracle's storage |
| KeylessDeploy | `0x6342000000000000000000000000000000000003` | Rex6's bytecode (1.0.0) | `crates/system-contracts/artifacts/KeylessDeploy-1.0.0.json` | Interface no longer declares four Rex-era errors; bytecode unchanged |
| MegaAccessControl | `0x6342000000000000000000000000000000000004` | Rex6's bytecode (1.0.0) | `crates/system-contracts/artifacts/MegaAccessControl-1.0.0.json` | Intercepted |
| MegaLimitControl | `0x6342000000000000000000000000000000000005` | Rex6's bytecode (1.0.0) | `crates/system-contracts/artifacts/MegaLimitControl-1.0.0.json` | Intercepted |
| SequencerRegistry | `0x6342000000000000000000000000000000000006` | 2.0.0 (deployed by Rex5, upgraded in place by Rex6) | `crates/system-contracts/artifacts/SequencerRegistry-2.0.0.json` | Runs its own bytecode; read by every transaction by code hash |
| EIP-7997 `CREATE2` factory | `0x4e59b44847b379578588920ca78fbf26c0b4956c` | Code hash `0x2fa86add0aed31f33a762c9d88e807c475bd51d0f52bd0955754b2608f7e4989` | From OP's genesis tooling | Checked, not deployed (`a:system/predeploys.rs` `CREATE2_FACTORY_CODE_HASH`) |

Addresses and versions are as implementation (a) holds them (`a:system/*.rs`, `a:system/predeploys.rs` `system_contract_specs`); implementation (b) holds the addresses it uses (`b:ledger.rs`, `b:keyless.rs`, `b:intercept.rs`, `b:satin_ext.rs`, `b:tx.rs` `SEQUENCER_REGISTRY_CODE_HASH`) and has no activation check ([QC-01](questions.md#qc-01)).
The six contracts' code hashes come from the `mega-system-contracts` crate (`LATEST_CODE_HASH` of each module); phase 2 writes them into the Satin pages after checking them against the artifacts and against the chain.

### Other contracts and protocol state

| Item | What Satin keeps | Source |
| --- | --- | --- |
| L1 block contract | OP's L1Block 1.6.0 (Isthmus) at `0x4200000000000000000000000000000000000015`, its DA footprint and operator fee scalars zero; Satin does not upgrade it | `satin.md §1` L89–L90 |
| EIP-2935 and EIP-4788 contracts | Their own code at their addresses; the pre-block calls run whatever code is there | `satin.md §18` L1212–L1213, L1231 |
| The registry's roles | What the registry holds, as `rex5InitialSequencer`, `rex5InitialAdmin` and `rex6MinRotationDelay` seeded it; Satin reads none of those keys | `satin.md` Node integrators L1526 |
| The Rex-era fixed system address | `MEGA_SYSTEM_ADDRESS` = `0xA887dCB9D5f39Ef79272801d05Abdf707CFBbD1d` (glossary); superseded by the registry's live system address since Rex5 | `docs/spec/glossary.md` "`MEGA_SYSTEM_ADDRESS`"; `a:system/tx.rs` |
| Accounts Rex-era keyless deployments left | A deploy address at nonce 1 with no code (a Rex6 deployment that returned empty code) collides with any later deployment there | `satin.md §15` L1095–L1096 |
| Addresses with nonce zero, empty code and storage | Can be in the state a block is given; a creation can land on them (no storage collision) | `satin.md §10` L716–L725 |
| Every account, slot and contract from earlier specs | Kept as state; earlier blocks keep their own spec's rules; contracts deployed earlier run under Satin's rules from `satinTime` ([QF-06](questions.md#qf-06)) | `satin.md` Safety and Compatibility L1563–L1566 |

### Genesis settings

The chain configuration gains one key, `satinTime`; every other setting is as in the Rex era (`satin.md` Node integrators L1539–L1553).
The base forks Satin runs on (Ethereum Shanghai to Osaka, Optimism Regolith to Karst) must be active by `satinTime`, and Jovian, Karst and Osaka no earlier (Node integrators L1555–L1559).
Implementation (a) reads the key in `a:block/genesis.rs` (`SatinChainConfig`) and checks the schedule in `a:block/hardfork.rs`; implementation (b) has no chain configuration ([QC-06](questions.md#qc-06)).

## 6. Code areas of both implementations, by rule area

| Rule area | Implementation (a) (`crates/mega-evm/src/`) | Implementation (b) (`next/`) |
| --- | --- | --- |
| Spec, base layer, opcode table | `evm/spec.rs`, `evm/instructions.rs`, `evm/host.rs`, `evm/context.rs`, `constants.rs` | `mega-evm2/src/lib.rs` (`satin_version`, `satin_table`), `op-evm2/src/spec.rs` |
| Gas schedule and intrinsic gas | `evm/schedule.rs`, `evm/prices.rs`, `evm/validation.rs` | `mega-evm2/src/lib.rs` (`satin_version`), `mega-evm2/src/tx.rs` (`adjust_intrinsic_gas`), evm2 `version/gas_params.rs` |
| Two pools, reservoir share, child merge, settlement | `evm/execution.rs`, `limit/ledger.rs`, `evm/result.rs` | `mega-evm2/src/ledger.rs` (`reservoir_share`, `pop_child`), `mega-evm2/src/tx.rs` (`before_initial_frame`, `settle_transaction`), evm2 `interpreter/gas.rs`, `evm/handler.rs` |
| State gas and SALT | `external/gas.rs`, `external/salt.rs`, `external/hasher/` | `mega-evm2/src/lib.rs` (`state_gas_price`, `reprice`), `mega-evm2/src/ledger.rs` (`multiplier`, `bucket_for`), `mega-evm2/src/salt_hash/`, evm2 `evm/config.rs` |
| History gas and allowance | `evm/history.rs`, `limit/mod.rs` | `mega-evm2/src/ledger.rs` (`charge_history`, `refill_history`), `mega-evm2/src/lib.rs` (`mega_log`, `sstore_completed`) |
| Gas forwarding | `evm/schedule.rs` (`FORWARD_REDUCTION_QUOTIENT`), `evm/execution.rs` | `mega-evm2/src/lib.rs` (`mega_call_impl`, `mega_create_impl`), evm2 `interpreter/instructions/system.rs` |
| Resource limits, frame budgets, order at a site | `limit/mod.rs`, `limit/limit.rs`, `limit/ledger.rs`, `limit/pool.rs`, `block/limit.rs` (`ProtocolLimits::for_spec`) | `mega-evm2/src/ledger.rs` (`Cfg`, `draw`, `draw_first_frame`, `hold_check`, `push_child`, `pop_child`), `mega-evm2/src/satin_ext.rs` (`hold_caller`) |
| Write records, data size, state growth | `limit/record.rs`, `evm/host.rs` | `mega-evm2/src/ledger.rs` (`changed`, `StartRecords`), `mega-evm2/src/lib.rs` (`count_start`, `mega_sstore`), evm2 `evm/state/account.rs` (`original`) |
| EIP-7702 authorizations before the first frame | `evm/execution.rs`, `evm/validation.rs` | `mega-evm2/src/eip7702.rs` (`simulate`, `execute`) |
| SELFDESTRUCT and the destruction table | `limit/record.rs` (`DestroyedParts`), `evm/host.rs` | `mega-evm2/src/lib.rs` (`mega_selfdestruct`, `beneficiary_read`) |
| Limit stops and outcomes | `limit/mod.rs` (`MegaLimitExceeded`, `LimitKind`), `evm/frame.rs`, `evm/result.rs` (`MegaTransactionOutcome::limit_stop`), `types.rs` | `mega-evm2/src/ledger.rs` (`stop_frame`, `revert_with`, `Settlement`), `mega-evm2/src/lib.rs` (`StartHooks`) |
| Gas detention | `access/detention.rs`, `access/volatile.rs`, `access/mod.rs`, `evm/instructions.rs`, `evm/precompiles.rs` (`PricedPrecompiles`) | `mega-evm2/src/detention.rs`, evm2 `evm/config.rs` (`gas_reserve`), `interpreter/instructions/reserve.rs`, `interpreter/instructions/account_load.rs` |
| Transfer logs | `limit/record.rs` (`emits_transfer_logs`) | evm2 `constants.rs` (`EIP7708_TRANSFER_TOPIC`), `mega-evm2/src/lib.rs` |
| Contract size limits and creation order | `constants.rs`, `evm/spec.rs`, the revm fork | `mega-evm2/src/lib.rs` (`satin_version`), evm2 `interpreter/instructions/system.rs` |
| Precompiles | `evm/precompiles.rs` | `mega-evm2/src/lib.rs` (`precompile_map`, `kzg100k`), `op-evm2/src/precompiles.rs`, evm2 `precompiles/` |
| Interception | `system/intercept.rs`, `evm/frame.rs` | `mega-evm2/src/intercept.rs`, `mega-evm2/src/lib.rs` (`StartHooks`) |
| Oracle reads and hints | `system/oracle.rs`, `external/oracle.rs`, `evm/host.rs`, `evm/state.rs` | `mega-evm2/src/lib.rs` (`mega_sload`), `mega-evm2/src/intercept.rs` (`hint_before`), `mega-evm2/src/satin_ext.rs` |
| KeylessDeploy | `system/keyless/` (`dispatch.rs`, `settle.rs`, `tx.rs`, `error.rs`, `mod.rs`) | `mega-evm2/src/keyless.rs` |
| MegaAccessControl and the refusal | `system/control.rs`, `access/detention.rs` | `mega-evm2/src/satin_ext.rs`, `mega-evm2/src/lib.rs` (`refuses_load`, `settle_refusal`) |
| MegaLimitControl | `system/limit_control.rs` | `mega-evm2/src/intercept.rs` (`remaining_compute_gas`) |
| SequencerRegistry and the live system address | `system/sequencer_registry.rs` | `mega-evm2/src/tx.rs` (`read_registry`, `live_system_address`) |
| Mega System Transactions, system-originated transactions | `system/tx.rs` | `mega-evm2/src/tx.rs` (`classify`, `prepare_legacy`, `check_system_sender`), `mega-evm2/src/ledger.rs` (`set_system_originated`) |
| Transaction validation | `evm/validation.rs`, `limit/mod.rs` | `mega-evm2/src/tx.rs` (`adjust_intrinsic_gas`), evm2's environment checks |
| Deposits and failed deposits | `evm/execution.rs`, the op-revm fork | `mega-evm2/src/tx.rs` (`prepare_deposit`, `execute_deposit_inner`, `failed_deposit`), `op-evm2/src/handler.rs` |
| System calls and the pre-block sequence | `block/eips.rs`, `block/executor.rs`, `evm/execution.rs` (`SYSTEM_CALL_REGULAR_GAS_LIMIT`) | `mega-evm2/src/block.rs` (`apply_pre_execution_changes`, `registry_due`), `mega-evm2/src/ledger.rs` (`begin_system_call`), evm2 `evm/system.rs` |
| Block limits and packing | `block/limit.rs`, `block/executor.rs`, `block/helpers.rs`, `block/result.rs` | `mega-evm2/src/block.rs` (`BlockLimiter`, `commit_transaction_outcome`) |
| Stateless witness | `evm/state.rs`, `block/l1_block_info.rs`, `block/eips.rs`, `block/executor.rs` | `mega-evm2/src/block.rs`, `mega-evm2/src/ledger.rs` (feature `witness`) |
| Activation and chain configuration | `block/hardfork.rs`, `block/genesis.rs`, `block/chain.rs`, `system/predeploys.rs` | none (`mega-evm2/src/block.rs` takes an `only_deposits` flag) |

## 7. Constants checked against both implementations

The accuracy rule of the writing rules asks every value to be verified against the implementation; here, against both.
"Same" means the value was found in both at the revisions above.

| Constant | Draft | (a) | (b) | Status |
| --- | --- | --- | --- | --- |
| `COST_PER_STATE_BYTE` | 1,530 (L346) | `constants.rs` 1,530 | `ledger.rs` `CPSB` 1,530 | Same |
| `COST_PER_HISTORY_BYTE` | 88 (L381) | `constants.rs` 88 | `ledger.rs` `CPHB` 88 | Same |
| `EXECUTION_CAP` | 200,000,000 (L166) | `constants.rs` `TX_GAS_LIMIT_CAP` | `ledger.rs` `EXECUTION_CAP` | Same |
| `MAX_CONTRACT_SIZE` / `MAX_INITCODE_SIZE` | 524,288 / 1,048,576 (L127–L128) | `constants.rs` | `lib.rs` `satin_version` | Same |
| `MIN_BUCKET_SIZE` | 256 (L347) | `external/salt.rs` | `ledger.rs` | Same |
| `TX_BODY_SIZE` (`TX_BASE_SIZE` + 5 × 40) | 310 (L387, L396) | `limit/mod.rs` 110 + 5 × 40 | `ledger.rs` 310 | Same |
| `WRITE_RECORD_SIZE` | 40 (L393) | `limit/mod.rs` | `ledger.rs` | Same |
| `AUTHORIZATION_SIZE` | 101 (L391) | `limit/mod.rs` | `eip7702.rs` | Same |
| Log bytes | 32 + 32 per topic + data (L392) | `limit/mod.rs` `LOG_BASE_SIZE`, `LOG_TOPIC_SIZE` | `lib.rs` `mega_log` | Same |
| Access-list sizes | 20 / 32 (L389–L390) | `limit/mod.rs` | not located | (b) to check in phase 2 |
| `TRANSFER_LOG_SIZE` / `HISTORY_ALLOWANCE_BYTES` | 160 / 160 (L539, L458) | `limit/mod.rs`, `evm/history.rs` | `ledger.rs` | Same |
| Frame share | 98/100 (L582) | `limit/mod.rs` `FRAME_DATA_SHARE_*` | `ledger.rs` `push_child` | Same (formula) |
| `TX_DATA_LIMIT`, `TX_KV_UPDATE_LIMIT`, `TX_STATE_GROWTH_LIMIT` | 13,107,200 / 500,000 / 1,000 (L533–L535) | `constants.rs` | configuration (`ledger.rs` `Cfg`) | (b) does not fix them ([QC-02](questions.md#qc-02)) |
| Block budgets | 13,107,200 / 500,000 / 1,000 (L1278–L1280) | `constants.rs` | `block.rs` `BLOCK_BUDGETS` | Same |
| Detention caps | 20,000,000 each (L954) | `constants.rs` | configuration (`ledger.rs` `Cfg`) | (b) does not fix them ([QC-02](questions.md#qc-02)) |
| Most compute a transaction can spend | 199,987,900 (L956) | `constants.rs` `MAX_TX_COMPUTE_GAS` | not present | Derived value; (b) needs none |
| `SYSTEM_CALL_REGULAR_GAS_LIMIT` | 30,000,000 (L1206) | `evm/execution.rs` | evm2 `evm/system.rs` `SYSTEM_CALL_GAS_LIMIT` | Same |
| `PRE_BLOCK_CALL_GAS_LIMIT` | 31,566,720 (L1210) | `constants.rs` | evm2 `evm/system.rs`: 30,000,000 plus `SYSTEM_MAX_SSTORES_PER_CALL` (16) fresh slots at the schedule's price | Same by construction |
| `KEYLESS_DEPLOY_OVERHEAD_GAS` | 100,000 (L1076) | `system/keyless/mod.rs` | `keyless.rs` `OVERHEAD` | Same |
| KZG point evaluation | 100,000 (L106) | `evm/precompiles.rs` `GAS_COST` | `lib.rs` `kzg100k` | Same |
| `P256VERIFY` | 6,900 (L108) | `evm/precompiles.rs` (test of the Osaka fee) | evm2 `precompiles/secp256r1.rs` | Same |
| OP input limits | 57,600 / 288,960 / 278,784 / 156,672 (L109–L112) | `evm/precompiles.rs` (from op-revm) | `op-evm2/src/precompiles.rs` | Same |
| The regular-gas entry table | L272–L309 | `evm/schedule.rs` (Amsterdam table of the revm fork) | `lib.rs` (Amsterdam table of evm2) | Not checked entry by entry; phase 2 checks each entry against both |

Implementation (a) marks every constant provisional, "a placeholder until the economics sign-off fixes the numbers" (`a:constants.rs`); see [QG-03](questions.md#qg-03).

## 8. What the cross-checks recorded

Three rounds of two-sided review ran implementation (b) against implementation (a) on inputs no fixed test held, and judged every difference against the draft.
Their results that bear on the specification:

- **Differences fixed toward the draft.** The start record charged at runtime rather than in validation (`satin.md §4` L213, `satin.md §5` L322, `satin.md §7` L402–L405); a deposit's start decided only after its created caller is paid (L321–L326, L1391); a SELFDESTRUCT's volatile reads committed after its last fallible step (L941); CREATE2's salt popped after the initcode and memory charges (L131–L133, fixed in the evm2 fork); the keyless value overhead decided under detention first (L1076–L1077, L981–L982); the Oracle read in a pre-block system call (L1150, L1230–L1232); the first frame held over a limit before it starts (L758–L780, L902–L903); a keyless signer that is the sender charged its nonce record only when the transaction had not changed it (L554, L1089, L1114); the transaction's spill unwound by the first frame's returned reservoir (L148–L159); a block without a parent beacon block root refused (L1217).
- **Differences still open in (b) at `785182eb`**: [QC-03](questions.md#qc-03), [QC-04](questions.md#qc-04), [QC-05](questions.md#qc-05).
- **Both implementations against the draft**: [QD-01](questions.md#qd-01) (the short authorization-list fast path, L786–L800) and [QE-01](questions.md#qe-01) (ModExp over EIP-7823's bound, L975–L978).
- **Points the draft leaves silent, decided in the implementations by following (a)**: [QE-02](questions.md#qe-02), [QE-03](questions.md#qe-03), [QA-08](questions.md#qa-08).
- **Accepted label-only and inspector-only differences**: [QA-01](questions.md#qa-01), [QA-02](questions.md#qa-02).
- **Verification gaps** (not questions for the owner, but rules phase 2 cannot yet back with a two-sided check): the activation block's deposit-only admission is outside the differential checks; no check carries state from one transaction into the next of a block; a creation transaction whose created address is the beneficiary was not drawn before the latest round; refusals carry no read set in the synthetic checks, so the reads a validation refusal makes are compared only on recorded blocks.
