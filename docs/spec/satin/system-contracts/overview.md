---
description: Satin (unstable) — System Contracts. The six MegaETH system contracts under Satin, their addresses and the code each must hold, and how a system contract differs from a precompile.
spec: Satin
maturity: unstable
---

# System Contracts

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
{% endhint %}

Abstract: The registry of MegaETH's six system contracts: their fixed addresses, the code each address holds, the rule that Satin deploys, upgrades and seeds none of them, and the distinction between a system contract, whose methods run as bytecode unless the node intercepts them, and a precompile.

## Motivation

MegaETH exposes protocol functions — oracle-fed storage, a sub-second timestamp, keyless deployment, volatile-data access control, a query of the remaining compute, and the registry of the system address and the sequencer — through contracts at fixed addresses.
Contracts deployed on the chain call them by address and ABI, and the node answers some of their methods itself.
If two nodes disagreed on which addresses are system contracts, on the code those addresses hold, or on which calls the node answers rather than the bytecode, a call to one of them would execute differently on each.

## Specification

### Registry

- `SATIN-SYSC-001` A node MUST treat the six contracts of the table below, at their addresses, as MegaETH's system contracts, and no other account.

| Contract                                                | Address                            | Page                                                                 |
| ------------------------------------------------------- | ---------------------------------- | -------------------------------------------------------------------- |
| Oracle                                                  | `ORACLE_CONTRACT_ADDRESS`          | [Oracle](oracle.md)                                                  |
| High-Precision Timestamp                                | `HIGH_PRECISION_TIMESTAMP_ADDRESS` | [High-Precision Timestamp](high-precision-timestamp.md)              |
| KeylessDeploy                                           | `KEYLESS_DEPLOY_ADDRESS`           | [KeylessDeploy](keyless-deploy.md)                                   |
| MegaAccessControl                                       | `MEGA_ACCESS_CONTROL_ADDRESS`      | [MegaAccessControl](mega-access-control.md)                          |
| MegaLimitControl                                        | `MEGA_LIMIT_CONTROL_ADDRESS`       | [MegaLimitControl](mega-limit-control.md)                            |
| SequencerRegistry                                       | `SEQUENCER_REGISTRY_ADDRESS`       | [SequencerRegistry](sequencer-registry.md)                           |

### Code

- `SATIN-SYSC-002` Each system contract's address MUST hold the code whose Keccak-256 code hash the table below names; that code hash is the normative identity of the contract's bytecode, and the bytecode defines every method a node does not intercept.
  The interface each contract page states is the ABI of that bytecode.
  The interface of KeylessDeploy no longer declares four errors (see [KeylessDeploy](keyless-deploy.md)); its bytecode is the one named below, which produces none of them.

| Contract                 | Version | Code hash                                                            |
| ------------------------ | ------- | -------------------------------------------------------------------- |
| Oracle                   | 2.0.0   | `ORACLE_CODE_HASH`                                                   |
| High-Precision Timestamp | N/A     | `HIGH_PRECISION_TIMESTAMP_CODE_HASH`                                 |
| KeylessDeploy            | 1.0.0   | `KEYLESS_DEPLOY_CODE_HASH`                                           |
| MegaAccessControl        | 1.0.0   | `MEGA_ACCESS_CONTROL_CODE_HASH`                                      |
| MegaLimitControl         | 1.0.0   | `MEGA_LIMIT_CONTROL_CODE_HASH`                                       |
| SequencerRegistry        | 2.0.0   | `SEQUENCER_REGISTRY_CODE_HASH`                                       |

- `SATIN-SYSC-003` A node MUST NOT deploy, upgrade or seed any system contract: no block installs code at a system-contract address or writes a system contract's storage other than through the execution of its transactions and its pre-block calls.
  The chain holds them when Satin activates, and the block in which Satin activates checks that each address holds the code above (see [Activation and Rex-Era Carry-Over](../block/activation.md)).

### Distinction from precompiles

- `SATIN-SYSC-004` A system contract MUST be executed as an account with code and storage, never as a precompile: it is read and written by `SLOAD`, `SSTORE`, `BALANCE` and every other account access as any account is, and a call to it runs its bytecode.
  The one exception is a call the node intercepts: a call to an intercepted method of a system contract is answered by the node, before a frame is built, as [Call Interception](interception.md) specifies, and every other call runs the contract's bytecode.
  A `keylessDeploy` call that is a transaction's own frame is a native creation rather than an interception (see [KeylessDeploy](keyless-deploy.md)).

## Constants

| Constant                             | Value                                                                | Description                                    |
| ------------------------------------ | -------------------------------------------------------------------- | ---------------------------------------------- |
| `ORACLE_CONTRACT_ADDRESS`            | `0x6342000000000000000000000000000000000001`                         | Oracle                                         |
| `HIGH_PRECISION_TIMESTAMP_ADDRESS`   | `0x6342000000000000000000000000000000000002`                         | High-Precision Timestamp                       |
| `KEYLESS_DEPLOY_ADDRESS`             | `0x6342000000000000000000000000000000000003`                         | KeylessDeploy                                  |
| `MEGA_ACCESS_CONTROL_ADDRESS`        | `0x6342000000000000000000000000000000000004`                         | MegaAccessControl                              |
| `MEGA_LIMIT_CONTROL_ADDRESS`         | `0x6342000000000000000000000000000000000005`                         | MegaLimitControl                               |
| `SEQUENCER_REGISTRY_ADDRESS`         | `0x6342000000000000000000000000000000000006`                         | SequencerRegistry                              |
| `ORACLE_CODE_HASH`                   | `0x71a65239db8d0f1bb765fad36e34f57600420d103a4401ef7555bd50b229dc55` | Oracle version 2.0.0                           |
| `HIGH_PRECISION_TIMESTAMP_CODE_HASH` | `0x1b2df8ca5350cd7106d67ed95532584526f97a5ca267c8eef73a1831f53720f2` | High-Precision Timestamp, the Oracle's address embedded |
| `KEYLESS_DEPLOY_CODE_HASH`           | `0x55020d41649acf7a84add6e628b887f802218d9ac86f142ef0994da43ea5eeb6` | KeylessDeploy version 1.0.0                    |
| `MEGA_ACCESS_CONTROL_CODE_HASH`      | `0x96d0f3ba6b474e9684a97e4388ec8dbb7929818b51e6b4f19f885ccbdf642f9b` | MegaAccessControl version 1.0.0                |
| `MEGA_LIMIT_CONTROL_CODE_HASH`       | `0x3927f2a4803c5e18153ff5742d0fa1acd9ad04538e4e6037cb4a9b28694ca87f` | MegaLimitControl version 1.0.0                 |
| `SEQUENCER_REGISTRY_CODE_HASH`       | `0xabd7e8f1c8f0f9ca0346df585b65d9791a7e9ba5c431cc4eda5d2c2f1f5e9c43` | SequencerRegistry version 2.0.0                |

The deployed bytecode of each version is published as the `deployedBytecode` field of its artifact in the [mega-evm repository](https://github.com/megaeth-labs/mega-evm/tree/main/crates/system-contracts/artifacts) (`Oracle-2.0.0.json`, `KeylessDeploy-1.0.0.json`, `MegaAccessControl-1.0.0.json`, `MegaLimitControl-1.0.0.json`, `SequencerRegistry-2.0.0.json`); its Keccak-256 hash is the code hash above.

## Rationale

**Why a code hash rather than a version name?**
A version name is a label; the code hash fixes the bytes every node executes.
Checking the hash once, at activation, is enough for a node to know that every later call to the contract runs the same methods everywhere.

**Why does Satin keep the Rex-era bytecode?**
Contracts deployed under Rex6 call these contracts by address and ABI, and the chain's storage in them — Oracle values, the registry's roles and histories — was written by that bytecode.
Satin changes how the node executes around them (Oracle reads, interception, keyless deployment), not the contracts; keeping the bytecode keeps every caller and every slot valid, and needs no upgrade at activation.

**Why does Satin deploy nothing?**
A chain reaches Satin through the Rex-era forks, which installed the six contracts at the versions Satin runs (Rex5 deployed the SequencerRegistry and upgraded the Oracle to 2.0.0; Rex6 upgraded the SequencerRegistry to 2.0.0).
Deploying them again would rewrite state the chain already holds; checking them instead fails closed on a chain that does not hold them.

## Security Considerations

- A node that treats another address as a system contract, or runs a system contract as a precompile, gives calls to it another result than every other node, and builds a different state.
- A chain whose system-contract address held other code would let that code answer as the Oracle or the registry; the activation check of [Activation and Rex-Era Carry-Over](../block/activation.md) is what refuses such a chain, so a node that skips it runs Satin on contracts nobody verified.
- A node that deploys or re-seeds a contract at activation overwrites the registry's roles or the Oracle's storage, changing the live system address and the values contracts read.

## Spec History

- [MiniRex](../../upgrades/minirex.md) — Introduced the Oracle and the High-Precision Timestamp.
- [Rex2](../../upgrades/rex2.md) — Introduced KeylessDeploy.
- [Rex4](../../upgrades/rex4.md) — Introduced MegaAccessControl and MegaLimitControl.
- [Rex5](../../upgrades/rex5.md) — Introduced the SequencerRegistry and upgraded the Oracle to 2.0.0.
- [Rex6](../../upgrades/rex6.md) — Upgraded the SequencerRegistry to 2.0.0; the Rex6 registry is specified in [System Contracts](../../system-contracts/overview.md).
- [Satin](../../upgrades/satin.md) — Keeps the six contracts' bytecode, deploys none of them, and checks them at activation.
