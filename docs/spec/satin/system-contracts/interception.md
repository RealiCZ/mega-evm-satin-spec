---
description: Satin (unstable) — Call Interception. How a node answers a call to an intercepted system-contract method before a frame is built, what runs the contract's bytecode instead, and how an answer is settled and detained.
spec: Satin
maturity: unstable
---

# Call Interception

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
{% endhint %}

Abstract: The generic mechanism by which a node answers a call to a system contract's intercepted method itself: which calls are intercepted, what falls through to the contract's bytecode, the call-depth gate, the value policy, and how an interceptor's answer returns to its caller and is held to gas detention.

## Motivation

Some system-contract methods need effects that bytecode cannot express: forwarding a hint to the node's oracle service, switching volatile-data access off for a call subtree, or reading how much regular gas the calling frame may still spend.
MegaETH reaches them through ordinary calls to fixed addresses, so that contracts use them with standard call syntax.
The node must then agree with every other node on exactly which calls it answers itself, what each answer costs and returns, and which calls run the contract's bytecode; a disagreement on any of them changes a call's result.

## Specification

### Which calls are intercepted

- `SATIN-ICPT-001` A node MUST answer a call itself, before a frame is built for it, when and only when the call is a `CALL` or a `STATICCALL`, its target is a system contract that has an interceptor, and the first four bytes of its input are the selector of one of that contract's intercepted methods.
  The intercepted methods are those the table below lists; the matching is on the address, then on the four-byte selector alone, whatever bytes follow it, and an input shorter than four bytes names no selector.
  A `DELEGATECALL` or `CALLCODE` of any of these contracts, a call to a selector the contract does not intercept, and a call to a system contract that has no interceptor MUST run the contract's bytecode.
  A transaction whose recipient is a system contract is a `CALL` at depth 0 and MUST be intercepted all the same, though no opcode initiated it.
  A `CREATE` or `CREATE2` is never intercepted.

| Contract                                     | Intercepted methods                                                                          | Answer                                                                 |
| -------------------------------------------- | -------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| [Oracle](oracle.md)                          | `sendHint(bytes32,bytes)`                                                                    | Forwards the hint, then the call runs the bytecode (see the page)      |
| [MegaAccessControl](mega-access-control.md)  | `disableVolatileDataAccess()`, `enableVolatileDataAccess()`, `isVolatileDataAccessDisabled()` | The node's answer; the bytecode does not run                           |
| [MegaLimitControl](mega-limit-control.md)    | `remainingComputeGas()`                                                                      | The node's answer; the bytecode does not run                           |

The High-Precision Timestamp and the SequencerRegistry have no interceptor.
KeylessDeploy has none either: its `keylessDeploy` call is recognized by the rule below and deployed natively.

- `SATIN-ICPT-006` A `keylessDeploy(bytes,uint256)` call MUST be recognized by its depth (0, the transaction's own frame), its scheme (`CALL`), its target (`KEYLESS_DEPLOY_ADDRESS`), its selector, and its arguments, which MUST decode under the Solidity ABI as `(bytes, uint256)`, bytes that follow a valid encoding not preventing it, whatever code the state holds at the address; what such a call does is specified in [KeylessDeploy](keyless-deploy.md).
  A call with the selector whose arguments do not decode is not recognized: the node charges it nothing, and it runs KeylessDeploy's bytecode, as every other call to KeylessDeploy does.

### The call-depth gate

- `SATIN-ICPT-002` A call whose frame would be deeper than `CALL_STACK_LIMIT` MUST NOT reach any interceptor, nor the `keylessDeploy` recognition.
  It MUST be answered as any call past the call-stack limit is, with the depth failure, its forwarded gas and its reservoir share returned to the caller whole, no interceptor effect made and no hint forwarded or counted.
  The depth gate comes before every other decision about the call, a limit included: a call past the depth limit counts no start toward any limit and cannot be stopped by one.

### The value policy

- `SATIN-ICPT-003` An intercepted method of MegaAccessControl or MegaLimitControl called with a non-zero value MUST be answered with a revert whose data is `NonZeroTransfer()`, before any value moves; the method's own answer is not made.
  The policy applies once the selector matched: a call carrying value to a selector the contract does not intercept runs the bytecode.
  A `sendHint` carrying value is admitted as any hint is, and then runs the Oracle's bytecode (see [Oracle](oracle.md)).

### The answer

- `SATIN-ICPT-004` An interceptor's answer MUST return to the caller as the result of a frame that ran on the gas the call forwarded: the call opcode's own charges, made before the call reached the interceptor, stay charged; the answer itself charges nothing unless its contract's page says otherwise; the forwarded regular gas returns to the caller untouched, and the reservoir share the caller gave the call returns to it by the child-merge rule of [Two-Pool Gas](../evm/gas-model.md).
  A successful answer's output is the method's ABI-encoded return value; a refusal's is the error's ABI encoding, returned with a revert.
  An answer writes no account, no storage and no log, and moves no value.
- `SATIN-ICPT-005` Under [gas detention](../evm/gas-detention.md), an answer whose regular spend exceeds the calling frame's allowance — state and history gas that regular gas paid not counted — MUST be the crossing: the answer's whole regular spend is treated as the one charge that crossed, none of it billed, the part within the allowance included, and the call is stopped as [Limit Stops](../evm/limit-stops.md) specifies, with the effect the answer would have made not made.

## Constants

| Constant                 | Value                                        | Description                                                  |
| ------------------------ | -------------------------------------------- | ------------------------------------------------------------ |
| `CALL_STACK_LIMIT`       | 1,024                                        | The deepest frame a call may start                           |
| `KEYLESS_DEPLOY_ADDRESS` | `0x6342000000000000000000000000000000000003` | KeylessDeploy (see [System Contracts](overview.md))          |

## Rationale

**Why answer before a frame is built?**
By then the call opcode has made its own charges, so the answer needs no accounting of its own, and no frame is created only to be discarded.
The answer then returns exactly as a frame's result would, so the caller settles it with the rules every call follows.

**Why not intercept `DELEGATECALL` or `CALLCODE`?**
Both run the target's code in the caller's context: the caller's address, value and storage.
An interceptor answering them would act for the wrong account, so they run the bytecode, whose fallback answers `NotIntercepted()` or whose method is a no-op.

**Why decode a keyless call's arguments before recognizing it?**
Rex6 decoded the outer call before its interceptor took it, so a call whose arguments did not decode reached KeylessDeploy's bytecode, which reverts, and was charged no dispatch overhead.
Satin keeps that boundary: only a call the deployment can read is a deployment, and only it pays step 1's overhead ([KeylessDeploy](keyless-deploy.md)).

**Why gate on depth first?**
The depth failure of an ordinary call is decided when its frame is built, after interception; without the gate an interceptor could answer at a depth no other call can reach.
Under the execution cap no frame reaches depth 1,024 with gas to make a call, since every call forwards at most 98/100 of its caller's regular gas, so the gate decides no reachable call; it is stated so that the order is fixed for every node.
Rex6 gave a transaction-level resource-limit overflow priority over the depth failure; in Satin a limit is a stop of the frame that crosses it, decided when a start is counted, and a call past the depth limit is answered before its start is counted, so the depth failure comes first.

**Why is an answer's whole spend the crossing under detention?**
An answer is one step with one result; billing part of it and refusing the rest would leave an effect half made.
Treating the whole spend as the charge that crossed keeps the stop's compute equal to the transaction's compute when the call started.

## Security Considerations

- An interceptor that consumed calls to unknown selectors would hide them from the bytecode, which answers them with a stable error; a contract relying on that error would then see a silent success.
- An interceptor reachable through `DELEGATECALL` would switch volatile-data access, or report gas, for a frame that is not the caller's.
- A node that answered a value-bearing intercepted call with success would let value reach a system contract that has no method to return it.
- A node that billed part of an answer that crossed detention's limit would let a transaction compute past its limit by that part.

## Spec History

- [Rex2](../../upgrades/rex2.md) — Introduced call interception.
- [Rex5](../../upgrades/rex5.md) — Gated interception on the call-depth limit.
- [Rex6](../../upgrades/rex6.md) — The Rex6 mechanism is specified in [Call Interception](../../system-contracts/interception.md), with KeylessDeploy as an interceptor.
- [Satin](../../upgrades/satin.md) — KeylessDeploy becomes a native creation, answers are held to gas detention, and the depth gate comes before every limit.
