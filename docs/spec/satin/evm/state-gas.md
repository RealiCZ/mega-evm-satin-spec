---
description: Satin (unstable) — State Gas and SALT Pricing. Stub of the Satin specification: the rules this page will specify.
spec: Satin
maturity: unstable
---

# State Gas and SALT Pricing

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
This page is a stub. It lists what the page will specify; the specification text is written after the outline is reviewed.
{% endhint %}

Abstract: How a state charge is priced: EIP-8037's byte counts at MegaETH's cost per state byte, scaled by the multiplier of the SALT bucket the state lands in, where each charge is made and how it is given back.

## Specification

The rules this page will specify, by their proposed ids:

- `SATIN-STATE-001` — Every EIP-8037 state charge is entry × m, entry being EIP-8037's byte count times COST_PER_STATE_BYTE = 1,530.
- `SATIN-STATE-002` — m = floor(bucket_capacity / MIN_BUCKET_SIZE), MIN_BUCKET_SIZE = 256.
- `SATIN-STATE-003` — The state byte table (fresh slot 64, new account 120, created account 120, deployed code 1 per byte, delegation indicator 23) and the bucket each lands in.
- `SATIN-STATE-004` — A state charge is made where the state is added: the SSTORE that fills a fresh slot; the value CALL, the balance-moving SELFDESTRUCT, the transaction value or the applied authorization that creates an account; CREATE, CREATE2 or a creation transaction.
- `SATIN-STATE-005` — m scales state gas and nothing else.
- `SATIN-STATE-006` — A bucket's multiplier is read at most once per transaction; every later charge and give-back in that bucket uses the same m.
- `SATIN-STATE-007` — A capacity below MIN_BUCKET_SIZE, or one the node cannot read, is a fault of the node, a deposit included: the transaction is neither priced nor settled and the node reports an internal error.
- `SATIN-STATE-008` — The only SSTORE that charges fresh-slot state gas has original zero, present zero, new non-zero; the only one that refills it has original zero, present non-zero, new zero, not on an account marked for deletion, at the price charged.
- `SATIN-STATE-009` — The protocol's own transactions are priced at m = 1 without reading a bucket; a deposit that is not system-originated is priced by bucket.
- `SATIN-STATE-010` — The function that maps an account or a storage slot to its SALT bucket.

## Spec History

- [Satin](../../upgrades/satin.md) — The reviewers' delta of Satin against Rex6.
