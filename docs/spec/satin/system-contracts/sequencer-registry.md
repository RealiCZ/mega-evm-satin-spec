---
description: Satin (unstable) — SequencerRegistry. The registry of the system address and the sequencer: its code, storage and interface, the read every transaction makes of it for the live system address, and its role changes applied by the pre-block step.
spec: Satin
maturity: unstable
---

# SequencerRegistry

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
{% endhint %}

Abstract: The SequencerRegistry system contract, which holds two roles — the system address that sends Mega System Transactions and the sequencer that signs mini-blocks — with their change schedules and histories: its code, storage layout and interface, the read every transaction makes of it for the live system address, and how a role change takes effect.

## Motivation

The address that sends the protocol's maintenance transactions, and the key that signs mini-blocks, must each be changeable without redeploying the contracts that depend on them, and a change must not take effect in the middle of a block.
Every node must also agree, for every transaction, on which address is the system address: a transaction from it is the protocol's own, exempt from fees and limits, and the same transaction from any other address is a user's.
If nodes read the system address at different points, or from different state, they classify the same transaction differently.

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
  The pair `(address(0), type(uint256).max)` cancels the pending change and needs no other check.
  Otherwise the activation block MUST be above the current block number (`InvalidActivationBlock()`), fit in a `uint96` (`ActivationBlockTooLarge()`), and the new address MUST be non-zero (`ZeroAddress()`).
  A sequencer change MUST further satisfy `activationBlock ≥ block.number + minRotationDelay()` (`RotationDelayTooShort()`) and carry `newSequencerSignature`, a 65-byte `r ‖ s ‖ v` signature by the new sequencer's key over `rotationDigest(newSequencer, activationBlock)`, with `s` at most half the secp256k1 order and `v` 27 or 28, recovering to `newSequencer` (`InvalidRotationProof()` otherwise).
  The checks of a sequencer change are made in the order `InvalidActivationBlock`, the cancellation, `ActivationBlockTooLarge`, `ZeroAddress`, `RotationDelayTooShort`, the signature.
  `rotationDigest` is the [EIP-712](https://eips.ethereum.org/EIPS/eip-712) digest `keccak256(0x1901 ‖ domainSeparator ‖ keccak256(abi.encode(SEQUENCER_ROTATION_TYPEHASH, newSequencer, activationBlock)))` with the domain `name = ROTATION_DOMAIN_NAME`, `version = ROTATION_DOMAIN_VERSION`, `chainId = block.chainid`, `verifyingContract` the registry, the domain separator computed at each call.

  **Applying.** `applyPendingChanges()` is permissionless: for each role whose pending change is due — a non-zero pending address whose activation block is at most the current block number — it sets the current address, appends a `ChangeRecord` to the role's history and clears the pending slots, both roles in one call.

  **Admin transfer.** `transferAdmin(newAdmin)`, by the admin, sets `_pendingAdmin` (zero cancels) and emits `AdminTransferStarted`; the admin's authority is unchanged until `acceptAdmin()`, by the pending admin alone (`NotPendingAdmin()` otherwise), sets `_admin` to the caller, clears `_pendingAdmin` and emits `AdminTransferred`.

### The live system address

- `SATIN-REG-002` Every transaction MUST read the registry when it is validated, whatever its type and whoever sent it: the node loads the registry's account and, from the transaction's own state, slot 0 (`_currentSystemAddress`).
  When the account's code hash is `SEQUENCER_REGISTRY_CODE_HASH` and the slot holds a non-zero value, the address the slot holds is the live system address for the transaction.
  The read MUST compare the account's code hash and MUST NOT load or run the registry's code.
- `SATIN-REG-003` The registry's account and slot 0 MUST be warm for the rest of the transaction, whatever the registry holds, as the block beneficiary is under [EIP-3651](https://eips.ethereum.org/EIPS/eip-3651).
  The read MUST NOT be charged and MUST write nothing, and it MUST land in the transaction's returned state, and so in the block's witness, whatever the pre-block states also hold of the registry (see [The Stateless Witness](../block/stateless-witness.md)).
- `SATIN-REG-004` A registry that is absent, holds other code, or whose slot 0 is zero names no live system address, and then no transaction is a Mega System Transaction (see [Mega System Transactions](system-tx.md)).
- `SATIN-REG-007` A registry read the node fails to make MUST give the transaction no outcome: it is a fault of the node, never a refusal or a result of the transaction (see [Transaction Validation and Refusals](../block/transaction-validation.md)).

### Role changes

- `SATIN-REG-005` A role change takes effect only in a later block than the one that scheduled it, and only through that block's pre-block call to `applyPendingChanges()` (see [System Calls and the Pre-Block Sequence](../block/system-calls.md)).
  So every transaction of a block MUST read the system address the block's pre-block step left, and a call to `applyPendingChanges()` inside a block finds no change due that the pre-block step did not apply.
- `SATIN-REG-006` The registry's roles MUST be what its storage holds.
  A node MUST NOT seed, overwrite or derive them from chain configuration: Satin reads no configuration key for the registry.

## Constants

| Constant                       | Value                                                                | Description                                  |
| ------------------------------ | -------------------------------------------------------------------- | -------------------------------------------- |
| `SEQUENCER_REGISTRY_ADDRESS`   | `0x6342000000000000000000000000000000000006`                         | SequencerRegistry                            |
| `SEQUENCER_REGISTRY_CODE_HASH` | `0xabd7e8f1c8f0f9ca0346df585b65d9791a7e9ba5c431cc4eda5d2c2f1f5e9c43` | SequencerRegistry version 2.0.0              |
| `SEQUENCER_ROTATION_TYPEHASH`  | `0xaebf84f20bcc14afc14200ed16cfb9314ef205d4d1d8fbcc0a256c39a3e79aa9` | `keccak256("SequencerRotation(address newSequencer,uint256 activationBlock)")` |
| `ROTATION_DOMAIN_NAME`         | `MegaETH SequencerRegistry`                                          | EIP-712 domain name of the rotation proof    |
| `ROTATION_DOMAIN_VERSION`      | `1`                                                                  | EIP-712 domain version of the rotation proof |

## Rationale

**Why two roles?**
The sender of maintenance transactions and the mini-block signing key are different keys with different operations; coupling them would make every sequencer key change revoke the Oracle's authority.

**Why does every transaction read the registry itself?**
Rex6 resolved the system address once per block, after the pre-block changes, and handed it to execution.
Reading it in every transaction's own state makes the classification a function of the state the transaction runs on, which a stateless validator holds in the witness; since a change can only take effect in a later block's pre-block step, every transaction of a block reads the same address.

**Why is the read warm and free?**
Every transaction makes it, whatever it does; charging it, or leaving the account cold, would make the first access to the registry cost differently depending on whether the protocol had read it, which is not the transaction's doing.

**Why compare the code hash?**
A registry with other code could name any address the system address; the hash fixes the contract whose slot 0 means what it says, and comparing it needs no code load.

**Why does Satin read no configuration for the roles?**
The Rex5 and Rex6 activations seeded the registry from their own configuration keys; from then on the roles are state, changed only through the registry.

## Security Considerations

- A node that resolved the system address from another state than the transaction's own would treat a retired system address's transactions as the protocol's, or the new one's as a user's.
- A node that did not check the code hash would let other code at the registry's address name a system address, and so exempt arbitrary transactions from fees and limits.
- The possession proof keeps a sequencer change from naming a key nobody holds; the rotation delay leaves a window to cancel a bad change. A registry without them could halt block production at the activation block.
- A node that counted the registry read as cold, or charged it, would compute another gas used for every transaction that touches the registry.

## Spec History

- [Rex5](../../upgrades/rex5.md) — Introduced the SequencerRegistry at version 1.0.0.
- [Rex6](../../upgrades/rex6.md) — Upgraded it to version 2.0.0 in place (rotation proof and delay); the Rex6 registry is specified in [SequencerRegistry](../../system-contracts/sequencer-registry.md).
- [Satin](../../upgrades/satin.md) — Every transaction reads the live system address from the registry itself; Satin seeds and upgrades nothing.
