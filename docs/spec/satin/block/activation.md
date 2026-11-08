---
description: Satin (unstable) — Activation and Rex-Era Carry-Over. When Satin takes effect, the chain configuration key that schedules it and the base forks it requires, the checks its activation block makes, the execution configuration the spec fixes, and what Satin carries over from the Rex era.
spec: Satin
maturity: unstable
---

# Activation and Rex-Era Carry-Over

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
{% endhint %}

Abstract: When Satin takes effect and how a chain configuration schedules it; the base forks that must be active when it does; the activation block, which admits only deposits and checks that the chain holds the system contracts and the EIP-7997 factory Satin runs on; the parts of the execution configuration the spec fixes whatever a node supplies; and what Satin requires of the state the Rex era left.

## Motivation

The spec restates the execution layer; it does not deploy or migrate anything.
It therefore runs only on a chain that already holds what it expects — the six system contracts at known code, the `CREATE2` factory, the L1 block contract — and on a base whose forks are all active by the time it starts.
A node that started the spec at another block, ran it on a chain without those contracts, or took a protocol value from its own configuration, would execute a different chain from every other node, and the difference might only show long after activation.

## Specification

### When Satin takes effect

- `SATIN-ACT-001` Satin follows Rex6 on the spec ladder.
  A node MUST execute every block whose timestamp is at or after `satinTime` under Satin, and every earlier block under the spec its timestamp resolves to.
  The block in which Satin activates is the block whose timestamp is at or after `satinTime` and whose parent's timestamp is before it (see [Base Layer](../base-layer.md), `SATIN-BASE-007`).
- `SATIN-ACT-008` Satin MUST NOT change how a block before `satinTime` executes: a node replaying history MUST resolve each block's spec from its timestamp and apply that spec's rules.
  From `satinTime` on, every account, contract and slot the earlier blocks left MUST be executed under Satin's rules: accounts, code and storage carry over unchanged and run under Satin's prices, pools and limits.
  A contract deployed under an earlier spec is not promised the outcome it had under that spec for the same gas: a gas budget fixed for Rex prices — a gas argument, a stored per-call limit, a signed gas limit — can be too small under Satin's prices — by about five times for a call that writes a fresh slot or creates an account without a reservoir — or larger than needed, as for deployed code, whose price per byte fell ([Two-Pool Gas](../evm/gas-model.md), [State Gas and SALT Pricing](../evm/state-gas.md)).

### The chain configuration

- `SATIN-ACT-002` A chain configuration's `config` object MUST schedule Satin by one key, `satinTime`, whose value is the activation timestamp: an unsigned integer of at most `MAX_TIMESTAMP`, given as a JSON number.
  Satin carries no parameter: no key names a limit, a detention cap, a price, or the SequencerRegistry's roles.
  A node MUST refuse a configuration that carries a key starting with `satin`, in any ASCII letter case, that is not exactly `satinTime`, whether or not it also carries `satinTime`.
  A key given twice MUST be read as its last copy.
- `SATIN-ACT-003` Every base fork Satin runs on — the Ethereum forks from Shanghai to Osaka and the Optimism forks from Regolith to Karst — MUST be active at `satinTime`, and a node MUST refuse a configuration that schedules Satin and leaves one of them inactive at `satinTime`.
- `SATIN-ACT-010` A node MUST work out, for every block it builds or validates, whether the block admits only deposits (`SATIN-BASE-006`) and whether Satin activates in it, from the chain configuration and the parent block's timestamp, and MUST execute the block accordingly; neither may be left to an input a caller can omit.
  The two differ: an Optimism fork's activation block admits only deposits and checks no predeploy.

### The activation block

- `SATIN-ACT-004` The block in which Satin activates MUST admit only deposits (`SATIN-BASE-006`), and MUST make the predeploy check of `SATIN-ACT-005` as the third step of its pre-block sequence, before its first transaction (see [System Calls and the Pre-Block Sequence](system-calls.md)).
- `SATIN-ACT-005` The predeploy check MUST read, in this order, the six system contracts in address order — Oracle, High-Precision Timestamp, KeylessDeploy, MegaAccessControl, MegaLimitControl, SequencerRegistry — and then the [EIP-7997](https://eips.ethereum.org/EIPS/eip-7997) `CREATE2` factory at `CREATE2_FACTORY_ADDRESS`, and each MUST hold an account whose code hash is the one the table below names.
  Their nonces, balances and storage are not checked.
  An address with no account, an account without code, an older version of its contract or any other code MUST make the block invalid.
  The check writes nothing: each account it reads is a read-only entry of the activation block's pre-block states, in the order above (see [The Stateless Witness](stateless-witness.md)).
  No other block reads the seven addresses before its transactions.

| Address                            | Code hash                            |
| ---------------------------------- | ------------------------------------ |
| `ORACLE_CONTRACT_ADDRESS`          | `ORACLE_CODE_HASH` (version 2.0.0)   |
| `HIGH_PRECISION_TIMESTAMP_ADDRESS` | `HIGH_PRECISION_TIMESTAMP_CODE_HASH` |
| `KEYLESS_DEPLOY_ADDRESS`           | `KEYLESS_DEPLOY_CODE_HASH`           |
| `MEGA_ACCESS_CONTROL_ADDRESS`      | `MEGA_ACCESS_CONTROL_CODE_HASH`      |
| `MEGA_LIMIT_CONTROL_ADDRESS`       | `MEGA_LIMIT_CONTROL_CODE_HASH`       |
| `SEQUENCER_REGISTRY_ADDRESS`       | `SEQUENCER_REGISTRY_CODE_HASH` (version 2.0.0) |
| `CREATE2_FACTORY_ADDRESS`          | `CREATE2_FACTORY_CODE_HASH`          |

  The addresses and the six contracts' code hashes are those of [System Contracts](../system-contracts/overview.md).

### Carry-over

- `SATIN-ACT-006` Satin MUST NOT deploy, upgrade or seed any account: a chain runs Satin on the six system contracts and the factory as its state holds them when Satin activates, and the predeploy check refuses a chain whose state does not hold them at the code above.
- `SATIN-ACT-007` Satin MUST NOT upgrade or write the L1 block contract: it runs on the contract the chain holds, which on a chain coming from the Rex era is OP's L1Block version 1.6.0 (Isthmus), whose data-availability footprint gas scalar and operator fee scalars are zero until the contract is upgraded and the scalars are set.
- `SATIN-ACT-009` Part of the execution configuration is fixed by the spec, whatever a node supplies: the Satin gas schedule and the byte prices of state and history gas; EIP-8037, EIP-2780 and EIP-7708 on; the execution cap; the chain-id check on; the code and initcode size limits; the per-transaction limits, the per-frame share and the detention caps; and the block's packing budgets.
  A node MUST execute every Satin block on these values and on no value its configuration or a block names, and a node that reads the configuration before it executes — to estimate gas against the execution cap, for one — MUST read these values.
  The values are those of the pages that state the rules: [Gas Schedule and Intrinsic Gas](../evm/gas-schedule.md), [State Gas and SALT Pricing](../evm/state-gas.md), [History Gas](../evm/history-gas.md), [Two-Pool Gas](../evm/gas-model.md), [Contract Size Limits](../evm/contract-limits.md), [Resource Limits](../evm/resource-limits.md), [Gas Detention](../evm/gas-detention.md), [Transaction Validation and Refusals](transaction-validation.md) and [Block Limits and Packing](block-limits.md).

## Constants

| Constant                    | Value                                                                | Description                                    |
| --------------------------- | -------------------------------------------------------------------- | ---------------------------------------------- |
| `MAX_TIMESTAMP`             | 2^64 − 1                                                             | The largest `satinTime`                        |
| `CREATE2_FACTORY_ADDRESS`   | `0x4e59b44847b379578588920ca78fbf26c0b4956c`                         | The EIP-7997 deterministic deployment proxy    |
| `CREATE2_FACTORY_CODE_HASH` | `0x2fa86add0aed31f33a762c9d88e807c475bd51d0f52bd0955754b2608f7e4989` | Code hash of the factory's runtime             |

## Rationale

**Why one key and no parameter?**
Every value Satin executes on is the spec's; a configuration that could name a limit or a role would let two chains run different rules under one spec name.
Refusing every other key that starts with `satin` keeps a file written against an earlier draft of the format — which named the registry's roles (`satinInitialSystemAddress`, `satinInitialSequencer`, `satinInitialAdmin`, `satinMinRotationDelay`), `satinInitialFromBlock` or the limits — from loading as if it were valid.
The key format is provisional until a network publishes a genesis file carrying it.
Some JSON readers hand a large number over as an object rather than a number; how a node reads such a representation is node documentation.

**Why must the base forks be active by `satinTime`?**
Every Satin block executes on Karst's rules; a Satin block before one of its base forks would run on rules the node's own schedule does not apply to it.
Whether Jovian, Karst or Osaka activate before `satinTime` is not the execution layer's to check: every block before `satinTime` runs the Rex-era engine, which builds on Isthmus whatever the configuration times those forks at.

**Why must the executor work out the activation flags itself?**
Block validity must not depend on a caller remembering to pass a flag: an execution not told that a block admits only deposits would accept a user transaction in it, and one not told that Satin activates would check no predeploy.
Both follow from the configuration and the parent's timestamp, which the executor is given.

**Why check the predeploys rather than deploy them?**
A chain reaches Satin through the Rex-era forks, which installed the six system contracts: Rex5 deployed the SequencerRegistry and upgraded the Oracle to 2.0.0, and Rex6 upgraded the SequencerRegistry to 2.0.0; OP's genesis tooling gave the chain the factory.
Checking that they are there, once, fails closed on a chain that did not run those forks, without rewriting state a chain that did run them holds.
A chain must therefore have run a Rex6 block before `satinTime`.

**Why does the compatibility statement promise the state carries over, and not that contracts behave the same?**
Satin changes nothing about earlier blocks, and every account, its code and its storage carry over; but a contract deployed under Rex6 runs, from `satinTime`, under Satin's prices, pools, `GAS` value and transfer logs, so it does not behave identically.
What a Rex-era contract can rely on is kept where Satin can keep it: no give-back of state or history gas raises a frame's regular gas, so gas a contract spent does not come back while the transaction runs, as under Rex6; and when a slot, an account or a creation is charged state gas, the legacy share keeps its regular price at least Ethereum's price before Amsterdam, which is Rex6's at multiplier 1 — not Rex6's at a higher multiplier, and not for a creation onto an address a transaction funded beforehand, which carries no state charge and so no share.
What it cannot rely on is any gas budget fixed for Rex prices: writing a fresh slot or creating an account without a reservoir costs regular gas about five times Rex6's at multiplier 1 — a cold fresh slot 113,540 against 22,100, a value call that creates an account about 204,940 against 36,600 — and more at a higher multiplier, while deployed code costs less than under Rex6; such a budget has to be derived again for Satin.
Nor can a post-call gas check ported from Ethereum, `gasleft() < gasInitial / 64` or `< gasRequested / 63`, be relied on: a caller has kept 2/100 of its gas at the forward since MiniRex, not 1/64, so such a check can miss a starved call, and with the history gas Satin charges a start's records after the forward it can also fire for a call that received all it asked for; where it fires depends on where `gasInitial` was measured and on how far the request exceeds what the caller can forward ([Gas Forwarding](../evm/gas-forwarding.md)).

**Why fix the configuration in the spec?**
A node that let its configuration override a price, a limit or a check would compute another chain from the same blocks; fixing them makes the spec, not the node, the source of every value a Satin block depends on.

## Security Considerations

- A node that activates Satin at another block than the schedule implies applies Satin's rules to a Rex6 block or Rex6's to a Satin block, and computes another state from there on.
- A node that skips the predeploy check runs Satin on a chain whose system contracts may be missing or carry other code, so the Oracle's authority or the live system address could be anyone's.
- A node that reads a limit or a price from its configuration diverges from every node that holds the spec's value.
- A node that relies on its caller to say whether a block admits only deposits accepts an activation block with user transactions when the caller forgets.

## Spec History

- [Rex5](../../upgrades/rex5.md) — Deployed the SequencerRegistry and upgraded the Oracle to 2.0.0.
- [Rex6](../../upgrades/rex6.md) — Upgraded the SequencerRegistry to 2.0.0; Rex6 deploys the system contracts as specified in [System Contracts](../../system-contracts/overview.md).
- [Satin](../../upgrades/satin.md) — Activation by `satinTime`, the deposit-only activation block with the predeploy check, and the configuration fixed by the spec.
