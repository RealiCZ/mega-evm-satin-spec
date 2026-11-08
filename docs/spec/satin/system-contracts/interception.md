---
description: Satin (unstable) — Call Interception. Stub of the Satin specification: the rules this page will specify.
spec: Satin
maturity: unstable
---

# Call Interception

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
This page is a stub. It lists what the page will specify; the specification text is written after the outline is reviewed.
{% endhint %}

Abstract: How the node answers a call to a system contract's intercepted method before a frame is built, what falls through to bytecode, and how an interceptor's answer is settled and detained.

## Specification

The rules this page will specify, by their proposed ids:

- `SATIN-ICPT-001` — A CALL or STATICCALL to a system contract with an interceptor whose selector names an intercepted method is answered before a frame is built; DELEGATECALL, CALLCODE and an unknown selector run the contract's bytecode.
- `SATIN-ICPT-002` — The interceptors' call-depth gate.
- `SATIN-ICPT-003` — An intercepted MegaAccessControl or MegaLimitControl method carrying value reverts with NonZeroTransfer().
- `SATIN-ICPT-004` — An interceptor's answer returns to the caller as a frame's result on the gas the caller forwarded, its reservoir share returned by the child-merge rule.
- `SATIN-ICPT-005` — Under gas detention an answer whose regular spend exceeds the frame's allowance is the crossing, none of it billed.
- `SATIN-ICPT-006` — KeylessDeploy is recognized by depth, scheme, target and selector, whatever code the state holds at its address.

## Spec History

- [Satin](../../upgrades/satin.md) — The reviewers' delta of Satin against Rex6.
