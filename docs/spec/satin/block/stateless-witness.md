---
description: Satin (unstable) — The Stateless Witness. What a stateless validator re-executing a block is given — the accounts, slots, code, block hashes and SALT capacities the block read — where each read lands, and the check a replay must pass.
spec: Satin
maturity: unstable
---

# The Stateless Witness

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
{% endhint %}

Abstract: The witness a stateless validator re-executes a block from: the state, code, block hashes and SALT bucket capacities it holds; which reads a transaction and the pre-block phase make and in which committed state each lands; the inputs a validator is given beside the witness; the exports block execution makes; and the check a replay on the witness must pass.

## Motivation

A stateless validator holds no state: it re-executes a block from a witness of what the block read.
The witness is built from what the block's execution reports, so the building node and the validator must agree exactly on which accounts, slots and code a block reads, on what is read outside the state or outside a transaction's journal — block hashes, SALT bucket capacities, the L1 block information — and on where each read is reported.
A read the building node does not report is missing from the witness, and the validator cannot execute the block; a read reported in a place the node does not collect is lost the same way; and a value served from outside the state that the validator cannot reproduce makes it compute another block.

## Specification

### The witness

- `SATIN-WIT-001` A block's witness MUST hold:
  - every account and every storage slot the block loads, in a pre-block step or in a transaction the block includes, as the chain held it before the block: an absent account recorded as absent, an empty slot of an account the chain holds recorded as zero, and no slot of an absent account;
  - the code the chain held before the block for every such account, whether or not the load that named the account loaded its code;
  - the hash of every block `BLOCKHASH` read during the block's execution (`SATIN-WIT-014`);
  - the capacity of every SALT bucket the block's execution exports (`SATIN-WIT-013`).

  It holds no answer of the oracle service: a system call, a deposit or a Mega System Transaction is given no value by the service (`SATIN-ORCL-005`), and every value the service gave a read of another transaction the block includes is in the Oracle's slot at that read, written before the transaction by a Mega System Transaction of the block, or, a value the transaction's own writes explain, by the transaction itself earlier in it (see [Oracle](../system-contracts/oracle.md), `SATIN-ORCL-012`, `SATIN-ORCL-013`).
- `SATIN-WIT-002` A transaction MUST load every account and slot its execution reads from the state: in its validation, in its fee settlement, and in any of its frames — a frame that reverted, halted or was stopped, and a frame of a deposit that failed, included.
  A failed frame's writes are taken back, not its reads; a failed deposit takes back everything but its sender's nonce bump and mint, not its reads.
- `SATIN-WIT-003` The L1 block information a transaction is priced against, and the data-availability footprint gas scalar every non-deposit transaction reads before it runs, are read outside the transaction's journal, and every account and slot such a read makes MUST be reported with the transaction that made it (`SATIN-WIT-011`).
- `SATIN-WIT-004` A read that gas or a limit skipped MUST load nothing (`SATIN-WIT-012`), with one exception: an authority account the EIP-7702 authorization preflight consulted MUST be loaded, with its code, whether or not the list is then applied.
  The preflight consults every authority whose entry passes the chain-id, nonce and signature gates, each distinct authority once, the whole list walked (see [EIP-7702 Authorizations Before the First Frame](../evm/authorizations.md)).
- `SATIN-WIT-005` Execution MUST report what it loaded in the states the block commits: each pre-block step in the state it commits on its own, and each transaction in its returned state, which names every account and slot the transaction loaded, whether it wrote it or not, whether the frame that loaded it succeeded or not, and, for a deposit, whether the deposit failed or not.
  The set of loads is a function of those states and of the exports alone, not of how the node caches state: a state names the keys it loaded even when a cache another block filled served the value.
  A state names the keys; the values are the chain's.
- `SATIN-WIT-006` A slot of an account the chain does not hold before the block MUST NOT be recorded: such an account has no storage, and a validator MUST answer every slot of it with zero without looking it up.
- `SATIN-WIT-007` The code a witness holds MUST be the chain's before the block, not the code a returned state carries: a transaction that replaces an account's code — an EIP-7702 authority delegated anew — is admitted against the code the chain held, and its returned state carries the code it wrote.
- `SATIN-WIT-017` A node MUST answer an address its state holds no account for as no account, never as an empty account, which is a leaf the state holds: the destruction table gives an account's leaf back only when no account stood at the address at the transaction's start (see [SELFDESTRUCT and the Destruction Table](../evm/selfdestruct.md)).

### Where each read lands

- `SATIN-WIT-008` A transaction's loads MUST be in its returned state: its sender, its recipient or created address, every account and every slot any of its frames loads, the fee recipients, every authority account the authorization preflight consulted, and a keyless deployment's signer and deploy address; the state names an account whether or not the load brought its code.
  The pre-block phase's loads MUST be in the states it commits, one per step and in the step order of [System Calls and the Pre-Block Sequence](system-calls.md): the EIP-2935 call's state, the EIP-4788 call's state, in Satin's activation block the factory's read-only entry, each system contract's deployment — the account it installed or rewrote, or the read-only entry of one it left as it was —, the registry's account and pending slots the due-change read loaded, the `applyPendingChanges()` call's state when the call is made, the registry's deployment, and last the registry's account and slot 0 the resolution of the live system address read.
  Each state MUST be committed whole, read-only entries included, and a node MUST collect the states as they are committed: what a commit keeps of a state is only what it changed, which holds none of the read-only entries.
- `SATIN-WIT-009` `BLOCKHASH` reads the chain's history outside the transaction's journal, and its reads MUST be exported (`SATIN-WIT-014`); a SALT bucket's capacity is read outside the database, and MUST be exported (`SATIN-WIT-013`); the L1 block information a fee computation or a footprint reads is read outside the transaction's journal, and MUST be reported with the transaction that read it (`SATIN-WIT-011`).
- `SATIN-WIT-010` A validator MUST be given, beside the witness: the block's header, the chain configuration (its fork schedule), the parent block's hash and timestamp, the parent beacon block root, and the block's extra data.
  Whether the block admits only deposits, and whether Satin activates in it, MUST be derived from the chain configuration and the two timestamps, as [Activation and Rex-Era Carry-Over](activation.md) specifies; `SLOTNUM` pushes zero (see [Base Layer](../base-layer.md)), so no slot number is an input.

### The L1 block information

- `SATIN-WIT-011` The L1 block contract at `L1_BLOCK_ADDRESS` is read, when it is needed, by two reads of the base layer:
  - a non-deposit transaction that pays an L1 fee is priced by the fee computation, which reads its L1 base fee slot (1), its Ecotone fee scalars slot (3), its Ecotone blob base fee slot (7), its operator fee scalars slot (8), and, only when the Ecotone scalars are empty (the blob base fee scalar and the eight bytes of the two scalars zero), its L1 fee overhead slot (5);
  - every non-deposit transaction, a Mega System Transaction included, which pays no fee, has its data-availability footprint computed from the footprint gas scalar, read from slot 8 before the transaction runs (see [Base Layer](../base-layer.md), `SATIN-BASE-009`).

  These reads are made on the block's state, not through a transaction's journal, so they land in no transaction's returned state; the node MUST nevertheless report the contract's account and every slot the block's transactions read by either, each once, as read-only entries of the state of the first transaction that read it, whether for its fee or for its footprint, so that the witness holds them; a read-only entry does not replace a write that transaction makes to the same account or slot.
  A block whose only non-deposit transactions are Mega System Transactions therefore still reports the account and slot 8, with the first of them, though no transaction of it pays an L1 fee.
  A state that holds no contract at the address MUST record the account as absent and read no slot.
  A slot neither read reaches is not read and need not be in the witness: a block with no non-deposit transaction reads none of it, and a slot the scalars leave unread is not read.
  A read the node fails to make is reported as `SATIN-VAL-010` classifies it: a fee computation's as a read of the transaction's own execution, the footprint scalar's as a read the block makes for the transaction (see [Transaction Validation and Refusals](transaction-validation.md)).
  The reads change nothing: the entries are not written.

### Reads a validator makes again

- `SATIN-WIT-012` A read that gas or a limit skipped is skipped again on replay, so the witness MUST NOT be required to carry it: a cold `SLOAD` or account load with less gas than its cold surcharge, other than an Oracle read, which is made before its charge (`SATIN-ORCL-004`), a `BLOCKHASH` of the current block, a future block or a block outside the last `BLOCKHASH_WINDOW` blocks, a read refused in a frame whose volatile-data access is off, a keyless deployment's reads after a step refused it, and the bucket of a state charge a system-originated transaction or a system call makes.

### The exports

- `SATIN-WIT-013` Block execution MUST export the set of SALT buckets the SALT environment answered with a valid capacity during the block, emptied when the block starts and accumulated over everything executed for the block.
  A bucket is in the set once it was answered with a valid capacity, whether or not the transaction that asked is in the block.
  A lookup that failed MUST NOT be in the set, whether the environment could not answer it or answered a capacity below `MIN_BUCKET_SIZE`: it is a fault of the node, for a deposit as for any transaction (see [Halts, Reverts and Stops](../evm/outcomes.md)).
  A witness MUST prove the capacity of every bucket in the set.
  A node that runs the block's transactions on several executions, or that empties the set between transactions, MUST take the union of what each reports; a transaction executed elsewhere and committed into the block adds nothing to the set of the execution it was committed into.
  The pre-block calls and the system-originated transactions price at `m = 1` and add no bucket.
  Which bucket an account or a slot lands in is SALT's own definition (see [State Gas and SALT Pricing](../evm/state-gas.md)).
- `SATIN-WIT-014` Block execution MUST export every block hash `BLOCKHASH` was served during the block, emptied when the block starts; it is not what a node's state cache holds, which may carry hashes an earlier block read.

### The check

- `SATIN-WIT-016` A block replayed on exactly its witness MUST produce the same receipts, state changes, gas ledgers, logs and block counters as the block's execution, and MUST read nothing the witness does not hold.
  Its exports MUST be a subset of the building node's, and MAY be a proper one: the building node's also hold the buckets and block hashes that candidates it executed and dropped asked for.
  A validator runs no oracle service: it reads every Oracle value from the slot (`SATIN-ORCL-012`), and hints, which reach the service alone, are not in the witness.

### Retired ids

- `SATIN-WIT-015` Retired, removed: no record of the oracle service's answers is kept beside the block; the sequencer persists before its reader every served value the reader's own writes do not explain (see [Oracle](../system-contracts/oracle.md), `SATIN-ORCL-012`), and a transaction whose reads of a slot no value written before it reproduces is not included (`SATIN-ORCL-013`).

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
The factory check, a deployment that leaves a contract as it is, the due-change read and the resolution of the system address write nothing, so a commit that keeps only changes would lose them; committing them as read-only states puts their loads where the witness is collected, as Rex6 records its deployments' and its resolution's reads.

**Rex6 defect fixed.** A block whose L1 attributes deposit leaves both Ecotone fee scalars zero, and whose transactions do not otherwise touch the L1 fee overhead slot 5, prices its first user transaction through the Bedrock fallback, which reads slot 5 outside the transaction's journal; Rex6 collected no state for that read, so a witness built from Rex6's committed states could lack slot 5, and a stateless validator could not price the transaction.
Satin reports every slot a fee computation or a footprint reads with the first transaction that read it (`SATIN-WIT-011`), a Mega System Transaction's footprint read included, and, as Rex6, reads none such a read does not need: no read is made before the block's transactions, and a block with no non-deposit transaction reads none of it.

**Rex6 defect fixed.** A keyless deployment's sandbox in Rex6 — an existing nonce-1 signer, a prefunded deploy address without code, a constructor that reverts — priced its creation against the deploy address's SALT bucket, but the bucket reads of the sandbox were not merged into the block's export, so a witness proving only the accounts could lack the bucket's capacity and a stateless validator could not price the creation.
Satin exports every bucket any execution of the block was answered, the union across every execution included (`SATIN-WIT-013`).

**Why does the witness carry no oracle answers?**
Every value the service gave a transaction is in the Oracle's slot at the read: written by a Mega System Transaction ordered before the transaction, as Rex6 requires, unless the transaction's own earlier write put it there; and a transaction whose reads of a slot no value written before it reproduces, its own writes included, is not included (see [Oracle](../system-contracts/oracle.md)); a validator therefore reads every Oracle value from the state the witness holds and the block's own writes, and needs nothing beside them.

**Why is a read that gas skipped not required in the witness?**
Rex6's node recreated a read that a cold `BALANCE` or `EXTCODECOPY` could not pay for, so its read set held an account the execution never used; Satin does not require it: the replay skips the same read on the same gas, so the data would only enlarge the proof, and a missing account could raise a fault at an opcode that cannot complete.
The Oracle read is the exception, made before its charge as in Rex6 (`SATIN-ORCL-004`).

**Why export the block hashes served, not the cache?**
Rex6 exported the block hashes its state cache held, which could carry a hash an earlier block read; Satin exports the hashes this block's execution was served, so the export, and the witness built from it, is a function of the block's execution and not of how a node reuses its cache.

**Why does an authority the preflight consulted stay loaded?**
The authorization list is decided by a simulation that reads each authority before it knows whether the list fits; a validator re-executing the decision makes the same reads, so the witness must hold them whether or not the list is applied.

**Why is a failed SALT lookup not exported?**
A lookup that failed gave the transaction no outcome; a bucket in the export the witness must prove would then be one no included transaction priced with.

## Security Considerations

- A node that collects only what a commit keeps produces a witness without the activation block's factory, the system contracts a deployment left as they were, the registry's pending slots and the registry slot the resolution read; a validator given it cannot execute the block.
- A node that does not report the L1 block slots a fee computation or a footprint read gives validators a witness without the inputs of that transaction's fee or footprint, a Mega System Transaction's footprint scalar among them.
- A node that answers an absent account as an empty one gives no destruction the account's leaf back, and executes a different chain from a node that answers it as absent.
- A node that exports the hashes its cache holds, rather than those served, gives validators a witness that differs from another node's for the same block.
- A node that includes a transaction whose served Oracle value, one its own writes do not explain, was not persisted before it, or one whose reads of a slot no value written before it reproduces, produces a block validators compute differently (see [Oracle](../system-contracts/oracle.md)).

## Spec History

- [Rex6](../../upgrades/rex6.md) — Exported the SALT buckets of one cache and whatever block hashes the state cache held; the pre-block states were collected through a hook, and the L1 information landed in no collected state.
- [Satin](../../upgrades/satin.md) — The witness defined by the committed states and exports, the read-only pre-block states, the L1 block slots each fee computation read, and no oracle answers beside the block.
