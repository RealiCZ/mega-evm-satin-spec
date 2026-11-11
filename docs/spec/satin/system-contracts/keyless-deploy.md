---
description: Satin (unstable) — KeylessDeploy. Keyless deployment (Nick's method) as a native creation: which calls deploy, the fifteen steps a deployment makes, the creation it starts, the signer's nonce, the answer, and what a limit does to a deployment.
spec: Satin
maturity: unstable
---

# KeylessDeploy

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
{% endhint %}

Abstract: The KeylessDeploy system contract and the native keyless deployment: the `keylessDeploy` calls that deploy, the fifteen charges and checks a deployment makes in order, the ordinary creation frame it starts, the rule for the signer's nonce, the answer it returns, and how a resource limit or gas detention stops a deployment.

## Motivation

Nick's method deploys a contract at the same address on every chain from a pre-signed, pre-EIP-155 creation transaction whose signer nobody holds a key for.
The signed gas limit was chosen for Ethereum's prices and is too low for MegaETH's, and a signed transaction cannot be re-signed with another.
MegaETH therefore deploys such a transaction through a system call that keeps the signer and the address but lets the submitter raise the gas.
The deployment must still be an ordinary creation — priced, limited, detained and logged as one — or a constructor would run under rules no other creation runs under; and a failed attempt must not leave the address unusable, since anyone may submit the signed bytes.

## Specification

### The contract

- `SATIN-KEY-001` KeylessDeploy MUST be the account at `KEYLESS_DEPLOY_ADDRESS` holding the code `KEYLESS_DEPLOY_CODE_HASH` (see [System Contracts](overview.md)), whose interface is:

```solidity
interface IKeylessDeploy {
    error MalformedEncoding();
    error NotContractCreation();
    error NotPreEIP155();
    error NonZeroTxNonce(uint64 txNonce);
    error NoEtherTransfer();
    error InvalidSignature();
    error InsufficientBalance();
    error ContractAlreadyExists();
    error SignerNonceTooHigh(uint64 signerNonce);
    error ExecutionReverted(uint64 gasUsed, bytes output);
    error ExecutionHalted(uint64 gasUsed);
    error EmptyCodeDeployed(uint64 gasUsed);
    error NoContractCreated();
    error AddressMismatch();
    error GasLimitTooLow(uint64 txGasLimit, uint64 providedGasLimit);
    error InitCodeTooLarge(uint64 size, uint64 max);
    error SignerHasCode();
    error NotIntercepted();

    function keylessDeploy(bytes calldata keylessDeploymentTransaction, uint256 gasLimitOverride)
        external
        returns (uint64 gasUsed, address deployedAddress, bytes memory errorData);
}
```

  Errors are ABI-encoded as Solidity custom errors: the four-byte selector of the signature, then the arguments.

### Which calls deploy

- `SATIN-KEY-002` A `keylessDeploy(bytes,uint256)` call recognized as the transaction's own frame (see [Call Interception](interception.md), `SATIN-ICPT-006`) MUST deploy the creation its first argument carries as an ordinary creation frame, a child of the call, by the steps below; no code runs in the call's own frame.
- `SATIN-KEY-003` A `keylessDeploy` call that a contract makes MUST run KeylessDeploy's bytecode: without value it reverts with `NotIntercepted()`, and with value it reverts with empty data, the method not being payable.

### The steps

- `SATIN-KEY-004` A deployment MUST make the charges and checks of the table below.
  A step's refusal MUST revert the call with the error the table names: the state and history gas the call was charged MUST be given back into the call's reservoir, never its regular gas (`SATIN-HIST-012`), and the regular gas it spent stays spent.
  A step that cannot pay its charge MUST halt the call out of gas, consuming the call's regular gas.
- `SATIN-KEY-005` The steps, in this order:

| Step | Check or charge | Refusal |
| ---- | --------------- | ------- |
| step-1 | Charge `KEYLESS_DEPLOY_OVERHEAD_GAS` of regular gas | Out of gas |
| step-2 | The call carries no value | `NoEtherTransfer()`, answered before the call's frame is built (see `SATIN-KEY-018`): no value moves |
| step-3 | The first argument — the `bytes` the call's arguments held when it was recognized, the length bytes after the length word that `SATIN-ICPT-006`'s offset points at, unpadded — decodes as a signed legacy transaction that is a creation (`to` empty), carries no chain id, and is followed by no trailing byte | In this order: `MalformedEncoding()` for an RLP encoding that does not decode or has trailing bytes, then `NotContractCreation()` for a transaction with `to` set, then `NotPreEIP155()` for one with a chain id |
| step-4 | The carried transaction's nonce is 0 | `NonZeroTxNonce(uint64)` |
| step-5 | The initcode is at most `MAX_INITCODE_SIZE` bytes | `InitCodeTooLarge(uint64,uint64)` |
| step-6 | `gasLimitOverride` (read as `MAX_UINT64` when larger) is at least the signed gas limit | `GasLimitTooLow(uint64,uint64)` |
| step-7 | The signer can be recovered from the signature, whether its `s` value is low or high: EIP-2's bound on `s` does not apply | `InvalidSignature()` |
| step-8 | The signer's nonce is at most 1 | `SignerNonceTooHigh(uint64)` |
| step-9 | Unless the node's configuration disables EIP-3607, the signer's code is empty or an EIP-7702 delegation indicator; with EIP-3607 disabled the step checks nothing | `SignerHasCode()` |
| step-10 | If the signer's account is empty (EIP-161), charge the state gas of a new account at the signer's bucket, with its legacy share | Out of gas |
| step-11 | `min(gasLimitOverride, available gas)` is at least the signed gas limit | `GasLimitTooLow(uint64,uint64)` |
| step-12 | The deploy address `keccak256(rlp([signer, 0]))[12:]` holds no code | `ContractAlreadyExists()` |
| step-13 | The signer's balance is at least the carried value | `InsufficientBalance()` |
| step-14 | Charge what a `CREATE` charges its frame for the start: `CREATE_GAS` plus EIP-3860's initcode cost of regular gas; the state gas of the created account at the deploy address's bucket if the deploy address is empty, with its legacy share; the history gas of the created account's write record, unless the transaction changed the deploy address's account already; and the history gas of the signer's nonce record, unless the transaction changed the signer's account already, the transaction's sender among such accounts | Out of gas |
| step-15 | `min(gasLimitOverride, available gas)` is still at least the signed gas limit | `GasLimitTooLow(uint64,uint64)` |

  "Available gas" is the call's regular gas a `CREATE` could forward, its withheld part included (see [Gas Detention](../evm/gas-detention.md)).
  The state charges of steps 10 and 14 are made as every state charge is, their legacy shares first from regular gas — 25,000 for the signer's new account and 20,000 for the created account at the current prices (`SATIN-STATE-012`) — then the reservoir, then the rest from regular gas (see [Two-Pool Gas](../evm/gas-model.md)), priced as [State Gas and SALT Pricing](../evm/state-gas.md) specifies; the history charge of step 14 is priced as [History Gas](../evm/history-gas.md) specifies.
- `SATIN-KEY-006` A call that more than one of steps 3 to 13 would refuse MUST be refused with the error of the first of them in the table's order, and a call that step 3 refuses for more than one reason with the first error in step 3's own order: a carried transaction with `to` set and a chain id is refused with `NotContractCreation()`.
- `SATIN-KEY-007` The read of the signer's account that steps 8 to 10 and 13 check MUST load the account into the transaction's state as an account access loads it, warm: with its code, unless the node's configuration disables EIP-3607, in which case without it, so that a deployment with EIP-3607 disabled loads no signer code and makes no signer-code refusal.
  The read of step 12 MUST load the deploy address's account warm, without its code.
  Neither read is charged, and no charge the call or its creation makes depends on either account's warmth: the creation loads both accounts again when it starts, as a creation loads its creator and the address it creates.
- `SATIN-KEY-008` Step 12 MUST check the deploy address's code alone.
  An address that holds a nonce other than zero but no code passes it, and the creation then collides there, as any creation onto an address with a nonce does (`SATIN-SD-016`), and fails; the call answers `ExecutionHalted` with the creation's whole forward spent, and the signer's nonce is kept or taken back as `SATIN-KEY-013` says.
  An address that holds only a balance — nonce zero and no code — passes it and is not a collision: the creation lands there and keeps that balance; the address is not empty under EIP-161 (`SATIN-STATE-011`), so step 14 charges no created-account state gas for it and the creation counts no rise for it.
- `SATIN-KEY-009` A creation at the deploy address whose constructor returns empty code MUST be refused its empty code deposit and MUST revert, its state, logs and records taken back as for a creation that reverted, so that the address stays deployable; the call answers `EmptyCodeDeployed`.
  A constructor that destroyed the account it was creating leaves no code either, and the call answers `EmptyCodeDeployed` for it too.
  The rule concerns the deploy address alone: a creation the constructor itself makes may return empty code.
- `SATIN-KEY-010` A signer that is the block beneficiary MUST be detained as a read of the beneficiary's account, made when the signer's account is read, after step 7 recovered the signer and before step 8's check; the read's compute is the call's `KEYLESS_DEPLOY_OVERHEAD_GAS` of step 1, so the limit it sets is that plus the cap, unless an earlier read set a lower limit (see [Gas Detention](../evm/gas-detention.md)).
- `SATIN-KEY-018` A call that carries value MUST first be held to gas detention for step 1's charge: when that charge is the crossing, the call is stopped with `MegaLimitExceeded(2, limit)` and none of it is billed; otherwise the charge is made (or halts the call out of gas) and the call reverts with `NoEtherTransfer()` before any value moves and before any frame is built.
  This holds whether or not the caller can fund the value: steps 1 and 2 are part of interception, which comes before the frame start where the funds are checked (`SATIN-ICPT-007`).

### The creation

- `SATIN-KEY-011` Once step 15 passed, the creation MUST start as a creation by the signer at the deploy address, one call level below the call, carrying the signed initcode and value, forwarding `min(gasLimitOverride, available gas)` of regular gas, drawn from the call's withheld gas first.
  The 98/100 forwarding cap of [Gas Forwarding](../evm/gas-forwarding.md) MUST NOT apply to that forward.
  The creation MUST receive the reservoir share of [Gas Forwarding](../evm/gas-forwarding.md) of the reservoir the call has left after step 14, the call keeping the rest, and, in data size, KV updates and state growth, the child share of the frame budgets the call has left (see [Resource Limits](../evm/resource-limits.md)).
  From its start it is an ordinary creation frame: priced, limited, detained and logged as any creation is, and its start bumps the signer's nonce as a creation bumps its creator's.
  `ORIGIN` and `GASPRICE` in the initcode MUST be the transaction's own.
- `SATIN-KEY-012` The signer's nonce record, and the signer's unit of state growth when the creation's nonce bump creates the signer's account, MUST be counted on the call when the creation has returned, once the nonce rule below has been applied.
- `SATIN-KEY-013` The signer's nonce:
  - a deployment from signer nonce 0 MUST keep the creation's bump;
  - a deployment from signer nonce 1 MUST take the bump back, setting the nonce to 1, when the creation's bump is the last change of the signer's nonce the deployment made, whether the deployment succeeded or failed;
  - a signer whose own code spent a nonce during the creation, a change that survives the creation, MUST keep every bump.

  The signer's write record MUST be counted after that rule: when the nonce set back leaves the signer's account as the transaction loaded it, no record stands, and the history gas step 14 charged for it MUST be given back into the call's reservoir; a signer's account another write changed — value a creation that returned without a revert or a halt moved out of it, or into it — keeps its record.
  When the signer's nonce stands where it was and step 10 charged state gas for the signer's account, that state gas MUST be given back into the call's reservoir.
  No execution reaches that last case: step 10 charges only a signer empty under EIP-161, whose nonce is zero, and once steps 11 to 15 have passed the creation always bumps that nonce, which a deployment from nonce zero keeps; the sentence gives the case an answer, and no test can reach it.

### The answer

- `SATIN-KEY-014` Unless a limit stopped it (`SATIN-KEY-016`), the call MUST succeed and return `(gasUsed, deployedAddress, errorData)`:
  - when the deploy address holds code afterwards: the deploy address and empty `errorData`;
  - otherwise the zero address and, as `errorData`, `ExecutionReverted(gasUsed, output)` for a creation that reverted (its revert data as `output`), `ExecutionHalted(gasUsed)` for one that halted, or `EmptyCodeDeployed(gasUsed)` for one `SATIN-KEY-009` refused or whose constructor destroyed the account.
- `SATIN-KEY-015` `gasUsed` MUST be what the creation spent from both pools taken together, without intrinsic gas and before the EIP-3529 refund: the regular gas and the reservoir the creation was given, less the regular gas and the reservoir it returned — its regular charges plus the state and history gas it kept, net of every give-back within the creation of a charge the creation made — a slot written back to its original value, a record taken back, the upfront state gas of a frame it started that failed, and the state and history gas a same-transaction destruction gives back, the deployed code's history gas included.
  The call's own charges of steps 1 and 14 are not part of it, and a give-back is not an EIP-3529 refund.
  A give-back the creation receives for a charge it did not make MUST NOT lower `gasUsed`, and MUST be added back to what the creation returned: the one such give-back is the destruction table's for the account being created, when a destruction of it — the constructor's `SELFDESTRUCT`, or one a frame the constructor calls makes in its context — stands when the creation ends, and step 14's state gas of the created account and history gas of its write record come back within the creation (`SATIN-SD-005`, `SATIN-SD-007`).
  So `gasUsed` is `(regular given − regular returned) + (reservoir given − reservoir returned) + the give-backs of step 14's charges the creation received`.
  The two pools MUST be netted together, not each clipped at zero: a creation that pays state from regular gas and reverts returns that state as reservoir, which lowers `gasUsed` by it; a creation whose constructor writes a fresh slot at `m = 1` from regular gas alone and reverts reports 12,109 for its regular charges, not 113,549.
  A constructor `ORIGIN; SELFDESTRUCT` (`0x32ff`) at `m = 1`, given 500,000 of regular gas and no reservoir, with a zero balance and the warm sender as beneficiary, spends 2 + 5,000 and receives step 14's 183,600 of state gas and 3,520 of history gas back into its reservoir; it returns 494,998 of regular gas and 187,120 of reservoir, and `gasUsed` is 5,002 + (0 − 187,120) + 187,120 = 5,002, not −182,118; the call answers `EmptyCodeDeployed(5002)` (`SATIN-KEY-009`).
  `gasUsed` is never less than the creation's regular charges, the regular gas it spent on anything but state and history: every give-back left in it is of a charge the creation made.
- `SATIN-KEY-017` The node MUST NOT produce the errors `ParentBudgetExceeded(uint8,uint64,uint64)`, `InvalidTransaction()`, `InsufficientComputeGas(uint64,uint64)` or `InternalError()`, which the interface no longer declares: a database read or SALT lookup the node fails to make gives the transaction no outcome (see [Transaction Validation and Refusals](../block/transaction-validation.md)).
  `AddressMismatch()` and `NoContractCreated()` remain the answers to a creation reported at another address or at none, which no deployment reaches.

### Limits

- `SATIN-KEY-016` A limit the creation crosses — its frame budget in data size, KV updates or state growth, the transaction's limit in one of those dimensions, or gas detention's compute limit, at the creation's start or in its initcode — MUST stop the creation (see [Limit Stops](../evm/limit-stops.md)); the call then answers `ExecutionReverted` with the stop's revert data as `output`.
  The creation keeps only what an ordinary failed creation keeps on its creator's side, under the nonce rule above: the deploy address's account, the value moved, the transfer log and the deploy address's write record are taken back.
  A limit the call's own charges cross — gas detention's compute limit, for one — MUST stop the call: it reverts with the stop, and the deployment, the signer's nonce included, is taken back.
  The signer's nonce record counted on the call at its settlement can cross the call's frame budget in data size and KV updates, its state-growth budget when the bump created the signer, and the transaction's data-size limit once Oracle hints the creation sent used what the transaction had left; when it does, the call MUST revert with that stop, and the deployment, the nonce included, is taken back.
  The call is the transaction's own frame, so a stop of the call is the transaction's result.

### Retired rule ids

None.

## Constants

| Constant                      | Value                                                                | Description                                                         |
| ----------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `KEYLESS_DEPLOY_ADDRESS`      | `0x6342000000000000000000000000000000000003`                         | KeylessDeploy                                                       |
| `KEYLESS_DEPLOY_CODE_HASH`    | `0x55020d41649acf7a84add6e628b887f802218d9ac86f142ef0994da43ea5eeb6` | KeylessDeploy version 1.0.0                                         |
| `KEYLESS_DEPLOY_OVERHEAD_GAS` | 100,000                                                              | Regular gas a deployment charges first                              |
| `MAX_INITCODE_SIZE`           | 1,048,576                                                            | The initcode size limit (see [Contract Size Limits](../evm/contract-limits.md)) |
| `CREATE_GAS`                  | 12,000                                                               | The regular gas of a creation (see [Gas Schedule and Intrinsic Gas](../evm/gas-schedule.md)) |
| `MAX_UINT64`                  | 2^64 − 1                                                             | The largest `uint64`, the bound of `gasLimitOverride` as the deployment reads it |

## Rationale

**Why a native creation instead of a sandbox?**
Rex6 ran the signed creation as a separate fee-free transaction with its own resource trackers and merged its state afterwards; its constructor saw the signer as `ORIGIN` and a zero `GASPRICE`, and a limit crossed after it ran halted the outer call.
Satin makes the constructor a native child of the outer transaction instead, a design choice: a native child creation runs under exactly the rules of every other creation, in the outer transaction's pools and limits, so nothing about a keyless constructor is special but its creator and its address, and a tracer or inspector follows it as it follows any frame.
Its constructor therefore sees the outer transaction's `ORIGIN` and `GASPRICE` (`SATIN-KEY-011`), where Rex6's saw the signer and zero; a constructor that stores or branches on either computes another result than under Rex6.

**Why are the signer and the deploy address loaded warm, in the outer transaction's warm set?**
Rex6's occupancy read of the deploy address did not warm it, and its sandbox ran on an access list of its own.
Satin's reads enter the outer transaction's state warm (`SATIN-KEY-007`) and the constructor runs in the outer warm set, because the creation is a frame of that transaction and loads its creator and its address when it starts in any case; a constructor's access to an account or slot only the outer transaction warmed is priced warm, where Rex6 priced it cold.

**Why does the constructor run on a child's share of the budgets, under the outer detention?**
Rex6's sandbox received the parent's remaining resource budget as its own transaction budget and merged its footprint afterwards.
A native child receives the child share of the call's frame budgets and shares the outer transaction's gas detention (`SATIN-KEY-011`, `SATIN-KEY-016`), as every creation does; a constructor that needs nearly all of what the call has left in a dimension can be stopped where Rex6's sandbox ran, the price of having one set of frame rules.

**Why is the forward not capped at 98/100?**
The signed gas limit is a promise to the constructor; Rex6's sandbox ran on `min(gasLimitOverride, remaining gas)`, and the call charges nothing after the creation returns, so nothing needs the 2/100 the cap would keep back.

**Why keep the step order?**
Steps 1 to 13 are Rex6's checks in Rex6's order, after the decoding of the call's arguments that decides whether the call is a deployment at all, as in Rex6 (`SATIN-ICPT-006`), so a call that fails several of them names the same error a Rex6 node named; step 14 is a `CREATE`'s own charges, after every check, as an opcode charges after its operands are known.

**Why give the nonce back from 1?**
The signed transaction carries nonce 0 and the deploy address is derived from the signer and nonce 0.
A signer at nonce 1 is the state Rex6 left after a deployment that did not deploy code; a native creation bumps the signer's real nonce, so keeping each attempt's bump would move the signer to 2, where step 8 refuses every later attempt, and one failing submission by anyone would make the address undeployable.
Taking the bump back keeps the address deployable until a deployment leaves code there.
Rex6's sandbox showed the constructor a nonce-1 signer as nonce 0, bumped to 1; under Satin the constructor runs while the signer's real nonce is bumped, 2 for a signer at nonce 1, until the take-back at the call's end, so only a constructor that calls a delegated signer which itself creates observes the difference, in the address that creation derives and in the nonce the signer keeps.

**Rex6 defect fixed.** A signed constructor that returned empty code on a path the submitter chooses — through the gas it is forwarded, for one — left a nonce-1 account without code at the deploy address in Rex6, onto which every later deployment collides, so anyone could make a Nick's-method address undeployable.
Satin reverts such a creation (`SATIN-KEY-009`), so the address stays free.

**Why refuse empty code at the deploy address?**
A creation that returns empty code leaves an account with a nonce and no code, onto which every later creation collides.
Whether initcode returns empty code depends on what it runs on — the forwarded gas, the outer transaction, the block, the state, the oracle's answers, the SALT capacities — part of which the submitter chooses; refusing the empty deposit removes the incentive to make it return empty code.

**Why are the four errors removed, and what does `gasUsed` report?**
They reported the sandbox's failures (a parent budget, a sandbox validation, the compute-gas limit, a failed read), none of which a native creation has.
Rex6 executed a second transaction and reported its settled gas, the inner transaction's intrinsic gas, refund and floor included, and refused an inner gas limit below that intrinsic gas with `InvalidTransaction()`; a native creation has no intrinsic gas of its own, so step 14 charges what a `CREATE` charges for its start and `gasUsed` reports the creation's own spend before the refund (`SATIN-KEY-015`), and a short constructor's `gasUsed` differs from Rex6's.

**Rex6 defect fixed.** A database or SALT read that failed in Rex6's sandbox — of the signer's or the deploy address's account, or of a bucket's capacity — became the transaction's result, a revert with `InternalError()`, so a node whose read failed recorded a failed deployment where a node holding the data executed it.
Satin gives such a transaction no outcome: a failed read is a fault of the node, never an answer of a transaction (`SATIN-KEY-017`, [Transaction Validation and Refusals](../block/transaction-validation.md)).

**Rex6 defect fixed.** Rex6's text promised that every call to KeylessDeploy the node did not intercept reverts with `NotIntercepted()`, yet a contract's `keylessDeploy` call carrying value reverted with empty data, the method not being payable, and `version()` answered.
Satin states what the unchanged bytecode does (`SATIN-KEY-003`).

**Rex6 defect fixed.** A fresh keyless signer was counted as one unit of state growth before a later refusal — `GasLimitTooLow`, the deploy address's code, `InsufficientBalance` — although no signer account was created, so the block's growth count, and its budget, carried an account that does not exist.
Satin counts the signer's growth only after the creation's nonce bump stands (`SATIN-KEY-012`); the state gas charged for the signer is given back on a refusal (`SATIN-KEY-004`).

**Why does step 9 follow the EIP-3607 switch?**
The signer is the sender of the signed creation, and EIP-3607 is the rule that refuses a sender with code; a node's configuration can switch it off for a user transaction in a simulation, and the deployment follows the same switch, loading no signer code when it is off.
Block execution never switches EIP-3607 off, so a block's deployments always make step 9.
Rex6, too, loaded no signer code with the check off, except for a signer already in its state without its code, whose code it loaded; Satin loads none in every case.

## Security Considerations

- A node that let a failed deployment keep the signer's bump from nonce 1 would let anyone make a Nick's-method address undeployable with one reverting submission.
- A node that let a constructor return empty code at the deploy address would leave the address occupied with no code, a permanent denial of the deployment.
- A node that charged the deployment outside the outer transaction's pools or limits would let a deployment create state or data past what its transaction is allowed.
- A node that answered a crossing of detention's limit after billing step 1 would let a valued call compute past the limit.
- The signer's nonce record is counted on the call after the creation returns, and can be the crossing; a node that skipped it would keep a record the limits never held.

## Spec History

- [Rex2](../../upgrades/rex2.md) — Introduced KeylessDeploy, executed in a sandbox.
- [Rex6](../../upgrades/rex6.md) — The Rex6 deployment, a sandboxed transaction merged into the outer one, is specified in [KeylessDeploy](../../system-contracts/keyless-deploy.md).
- [Satin](../../upgrades/satin.md) — Deployment as a native child creation, in the outer transaction's context, warm set, budgets and detention; the nonce take-back from 1, the empty-code refusal, `gasUsed` without intrinsic gas, four errors removed, and the signer's growth counted only once it stands.
