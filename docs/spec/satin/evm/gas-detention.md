---
description: Satin (unstable) — Gas Detention. Gas detention on withheld gas — what is volatile, how a transaction's compute is measured, the limit a read sets, how every frame's regular gas is split into spendable and withheld parts, the crossing that stops a frame, and the precompile and interceptor cases.
spec: Satin
maturity: unstable
---

# Gas Detention

{% hint style="warning" %}
**Unstable** — Satin is under active development: every value and rule on this page may change before Satin is frozen.
{% endhint %}

Abstract: Once a transaction reads [volatile data](../../glossary.md#volatile-data), [gas detention](../../glossary.md#gas-detention) bounds the computation it may still do to a cap above its compute at the read; every frame's regular gas is split into a spendable part, which is all a regular charge may draw, and a withheld part, which every other reader of the gas still sees, so the transaction runs as it would without the read until a regular charge needs the withheld gas, and that charge stops its frame.

## Motivation

Many transactions read the same volatile data: the block's number and timestamp, the block beneficiary's balance, the Oracle's prices.
A transaction that reads such data and then computes for a long time conflicts with every other transaction that touches it, so a parallel executor or a builder has to serialize it, re-run it, or hold back the block.
Bounding the computation that may follow a volatile read keeps such conflicts short.

Rex6 bounded it by lowering the transaction's limit on a separate compute-gas ledger and halting the transaction when it crossed; the lowered limit also changed what `GAS` reported and what a call forwarded, so a transaction that read volatile data behaved differently from the first instruction after the read, not only when it computed too long.

## Specification

### What is volatile

- `SATIN-DET-001` A read of each of the following MUST be a volatile read:
  - the block environment: `NUMBER`, `TIMESTAMP`, `COINBASE`, `PREVRANDAO`, `GASLIMIT`, `BASEFEE`, `BLOBBASEFEE`, `SLOTNUM` and `BLOCKHASH`;
  - the block beneficiary's account, through `BALANCE`, `SELFBALANCE`, `EXTCODESIZE`, `EXTCODECOPY`, `EXTCODEHASH`, the four call opcodes and the EIP-7702 delegate they follow, `SELFDESTRUCT` at either end, a transaction's sender or call recipient that is the beneficiary, a recipient that delegates to it, an applied EIP-7702 authority that is the beneficiary, and a keyless deployment's signer that is the beneficiary ([KeylessDeploy](../system-contracts/keyless-deploy.md));
  - the Oracle's storage, through `SLOAD` in the Oracle's own frame ([Oracle](../system-contracts/oracle.md)).
- `SATIN-DET-002` `BLOBHASH` MUST NOT be a volatile read: it reads the transaction's own blob hashes.
- `SATIN-DET-003` A read MUST be marked where its opcode loads the value, and only once the opcode completed; a load that fails, and a read whose opcode then fails, MUST mark nothing.
- `SATIN-DET-004` Every `BLOCKHASH` MUST be a read of the block environment, whatever its operand: the opcode loads the block number before it decides whether its operand is in range, so one of the current block, of a future block or of a block outside the last 256 is a read, and one in range reads the hash as well.
- `SATIN-DET-005` A call to the EIP-2935 history contract MUST be a read of the block environment, because the contract's `get` path executes `NUMBER` before it loads the slot.
  An `SLOAD` of the storage the EIP-2935 and EIP-4788 pre-block calls write MUST NOT be a volatile read: it is state committed before the block's first transaction.
- `SATIN-DET-006` A `CREATE` or `CREATE2` MUST NOT be marked as a read, and MUST NOT be refused in a frame whose volatile-data access is off ([MegaAccessControl](../system-contracts/mega-access-control.md)), also when its creator or its created address is the block beneficiary: its loads of them — the creator's, to check its balance and nonce, and the created address's, to decide the created account's state gas — are the creation's own checks.
  A creation transaction is not detained from its start because its created address is the block beneficiary.
- `SATIN-DET-007` A frame running as the beneficiary MUST mark the beneficiary's account by its own `SELFBALANCE`, `SELFDESTRUCT` and the other reads of `SATIN-DET-001`, and with access off is refused them ([MegaAccessControl](../system-contracts/mega-access-control.md)).
- `SATIN-DET-008` A transaction whose sender, call recipient or applied EIP-7702 authority is the block beneficiary MUST be detained from its start, as a read of the beneficiary's account made before its first frame.

### Compute

- `SATIN-DET-009` A transaction's compute MUST be every regular charge its frames make, whoever funds it: the running frame's regular gas spent, plus every suspended caller's, each less the regular gas it forwarded to its child, less the state and history gas that spilled onto its regular gas, and less what halting frames burned (`SATIN-DET-011`).
- `SATIN-DET-010` A value call's `CALL_STIPEND` is not forwarded gas: what the callee runs on it MUST count as compute, as the rest of what it runs does.
  The stipend MUST NOT lower compute either: when a value call returns, what the callee left of the stipend comes back to its caller with the rest of the callee's gas, and compute MUST NOT fall with the caller's spent regular gas.
  Compute can therefore exceed the transaction's regular ledger by the stipends of its value calls.
- `SATIN-DET-011` What a halting frame burns — the regular gas it had left when it halted — MUST NOT count as compute, whatever it could not pay: a dynamic charge, an opcode's static gas, a cold access, or state or history gas that spilled past the reservoir.
  A precompile that runs out of gas MUST count nothing of its forward as compute: it burns the forward, a value call's stipend included, unless it is the crossing (`SATIN-DET-021`), and then the forward returns to its caller.

### The limit

- `SATIN-DET-012` A volatile read MUST set `limit = compute_at_read + cap` when it lowers the transaction's limit, and the limit MUST only go down, so the most restrictive read binds:
  - `compute_at_read` — the transaction's compute when the read is marked.
  - `cap` — `BLOCK_ENV_ACCESS_COMPUTE_GAS` for a read of the block environment or of the beneficiary's account, and `ORACLE_ACCESS_COMPUTE_GAS` for a read of the Oracle's storage.
- `SATIN-DET-013` The caps are protocol values fixed by the spec with the other limits (`SATIN-LIM-017`), and MUST NOT be taken from configuration.
  Both are below `MAX_TX_COMPUTE_GAS`, the most compute a transaction can spend: `EXECUTION_CAP − TX_BASE_COST − WARM_STORAGE_READ_COST`, the execution cap less the base cost every transaction pays and the least a frame pays for the code it runs.

### Withheld gas

- `SATIN-DET-014` Once a limit is set, every frame's regular gas MUST be split into a spendable part, held at what the limit leaves the transaction (`limit − compute`, or zero once compute has reached the limit), and a withheld part, the rest of the frame's regular gas.
  The split MUST be applied when the read's opcode completes, when a frame starts or resumes, and after an `SSTORE`, whose restore of a slot can give regular gas back.
- `SATIN-DET-015` Only a regular charge MUST be limited to the spendable part.
  Every other reader of the frame's gas MUST see both parts: `GAS`, the forward of [Gas Forwarding](gas-forwarding.md) and the clamp of an explicit call gas, the `SSTORE` minimum-gas check, the checks that decide whether a cold load is attempted, the gas a child returns, and the settlement at the end of the transaction.
- `SATIN-DET-016` At the settlement the withheld part MUST be unspent gas: it returns to the sender with the rest of the unspent gas, and it is not part of the gas used that caps the EIP-3529 refund.
  A failed deposit returns none of it, as it returns no unspent gas and no reservoir ([Deposit Transactions](../block/deposits.md)).
- `SATIN-DET-017` A forward and a spill of state or history gas MUST draw the withheld part first.

A transaction that read volatile data therefore runs exactly as it would without the read until a regular charge needs the withheld part.

### The crossing

- `SATIN-DET-018` A regular charge that the spendable part cannot pay but the frame's whole regular gas can is the crossing: the charge MUST NOT be made, the frame's gas MUST be put back to what it was before the charge, and the frame MUST be stopped with `MegaLimitExceeded(2, limit)` ([Limit Stops](limit-stops.md)).
  What the frame spent before the crossing charge stays spent, and its caller MUST get back everything the frame had, the withheld part included.
- `SATIN-DET-019` At the crossing the transaction's compute is at most the limit and less than the crossing charge short of it; a caller the stop returns into MUST resume held to what the limit leaves the transaction, so any regular charge of its own past that is a crossing too.
  What a halting frame burns adds nothing to compute, while its paid work before the halt still counts, so no halt takes the transaction's compute past the limit: the compute since a read is at most its cap.
- `SATIN-DET-020` A regular charge beyond the frame's whole regular gas, and every other out-of-gas, MUST halt as it would without the read.

### Precompiles

- `SATIN-DET-021` A call to a precompile MUST make its own regular charges first, as any opcode's — its static cost, its memory, the value transfer and a cold access — and one that crosses MUST stop the calling frame before the price is consulted and before anything moves, whether or not the caller can fund the value (`SATIN-LIM-010`).
  A call to a precompile forwarded more regular gas than the frame's allowance — what the limit leaves the transaction at the call — MUST then be decided from the precompile's price, read before it runs, for the precompile and input of the called address (`SATIN-PCMP-008`):
  - priced within the allowance, it runs on its whole forward;
  - priced past the allowance and within its forward, it MUST NOT run and is the crossing;
  - priced past its whole forward, it runs on its forward and fails, as without the read.
- `SATIN-DET-022` The call's value has not moved when the price is consulted, so a call that is the crossing MUST be held to the price alone: the stop is kind 2, whatever records its value transfer would have made.
- `SATIN-DET-023` Every precompile of the precompile set (`SATIN-PCMP-001`, [Precompiles](precompiles.md)) MUST have a price for every input, which is the gas the precompile charges for that input before any check it makes after its gas charge:
  - an input over an OP precompile's size limit (`SATIN-PCMP-004`) is priced at zero, since it is refused before any gas check;
  - a ModExp input is priced by its Osaka formula whatever its lengths, an input over EIP-7823's bound included, since ModExp charges that price before it checks the bound (`SATIN-PCMP-007`).
- `SATIN-DET-024` An input priced between the allowance and the forward that would fail a check the precompile makes after its gas charge — a ModExp input over EIP-7823's bound among them — is the crossing too.
  A call refused on its caller's account — a value the caller cannot fund — runs no precompile and MUST be answered as without the read.

### Interceptor answers

- `SATIN-DET-025` A system contract's intercepted answer ([Call Interception](../system-contracts/interception.md)) that spent more regular gas than the frame's allowance, state and history gas that spilled onto its regular gas not counted, MUST be the crossing.
  The answer's whole regular spend MUST be treated as the one charge that crossed: none of it is billed, the part within the allowance included, so the stop's compute is the transaction's compute when the frame started.

### Exemptions and scope

- `SATIN-DET-026` A system-originated transaction and a system call MUST NOT be detained, whatever they read ([Mega System Transactions and the Protocol's Own Transactions](../system-contracts/system-tx.md)).
  A deposit that is not system-originated is detained as any transaction.
- `SATIN-DET-027` Gas detention MUST price exactly the precompiles of the precompile set (`SATIN-PCMP-001`); a precompile a node adds or replaces is outside that set and outside this specification.

### Retired ids

None.

## Constants

| Constant                       | Value       | Description                                                                          |
| ------------------------------ | ----------- | ------------------------------------------------------------------------------------ |
| `BLOCK_ENV_ACCESS_COMPUTE_GAS` | 20,000,000  | Compute a transaction may still spend after a read of the block environment or the beneficiary |
| `ORACLE_ACCESS_COMPUTE_GAS`    | 20,000,000  | Compute a transaction may still spend after a read of the Oracle's storage            |
| `MAX_TX_COMPUTE_GAS`           | 199,987,900 | The most compute a transaction can spend                                              |
| `EXECUTION_CAP`                | 200,000,000 | The execution cap ([Two-Pool Gas](gas-model.md))                                      |
| `TX_BASE_COST`                 | 12,000      | EIP-2780 base cost ([Gas Schedule and Intrinsic Gas](gas-schedule.md))                |
| `WARM_STORAGE_READ_COST`       | 100         | Warm account access                                                                   |
| `CALL_STIPEND`                 | 2,300       | Value-transfer stipend ([Gas Forwarding](gas-forwarding.md))                          |

## Rationale

**Why withhold gas instead of lowering a limit?**
Under Rex6 a read lowered the transaction's compute-gas limit, so from the read on `GAS`, forwarding and the `SSTORE` minimum-gas check saw less gas than the transaction had, and contracts behaved differently long before they computed too much.
Withholding the gas inside each frame changes only what a regular charge may draw: everything else sees the frame's whole gas, so a transaction behaves exactly as without the read until the bound is actually reached, and then one charge stops one frame.

**Why a stop rather than a halt?**
Rex6 halted with `VolatileDataAccessOutOfGas`, which consumed the transaction's gas and took down every caller.
As a limit stop, kind 2, the crossing reverts only the frame that made the charge, its caller can catch it, and the withheld gas returns to the sender.

**Why is `BLOBHASH` no longer volatile?**
It reads the transaction's own blob hashes, which no other transaction shares, so it causes no conflict; Rex6 treated it as volatile.

**Why are creations not reads?**
A creation loads its creator to check balance and nonce and its created address to decide the created account's state gas, as a value call checks its caller's balance; neither is a read of the beneficiary's state that another transaction conflicts on, and Rex6 neither marked nor refused a creation.

**Why decide a precompile call from its price?**
A precompile is one indivisible charge: it cannot be stopped part-way, and running it to find out that it costs too much would let it compute past the limit.
Reading its price first decides the call before anything runs, which is why every precompile of the set must have a price for every input.

**Why price an over-bound ModExp input by its formula?**
ModExp charges its formula price before it checks EIP-7823's bound, as go-ethereum orders it, so the gas such a call costs is that price; the detention decision uses the same price, so a call is decided by what it would actually be charged.

## Security Considerations

- If any reader other than a regular charge saw only the spendable part, a transaction's behaviour would change at the read rather than at the crossing, and two nodes that apply the split at different points would forward different gas.
- If what a halting frame burns counted as compute, a callee could halt on purpose to drive its caller's compute past the limit without doing the work.
- If a precompile were run before its price was compared with the allowance, a single call could compute up to its whole forward past the detention limit.
- If a node priced a ModExp input over EIP-7823's bound below its formula price, it would run on one node and stop on another under the same allowance.
- If a system call or the protocol's own transactions were detained, a pre-block call or an oracle update could be stopped by the volatile data it exists to write.
- This page preserves the invariant that a transaction's compute since a volatile read never exceeds that read's cap.

## Spec History

- [Satin](../../upgrades/satin.md) — Replaced the Rex6 detained compute limit of [Gas Detention](../../evm/gas-detention.md), which halted the transaction, with withheld gas inside each frame and a kind-2 stop of the crossing frame; `BLOBHASH` is no longer volatile and creations are never reads.
