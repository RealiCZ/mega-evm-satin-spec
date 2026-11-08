# Satin Specification — Implementation Changes (overview, base layer, system contracts, blocks)

Where an implementation differs from the text of the Satin pages `satin/overview.md`, `satin/base-layer.md`, `satin/system-contracts/` and `satin/block/`, this list names the rule, the implementation, the place, and what must change.
(a) is mega-evm `5e3f30ad` (`a:` = `crates/mega-evm/src/`); (b) is the `next/` workspace at mega-evm `785182eb` (`b:` = `next/mega-evm2/src/`, `op:` = `next/op-evm2/src/`), on the evm2 fork at `91518705` (`evm2:` = `crates/evm2/src/`).
Line numbers are of those commits.

| Counts | (a) | (b) |
| --- | --- | --- |
| Changes | 6 | 9 |
| Of which in both | 3 (`SATIN-BASE-005`, `SATIN-WIT-004`, `SATIN-ACT-010`) | 3 (the same) |

## Implementation (a)

| Rule | Place | What must change |
| --- | --- | --- |
| `SATIN-MST-007` | `a:system/tx.rs:156` `originates_from_the_protocol` | A transaction is system-originated only when it is a Mega System Transaction (evm2's behaviour: (b) exempts only the promoted system transaction and its system calls). Drop the two other disjuncts — a caller equal to `0xff…fe` and a deposit carrying `MEGA_SYSTEM_TRANSACTION_SOURCE_HASH` — and mark the pre-block system calls as the protocol's own by another means than their caller. Reachable only outside a block (a simulation from `0xff…fe`, or a deposit handed over with the promotion's hash). |
| `SATIN-MST-005` | `a:system/tx.rs:174`–`205` `validate_and_promote` (`validate_account_nonce_and_code` at `:199` with `eip3607_disabled`, `nonce_check_disabled`) | The nonce and EIP-3607 checks of a Mega System Transaction are made whatever the configuration says, as (b)'s `check_system_sender` (`b:tx.rs:225`) makes them. Reachable only with a configuration that turns the checks off (a simulation). |
| `SATIN-KEY-005`/step-9 | `a:system/keyless/dispatch.rs:327` (`checks_code = !ctx.cfg().is_eip3607_disabled()`) | Step 9 is unconditional (QC-04 under the owner's general rule: (b) loads and refuses regardless, `b:keyless.rs` `run`). |
| `SATIN-BASE-005` | `a:evm/host.rs:200`–`205` `slot_num` | `SLOTNUM` pushes zero (QA-05). The engine pushes the slot number its block environment carries; either the engine pushes zero, or every node supplies zero — the spec has no slot-number input any more (`SATIN-WIT-010`). |
| `SATIN-WIT-004` | `a:evm/execution.rs:1430` `hold_authorization_list`; `a:limit/limit.rs:443` `authorization_list_may_cross` | No short-list fast path (QD-01 as the brief states it): the preflight simulation runs for every EIP-7702 list, loading every authority whose entry passes the chain-id, nonce and signature gates, so the witness holds them whether or not the list could cross a limit. |
| `SATIN-ACT-010`, `SATIN-BASE-006` | `a:block/executor.rs:193` `with_no_user_tx_activation_block`, `:199` `with_satin_activation_block` | The executor derives both flags itself from the chain configuration and the parent block's timestamp (QB-02 option 1) instead of taking them from its caller, defaulting to false. |

## Implementation (b)

| Rule | Place | What must change |
| --- | --- | --- |
| `SATIN-ICPT-002` | `b:lib.rs:1080`–`1088` (`StartHooks::before`: `keyless::before`, `intercept::hint_before`, `intercept::answer_before`), ahead of evm2's depth check (`evm2:evm/mod.rs:1361` `execute_message_impl` → `dispatch_message`) | A call past the call-stack limit must not reach an interceptor or count a hint: gate the `before` hook's interceptors on `depth ≤ 1024`, answering `CallTooDeep` first, as (a) does (`a:evm/execution.rs:1518` `call_too_deep`). Unreachable under the execution cap (a frame at depth 1,024 has under one gas), so no observable difference today. |
| `SATIN-ACT-005`, `SATIN-ACT-004`, `SATIN-PBLK-003` step 3, `SATIN-SYSC-003` | `b:block.rs:211` `apply_pre_execution_changes` ("no activation block: the predeploy check is not made") | Add the activation block's predeploy check of the six system contracts and the EIP-7997 factory, read-only, between the EIP-4788 call and the due-change read (QC-01 option 1). |
| `SATIN-ACT-010`, `SATIN-BASE-006` | `b:block.rs:149`, `:166` (`only_deposits: false`) | Derive "admits only deposits" and "Satin activates" from the chain configuration and the parent's timestamp (QB-02 option 1); today the flag is a field defaulting to false and no activation flag exists. |
| `SATIN-PBLK-004`, `SATIN-WIT-008`, `SATIN-WIT-011`, `SATIN-PBLK-003` steps 4–5 | `b:block.rs:186`–`205` `registry_due`; `b:block.rs:227`–`233` (L1 block info read) | Both reads use evm2's non-loading peeks (`account_info_untracked`, `storage_slot_untracked`, which do not cache into the overlay), so neither lands in a committed state; commit each as a read-only pre-block state of its own, in step order, so a witness built from the committed states holds the registry's account and pending slots and the L1 block contract's account and five slots. |
| `SATIN-ACT-009` | `b:ledger.rs:35`–`47` `Cfg` (`limits`, `cap`, `oracle_cap`) | The per-transaction limits and the detention caps are fixed by the spec, not node-supplied (QC-02 option 1; the derived default is zero, not Satin's values). The block budgets are already fixed (`b:block.rs:35`). |
| `SATIN-REG-002` | `b:ledger.rs:42` `Cfg::registry_slot`, read at `b:tx.rs:184` and `b:tx.rs:412` | The registry slot that holds the live system address is slot 0, fixed; not a configuration value. |
| `SATIN-BASE-005` | `b:lib.rs:208` (`ins::slotnum`) | `SLOTNUM` pushes zero (QA-05); the instruction pushes the block environment's slot number. As for (a): the engine or every node fixes it at zero. |
| `SATIN-WIT-004` | `b:eip7702.rs:194`–`198` (`simulate` only when `entries > kv_room \|\| entries > growth_room`) | No short-list fast path (QD-01 as the brief states it): simulate every list, loading every authority whose entry passes the chain-id, nonce and signature gates. |
| `SATIN-ACT-001`, `SATIN-ACT-002`, `SATIN-ACT-003` | none (b has no chain configuration, schedule or activation logic, QC-06) | The chain configuration key, the refused `satin…` keys and the base-fork check are part of the specification (QG-05 option 1); (b), or the node that embeds it, must implement them. |

## Noted, no change required

| Rule | Implementation | Note |
| --- | --- | --- |
| `SATIN-MAC-002` | (b) `b:intercept.rs:92`–`103` sets the switch as the answer is made, before detention could turn it into the stop | MegaAccessControl's answers spend no regular gas, so none can be the crossing; the order is unobservable. |
| `SATIN-DEP-011` | both | Owner decision QE-03 option (3): a balance plus mint above 2^256 − 1 is an invalid prestate; no change. |
| `SATIN-ACT-002` | (a) `a:block/genesis.rs:32` accepts `{"$serde_json::private::Number": "<digits>"}` for `satinTime` | The specification states the key as a JSON number and leaves a reader's handling of other number representations to node documentation (QG-04 option 1); (a) may keep accepting it. |
| `SATIN-ACT-003` | (a) `a:block/hardfork.rs:144` `validate_schedule` | Checks only that the base forks are active at `satinTime`, which is the whole rule now that QB-01 dropped the other half. |
