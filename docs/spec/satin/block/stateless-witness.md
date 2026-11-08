---
description: Satin (unstable) — The Stateless Witness. What a stateless validator re-executing a block is given — the accounts, slots, code, block hashes, SALT capacities and oracle answers the block read — where each read lands, and the check a replay must pass.
spec: Satin
maturity: unstable
---

# The Stateless Witness

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
{% endhint %}

Abstract: The witness a stateless validator re-executes a block from: the state, code, block hashes, SALT bucket capacities and oracle answers it holds; which reads a transaction and the pre-block phase make and in which committed state each lands; the inputs a validator is given beside the witness; the exports block execution makes; and the check a replay on the witness must pass.

## Motivation

A stateless validator holds no state: it re-executes a block from a witness of what the block read.
The witness is built from what the block's execution reports, so the building node and the validator must agree exactly on which accounts, slots and code a block reads, on what is read outside the state — block hashes, SALT bucket capacities, oracle answers — and on where each read is reported.
A read the building node does not report is missing from the witness, and the validator cannot execute the block; a read reported in a place the node does not collect is lost the same way; and a value served from outside the state that the validator cannot reproduce makes it compute another block.

## Specification

### The witness

- `SATIN-WIT-001` A block's witness MUST hold:
  - every account and every storage slot the block loads, in a pre-block step or in a transaction the block includes, as the chain held it before the block: an absent account recorded as absent, an empty slot of an account the chain holds recorded as zero, and no slot of an absent account;
  - the code the chain held before the block for every such account, whether or not the load that named the account loaded its code;
  - the hash of every block `BLOCKHASH` read during the block's execution (`SATIN-WIT-014`);
  - the capacity of every SALT bucket the block's execution exports (`SATIN-WIT-013`);
  - the oracle service's answer to every Oracle read the block's included transactions recorded, in block order (`SATIN-WIT-015`).
- `SATIN-WIT-002` A transaction MUST load every account and slot its execution reads from the state: in its validation (the registry's account and slot 0 every transaction reads included, see [SequencerRegistry](../system-contracts/sequencer-registry.md)), in its fee settlement, and in any of its frames — a frame that reverted, halted or was stopped, and a frame of a deposit that failed, included.
  A failed frame's writes are taken back, not its reads; a failed deposit takes back everything but its sender's nonce bump and mint, not its reads.
- `SATIN-WIT-003` The L1 block information a transaction is priced against MUST be loaded by the pre-block phase for the whole block (`SATIN-WIT-011`), not by the transaction.
- `SATIN-WIT-004` A read that gas or a limit skipped MUST load nothing (`SATIN-WIT-012`), with one exception: an authority account the EIP-7702 authorization preflight consulted MUST be loaded, with its code, whether or not the list is then applied.
  The preflight consults every authority whose entry passes the chain-id, nonce and signature gates, each distinct authority once, the whole list walked (see [EIP-7702 Authorizations Before the First Frame](../evm/authorizations.md)).
- `SATIN-WIT-005` Execution MUST report what it loaded in the states the block commits: each pre-block step in the state it commits on its own, and each transaction in its returned state, which names every account and slot the transaction loaded, whether it wrote it or not, whether the frame that loaded it succeeded or not, and, for a deposit, whether the deposit failed or not.
  The set of loads is a function of those states and of the exports alone, not of how the node caches state: a state names the keys it loaded even when a cache another block filled served the value.
  A state names the keys; the values are the chain's.
- `SATIN-WIT-006` A slot of an account the chain does not hold before the block MUST NOT be recorded: such an account has no storage, and a validator MUST answer every slot of it with zero without looking it up.
- `SATIN-WIT-007` The code a witness holds MUST be the chain's before the block, not the code a returned state carries: a transaction that replaces an account's code — an EIP-7702 authority delegated anew — is admitted against the code the chain held, and its returned state carries the code it wrote.
- `SATIN-WIT-017` A node MUST answer an address its state holds no account for as no account, never as an empty account, which is a leaf the state holds: the destruction table gives an account's leaf back only when no account stood at the address at the transaction's start (see [SELFDESTRUCT and the Destruction Table](../evm/selfdestruct.md)).

### Where each read lands

- `SATIN-WIT-008` A transaction's loads MUST be in its returned state: its sender, its recipient or created address, every account and every slot any of its frames loads, the fee recipients, the registry's account and slot 0, every authority account the authorization preflight consulted, and a keyless deployment's signer and deploy address; the state names an account whether or not the load brought its code.
  The pre-block phase's loads MUST be in the states it commits, one per step and in the step order of [System Calls and the Pre-Block Sequence](system-calls.md): the EIP-2935 call's state, the EIP-4788 call's state, in Satin's activation block each predeploy's read-only entry, the registry's account and pending slots the due-change read loaded, the `applyPendingChanges()` call's state when the call is made, and last the L1 block information.
  Each state MUST be committed whole, read-only entries included, and a node MUST collect the states as they are committed: what a commit keeps of a state is only what it changed, which holds none of the read-only entries.
- `SATIN-WIT-009` `BLOCKHASH` reads the chain's history outside the transaction's journal, and its reads MUST be exported (`SATIN-WIT-014`); a SALT bucket's capacity and the oracle service's answer are read outside the database, and MUST be exported (`SATIN-WIT-013`) or recorded (`SATIN-WIT-015`).
- `SATIN-WIT-010` A validator MUST be given, beside the witness: the block's header, the chain configuration (its fork schedule), the parent block's hash and timestamp, the parent beacon block root, and the block's extra data.
  Whether the block admits only deposits, and whether Satin activates in it, MUST be derived from the chain configuration and the two timestamps, as [Activation and Rex-Era Carry-Over](activation.md) specifies; `SLOTNUM` pushes zero (see [Base Layer](../base-layer.md)), so no slot number is an input.

### The L1 block information

- `SATIN-WIT-011` A non-deposit transaction is priced against the L1 block contract at `L1_BLOCK_ADDRESS`: its L1 base fee slot (1), its Ecotone fee scalars slot (3), its Ecotone blob base fee slot (7), its operator fee scalars slot (8), which also holds the data-availability footprint gas scalar, and, only when the Ecotone scalars are empty (the blob base fee scalar and the eight bytes of the two scalars zero), its L1 fee overhead slot (5).
  These reads are made on the block's state, not through a transaction's journal, so they land in no transaction's returned state; none is made before the block's first non-deposit transaction other than a Mega System Transaction, and each finds the state the transactions before it left.
  The pre-block phase MUST therefore read the contract's account and all five slots, whatever the scalars it reads hold, and commit them as a state of its own, of read-only entries, after every other pre-block step.
  A state that holds no contract at the address MUST record the account as absent and read no slot.
  A state that cannot serve the account or one of the five slots of a contract it holds MUST fail the block as an internal error of the node, not a verdict on the block — for a stateless validator, a defect of the witness it was given — whether or not a transaction would have been priced with it.
  The read changes nothing: the entries are not written.

### Reads a validator makes again

- `SATIN-WIT-012` A read that gas or a limit skipped is skipped again on replay, so the witness MUST NOT be required to carry it: a cold `SLOAD` or account load with less gas than its cold surcharge, a `BLOCKHASH` of the current block, a future block or a block outside the last `BLOCKHASH_WINDOW` blocks, an Oracle read the frame cannot pay, a read refused in a frame whose volatile-data access is off, a keyless deployment's reads after a step refused it, and the bucket of a state charge a system-originated transaction or a system call makes.

### The exports

- `SATIN-WIT-013` Block execution MUST export the set of SALT buckets the SALT environment answered with a valid capacity during the block, emptied when the block starts and accumulated over everything executed for the block.
  A bucket is in the set once it was answered with a valid capacity, whether or not the transaction that asked is in the block.
  A lookup that failed MUST NOT be in the set, whether the environment could not answer it or answered a capacity below `MIN_BUCKET_SIZE`: it is a fault of the node, for a deposit as for any transaction (see [Halts, Reverts and Stops](../evm/outcomes.md)).
  A witness MUST prove the capacity of every bucket in the set.
  A node that runs the block's transactions on several executions, or that empties the set between transactions, MUST take the union of what each reports; a transaction executed elsewhere and committed into the block adds nothing to the set of the execution it was committed into.
  The pre-block calls and the system-originated transactions price at `m = 1` and add no bucket.
  Which bucket an account or a slot lands in is SALT's own definition (see [State Gas and SALT Pricing](../evm/state-gas.md)).
- `SATIN-WIT-014` Block execution MUST export every block hash `BLOCKHASH` was served during the block, emptied when the block starts; it is not what a node's state cache holds, which may carry hashes an earlier block read.
- `SATIN-WIT-015` The oracle records:
  - Execution MUST record every Oracle read a transaction makes through the service, with the service's answer, in order, on the transaction's outcome; an answer can be none, where the service had no value and the slot's loaded value stood.
  - A node MUST take the records of the transactions it includes from their outcomes, in block order, and nothing of a candidate it executed and dropped.
  - A validator MUST either be given those records and answer each Oracle read its own execution makes from them, in order; or run no service and find each answer in the Oracle's slot at its read — the value the journal holds for the slot when the read is made, as the block's earlier included transactions and the reading transaction's own frames left it.
    The second reproduces the block only when every answer an included transaction recorded equals the slot's value at that read, which an answer of none always does.
  - A node that serves validators running no service MUST either give them the included transactions' own records, or leave out of the block every transaction whose recorded answers the slot cannot hold at its reads.

  Hints reach the service alone: they are not in the witness, and change nothing a validator computes except through the answers the records carry.

### The check

- `SATIN-WIT-016` A block replayed on exactly its witness MUST produce the same receipts, state changes, gas ledgers, logs and block counters as the block's execution, and MUST read nothing the witness does not hold.
  Its exports MUST be a subset of the building node's, and MAY be a proper one: the building node's also hold the buckets and block hashes that candidates it executed and dropped asked for.

## Constants

| Constant           | Value                                        | Description                                                  |
| ------------------ | -------------------------------------------- | ------------------------------------------------------------ |
| `L1_BLOCK_ADDRESS` | `0x4200000000000000000000000000000000000015` | The OP Stack L1 block contract                               |
| `BLOCKHASH_WINDOW` | 256                                          | The number of most recent blocks whose hash `BLOCKHASH` serves |
| `MIN_BUCKET_SIZE`  | 256                                          | The least valid SALT bucket capacity (see [State Gas and SALT Pricing](../evm/state-gas.md)) |

## Rationale

**Why define the witness by the committed states?**
The states a block commits are what every node produces anyway; defining the witness by them, rather than by a node's caches, makes it a function of the execution alone, so two nodes with different caches build the same witness.

**Why commit read-only states in the pre-block phase?**
The activation check, the due-change read and the L1 information read write nothing, so a commit that keeps only changes would lose them; committing them as read-only states puts their loads where the witness is collected.

**Why read the L1 overhead slot even when the scalars are set?**
Whether a transaction reads the overhead depends on the scalars the transactions before it left, which the pre-block phase cannot know; reading all five slots keeps the witness sufficient whatever the block's deposits write.

**Why can a validator run without a service only under a condition?**
One transaction can be answered two values for one slot — it reads the slot, sends a hint that has the service fetch another value, and reads it again — while only the system address writes the slot; no single slot value reproduces both answers.
A validator without a service therefore needs either the records or a block in which every answer is the slot's value.

**Why does an authority the preflight consulted stay loaded?**
The authorization list is decided by a simulation that reads each authority before it knows whether the list fits; a validator re-executing the decision makes the same reads, so the witness must hold them whether or not the list is applied.

**Why is a failed SALT lookup not exported?**
A lookup that failed gave the transaction no outcome; a bucket in the export the witness must prove would then be one no included transaction priced with.

## Security Considerations

- A node that collects only what a commit keeps produces a witness without the activation block's predeploys, the registry's pending slots and the L1 information; a validator given it cannot execute the block.
- A node that answers an absent account as an empty one gives no destruction the account's leaf back, and executes a different chain from a node that answers it as absent.
- A node that exports the hashes its cache holds, rather than those served, gives validators a witness that differs from another node's for the same block.
- A node that includes a transaction whose oracle answers the slot cannot hold, while serving validators without a service and without records, produces a block those validators compute differently.

## Spec History

- [Rex6](../../upgrades/rex6.md) — Exported the SALT buckets of one cache and whatever block hashes the state cache held; the pre-block states were collected through a hook, and the L1 information landed in no collected state.
- [Satin](../../upgrades/satin.md) — The witness defined by the committed states and exports, the read-only pre-block states, and the oracle records.
