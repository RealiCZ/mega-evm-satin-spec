---
description: Satin (unstable) — Call Interception. How a node answers a call to an intercepted system-contract method before a frame is built, what runs the contract's bytecode instead, and how an answer is settled and detained.
spec: Satin
maturity: unstable
---

# Call Interception

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
{% endhint %}

Abstract: The generic mechanism by which a node answers a call to a system contract's intercepted method itself: which calls are intercepted, what falls through to the contract's bytecode, the call-depth gate, the order of a call's decisions, the value policy, and how an interceptor's answer returns to its caller and is held to gas detention.

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

- `SATIN-ICPT-006` A `keylessDeploy(bytes,uint256)` call MUST be recognized by its depth (0, the transaction's own frame), its scheme (`CALL`), its target (`KEYLESS_DEPLOY_ADDRESS`), its selector, and its arguments, whatever code the state holds at the address; what such a call does is specified in [KeylessDeploy](keyless-deploy.md).
  The arguments MUST be accepted exactly when KeylessDeploy's own compiled calldata decoder for `(bytes calldata, uint256)` accepts them, that is when the input after the selector, each word read as a 32-byte big-endian integer, meets all of the following:
  1. it holds a head of at least 64 bytes, two 32-byte words;
  2. the head's first word, the offset of the `bytes`, is below 2^64;
  3. the word that starts at that offset, the length of the `bytes`, is below 2^64;
  4. offset + 32 + length is at most the length of the input after the selector; the `bytes` are the length bytes that follow the length word;
  5. nothing more is required: the `bytes` need no padding to a whole word, the offset need not be the canonical 64 and may point into the head, trailing bytes after the encoding are allowed, and the head's second word, `gasLimitOverride`, may hold any value.

  A call with the selector whose arguments the decoder refuses is not recognized: the node charges it nothing, and it runs KeylessDeploy's bytecode, as every other call to KeylessDeploy does; the bytecode's decoder refuses the same arguments, so the call reverts with empty data.

The table below is informative: each input is the selector followed by the words and bytes shown, `word(x)` being `x` as a 32-byte big-endian word and `gas` any `gasLimitOverride`, sent by a transaction's own `CALL` without value.

| Arguments after the selector | Recognized | What follows |
| ---------------------------- | ---------- | ------------ |
| `word(0x40)`, `word(gas)`, `word(5)`, 5 bytes: the tail padding cut | Recognized | The deployment's steps run, step 3 reading the 5 bytes |
| `word(0x20)`, `word(3)`, 3 bytes: the offset points at the second head word, which is read as the length | Recognized | The first argument is the 3 bytes, and `gasLimitOverride` is 3 |
| `word(0)`, `word(gas)`: offset zero, so the first head word is read as the length, and the `bytes` are empty | Recognized | Step 1 charges the overhead, and step 3 refuses the empty argument with `MalformedEncoding()` |
| The first input one byte short of its declared length: `word(0x40)`, `word(gas)`, `word(5)`, 4 bytes | Not recognized | KeylessDeploy's bytecode runs and reverts with empty data; the node charges nothing |

### The call-depth gate

- `SATIN-ICPT-002` A call whose frame would be deeper than `CALL_STACK_LIMIT` MUST NOT reach any interceptor, nor the `keylessDeploy` recognition.
  It MUST be answered as any call past the call-stack limit is, with the depth failure: the child's regular gas, a value call's `CALL_STIPEND` included (`SATIN-FWD-003`), and its reservoir share MUST return to the caller whole, the records' history and a new account's state gas the opcode charged for the start MUST be given back into the caller's reservoir (`SATIN-HIST-023`, `SATIN-POOL-015`), and no interceptor effect is made and no hint forwarded or counted.
  The depth gate comes before every other decision about the call, a limit included: a call past the depth limit counts no start toward any limit and cannot be stopped by one.

### The order of a call's decisions

- `SATIN-ICPT-007` Once the call opcode has made every charge of its own (its regular charges, a new account's state gas, the forward, and the history of the records its start would make as the state stands, steps 1 to 4 of `SATIN-HIST-010`), as the principle of `SATIN-HIST-023` orders it, a `CALL` or `STATICCALL` MUST be decided in this order: first the depth gate (`SATIN-ICPT-002`); then interception, which is every interceptor's answer, its value policy included (`SATIN-ICPT-003`), the admission of a `sendHint` and the data-size check of its input ([Oracle](oracle.md)), and the `keylessDeploy` recognition (`SATIN-ICPT-006`) with steps 1 and 2 of the deployment ([KeylessDeploy](keyless-deploy.md)); and only then the frame start, where the caller's funds are checked and the value moves ([Resource Limits](../evm/resource-limits.md), `SATIN-LIM-013`, `SATIN-LIM-015`).
  Interception therefore comes before the funds check, and whether the caller can fund the call's value changes nothing interception does:
  - a `sendHint` carrying a value its caller cannot fund is admitted, forwarded and counted as any hint is, and then its frame start refuses the call for the value, which fails with empty return data (`SATIN-OUT-010`), the hint staying counted;
  - a `sendHint` whose input would take the transaction over its data-size limit is answered `MegaLimitExceeded(0, limit)`, nothing forwarded or counted (`SATIN-ORCL-010`), whether or not its caller can fund its value;
  - an intercepted method of MegaAccessControl or MegaLimitControl called with value is answered `NonZeroTransfer()` (`SATIN-ICPT-003`), whether or not its caller can fund the value;
  - a recognized `keylessDeploy` call carrying value is charged step 1's overhead and answered `NoEtherTransfer()` (`SATIN-KEY-018`), whether or not its caller can fund the value.

  The charges come before all three decisions, so a caller that cannot pay one of them halts out of gas before the depth gate: no answer is made and no hint is admitted.
  A value call its caller can fund that interception answers or stops was charged the history of the records its transfer would make, and MUST be given it back into the caller's reservoir when the answer returns (`SATIN-HIST-023`); a value its caller cannot fund makes no record, so nothing was charged for it and nothing is given back (`SATIN-HIST-015`).
  A transaction's own frame that its authorization list stops before it runs (`SATIN-AUTH-010`) is stopped before any of these, and reaches no interceptor.

### The value policy

- `SATIN-ICPT-003` An intercepted method of MegaAccessControl or MegaLimitControl called with a non-zero value MUST be answered with a revert whose data is `NonZeroTransfer()`, before any value moves and whether or not the caller can fund the value (`SATIN-ICPT-007`); the method's own answer is not made.
  The policy applies once the selector matched: a call carrying value to a selector the contract does not intercept runs the bytecode.
  A `sendHint` carrying value is admitted as any hint is, and then runs the Oracle's bytecode, or, when its caller cannot fund the value, fails at its frame start, the hint counted all the same (see [Oracle](oracle.md)).

### The answer

- `SATIN-ICPT-004` An interceptor's answer MUST return to the caller as the result of a frame that ran on the child's regular gas, the forward plus a value call's `CALL_STIPEND` (`SATIN-FWD-003`): the call opcode's regular charges, made before the call reached the interceptor, stay charged; the history the opcode charged for the records of a value call its caller can fund is given back into the caller's reservoir, since an answer moves no value (`SATIN-HIST-023`); the answer itself charges nothing unless its contract's page says otherwise; the child's regular gas returns to the caller untouched, the stipend included, and the reservoir share the caller gave the call returns to it by the child-merge rule of [Two-Pool Gas](../evm/gas-model.md) (`SATIN-POOL-012`).
  A successful answer's output is the method's ABI-encoded return value; a refusal's is the error's ABI encoding, returned with a revert.
  An answer writes no account, no storage and no log, and moves no value.
- `SATIN-ICPT-005` Under [gas detention](../evm/gas-detention.md), an answer whose regular spend exceeds the calling frame's allowance — state and history gas that regular gas paid not counted — MUST be the crossing: the answer's whole regular spend is treated as the one charge that crossed, none of it billed, the part within the allowance included, and the call is stopped as [Limit Stops](../evm/limit-stops.md) specifies, with the effect the answer would have made not made.

## Constants

| Constant                 | Value                                        | Description                                                  |
| ------------------------ | -------------------------------------------- | ------------------------------------------------------------ |
| `CALL_STACK_LIMIT`       | 1,024                                        | The deepest frame a call may start                           |
| `KEYLESS_DEPLOY_ADDRESS` | `0x6342000000000000000000000000000000000003` | KeylessDeploy (see [System Contracts](overview.md))          |
| `CALL_STIPEND`           | 2,300                                        | Stipend a value-transferring `CALL` adds to the child ([Gas Forwarding](../evm/gas-forwarding.md)) |

## Rationale

**Why answer before a frame is built?**
By then the call opcode has made its own charges, so the answer needs no accounting of its own, and no frame is created only to be discarded.
The answer then returns exactly as a frame's result would, so the caller settles it with the rules every call follows: the child's gas comes back, and what the opcode charged for a start that did not happen is given back, as after any call that fails ([History Gas and the History Allowance](../evm/history-gas.md), `SATIN-HIST-023`).

**Why intercept before the frame start, the funds check included?**
Rex6 ran its interceptors before it built the call's frame, and building the frame is where the caller's funds were checked and the value moved; Satin keeps that order (`SATIN-ICPT-007`).
No answer moves value, so whether the caller could fund the value bears on no answer: a value call to MegaAccessControl or MegaLimitControl is refused with `NonZeroTransfer()`, and a keyless call with `NoEtherTransfer()`, on every node alike.
A hint is handed to the service when it is admitted, before the frame start can refuse the call, and stays counted, as any admitted hint whose call later fails does.

**Why not intercept `DELEGATECALL` or `CALLCODE`?**
Both run the target's code in the caller's context: the caller's address, value and storage.
An interceptor answering them would act for the wrong account, so they run the bytecode, whose fallback answers `NotIntercepted()` or whose method is a no-op.

**Why decode a keyless call's arguments before recognizing it?**
Rex6 decoded the outer call before its interceptor took it, so a call whose arguments did not decode reached KeylessDeploy's bytecode, which reverts, and was charged no dispatch overhead.
Satin keeps that boundary: only a call the deployment can read is a deployment, and only it pays step 1's overhead ([KeylessDeploy](keyless-deploy.md)).

**Why recognize exactly the arguments the contract's own decoder accepts?**
KeylessDeploy's method takes `bytes calldata`, and its compiled decoder accepts exactly the inputs of `SATIN-ICPT-006`'s five conditions; Rex6's node decoded the arguments without checking that their encoding was canonical, which accepts the same inputs.
With that set, a `keylessDeploy` call a transaction makes has two outcomes: the node recognizes it and the deployment's steps run, or the node does not, and the bytecode's decoder refuses it with empty data, nothing charged.
A stricter test — a canonical offset, padded bytes, no trailing bytes — would add a third: a call the node does not recognize whose arguments the bytecode reads, so that it reaches the method's body and reverts with `NotIntercepted()`, a transaction's deployment answered as a contract's call is.
A looser test would charge the overhead to calls the contract cannot read.

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
- A node that checked the caller's funds before interception would answer an unfunded value call to MegaAccessControl or MegaLimitControl with empty data instead of `NonZeroTransfer()`, and would drop a hint every other node forwards and counts, reporting another data size for the transaction and the block.
- A node whose keyless recognition were stricter or looser than the contract's decoder would run the bytecode where every other node deploys, or charge an overhead no other node charges.
- The five conditions of `SATIN-ICPT-006` define the recognized set, not any decoder library: a node that takes the set from a library keeps it to those conditions whichever version of the library resolves, and never uses a strict or validating mode, which would refuse a non-canonical offset, unpadded bytes or trailing bytes and run the bytecode where every other node deploys.
- A node that billed part of an answer that crossed detention's limit would let a transaction compute past its limit by that part.

## Spec History

- [Rex2](../../upgrades/rex2.md) — Introduced call interception.
- [Rex5](../../upgrades/rex5.md) — Gated interception on the call-depth limit.
- [Rex6](../../upgrades/rex6.md) — The Rex6 mechanism is specified in [Call Interception](../../system-contracts/interception.md), with KeylessDeploy as an interceptor.
- [Satin](../../upgrades/satin.md) — KeylessDeploy becomes a native creation, answers are held to gas detention, and the depth gate comes before every limit.
