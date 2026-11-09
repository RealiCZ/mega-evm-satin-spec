---
description: Satin (unstable) — SequencerRegistry. The registry of the system address and the sequencer: its code, storage and interface, its deployment, seeding and migration in every block, the block's resolution of the live system address from it, and its role changes applied by the pre-block step.
spec: Satin
maturity: unstable
---

# SequencerRegistry

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
{% endhint %}

Abstract: The SequencerRegistry system contract, which holds two roles — the system address that sends Mega System Transactions and the sequencer that signs mini-blocks — with their change schedules and histories: its code, storage layout and interface, its deployment, seeding and migration in every block, the block's resolution of the live system address from it, and how a role change takes effect.

## Motivation

The address that sends the protocol's maintenance transactions, and the key that signs mini-blocks, must each be changeable without redeploying the contracts that depend on them, and a change must not take effect in the middle of a block.
Every node must also agree, for every transaction, on which address is the system address: a transaction from it is the protocol's own, exempt from fees and limits, and the same transaction from any other address is a user's.
If nodes read the system address at different points, or from different state, they classify the same transaction differently; and if they seeded or upgraded the registry differently, they would hold different roles from the first block that has one.

## Specification

### The contract

- `SATIN-REG-001` The SequencerRegistry MUST be the account at `SEQUENCER_REGISTRY_ADDRESS` holding the code of version 2.0.0 (`SEQUENCER_REGISTRY_CODE_HASH`, see [System Contracts](overview.md)), which has no interceptor: every call to it runs its bytecode.
  Its storage layout, interface and behaviour are the following.

  **Storage layout.**

| Slot | Name                            | Type             |
| ---- | ------------------------------- | ---------------- |
| 0    | `_currentSystemAddress`         | `address`        |
| 1    | `_currentSequencer`             | `address`        |
| 2    | `_admin`                        | `address`        |
| 3    | `_pendingAdmin`                 | `address`        |
| 4    | `_initialSystemAddress`         | `address`        |
| 5    | `_initialSequencer`             | `address`        |
| 6    | `_initialFromBlock`             | `uint256`        |
| 7    | `_pendingSystemAddress`         | `address`        |
| 8    | `_systemAddressActivationBlock` | `uint256`        |
| 9    | `_pendingSequencer`             | `address`        |
| 10   | `_sequencerActivationBlock`     | `uint256`        |
| 11   | `_systemAddressHistory`         | `ChangeRecord[]` |
| 12   | `_sequencerHistory`             | `ChangeRecord[]` |
| 13   | `_minRotationDelay`             | `uint256`        |

  A `ChangeRecord` is packed in one slot as `uint96 fromBlock` followed by `address addr`.
  Slots 0 to 12 are those of version 1.0.0; slot 13 is version 2.0.0's.
  A later version of the contract MUST only append storage slots after slot 13: it MUST NOT reorder the slots above or insert a slot before slot 14, since the keys of the two history arrays derive from their slots.

  **Interface.**

```solidity
interface ISequencerRegistry {
    struct ChangeRecord { uint96 fromBlock; address addr; }

    function currentSystemAddress() external view returns (address);
    function systemAddressAt(uint256 blockNumber) external view returns (address);
    function scheduleNextSystemAddressChange(address newSystemAddress, uint256 activationBlock) external;
    event SystemAddressChangeScheduled(address indexed oldSystemAddress, address indexed newSystemAddress, uint256 activationBlock);

    function currentSequencer() external view returns (address);
    function sequencerAt(uint256 blockNumber) external view returns (address);
    function scheduleNextSequencerChange(address newSequencer, uint256 activationBlock, bytes calldata newSequencerSignature) external;
    event SequencerChangeScheduled(address indexed oldSequencer, address indexed newSequencer, uint256 activationBlock);

    function minRotationDelay() external view returns (uint256);
    function rotationDigest(address newSequencer, uint256 activationBlock) external view returns (bytes32);

    function applyPendingChanges() external;
    function admin() external view returns (address);
    function pendingAdmin() external view returns (address);
    function transferAdmin(address newAdmin) external;
    function acceptAdmin() external;
    event AdminTransferStarted(address indexed currentAdmin, address indexed newPendingAdmin);
    event AdminTransferred(address indexed oldAdmin, address indexed newAdmin);

    function version() external view returns (string memory); // "2.0.0"

    error FutureBlock();
    error BeforeInitialBlock();
    error NotAdmin();
    error NotPendingAdmin();
    error ZeroAddress();
    error InvalidActivationBlock();
    error ActivationBlockTooLarge();
    error RotationDelayTooShort();
    error InvalidRotationProof();
}
```

  **Reads.** `currentSystemAddress()` and `currentSequencer()` return slots 0 and 1, which only `applyPendingChanges()` updates.
  `systemAddressAt(n)` and `sequencerAt(n)` return the role's address active at block `n`, from its history; they revert with `FutureBlock()` when `n` is above the current block number and with `BeforeInitialBlock()` when `n` is below `_initialFromBlock`, which both roles share.

  **Scheduling.** Only the admin may schedule a change (`NotAdmin()` otherwise).
  Each role has at most one pending change; a new schedule overwrites it.
  Both scheduling methods first require the activation block to be above the current block number (`InvalidActivationBlock()`).
  An activation block of `type(uint256).max` then cancels the role's pending change: the new address MUST be zero, and a non-zero one reverts with `ZeroAddress()`; a sequencer change's signature is ignored; and no other check is made, the `uint96` bound included, so `(0x11…11, type(uint256).max)` reverts with `ZeroAddress()` and not `ActivationBlockTooLarge()`.
  Any other activation block MUST fit in a `uint96` (`ActivationBlockTooLarge()`), and the new address MUST be non-zero (`ZeroAddress()`).
  A sequencer change MUST further satisfy `activationBlock ≥ block.number + minRotationDelay()` (`RotationDelayTooShort()`) and carry `newSequencerSignature`, a 65-byte `r ‖ s ‖ v` signature by the new sequencer's key over `rotationDigest(newSequencer, activationBlock)`, with `s` at most half the secp256k1 order and `v` 27 or 28, recovering to `newSequencer` (`InvalidRotationProof()` otherwise).
  The checks of a sequencer change are made in the order `InvalidActivationBlock`, the cancellation, `ActivationBlockTooLarge`, `ZeroAddress`, `RotationDelayTooShort`, the signature.
  `rotationDigest` is the [EIP-712](https://eips.ethereum.org/EIPS/eip-712) digest `keccak256(0x1901 ‖ domainSeparator ‖ keccak256(abi.encode(SEQUENCER_ROTATION_TYPEHASH, newSequencer, activationBlock)))` with the domain `name = ROTATION_DOMAIN_NAME`, `version = ROTATION_DOMAIN_VERSION`, `chainId = block.chainid`, `verifyingContract` the registry, the domain separator computed at each call.

  **Applying.** `applyPendingChanges()` is permissionless: for each role whose pending change is due — a non-zero pending address whose activation block is at most the current block number — it sets the current address, appends a `ChangeRecord` to the role's history and clears the pending slots, both roles in one call.

  **Admin transfer.** `transferAdmin(newAdmin)`, by the admin, sets `_pendingAdmin` (zero cancels) and emits `AdminTransferStarted`; the admin's authority is unchanged until `acceptAdmin()`, by the pending admin alone (`NotPendingAdmin()` otherwise), sets `_admin` to the caller, clears `_pendingAdmin` and emits `AdminTransferred`.

### The live system address

- `SATIN-REG-002` Once per block, after every other pre-block step (see [System Calls and the Pre-Block Sequence](../block/system-calls.md)), the node MUST resolve the block's live system address from the registry: it loads the registry's account and slot 0 (`_currentSystemAddress`) from the state those steps left, compares the account's code hash with `SEQUENCER_REGISTRY_CODE_HASH`, and takes the address the slot holds.
  The read MUST compare the code hash and MUST NOT load or run the registry's code; it is not charged, writes nothing, and is committed as a read-only state of the pre-block phase, after the other steps (see [The Stateless Witness](../block/stateless-witness.md)).
  Every transaction of the block MUST be classified against that address; no transaction reads the registry, or finds its account or slot warm, for its classification.
- `SATIN-REG-004` A registry that is absent, holds other code, or whose slot 0 is zero when the block resolves the live system address MUST make the block invalid.
- `SATIN-REG-007` A registry read the node fails to make — in the resolution, in the due-change read of the pre-block sequence, or in the registry's deployment — MUST be reported as an internal error of the node, never as an invalid block or as a result of a transaction (see [System Calls and the Pre-Block Sequence](../block/system-calls.md)).

### Role changes

- `SATIN-REG-005` A role change takes effect only in a later block than the one that scheduled it, and only through that block's pre-block call to `applyPendingChanges()` (see [System Calls and the Pre-Block Sequence](../block/system-calls.md)).
  So every transaction of a block is classified against the address the block resolved after its pre-block steps (`SATIN-REG-002`), and a call to `applyPendingChanges()` inside a block finds no change due that the pre-block step did not apply.
- `SATIN-REG-006` The registry's roles MUST be what its storage holds: a node writes them only when it deploys the registry new (`SATIN-REG-008`), from the bootstrap values of the chain configuration (`SATIN-REG-009`), and MUST NOT otherwise seed, overwrite or derive them.

### Deployment

- `SATIN-REG-008` Every block MUST deploy the registry as a step of its pre-block sequence, after the due-change read and the `applyPendingChanges()` call (see [System Calls and the Pre-Block Sequence](../block/system-calls.md)), by what the state then holds at `SEQUENCER_REGISTRY_ADDRESS`:
  - an account whose code hash is `SEQUENCER_REGISTRY_CODE_HASH` (version 2.0.0) MUST be left as it is, and recorded as a read-only entry;
  - an account whose code hash is `SEQUENCER_REGISTRY_V1_CODE_HASH` (version 1.0.0) MUST be migrated in place: its code replaced by version 2.0.0, slot 13 (`_minRotationDelay`) written with the configured minimum rotation delay, and every other slot — the roles, the pending changes, the histories — kept, as its nonce and balance are;
  - an address with no account, or an account without code, MUST receive version 2.0.0 as a new contract, an existing account's nonce and balance kept and its storage cleared, and its storage seeded with: slots 0 (`_currentSystemAddress`) and 4 (`_initialSystemAddress`) the address `MEGA_SYSTEM_ADDRESS`; slots 1 (`_currentSequencer`) and 5 (`_initialSequencer`) the configured initial sequencer; slot 2 (`_admin`) the configured initial admin; slot 6 (`_initialFromBlock`) the block's number; and slot 13 (`_minRotationDelay`) the configured minimum rotation delay;
  - an account holding any other code MUST make the block invalid: the registry's storage is never overwritten by code it was not migrated to.

  The step writes nothing else, is charged nothing and counts toward none of the block's counters.
- `SATIN-REG-009` A chain configuration that schedules Satin MUST carry the registry's bootstrap values, under the keys the Rex era introduced: `rex5InitialSequencer` and `rex5InitialAdmin`, each a non-zero address, and `rex6MinRotationDelay`, a non-zero number of blocks.
  A node MUST refuse a configuration that lacks one of them or gives one as zero.
  The values are read only by the deployment of `SATIN-REG-008`, every block; once the registry holds its roles, its storage, not the configuration, decides them.

### Retired ids

- `SATIN-REG-003` Retired, removed: no transaction reads the registry, or finds its account or slot warm, for its classification; the block resolves the live system address once (`SATIN-REG-002`).

## Constants

| Constant                       | Value                                                                | Description                                  |
| ------------------------------ | -------------------------------------------------------------------- | -------------------------------------------- |
| `SEQUENCER_REGISTRY_ADDRESS`   | `0x6342000000000000000000000000000000000006`                         | SequencerRegistry                            |
| `SEQUENCER_REGISTRY_CODE_HASH` | `0xabd7e8f1c8f0f9ca0346df585b65d9791a7e9ba5c431cc4eda5d2c2f1f5e9c43` | SequencerRegistry version 2.0.0              |
| `SEQUENCER_REGISTRY_V1_CODE_HASH` | `0x63cd411a379be1c198613ef1d15c3058e7b0db4a5d07d4bcf07014af90040315` | SequencerRegistry version 1.0.0, migrated in place |
| `MEGA_SYSTEM_ADDRESS`          | `0xA887dCB9D5f39Ef79272801d05Abdf707CFBbD1d`                         | The initial system address a new registry is seeded with |
| `SEQUENCER_ROTATION_TYPEHASH`  | `0xaebf84f20bcc14afc14200ed16cfb9314ef205d4d1d8fbcc0a256c39a3e79aa9` | `keccak256("SequencerRotation(address newSequencer,uint256 activationBlock)")` |
| `ROTATION_DOMAIN_NAME`         | `MegaETH SequencerRegistry`                                          | EIP-712 domain name of the rotation proof    |
| `ROTATION_DOMAIN_VERSION`      | `1`                                                                  | EIP-712 domain version of the rotation proof |

## Rationale

**Why two roles?**
The sender of maintenance transactions and the mini-block signing key are different keys with different operations; coupling them would make every sequencer key change revoke the Oracle's authority.

**Why resolve the system address once per block?**
A role change takes effect only in a block's pre-block step, so one read after those steps names the system address for every transaction of the block, as Rex6 resolves it.
The read is a read-only state of the pre-block phase, so a stateless validator holds it in the witness; and since no transaction reads or warms the registry for its classification, no transaction's gas or read set depends on that read.

**Why compare the code hash, and fail the block?**
A registry with other code could name any address the system address; the hash fixes the contract whose slot 0 means what it says, and comparing it needs no code load.
A registry that is absent, holds other code or names no system address after the deployment step can only come from a corrupted state or a wrong configuration; as in Rex6 the block is then invalid, rather than executed as a block whose protocol transactions are users'.

**Why seed the registry from the configuration?**
`_initialFromBlock` is the number of the block that deploys the registry, which no bytecode constant can carry, and the initial sequencer, the admin and the rotation delay are each network's own; seeding them at the deployment keeps one code hash for every network, as Rex6 does.
The initial system address is not configurable: it is `MEGA_SYSTEM_ADDRESS`, the address every node, pool and replay path treats as the system address until the registry names another.

**Why never overwrite other code at the registry's address?**
Unlike the other system contracts, the registry holds roles and histories in its storage; replacing foreign code without a migration for it would reinterpret that storage under another layout.
The one migration is version 1.0.0's, whose slots 0 to 12 version 2.0.0 keeps: the code is replaced and only the new slot written, so a pending change scheduled under version 1.0.0 still activates.

## Security Considerations

- A node that resolved the system address from another state than the one the block's pre-block steps left would treat a retired system address's transactions as the protocol's, or the new one's as a user's.
- A node that did not check the code hash, or executed a block whose registry names no system address, would let other code at the registry's address name a system address, and so exempt arbitrary transactions from fees and limits, or run a block without the protocol's transactions.
- A node that seeded the registry over an existing one, or replaced foreign code at its address, would reset or reinterpret its roles and histories.
- The possession proof keeps a sequencer change from naming a key nobody holds; the rotation delay leaves a window to cancel a bad change. A registry without them could halt block production at the activation block.
- A node that warmed the registry for a transaction, or charged a transaction for the resolution, would compute another gas used for every transaction that touches the registry.

## Spec History

- [Rex5](../../upgrades/rex5.md) — Introduced the SequencerRegistry at version 1.0.0.
- [Rex6](../../upgrades/rex6.md) — Upgraded it to version 2.0.0 in place (rotation proof and delay); the Rex6 registry is specified in [SequencerRegistry](../../system-contracts/sequencer-registry.md).
- [Satin](../../upgrades/satin.md) — The registry, its deployment and its resolution once per block are Rex6's; its layout's append-only rule is restated.
