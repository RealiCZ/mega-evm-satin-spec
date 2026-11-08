---
description: Satin (unstable) — Activation and Rex-Era Carry-Over. Stub of the Satin specification: the rules this page will specify.
spec: Satin
maturity: unstable
---

# Activation and Rex-Era Carry-Over

{% hint style="warning" %}
**Unstable** — Satin is under active development: everything on this page may change before Satin is frozen.
This page is a stub. It lists what the page will specify; the specification text is written after the outline is reviewed.
{% endhint %}

Abstract: When Satin takes effect, the chain configuration key that schedules it and the base forks it requires, the checks its activation block makes, and what it carries over from the Rex era unchanged.

## Specification

The rules this page will specify, by their proposed ids:

- `SATIN-ACT-001` — Satin follows Rex6 on the spec ladder; a block from satinTime on executes Satin, every earlier block the spec its timestamp resolves to.
- `SATIN-ACT-002` — The chain configuration carries Satin as one key, satinTime (a JSON number up to 2^64 − 1, or the arbitrary-precision object form); Satin carries no parameter; no key names a limit or the registry's roles; another key starting with satin is refused; a duplicated key is read as its last copy; the format is provisional.
- `SATIN-ACT-003` — Every base fork (Ethereum Shanghai to Osaka, Optimism Regolith to Karst) is active by satinTime, and Jovian, Karst and Osaka activate no earlier than satinTime; a node refuses a configuration that breaks either.
- `SATIN-ACT-004` — Satin's activation block admits only deposits and checks the predeploys before its transactions.
- `SATIN-ACT-005` — The activation check: the six system contracts in address order, then the EIP-7997 CREATE2 factory at 0x4e59b448…, each holding exactly the code Satin expects (Oracle and SequencerRegistry at 2.0.0, the others at Rex6's bytecode, the factory's code hash 0x2fa86add…); nonces, balances and storage unchecked; any other state makes the block invalid; the reads are read-only entries; no other block reads the seven.
- `SATIN-ACT-006` — Satin deploys, upgrades and seeds nothing: the chain holds the six contracts at the versions the legacy forks left (Rex5 deployed the SequencerRegistry and upgraded the Oracle to 2.0.0, Rex6 upgraded the SequencerRegistry to 2.0.0) and the factory from genesis, so a chain runs a Rex6 block before satinTime.
- `SATIN-ACT-007` — Satin starts from the L1 block contract the Rex era left, OP's L1Block 1.6.0 (Isthmus) with zero DA footprint and operator fee scalars, and does not upgrade it.
- `SATIN-ACT-008` — State and contracts from earlier specs keep working: Satin changes nothing about blocks under earlier specs, and contracts deployed earlier run under the Satin rules.
- `SATIN-ACT-009` — Part of the execution configuration is fixed by the spec whatever a node supplies: the Satin gas schedule, EIP-8037, EIP-2780 and EIP-7708 on, the 200,000,000 execution cap, the chain-id check on, the two code-size limits, the byte prices (no build that reads them at run time), and the limits; a node that reads the configuration before executing reads these values, not its own.
- `SATIN-ACT-010` — Whether a block admits only deposits, and whether Satin activates in it, are worked out from the chain configuration and the parent's timestamp for every block built or validated and given to the executor and to a stateless validator; the derivation node and builders enforce deposit-only activation blocks for Satin and every later MegaETH fork; an execution not told the first runs the block as one that admits non-deposit transactions, and one not told the second checks no predeploy.

## Spec History

- [Satin](../../upgrades/satin.md) — The reviewers' delta of Satin against Rex6.
