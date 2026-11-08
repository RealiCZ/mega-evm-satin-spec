# Satin Specification — Implementation Changes for the Execution Pages

Every place where implementation (a) or implementation (b) differs from the text of the Satin execution pages (`docs/spec/satin/evm/`), by rule id.
(a) is mega-evm `5e3f30ad` (`crates/mega-evm/src/`, its revm fork at `4c8f0d43` written `revm:`); (b) is the `next/` workspace at mega-evm `785182eb` (`next/mega-evm2/src/`, written `b:`), with the evm2 fork at `91518705` (`crates/evm2/src/`, written `evm2:`).
Line numbers are of those revisions, except rows 11 to 13, which were read at (b) `d04e8f80` on the evm2 fork at `8751da2b`, and (a) at the same `5e3f30ad`.
Each change follows an owner decision recorded in [decisions.md](decisions.md); a value or behaviour not listed here was found to match the text in both implementations, or was not reached by this check (see "Not checked" below).

## Counts

| Implementation | Changes | Of which latent (no observable difference today) |
| --- | --- | --- |
| (a) | 3 | 0 |
| (b) | 10 | 2 |

Three decisions change both implementations (QD-01: rows 1 and 2; QE-01: rows 3 and 4; QH-02: rows 11 and 12); each row above is counted once, under its implementation.

## Changes

| # | Rule | Implementation | Where | What must change | Decision |
| --- | --- | --- | --- | --- | --- |
| 1 | `SATIN-AUTH-001`, `SATIN-AUTH-005` | (a) | `evm/execution.rs:1429–1432` (`hold_authorization_list` returns before the simulation when `authorization_list_may_cross` is false, `limit/limit.rs:443`) | Run the simulation for every EIP-7702 list, whatever its length, so every authority that passes the chain-id, nonce and signature gates is loaded; keep the limit decision as it is | QD-01 |
| 2 | `SATIN-AUTH-001`, `SATIN-AUTH-005` | (b) | `b:eip7702.rs:193–197` (`simulate` runs only when `entries > kv_room \|\| entries > growth_room`) | Run `simulate` for every list (system-originated transactions carry none) | QD-01 |
| 3 | `SATIN-PCMP-007`, `SATIN-DET-023`, `SATIN-DET-024` | (a) | `revm:crates/precompile/src/modexp.rs:213–226` (`run_inner` refuses a length that does not fit a `usize` and checks EIP-7823's bound before the formula price); its price follows the run (`revm:crates/precompile/src/required_gas.rs:213–240`), and the engine's tests expect 500 for such an input (`evm/precompiles.rs:568`, `:592`, `:601`) | Charge the 500 minimum, then the formula price (lengths saturated to 64 bits, as evm2 upstream #874 does), then check the bound; the price of an over-bound input becomes its formula price; update the tests | QE-01 |
| 4 | `SATIN-PCMP-007`, `SATIN-DET-023`, `SATIN-DET-024` | (b) | `evm2:precompiles/modexp.rs:216–226` (fork commit `de8c5cd0` moved the bound before the formula price); `b:detention.rs:550–559` (the two-step ModExp probe) | Drop `de8c5cd0` and take upstream's order (#874: minimum, formula price, then the bound); confirm the two-step probe then reads the formula price for an over-bound input | QE-01 |
| 5 | `SATIN-DET-006`, `SATIN-DET-008` | (b) | `b:lib.rs:1050–1063` (`before`: the transaction is detained from its start when `msg.call_target` or `msg.code_address` is the beneficiary, which for a creation is the derived address) | Detain from the start only for a sender, a call's recipient or the delegate a recipient follows, never for a creation's created address | QC-03 |
| 6 | `SATIN-PCMP-008`, `SATIN-DET-021` | (b) | `b:detention.rs:539–541` (`precompile_price_of` looks the precompile up and prices it by `msg.code_address`, which for a precompile address holding a delegation is the delegate) | Dispatch and price a call to a precompile address by the called address, whatever code it holds | QC-05 |
| 7 | `SATIN-LIM-001`, `SATIN-LIM-017`, `SATIN-DET-012`, `SATIN-DET-013` | (b) | `b:ledger.rs:35–47` (`Cfg` takes the three transaction limits and both detention caps from the node; its derived default is zero) | Fix 13,107,200 / 500,000 / 1,000 and 20,000,000 / 20,000,000 in the engine for Satin, as `b:block.rs` fixes the block budgets | QC-02 |
| 8 | `SATIN-STATE-010` | (b) | `b:ledger.rs:599–612` (`bucket_id` is an FNV-1a test hasher unless the `salt-ahash` feature, `next/mega-evm2/Cargo.toml:36`, is on) | Make SALT's production hasher the default | QA-04 |
| 9 | `SATIN-LIM-015` | (b) | evm2's initial frame for types 0, 1 and 2 (`evm2:ethereum/mod.rs:572` `prepare_initial_frame`) deploys at the address of nonce `2^64 − 1` when the nonce check is off; `b:tx.rs:695–710` (`creation_nonce_unbumpable`) handles deposits only | A creation transaction whose sender's nonce cannot be bumped creates nothing and succeeds, as (a) and both deposit paths do | QA-08 |
| 10 | `SATIN-SCHED-001`, `SATIN-STATE-003` (latent) | (b) | `b:lib.rs:249–265` (`satin_version` rebuilds four state-gas entries at `CPSB` but leaves `TxEip7702PerAuthState` at Amsterdam's `23 × 1,530`, `evm2:version/mod.rs:895`) | Rebuild the delegation-indicator entry from `CPSB` too; the value is equal today, and differs only once the cost per state byte changes | none (the rule's own text) |
| 11 | `SATIN-STATE-011`, `SATIN-SCHED-008` step 2, `SATIN-AUTH-008`, `SATIN-ACCT-014` | (a) | `revm:crates/handler/src/pre_execution.rs:394–398` (an authority "existed" unless its info is empty **and** it was loaded as not existing and not touched), charge at `:417–428`; `evm/execution.rs:1476–1478` (the list simulation's `absent`, the same test) and `:1597–1602` (the applied authorities' growth: `is_loaded_as_not_existing() && original_info().is_empty()`) | Decide an applied authority's new-account state gas, its unit of state growth and the simulation's created count by EIP-161 emptiness (no account, or nonce zero, zero balance and no code), as the transaction's recipient (`revm:crates/handler/src/execution.rs:66`) and the deposit caller (`evm/execution.rs:1543`) already are; an authority whose leaf is in the state but empty is then charged and counted | QH-02 |
| 12 | `SATIN-STATE-011`, `SATIN-SCHED-008` step 2, `SATIN-AUTH-008`, `SATIN-ACCT-014` | (b) | `evm2:ethereum/eip7702.rs:268` (`existed = account.exists() \|\| account.is_touched()`, `exists()` being a present overlay entry, `evm2:evm/state/account.rs:403–405`), charge at `evm2:ethereum/eip7702.rs:376–390`; `b:eip7702.rs:108` (simulation `absent`) and `:224` (applied growth from `existed`) | Decide the authority's charge, growth and simulated count by EIP-161 emptiness, as `b:tx.rs:124` (the transaction's recipient) and `b:tx.rs:555` (the deposit caller) already do | QH-02 |
| 13 | `SATIN-SD-004` (slot row "non-zero / any"), `SATIN-SD-019` step 3 (latent) | (b) | `b:lib.rs:631–636` (every slot record of the destroyed account is collected, a slot whose original value is not zero included), `:668–673` and `:702–707` (all are taken back with their bytes and history); nothing at `:677–699` makes the record of a loaded slot still at its original value. (a) takes back only original-zero slots made non-zero and makes the record of an unchanged non-zero-original slot (`a:limit/record.rs:366–376`) | Take back only the records of slots whose original value is zero; leave a changed non-zero-original slot's record standing, and make the record of a loaded slot still holding a non-zero original at the deletion (KV +1, data size +40, 3,520 history gas on the destroying frame). Latent in block execution: a slot of the created address has a non-zero original only when it was loaded before the creation, which no instruction does there (an access list warms a slot without loading it, and no frame runs on the address's storage before its creation); a slot first accessed after the creation reads zero in both | none (the rule's own text) |

## No change

These decisions leave both implementations as they are:

- QA-01 (`SATIN-OUT-017`): what a tracer is shown is outside the specification.
- QA-02 (`SATIN-OUT-018`): no halt reason is named; the two labels may stay different.
- QA-06 (`SATIN-LIM-009`): (a)'s per-frame data-size knob (`limit/mod.rs` `EvmTxRuntimeLimits`) stays an implementation detail, unlimited under Satin.
- QE-03: a deposit whose sender balance plus mint exceeds `2^256 − 1` is an invalid prestate outside the specification (the deposit pages own the rule).
- QG-06 (`SATIN-LIM-018` retired): executions outside a block are node documentation.

## Not checked

- The checked values are every constant and table of the execution pages: the gas-entry table (`SATIN-SCHED-003`) against (a)'s schedule tests (`evm/schedule.rs` `test_the_eip8038_entries_carry_the_amsterdam_numbers`, `test_every_regular_entry_is_amsterdam`) and against evm2's Amsterdam table (`evm2:version/mod.rs:868–957`, `evm2:interpreter/gas.rs:48–132`) with (b)'s overrides (`b:lib.rs:249–265`); the remaining constants against the inventory's checked table (`plan/inventory.md` §7).
- The gas-entry table holds Amsterdam's numbers except the three changes of `SATIN-SCHED-001`; the third, the 98/100 forwarding reduction (`SATIN-FWD-001`), is overridden in both implementations (`a:evm/schedule.rs:139–147`, `b:lib.rs:252–258`) and is left out of (a)'s equality test (`a:evm/schedule.rs:175–185`), so that test checks every entry but the forwarding reduction.
- One open point is a question, not a change: (b) answers a bucket that its configuration does not list as the minimum bucket (`b:ledger.rs:39–40`), where `SATIN-STATE-007` makes a capacity the node cannot read a fault; whether (b)'s configuration map stands for SALT's whole state is for (b)'s maintainers to confirm.
