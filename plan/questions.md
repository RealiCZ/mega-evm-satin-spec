# Satin Specification — Questions for the Owner

Everything the owner had to decide before the specification text of the Satin section was written.
Every item below carries the owner's **Decision** (8 November 2026), also listed in [decisions.md](decisions.md); [QG-07](#qg-07), added while the execution pages were written, was decided on 9 November 2026, with the two items of (h) the review of the written section raised.
Each item gives its evidence, the options, a recommendation where the evidence supports one, and **Change needed**: which implementation would have to change under each option — (a) is mega-evm `5e3f30ad` (`crates/mega-evm/src/`, written `a:`), (b) is the `next/` workspace at mega-evm `785182eb` (`next/mega-evm2/src/`, written `b:`; `op:` for `next/op-evm2/src/`, `evm2:` for the evm2 fork at `91518705`).
Line numbers are of `docs/spec/upgrades/satin.md` (the draft).
**Outline** names the rules of [outline.md](outline.md) whose text waits on the answer.

| Category | Items |
| --- | --- |
| (a) Behaviour an implementation has that no source states | 10 |
| (b) The draft against implementation (a) | 2 |
| (c) The draft against implementation (b) | 6 |
| (d) Both implementations agree, the draft says otherwise | 1 |
| (e) Open points the cross-checks recorded | 3 |
| (f) Layout | 9 |
| (g) Writing policy | 7 |
| (h) Raised by the review of the written section | 2 |
| Total | 40 |

## (a) Behaviour an implementation has that no source states

### QA-01

**What a tracer sees for a first frame whose runtime gas phase cannot be paid.**

- Evidence: when a transaction's own first frame runs out of gas in its runtime gas phase (before any instruction), (b) reports one halted root frame to an inspector, as evm2 pull request #871 and go-ethereum's `haltTopFrame` do, for legacy, EIP-2930, EIP-1559 and deposit envelopes (`b:tx.rs` `settle_first_frame`); its EIP-7702 path settles the same case with no frame (`b:eip7702.rs` `execute`); (a) opens no frame.
  Outcome, gas, state and read set are equal on both; only the inspector differs. The draft says nothing about tracing.
- Options: (1) the specification does not cover what an inspector sees (tracing is outside the verifiable behaviour); (2) it specifies one halted root frame; (3) it specifies none.
- Recommendation: (1), stated once on `satin/evm/outcomes.md` as out of scope.
- Change needed: (1) none; (2) (a), and (b)'s EIP-7702 path; (3) (b).
- Outline: `SATIN-OUT-017`.
- **Decision**: (1): what a tracer or inspector is shown is outside the specification, stated once as `SATIN-OUT-017`. Reason: Tracing changes no outcome, gas figure, state or read set.

### QA-02

**The halt reason of a failed `DUP`, `DUPN`, `SWAPN` or `EXCHANGE`.**

- Evidence: a `DUP1`–`DUP16` or `DUPN` deeper than the stack halts as `StackOverflow` on (a) (revm maps every failed `DUP` to overflow) and as `StackUnderflow` on (b); an EIP-8024 immediate that the EIP rejects halts as `OpcodeNotFound` on (a) and as `InvalidImmediateEncoding` on (b) (`evm2:interpreter/instructions/stack.rs`).
  Gas, output and state are equal; the label is not in a receipt. The draft names no halt reason.
- Options: (1) the specification names no halt reason (a halt is a halt); (2) it names them, and the side that differs changes.
- Recommendation: (1).
- Change needed: (1) none; (2) (a) for the `DUP` label (b's is the accurate one) and one side for the immediate label.
- Outline: `SATIN-OUT-018`.
- **Decision**: (1): the specification names no halt reason (`SATIN-OUT-018`). Reason: A halt's label is in no receipt and changes no state.

### QA-03

**The order, and the error kinds, of the inherited validation checks relative to Satin's own.**

- Evidence: the draft orders Satin's checks (body against the data-size limit, intrinsic regular gas, floor, execution cap, intrinsic plus body history; L217) but not the base layer's environment checks around them.
  (a) runs revm's order (chain id, gas cap, per-type fee and list checks, block gas limit, initcode); (b) runs evm2's (priority fee, gas price, chain id, cap, block gas limit, initcode, nonce overflow), with Satin's body check after them and the floor before the history-inclusive intrinsic check.
  A transaction failing two checks at once is refused by both, under different error kinds.
- Options: (1) the specification fixes only which transactions are refused, not which error is named when several checks fail; (2) it fixes the full order, and one implementation changes.
- Recommendation: (1), keeping the draft's order of Satin's own checks as normative since it names the error a pool reports.
- Change needed: (1) none; (2) (a) or (b).
- Outline: `SATIN-VAL-003`, `SATIN-VAL-007`.
- **Decision**: (1): the specification fixes which transactions are refused, not which error names a transaction that fails several checks; the order of Satin's own checks stays normative. Reason: Only the refusal is consensus; the error a pool reports follows Satin's own order.

### QA-04

**The function that maps an account or a slot to its SALT bucket.**

- Evidence: a state charge is priced by the multiplier of "the SALT bucket the state lands in" (L347, L349–L355), and the witness exports buckets by id (L1414–L1421), but no source defines the mapping.
  (a) takes it from the node (`a:external/salt.rs` `bucket_id_for_account`, `bucket_id_for_slot`; production hasher in `a:external/hasher/`); (b) uses an FNV-1a test hasher by default and the production hasher only with the `salt-ahash` feature (`b:ledger.rs` `bucket_id`, `b:salt_hash/`), which its continuous integration never builds.
  The two agree only while every bucket is at the minimum size.
- Options: (1) the Satin section defines the mapping (the key encoding of an account and a slot, the hash, the bucket count and the meta-bucket offset); (2) it references SALT's own definition as an external input, as it does for capacities.
- Recommendation: (1) or (2), but in either case stated: two nodes hashing differently price differently.
- Change needed: (b) makes the production hasher its default under either option.
- Outline: `SATIN-STATE-010`.
- **Decision**: (2): the bucket mapping is SALT's own definition, an input to the specification (`SATIN-STATE-010`); (b) makes SALT's production hasher its default. Reason: The mapping is SALT's, as the capacities are; two hashers price differently.

### QA-05

**Which number `SLOTNUM` pushes on MegaETH.**

- Evidence: the draft says the node supplies the slot number with the block, and a block without one runs with zero (L77–L78, L1402–L1403); (a) and (b) push what they are given (`a:evm/host.rs` `slot_num`; `b:lib.rs` `satin_table`). No source says what number a MegaETH node supplies for a block (EIP-7843 defines it from the beacon chain's slot).
- Options: (1) always zero on MegaETH; (2) a value derived from the block (for example from its timestamp), defined in the Satin section; (3) an input of the block, defined outside the specification.
- Change needed: none in the engines under any option; the node and the derivation pipeline under (1) and (2).
- Outline: `SATIN-BASE-005`, `SATIN-WIT-010`.
- **Decision**: (1): `SLOTNUM` pushes zero, and stays a volatile read. Reason: MegaETH has no slot; the OP Stack hard-codes zero.

### QA-06

**A separate per-frame data-size cap.**

- Evidence: the draft sets "no further per-frame cap" (L608). (a) keeps a knob for one (`a:limit/mod.rs` `EvmTxRuntimeLimits`, `with_frame_data_size_limit`), unlimited under Satin; (b) has none.
- Options: (1) the specification has no such cap and (a)'s knob is an implementation detail outside it; (2) the knob is removed from (a).
- Recommendation: (1); whether (a) keeps the knob is a code decision.
- Change needed: none for (1); (a) for (2).
- Outline: `SATIN-LIM-009`.
- **Decision**: (1): no per-frame cap beyond the frame budgets (`SATIN-LIM-009`); (a)'s knob is an implementation detail. Reason: The knob is unlimited under Satin and specifies nothing.

### QA-07

**A deposit that carries a gas price.**

- Evidence: an OP deposit has no gas price. (a)'s transaction environment would keep one and refund unused gas at it; (b)'s deposit envelope has none. No source states which, and neither the differential inputs nor the chain contain such a deposit.
- Options: (1) the specification says a deposit is priced at zero whatever its envelope carries; (2) such an envelope is malformed and outside the specification.
- Recommendation: (2), as the OP specification has it.
- Change needed: none.
- Outline: `SATIN-DEP-013`.
- **Decision**: (2): a deposit envelope that carries a gas price is malformed and outside the specification. Reason: The OP specification has no deposit gas price.

### QA-08

**A creation transaction from a sender at nonce 2^64 − 1 when the nonce check is off.**

- Evidence: block execution checks the nonce, so no block reaches this; an RPC simulation with the nonce check off does. (a) answers a creation whose nonce cannot be bumped with a success that creates nothing; (b) deploys at the address of nonce 2^64 − 1 for types 0, 1 and 2 (evm2's `prepare_initial_frame`); for deposits, which a block can reach, both answer as (a) does.
  The draft covers a frame start whose creator nonce cannot be bumped (L781) and asks simulations to follow block rules (L849), but says nothing of a top-level creation transaction.
- Options: (1) state that a creation transaction whose sender's nonce cannot be bumped creates nothing (as L781 for a start); (2) leave executions with the nonce check off outside the specification.
- Recommendation: (1), since it costs one sentence and matches the deposit rule.
- Change needed: (1) (b); (2) none.
- Outline: `SATIN-LIM-015`, `SATIN-DEP-010`.
- **Decision**: (1): a creation transaction whose sender's nonce cannot be bumped creates nothing (`SATIN-LIM-015`). Reason: One sentence, and it matches the deposit rule.

### QA-09

**When the SequencerRegistry has a role change due.**

- Evidence: the pre-block step calls `applyPendingChanges()` when a change is due (L1219); the Rex page says "when a pre-check confirms any role change is due" (`docs/spec/system-contracts/sequencer-registry.md` "Pre-Block Apply"). Neither says what the pre-check reads.
  Both implementations read the registry's pending slots (pending system address and its activation block, pending sequencer and its activation block) and call when a pending value is non-zero and its activation block is at most the block's number (`a:system/sequencer_registry.rs` `is_apply_pending_changes_due`; `b:block.rs` `registry_due`), and that read lands in the witness (L1399).
- Options: (1) the Satin section states the predicate at the storage level (the slots and the comparison), since the witness carries those slots; (2) it states it at the contract level ("a pending change whose activation block has come").
- Recommendation: (1).
- Change needed: none.
- Outline: `SATIN-PBLK-004`.
- **Decision**: (1): the due-change predicate is stated at the storage level. Reason: The witness carries those slots.

### QA-10

**Rex-era rules the draft neither restates nor drops.**

- Evidence: the draft says a Rex6 rule it does not carry over does not apply under Satin (L31–L32). Several Rex-era rules about the system contracts are kept by both implementations but never mentioned in the draft: the interceptors' call-depth gate and its priority over a resource-limit overflow (`docs/spec/system-contracts/interception.md` "Call-Depth Gate"), `NonZeroTransfer()` for a valued call to an intercepted method ("Interception Outcomes"), the contracts' interfaces, storage layouts and read methods, the High-Precision Timestamp's service semantics, MegaLimitControl's address and scope, and the distinction between system contracts and precompiles.
  Read literally, L31–L32 drops all of them; the brief that Rex-era contracts must keep working, and both implementations, keep them.
  The call-depth gate's priority rule names a Rex6 halt that Satin no longer has.
- Options: (1) the Satin section restates every such rule as Satin's, each verified against both implementations, and L31–L32 is read as "a Rex6 execution rule that Satin replaces"; (2) each is decided one by one.
- Recommendation: (1), with the call-depth priority rule rewritten for the revert-class stop and checked against both implementations.
- Change needed: none known; phase 2 checks each rule against both.
- Outline: `SATIN-SYSC-004`, `SATIN-ICPT-002`, `SATIN-ICPT-003`, `SATIN-HPTS-002`, `SATIN-MLC-001`.
- **Decision**: (1): every Rex-era rule both implementations keep is restated as Satin's. Reason: A Satin page never relies on a Rex-era page.

## (b) The draft against implementation (a)

### QB-01

**The second half of the schedule check.**

- Evidence: the draft requires a node to refuse a configuration that activates Jovian, Karst or Osaka before `satinTime`, "a half the reference implementation does not check" (L1558); (a)'s `validate_schedule` refuses only a base fork that is not active by `satinTime` (`a:block/hardfork.rs`). (b) has no schedule (QC-06).
- Options: (1) keep the rule and add the check to (a) (and to whichever implementation ships); (2) keep the rule as a node obligation outside the executor; (3) drop the rule, since every block before `satinTime` runs the legacy engine on Isthmus whatever the configuration says.
- Change needed: (1) (a), and (b) if it ships; (2), (3) none.
- Outline: `SATIN-ACT-003`.
- **Decision**: (3): the schedule's second half-check is dropped from the specification. Reason: It is not the execution layer's job.

### QB-02

**Deposit-only activation blocks enforced only when the executor is told.**

- Evidence: a non-deposit transaction in an activation block makes the block invalid (L80, L1349, L1366), but block execution does not work this out: it is told, refuses only when told, and an execution not told accepts such a block (L1506–L1512).
  (a) takes the flag from its caller (`a:block/executor.rs` `with_no_user_tx_activation_block`); (b) takes `only_deposits`, false by default (`b:block.rs`), and neither differential check runs it on.
  So block validity depends on a caller remembering a flag.
- Options: (1) keep the rule as block validity and require the executor to derive the flag from the schedule and the parent timestamp it is given; (2) keep the split as the draft has it, with the rule on the derivation node and builders.
- Recommendation: (1): a validity rule should not depend on a flag a caller can forget.
- Change needed: (1) (a) and (b); (2) none.
- Outline: `SATIN-BASE-006`, `SATIN-ACT-004`, `SATIN-ACT-010`.
- **Decision**: (1): the executor derives whether a block admits only deposits from the schedule and the parent timestamp. Reason: A validity rule must not depend on a flag a caller can forget.

## (c) The draft against implementation (b)

### QC-01

**The activation block's predeploy check.**

- Evidence: Satin's activation block reads the six system contracts and the EIP-7997 factory and is invalid unless each holds exactly the expected code (L1221–L1228, L1365). (a) makes the check (`a:system/predeploys.rs` `check_system_contract`); (b)'s pre-block step does not ("no activation block: the predeploy check is not made", `b:block.rs` `apply_pre_execution_changes`).
- Options: (1) keep the rule; (2) drop the check from the specification.
- Recommendation: (1): it is how Satin fails closed on a chain without the contracts.
- Change needed: (1) (b); (2) (a).
- Outline: `SATIN-PBLK-003`, `SATIN-ACT-005`, `SATIN-SYSC-003`.
- **Decision**: (1): the activation block's predeploy check stays. Reason: It is how Satin fails closed on a chain without the contracts.

### QC-02

**Per-transaction limits and detention caps as configuration.**

- Evidence: the draft fixes the transaction limits, the frame share and the detention caps per spec, never as configuration (L844–L848, L955). (a) holds them in `ProtocolLimits::for_spec` (`a:block/limit.rs`); (b) takes the three transaction limits and both caps from a node-supplied `Cfg` (`b:ledger.rs`; its derived default is zero, not Satin's values), and fixes only the block budgets (`b:block.rs` `BLOCK_BUDGETS`).
- Options: (1) keep the rule; (2) let a node configure them.
- Recommendation: (1).
- Change needed: (1) (b) fixes the values in the engine; (2) (a).
- Outline: `SATIN-LIM-001`, `SATIN-LIM-017`, `SATIN-DET-012`, `SATIN-DET-013`.
- **Decision**: (1): the transaction limits, the frame share and the detention caps are protocol values (`SATIN-LIM-017`, `SATIN-DET-013`). Reason: A limit is part of block validity.

### QC-03

**A creation transaction whose created address is the block beneficiary.**

- Evidence: the transaction is detained from its start on (b), because (b) tests the message's target and code address, which evm2 sets to the derived address for a creation; on (a) it is not, since only a sender, a call's recipient or an applied authority that is the beneficiary detains from the start (L939), and a creation is never a read (L944). At the default cap a constructor that calls `remainingComputeGas()` sees different values.
  Reaching it needs a beneficiary equal to a sender's next creation address, an operator's choice.
- Options: (1) keep the draft (no detention); (2) detain, and change the draft.
- Recommendation: (1).
- Change needed: (1) (b); (2) (a).
- Outline: `SATIN-DET-006`, `SATIN-DET-008`.
- **Decision**: (1): a creation whose created address is the beneficiary is not detained from its start (`SATIN-DET-006`, `SATIN-DET-008`). Reason: A creation's loads are its own checks, not volatile reads.

### QC-04

**A keyless deployment with EIP-3607 disabled.**

- Evidence: step 9 refuses a signer with code "unless EIP-3607 is disabled" (L1084). (a) skips the load and the refusal when it is disabled; (b) loads and refuses regardless (`b:keyless.rs` `run`). Blocks run with EIP-3607 on, so only a simulation or an embedding reaches it.
- Options: (1) keep the draft; (2) make step 9 unconditional.
- Change needed: (1) (b); (2) (a).
- Outline: `SATIN-KEY-005`.
- **Decision**: (1): the draft is kept — with EIP-3607 disabled, step 9 of a keyless deployment neither loads the signer's code nor refuses it; (b) changes. Reason: A disabled EIP-3607 disables its check, here as for any sender.

### QC-05

**A precompile address that holds an EIP-7702 delegation.**

- Evidence: under detention a call is decided from "the precompile's price" (L975). (b) prices by the call's code address, so a precompile address holding a delegation is priced by its delegate and not held (`b:detention.rs` `precompile_price_of`); (a) and evm2's own dispatch key on the called address. No chain can produce the prestate: a precompile has no key to sign an authorization.
- Options: (1) state that a precompile address runs and is priced as the precompile whatever code it holds; (2) leave the prestate outside the specification.
- Recommendation: (1).
- Change needed: (1) (b); (2) none.
- Outline: `SATIN-PCMP-008`, `SATIN-DET-021`.
- **Decision**: (1): a precompile address runs and is priced as the precompile whatever code it holds (`SATIN-PCMP-008`). Reason: Every node then dispatches the same call the same way.

### QC-06

**Chain configuration and the fork schedule in (b).**

- Evidence: the draft defines the `satinTime` key, its format, the refused keys and the schedule check (Node integrators L1539–L1559); (a) implements them (`a:block/genesis.rs`, `a:block/hardfork.rs`); (b) has no chain configuration, no schedule and no activation logic, its block executor being told what it needs.
- Options: (1) the chain configuration is part of the specification (then (b) or its node needs it); (2) it is node documentation (QG-05).
- Change needed: (1) (b); (2) none.
- Outline: `SATIN-BASE-007`, `SATIN-ACT-002`.
- **Decision**: (1), which QG-05's decision implies (the question has no recommendation of its own): the chain configuration's consensus parts are in the specification. Reason: The configuration key and schedule decide which blocks run Satin.

## (d) Both implementations agree, the draft says otherwise

### QD-01

**A short authorization list's fast path.**

- Evidence: before the first frame the draft decides the list by a simulation in which every entry that passes the chain-id, nonce and signature gates loads its authority's account with its code, each distinct authority once, the whole list walked (L786–L800); the witness holds every authority the simulation loaded (L826, L1391).
  Both implementations take a fast path for a short list that skips the full preflight load of every authority, and agree with each other on it.
- Options: (1) the specification allows the fast path and states exactly which authorities it loads (and so which the witness holds); (2) both implementations make the full preflight.
- Change needed: (1) none; (2) (a) and (b).
- Outline: `SATIN-AUTH-003`, `SATIN-AUTH-005`, `SATIN-WIT-004`.
- **Decision**: (2): every authority whose entry passes the chain-id, nonce and signature gates is loaded by the list simulation, for every list; no short-list fast path (`SATIN-AUTH-001`, `SATIN-AUTH-005`). Reason: The accounts a transaction loads, and so its witness, must not depend on the list's length or on where an out-of-gas falls.

## (e) Open points the cross-checks recorded

### QE-01

**The price of a ModExp input over EIP-7823's bound.**

- Evidence: the draft says an input over a size limit is priced at zero, since it is refused before any gas check (L977), and decides a call under detention from the price (L975–L978). For ModExp both implementations charge the 500 minimum first, then refuse an Osaka input over EIP-7823's 1,024-byte bound, and only then price by the formula (revm's order; the evm2 fork was changed to it, `evm2:precompiles/modexp.rs`). So under detention both decide such a call by 500, not by zero.
  This is also a case of (d): both agree against L977.
- Options: (1) state the 500 minimum for ModExp's over-bound input (and that the bound is checked before the formula price); (2) keep "priced at zero" and change both.
- Recommendation: (1).
- Change needed: (1) none; (2) (a) and (b).
- Outline: `SATIN-DET-023`, `SATIN-PCMP-007`.
- **Decision**: Neither option: ModExp charges its formula price and then checks EIP-7823's bound, as evm2 upstream #874 and go-ethereum order it; an over-bound input is priced by its formula, not at zero or at 500 (`SATIN-PCMP-007`, `SATIN-DET-023`). Reason: The price detention reads is then the price the call is charged.

### QE-02

**Whether a deposit that fails before its first frame loads its recipient.**

- Evidence: a deposit that cannot pay its created caller's state gas, or fails its intrinsic check, becomes a failed deposit before its first frame (L322, L326, L1338). The witness holds what the block loads, and a read gas skipped loads nothing (L1391, L1440). Neither says whether such a deposit loads its recipient (or a delegated sender's code).
  Both implementations load neither (in (b) since the cross-checks: `b:tx.rs` `prepare_deposit`, `park_start`).
- Options: (1) state it: a deposit that fails before its first frame loads nothing of its recipient, and a sender's code only once its intrinsic and floor checks passed; (2) leave it to the general witness rule.
- Recommendation: (1): the read set is consensus for a stateless validator.
- Change needed: none.
- Outline: `SATIN-DEP-012`.
- **Decision**: (1): a deposit that fails before its first frame loads nothing of its recipient. Reason: The read set is consensus for a stateless validator; both implementations agree.

### QE-03

**A failed deposit whose mint would overflow its sender's balance.**

- Evidence: a failed deposit "credits its mint" (L1338). Both implementations credit with a checked add and leave a balance that cannot hold the mint as it was, as op-revm does (`b:tx.rs` `failed_deposit`); op-geth wraps; the success path saturates (op-revm and op-evm2). No chain holds the prestate (a mint is far below 2^128).
- Options: (1) a checked credit (the balance stays); (2) a wrapping credit; (3) declare a balance that cannot hold the mint an invalid prestate, for both deposit paths.
- Recommendation: (1), stated in one sentence.
- Change needed: (1) none; (2) (a) and (b); (3) none.
- Outline: `SATIN-DEP-011`.
- **Decision**: (3): a prestate in which a deposit's sender balance plus its mint exceeds 2^256 − 1 is invalid and outside the specification, for successful and failed deposits alike; no implementation changes. Reason: Unreachable: all ether is about 1.2 × 10^26 wei.

## (f) Layout

### QF-01

**Rex7: does Satin succeed Rex6 or Rex7?**

- Evidence: `main` at `d4c913c5` has no `upgrades/rex7.md`: Rex7 was removed from `main` by pull request #402 ("remove REX7 and refresh stale docs", commit `f78e75c6`, an ancestor of `d4c913c5`, which is also the legacy engine's pin), after the documentation commit "remove Rex7; Satin follows Rex6 as the one unstable spec". The Satin draft follows Rex6 (L31), and (a) refuses `Rex7` as a spec name.
  So there was no `rex7.md` to keep; this repository has none.
- Options: (1) Satin succeeds Rex6 and the ladder has no Rex7 (the state of `main` and the draft); (2) restore a Rex7 upgrade page from history as a withdrawn rung.
- Recommendation: (1).
- Change needed: none.
- Outline: `SATIN-ACT-001`.
- **Decision**: (1): Satin succeeds Rex6; there is no Rex7. Reason: The state of `main` and of the draft.

### QF-02

**The Satin section's place, groups and file names.**

- Evidence: this repository puts it at `docs/spec/satin/` with `evm/`, `system-contracts/` and `block/` groups, file names matching the Rex pages they succeed, plus pages Rex has no counterpart for (`base-layer.md`, `state-gas.md`, `history-gas.md`, `authorizations.md`, `limit-stops.md`, `outcomes.md`, `transfer-logs.md`, and the six `block/` pages). The writing rules say how the section moves up when Satin is frozen (`docs/spec/AGENTS.md` "Sealing Satin").
- Options: (1) as laid out; (2) another directory name, or a flat section.
- Change needed: none.
- **Decision**: (1): the section's place, groups and file names as laid out. Reason: As recommended.

### QF-03

**How maturity is shown on Satin pages.**

- Evidence: the writing rules require `<details>` blocks for unstable content, which cannot carry a whole standalone section; this repository uses frontmatter `spec: Satin` and `maturity: unstable` and a warning hint at the top of every Satin page instead (`docs/spec/AGENTS.md` "Maturity While Unstable").
- Options: (1) as amended; (2) another frontmatter field or none, with the hint only.
- Change needed: none.
- **Decision**: (1): `spec: Satin`, `maturity: unstable` and a warning hint on every Satin page. Reason: A `<details>` block cannot carry a standalone section.

### QF-04

**The role of `upgrades/satin.md` while the section is written.**

- Evidence: the draft calls itself "the Satin specification" and says it states the rules normatively while the concept pages describe Rex6 (L7–L8); the upgrade-page rules require an informative summary. Option B makes the Satin section the specification and the draft the reviewers' delta. Phase 1 keeps the draft unchanged.
- Options: (1) keep the draft frozen until the section is written, then rewrite it as the informative delta; (2) update it alongside each Satin page.
- Recommendation: (1), so the section is written from one fixed source.
- Change needed: none.
- **Decision**: (1): the draft stays frozen until the section is written, then becomes the informative delta. Reason: The section is written from one fixed source.

### QF-05

**The Satin glossary entries.**

- Evidence: the draft links six glossary anchors `main`'s glossary lacks (`execution-cap`, `reservoir`, `state-gas`, `history-gas`, `write-record`, `history-allowance`); this repository adds short entries for them, marked unstable, with values checked against both implementations. #409's longer entries restate rules, which the glossary should not.
- Options: (1) keep the short entries and add terms in phase 2 (limit stop, withheld gas, live system address, failed deposit, system-originated); (2) other wording.
- Change needed: none.
- **Decision**: (1): short glossary entries, more terms added as the section needs them. Reason: The glossary defines terms, not rules.

### QF-06

**The backward-compatibility statements.**

- Evidence: `overview.md` and `hardfork-spec.md` say that a new spec "may add behavior" and that "contracts deployed under a given spec will continue to behave identically, regardless of future upgrades"; `system-contracts/overview.md` says a frozen spec's system-contract behaviour stays unchanged. Satin leaves Rex-era blocks unchanged (L1563), but a contract deployed under Rex6 runs under Satin's prices, pools, `GAS` value and transfer logs from `satinTime` on: it keeps working, not behaving identically. This repository leaves those sentences as they are.
- Options: (1) reword them to say that a spec never changes how earlier blocks execute and that contracts keep working under later specs; (2) keep them and qualify Satin as a restatement.
- Recommendation: (1).
- Change needed: none.
- Outline: `SATIN-ACT-008`.
- **Decision**: (1): the backward-compatibility statements are reworded: a spec never changes earlier blocks, and contracts keep working. Reason: Contracts deployed under Rex6 run under Satin's prices.

### QF-07

**The reference implementation named on the overview page.**

- Evidence: `overview.md` names mega-evm on revm 40.0.3 and op-revm 20.0.0; the draft's edit of it (not taken here) would name revm 27.1.0, op-revm 8.1.0 and alloy-evm 0.15.0, older than `main`'s, and adds a Satin note naming the revm fork commits. Two Satin implementations exist and one will ship.
- Options: (1) name no Satin reference implementation until one is chosen; (2) name both as candidates.
- Recommendation: (1).
- Change needed: none.
- **Decision**: (1): no Satin reference implementation is named. Reason: Two implementations exist and one will ship.

### QF-08

**Pages that gather rules other pages own.**

- Evidence: `satin/evm/outcomes.md` (halts, reverts and stops) and `satin/block/deposits.md` gather, from many draft sections, rules whose detail also lives on another page (the limit-stop page, the gas pages, validation).
- Options: (1) each rule has one home, and the gathering pages state the unified rule and link the detail; (2) the gathering pages restate the detail with the same ids.
- Recommendation: (1), so a rule is never stated twice.
- Change needed: none.
- **Decision**: (1): each rule has one home; a gathering page states the unified rule and links the detail. Reason: A rule is never stated twice.

### QF-09

**Adopting the rule-id scheme.**

- Evidence: [rule-ids.md](rule-ids.md) proposes `SATIN-<AREA>-<NNN>`, written as leading inline code, never renumbered, with the citation forms for tests and fixtures; the outline assigns 384 ids over 31 areas.
- Options: (1) adopt as proposed; (2) adopt with other area codes or another placement; (3) no ids.
- Change needed: none in phase 2; the implementations' tests cite ids afterwards.
- **Decision**: (1): the rule-id scheme is adopted. Reason: Tests and fixtures cite rules by id.

## (g) Writing policy

### QG-01

**Standalone text or references for EIP-8037.**

- Evidence: the draft applies EIP-8037 "as of commit `c406bdb2ff`" with later commits taken and declined (L146–L163, L225–L249), and states Satin's departures; it does not restate the EIP's mechanics (pool accounting, the system-call reservoir, the revert give-back).
  The brief asks for a standalone definition of current behaviour.
- Options: (1) restate every EIP-8037 rule Satin executes, in the Satin section, citing the EIP for provenance; (2) cite the EIP at its commit and restate only Satin's profile and departures.
- Recommendation: (1) for the rules a transaction's outcome depends on.
- Change needed: none.
- Outline: `SATIN-POOL-001`.
- **Decision**: (1): every EIP-8037 rule a transaction's outcome depends on is restated, the EIP cited for provenance. Reason: The section is standalone.

### QG-02

**EIP revisions the draft does not pin.**

- Evidence: the draft pins only EIP-8037. It applies the Amsterdam schedule with EIP-8038, EIP-2780, EIP-7976 and EIP-7981 (L262), EIP-7708 (L1042), EIP-8024 and EIP-7843 (L76), EIP-7951 (L108) and EIP-7623 (L208), several of them drafts that keep changing; the implementations follow whatever revision their revm and evm2 forks carry.
- Options: (1) pin each to a commit as EIP-8037 is, and check both forks against it; (2) restate their rules in the Satin section (QG-01 option 1), making the revision moot.
- Change needed: (1) whichever fork differs from the pinned revision.
- Outline: `SATIN-BASE-001`, `SATIN-BASE-004`, `SATIN-POOL-020`, `SATIN-SCHED-001`, `SATIN-SCHED-003`, `SATIN-LOG-001`, `SATIN-PCMP-003`.
- **Decision**: (1): each EIP the section applies is pinned to a commit; the commits are an open item ([QG-07](questions.md#qg-07)). Reason: Draft EIPs keep changing.

### QG-03

**Provisional values.**

- Evidence: (a) marks every constant "provisional: a placeholder until the economics sign-off fixes the numbers" (`a:constants.rs`); the draft states the values as rules and says any value may change before Satin is frozen (L12).
- Options: (1) write the current values, as the draft does; (2) write named constants only, with values once signed off.
- Recommendation: (1); the warning hint already says values may change.
- Change needed: none.
- **Decision**: (1): the current values are written. Reason: The unstable hint already says values may change.

### QG-04

**Implementation-specific statements in the draft.**

- Evidence: the writing rules forbid implementation details in the specification, but the draft carries several as rules or as the way a rule is met: error type names (`MegaBlockExecutionError::UnexpectedSystemContractCode`, L1226; `StaleOutcome`, L1529), APIs (`LimitStop::from_result`, `MegaTransactionOutcome::limit_stop`, L1538; `MegaEvm::with_dyn_precompiles`, L1489; `State::set_state_hook`, L1517; `Database::basic`, L1521; `MegaBlockExecutionCtx::satin_activation_block`, L1511), a build feature (`mega-evm/satin-price-override`, L1485), and orders explained by "revm's creation opcode" (L436, L944). It also leaves precompiles a node adds or replaces outside the specification (L988–L991).
- Options: (1) restate each as behaviour (what a node does, not which type it uses), and move the rest to node documentation; (2) keep them where the draft has them.
- Recommendation: (1).
- Change needed: none.
- Outline: `SATIN-DET-027`, `SATIN-ACT-009`.
- **Decision**: (1): implementation-specific statements are restated as behaviour; the rest goes to node documentation. Reason: The specification describes behaviour, not code.

### QG-05

**Node-integrator content.**

- Evidence: "Node integrators" (L1479–L1559) holds rules for nodes outside block execution: what a transaction pool can check without state, the chain configuration's key format and its refused keys, the derivation node's and builders' duties for activation blocks, the checked commit of a delayed outcome, and how a node reports a stop.
- Options: (1) the Satin section specifies the parts that decide consensus (the configuration key and schedule, activation-block validity, the stale-commit refusal) and leaves pool and RPC behaviour to node documentation; (2) all of it in the specification; (3) none of it.
- Recommendation: (1).
- Change needed: none.
- Outline: `SATIN-VAL-009`, `SATIN-ACT-002`.
- **Decision**: (1): the node-integrator parts that decide consensus are in the specification; pool and RPC behaviour is node documentation. Reason: Only consensus belongs in the specification.

### QG-06

**Executions outside a block.**

- Evidence: the draft recommends, without requiring, that a call, gas estimate or simulation use the block's limits and caps, and that a node using others does so as its own policy (L849–L850).
- Options: (1) keep it as a recommendation in the Satin section; (2) move it to node documentation, the specification covering block execution only.
- Change needed: none.
- Outline: `SATIN-LIM-018`.
- **Decision**: (2): executions outside a block are node documentation; `SATIN-LIM-018` is retired. Reason: The specification covers block execution and validation.

### QG-07

**The commits the EIP pins of QG-02 name.**

- Evidence: QG-02 decided that each EIP the Satin section applies is pinned to a commit, as EIP-8037 is (`SATIN-POOL-001`). The sources this phase works from name no commit for EIP-8038, EIP-2780, EIP-7976, EIP-7981, EIP-7623, EIP-7708, EIP-7951, EIP-8024 or EIP-7843: implementation (a) follows the revisions its revm fork carries, and (b) those of its evm2 fork, whose comments cite the glamsterdam devnet-8 values and, for EIP-2780, pull request ethereum/EIPs#11844.
  The values the section depends on are restated in full (the entry table of `SATIN-SCHED-003`, the floor and intrinsic rules, the transfer-log constants, the precompile prices), so the pins are provenance and do not change any rule's text.
- Options: (1) the owner names the commit of each EIP, and each fork is checked against it; (2) the section pins each EIP at the commit current on a chosen date, looked up when the network is available.
- Recommendation: (2), with the date of the EIP-8037 freeze point (18 September 2026).
- Change needed: whichever fork differs from the pinned revision.
- Outline: `SATIN-POOL-020`, `SATIN-SCHED-001`, `SATIN-LOG-001`, `SATIN-PCMP-003`; the block pages' `SATIN-BASE-001`, `SATIN-BASE-004`.
- **Decision**: (2), on 9 November 2026: each EIP is pinned at the revision of its file current at the EIP-8037 freeze commit `dbc6d457cb` (18 September 2026, 10:41 UTC), read from `ethereum/EIPs`; since then only authors, status, titles and the methodology text of EIP-8038 and EIP-2780 changed, no parameter value:

  | EIP | Commit | Date | Where |
  | --- | --- | --- | --- |
  | EIP-8038 | `4c7e2487e4da3131bcadc7399f8b153f5344c0b7` | 18 September 2026 | `SATIN-SCHED-001` |
  | EIP-2780 | `7243c92ba812437c64bae9fc6524ee269b29daa9` | 4 September 2026 | `SATIN-SCHED-001` |
  | EIP-7976 | `c998ef94eb16a6af8a9b8e2084f947b17ea14865` | 7 July 2026 | `SATIN-SCHED-001`, `SATIN-POOL-020` |
  | EIP-7981 | `747b78c0edfdf04e9e2933ad1bec592d3318e1d9` | 7 July 2026 | `SATIN-SCHED-001`, `SATIN-POOL-020` |
  | EIP-7623 | `451cd9e1ecb30b19be1c02199760a70d6248e604` | 15 May 2025 (Final) | `SATIN-POOL-020` |
  | EIP-7708 | `f7230c46a743313957d8f38a159bda934cc735b2` | 10 July 2026 | `SATIN-LOG-001` |
  | EIP-7951 | `b55cdb0ee78a696327cf76d1c5cf8088d73499ca` | 21 January 2026 (Final) | `SATIN-PCMP-003` |
  | EIP-8024 | `34b49095ca5f7343045da279f04e7ecd1e451393` | 10 June 2026 | `SATIN-BASE-004` |
  | EIP-7843 | `e44e1960a9328282af8dd884837c2302f6a45c3d` | 17 September 2026 | `SATIN-BASE-005` |

  Whether each fork follows its pinned revision in every respect was not checked; the values a transaction's outcome depends on are restated in the pages and were checked against both implementations when the pages were written.

## (h) Raised by the review of the written section

Two questions the review of the Satin section raised, where both implementations agree with each other and the text said otherwise; (a) is mega-evm `5e3f30ad`, (b) the `next/` workspace at mega-evm `d04e8f80` on the evm2 fork at `8751da2b`.

### QH-01

**Which frame a record's give-back goes to.**

- Evidence: `SATIN-HIST-007` said that every record other than the destruction table's is given back "to the frame that paid it": a slot written back to its original value, an account returned to what the transaction loaded.
  Both implementations credit the frame that takes the record back instead, in that frame's refill order: (a) refills the running frame's gas when the write completes (`a:evm/host.rs:357–360`, the revm fork's `cfg/gas.rs:484–495`), (b) books the give-back on the running frame (`b:lib.rs:533` → `b:ledger.rs:591–597`, `evm2:interpreter/gas.rs:461–468`).
  Example: a contract P whose slot 0 holds 7 writes 8, paying the record's 3,520 history gas, then `DELEGATECALL`s C with no reservoir; C emits an empty `LOG0`, its 2,816 history gas spilling onto C's regular gas, writes slot 0 back to 7 and reads `GAS`. Under the text the 3,520 go to P; under both implementations they go to C, 2,816 unwinding C's spill and 704 entering C's reservoir, so C's `GAS` is 2,816 higher than the text says.
  EIP-8037's own state-gas refill credits the running frame too (a slot written from zero and back refills the frame that writes it back), so under the text one `SSTORE`'s state and history give-backs would land in different frames.
- Options: (1) the text follows both implementations: every give-back of state or history gas but the destruction table's goes to the frame that makes it; (2) both implementations change to credit the payer.
- Recommendation: (1).
- Change needed: (1) none; (2) (a) and (b).
- **Decision**: (1), on 9 November 2026: every give-back of state gas or history gas, except the destruction table's (`SATIN-HIST-007` first sentence, `SATIN-SD-005`), goes to the frame that makes it, in the refill order of `SATIN-HIST-012`; a failed frame's rollback stays as `SATIN-POOL-014` says. The text states the consequence once (`SATIN-HIST-007`): a callee can spend, while it runs, gas an ancestor paid for records the callee takes back, bounded by those records' prices; the transaction's total is unchanged unless that gas changes the callee's path.

### QH-02

**What "new account" means for a deposit's caller and the other new-account sites.**

- Evidence: the deposit rules charged the caller's new-account state gas and counted its unit of state growth when the caller "does not exist", and `SATIN-ACCT-015` said an account that already exists is never a rise; `SATIN-WIT-017` separates no account from an account leaf that is empty under EIP-161.
  Both implementations decide the deposit caller by EIP-161 emptiness: (a) `a:evm/execution.rs:1543`, (b) `b:tx.rs:555`; so does Rex6 (`crates/mega-evm/src/evm/execution.rs:893` at `d4c913c5`).
  Example: a deposit whose sender's leaf is in the state with nonce zero, zero balance and no code, calling an existing account with zero value and a gas limit of 100,000, is charged 183,600 state gas at the minimum bucket by both implementations, and so becomes a failed deposit counting one unit of state growth; the text charged nothing and counted nothing.
  The other new-account sites use EIP-161 emptiness in both implementations too (a value call's recipient, a `SELFDESTRUCT`'s beneficiary, the transaction's recipient, a created address), except an EIP-7702 authority, which both decide by the account's absence (`revm:crates/handler/src/pre_execution.rs:394–398`, `evm2:ethereum/eip7702.rs:268`).
- Options: (1) one predicate for every new-account charge and state-growth rise, EIP-161 emptiness; (2) existence of the leaf everywhere, and both implementations change for every site but the authority; (A) EIP-161 emptiness at every site but an EIP-7702 authority, which keeps leaf existence, as EIP-7702 has it and Ethereum's Amsterdam specification decides it (an authority by whether it exists, the other sites by whether the account is alive).
- Recommendation: (1).
- Change needed: (1) both implementations' authority predicate; (2) (a) and (b) at every other site; (A) none.
- **Decision**: (1) on 9 November 2026, amended the same day to (A): two predicates, stated once as `SATIN-STATE-011`. An EIP-7702 authority is new when the state holds no account at its address — leaf existence, as Rex6, both implementations, upstream and Ethereum's Amsterdam specification decide it — for its new-account state gas and its unit of state growth (`SATIN-SCHED-008` step 2, `SATIN-AUTH-008`, `SATIN-ACCT-014`). Every other new-account charge and state-growth rise uses EIP-161 emptiness — no account, or nonce zero, zero balance and no code: a deposit's or Mega System Transaction's caller (`SATIN-DEP-003`, `SATIN-DEP-005`, `SATIN-SCHED-008` step 1), a value call's recipient and a creation's address (`SATIN-HIST-010`, `SATIN-HIST-011`, `SATIN-POOL-015`), a transaction's value recipient (`SATIN-SCHED-008` step 4), a `SELFDESTRUCT`'s beneficiary (`SATIN-SD-018`) and a keyless signer. `SATIN-ACCT-015` gains the matching exception; `SATIN-WIT-017` stays: the witness still answers no account as no account and an empty leaf as a leaf. No implementation changes.
