# Satin Specification — The Owner's Decisions

The owner's answers to the questions of [questions.md](questions.md), decided on 8 November 2026 (QG-07, and QH-01 and QH-02, raised by the review of the written section, on 9 November 2026), as the Satin section is written from them.
Each line gives the question, the decision, and the reason in one line; where a decision changes an implementation, the change is listed in [changes-evm.md](changes-evm.md) for the execution pages and in the block pages' own list for the rest.

## The rule for the QE items

Among the QE items, where the two implementations differ, Satin follows the behaviour of evm2 — implementation (b) and evm2 upstream — and implementation (a) changes where it differs.
This rule covers the QE items only; every other question follows its recommendation unless the table says otherwise.

## The decisions

| Question | Decision | Reason |
| --- | --- | --- |
| [QA-01](questions.md#qa-01) | (1): what a tracer or inspector is shown is outside the specification, stated once as `SATIN-OUT-017` | Tracing changes no outcome, gas figure, state or read set |
| [QA-02](questions.md#qa-02) | (1): the specification names no halt reason (`SATIN-OUT-018`) | A halt's label is in no receipt and changes no state |
| [QA-03](questions.md#qa-03) | (1): the specification fixes which transactions are refused, not which error names a transaction that fails several checks; the order of Satin's own checks stays normative | Only the refusal is consensus; the error a pool reports follows Satin's own order |
| [QA-04](questions.md#qa-04) | (2): the bucket mapping is SALT's own definition, an input to the specification (`SATIN-STATE-010`); (b) makes SALT's production hasher its default | The mapping is SALT's, as the capacities are; two hashers price differently |
| [QA-05](questions.md#qa-05) | (1): `SLOTNUM` pushes zero, and stays a volatile read | MegaETH has no slot; the OP Stack hard-codes zero |
| [QA-06](questions.md#qa-06) | (1): no per-frame cap beyond the frame budgets (`SATIN-LIM-009`); (a)'s knob is an implementation detail | The knob is unlimited under Satin and specifies nothing |
| [QA-07](questions.md#qa-07) | (2): a deposit envelope that carries a gas price is malformed and outside the specification | The OP specification has no deposit gas price |
| [QA-08](questions.md#qa-08) | (1): a creation transaction whose sender's nonce cannot be bumped creates nothing (`SATIN-LIM-015`) | One sentence, and it matches the deposit rule |
| [QA-09](questions.md#qa-09) | (1): the due-change predicate is stated at the storage level | The witness carries those slots |
| [QA-10](questions.md#qa-10) | (1): every Rex-era rule both implementations keep is restated as Satin's | A Satin page never relies on a Rex-era page |
| [QB-01](questions.md#qb-01) | (3): the schedule's second half-check is dropped from the specification | It is not the execution layer's job |
| [QB-02](questions.md#qb-02) | (1): the executor derives whether a block admits only deposits from the schedule and the parent timestamp | A validity rule must not depend on a flag a caller can forget |
| [QC-01](questions.md#qc-01) | (1): the activation block's predeploy check stays | It is how Satin fails closed on a chain without the contracts |
| [QC-02](questions.md#qc-02) | (1): the transaction limits, the frame share and the detention caps are protocol values (`SATIN-LIM-017`, `SATIN-DET-013`) | A limit is part of block validity |
| [QC-03](questions.md#qc-03) | (1): a creation whose created address is the beneficiary is not detained from its start (`SATIN-DET-006`, `SATIN-DET-008`) | A creation's loads are its own checks, not volatile reads |
| [QC-04](questions.md#qc-04) | (1): the draft is kept — with EIP-3607 disabled, step 9 of a keyless deployment neither loads the signer's code nor refuses it; (b) changes | A disabled EIP-3607 disables its check, here as for any sender |
| [QC-05](questions.md#qc-05) | (1): a precompile address runs and is priced as the precompile whatever code it holds (`SATIN-PCMP-008`) | Every node then dispatches the same call the same way |
| [QC-06](questions.md#qc-06) | (1), which QG-05's decision implies (the question has no recommendation of its own): the chain configuration's consensus parts are in the specification | The configuration key and schedule decide which blocks run Satin |
| [QD-01](questions.md#qd-01) | (2): every authority whose entry passes the chain-id, nonce and signature gates is loaded by the list simulation, for every list; no short-list fast path (`SATIN-AUTH-001`, `SATIN-AUTH-005`) | The accounts a transaction loads, and so its witness, must not depend on the list's length or on where an out-of-gas falls |
| [QE-01](questions.md#qe-01) | Neither option: ModExp charges its formula price and then checks EIP-7823's bound, as evm2 upstream #874 and go-ethereum order it; an over-bound input is priced by its formula, not at zero or at 500 (`SATIN-PCMP-007`, `SATIN-DET-023`) | The price detention reads is then the price the call is charged |
| [QE-02](questions.md#qe-02) | (1): a deposit that fails before its first frame loads nothing of its recipient | The read set is consensus for a stateless validator; both implementations agree |
| [QE-03](questions.md#qe-03) | (3): a prestate in which a deposit's sender balance plus its mint exceeds 2^256 − 1 is invalid and outside the specification, for successful and failed deposits alike; no implementation changes | Unreachable: all ether is about 1.2 × 10^26 wei |
| [QF-01](questions.md#qf-01) | (1): Satin succeeds Rex6; there is no Rex7 | The state of `main` and of the draft |
| [QF-02](questions.md#qf-02) | (1): the section's place, groups and file names as laid out | As recommended |
| [QF-03](questions.md#qf-03) | (1): `spec: Satin`, `maturity: unstable` and a warning hint on every Satin page | A `<details>` block cannot carry a standalone section |
| [QF-04](questions.md#qf-04) | (1): the draft stays frozen until the section is written, then becomes the informative delta | The section is written from one fixed source |
| [QF-05](questions.md#qf-05) | (1): short glossary entries, more terms added as the section needs them | The glossary defines terms, not rules |
| [QF-06](questions.md#qf-06) | (1): the backward-compatibility statements are reworded: a spec never changes earlier blocks, and contracts keep working | Contracts deployed under Rex6 run under Satin's prices |
| [QF-07](questions.md#qf-07) | (1): no Satin reference implementation is named | Two implementations exist and one will ship |
| [QF-08](questions.md#qf-08) | (1): each rule has one home; a gathering page states the unified rule and links the detail | A rule is never stated twice |
| [QF-09](questions.md#qf-09) | (1): the rule-id scheme is adopted | Tests and fixtures cite rules by id |
| [QG-01](questions.md#qg-01) | (1): every EIP-8037 rule a transaction's outcome depends on is restated, the EIP cited for provenance | The section is standalone |
| [QG-02](questions.md#qg-02) | (1): each EIP the section applies is pinned to a commit; the commits are an open item ([QG-07](questions.md#qg-07)) | Draft EIPs keep changing |
| [QG-03](questions.md#qg-03) | (1): the current values are written | The unstable hint already says values may change |
| [QG-04](questions.md#qg-04) | (1): implementation-specific statements are restated as behaviour; the rest goes to node documentation | The specification describes behaviour, not code |
| [QG-05](questions.md#qg-05) | (1): the node-integrator parts that decide consensus are in the specification; pool and RPC behaviour is node documentation | Only consensus belongs in the specification |
| [QG-06](questions.md#qg-06) | (2): executions outside a block are node documentation; `SATIN-LIM-018` is retired | The specification covers block execution and validation |
| [QG-07](questions.md#qg-07) | (2), on 9 November 2026: each of the nine EIPs is pinned at its file's revision current at the EIP-8037 freeze commit `dbc6d457cb` (18 September 2026), the pins of `SATIN-SCHED-001`, `SATIN-POOL-020`, `SATIN-LOG-001`, `SATIN-PCMP-003`, `SATIN-BASE-004` and `SATIN-BASE-005` | One date for every EIP the section applies, the date its EIP-8037 profile was frozen |
| [QH-01](questions.md#qh-01) | (1): every give-back of state gas or history gas, except the destruction table's (`SATIN-HIST-007` first sentence, `SATIN-SD-005`), goes to the frame that makes it, in the refill order of `SATIN-HIST-012`; a failed frame's rollback stays as `SATIN-POOL-014` says; no implementation changes | Both implementations credit the frame that takes the record back, as EIP-8037's own state-gas refill does, so one `SSTORE`'s state and history give-backs land in the same frame |
| [QH-02](questions.md#qh-02) | (1), amended to option A on 9 November 2026: two predicates, stated once as `SATIN-STATE-011` — an EIP-7702 authority is new when the state holds no account at its address (leaf existence); every other new-account charge and state-growth rise (a deposit's or Mega System Transaction's caller, a value call's recipient, a transaction's value recipient, a `SELFDESTRUCT`'s beneficiary, a created address, a keyless signer) uses EIP-161 emptiness (no account, or nonce zero, zero balance and no code); `SATIN-ACCT-015` gains the matching exception; `SATIN-WIT-017` stays; no implementation changes | Each site keeps the test Ethereum's Amsterdam specification uses for it — existence for an authority, as EIP-7702, Rex6 and both implementations have it; emptiness for every other site, as EIP-161 has it and both implementations do |

## Added requirement

The Satin section has one page that lists every Satin rule — its id, one line, and a link to its home — so a reader never has to open a Rex-era page; the Satin section restates every rule it keeps, and none says "same as Rex".
