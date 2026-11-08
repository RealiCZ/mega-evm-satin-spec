---
description: Satin (unstable) — MegaAccessControl. Stub of the Satin specification: the rules this page will specify.
spec: Satin
maturity: unstable
---

# MegaAccessControl

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
This page is a stub. It lists what the page will specify; the specification text is written after the outline is reviewed.
{% endhint %}

Abstract: Switching volatile-data access off for a call subtree under Satin: where a read is refused, what a refused read pays, and the access types its error carries.

## Specification

The rules this page will specify, by their proposed ids:

- `SATIN-MAC-001` — Address 0x6342…0004; interface, errors and the scope of disableVolatileDataAccess(), enableVolatileDataAccess() and isVolatileDataAccessDisabled() unchanged; bytecode unchanged.
- `SATIN-MAC-002` — disableVolatileDataAccess() switches access off once its answer is settled; an answer detention turns into the compute stop leaves the switch as it was.
- `SATIN-MAC-003` — A read is refused where the opcode loads the value, after its operands (an opcode failing on its operands fails as with access on); a read on a full stack is refused rather than overflowing; BLOCKHASH is refused as BLOCKHASH (7) whatever its operand.
- `SATIN-MAC-004` — A refused read reverts the frame with VolatileDataAccessDisabled(accessType) on the gas it had after the opcode's static gas (2, 5, 20, 100, 200 or 5,000 by opcode); what it charged after the static gas and before the load is given back.
- `SATIN-MAC-005` — The accessType values (0 NUMBER, 1 TIMESTAMP, 2 COINBASE, 4 GASLIMIT, 5 BASEFEE, 6 PREVRANDAO, 7 BLOCKHASH, 8 BLOBBASEFEE, 10 beneficiary, 11 Oracle, 12 SLOTNUM), ABI-encoded as uint8; 3 and 9 never produced; 12 outside the contract's enum.
- `SATIN-MAC-006` — A CREATE or CREATE2 is not refused in a frame whose access is off.
- `SATIN-MAC-007` — A call's EIP-7702 delegate that is the beneficiary is refused at its own load.

## Spec History

- [Satin](../../upgrades/satin.md) — The reviewers' delta of Satin against Rex6.
