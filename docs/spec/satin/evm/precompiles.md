---
description: Satin (unstable) — Precompiles. The Satin precompile set — Optimism Karst's, with KZG point evaluation at a fixed 100,000 gas — the OP input size limits and how an input over one fails, ModExp's order of price and EIP-7823 bound, and how a call to a precompile address is dispatched and priced.
spec: Satin
maturity: unstable
---

# Precompiles

{% hint style="warning" %}
**Unstable** — Satin is under active development: every value and rule on this page may change before Satin is frozen.
{% endhint %}

Abstract: The precompile set is Optimism Karst's, with KZG point evaluation at MegaETH's fixed price of 100,000 gas; this page lists the entries that differ from the Rex6 set, the input size limits and how an input over one fails, the order in which ModExp charges and checks its input, and which address a call to a precompile is dispatched and priced by.

## Motivation

A precompile's price is set for Ethereum's hardware and block times; KZG point evaluation at 50,000 gas costs a MegaETH sequencer more time per gas than any opcode, so a block of such calls takes longer to execute than its gas suggests.
Precompiles whose cost grows with their input, the BN254 and BLS12-381 pairings and multi-scalar multiplications, need an input bound on a chain with gas limits far above Ethereum's, or a single call can run for seconds.

Gas detention decides a precompile call from its price before it runs ([Gas Detention](gas-detention.md)), so the order in which a precompile charges and checks its input, and the address it is priced by, decide whether the call runs or stops.

## Specification

- `SATIN-PCMP-001` The precompile set MUST be Optimism Karst's, with KZG point evaluation (`0x0A`) at a fixed `KZG_POINT_EVALUATION_GAS`:

  | Precompile             | Address | Rule                                                            |
  | ---------------------- | ------- | --------------------------------------------------------------- |
  | KZG point evaluation   | `0x0A`  | Fixed `KZG_POINT_EVALUATION_GAS`                                |
  | ModExp                 | `0x05`  | Osaka schedule (`SATIN-PCMP-002`)                               |
  | `P256VERIFY`           | `0x100` | `P256VERIFY_GAS` (`SATIN-PCMP-003`)                             |
  | BN254 pairing          | `0x08`  | Input of at most `BN254_PAIRING_MAX_INPUT_SIZE` bytes            |
  | BLS12-381 G1 MSM       | `0x0C`  | Input of at most `BLS12_G1_MSM_MAX_INPUT_SIZE` bytes             |
  | BLS12-381 G2 MSM       | `0x0E`  | Input of at most `BLS12_G2_MSM_MAX_INPUT_SIZE` bytes             |
  | BLS12-381 pairing      | `0x0F`  | Input of at most `BLS12_PAIRING_MAX_INPUT_SIZE` bytes            |
  | Every other precompile | Any     | As Karst defines it                                             |

  The system contracts are not precompiles ([System Contracts](../system-contracts/overview.md)).
- `SATIN-PCMP-002` ModExp (`0x05`) MUST run on the Osaka schedule: [EIP-7823](https://eips.ethereum.org/EIPS/eip-7823)'s bound of `MODEXP_MAX_INPUT_SIZE` bytes on each of its three lengths, and [EIP-7883](https://eips.ethereum.org/EIPS/eip-7883)'s pricing with its minimum of `MODEXP_MIN_GAS`.
- `SATIN-PCMP-007` ModExp MUST charge and check its input in this order: its `MODEXP_MIN_GAS` minimum, a call that cannot pay it failing before the lengths are read; then the rest of its formula price; then EIP-7823's bound, an input over it failing after its whole formula price is charged; then its computation.
  Lengths too large to price are priced past any gas a call can hold.
- `SATIN-PCMP-003` `P256VERIFY` (`0x100`) MUST cost `P256VERIFY_GAS` ([EIP-7951](https://eips.ethereum.org/EIPS/eip-7951)).
  <!-- pending owner decision: QG-07 the EIP-7951 revision to pin -->
- `SATIN-PCMP-004` The OP precompiles' input size limits MUST be: BN254 pairing (`0x08`) `BN254_PAIRING_MAX_INPUT_SIZE` bytes; BLS12-381 G1 MSM (`0x0C`) `BLS12_G1_MSM_MAX_INPUT_SIZE`; G2 MSM (`0x0E`) `BLS12_G2_MSM_MAX_INPUT_SIZE`; pairing (`0x0F`) `BLS12_PAIRING_MAX_INPUT_SIZE`.
- `SATIN-PCMP-005` An input over one of those size limits MUST fail the call before any gas check, as the Optimism specification of the limit has it, a call forwarded no gas included, and MUST consume all the gas forwarded to it, as every precompile call that fails does.
- `SATIN-PCMP-006` A KZG point evaluation call given less than `KZG_POINT_EVALUATION_GAS` MUST fail out of gas before any verification runs; a successful call MUST be charged exactly `KZG_POINT_EVALUATION_GAS`; and a call given at least `KZG_POINT_EVALUATION_GAS` that fails otherwise — an input of the wrong length, a versioned hash that does not match the commitment, a proof that does not verify — MUST consume all the gas forwarded to it.
- `SATIN-PCMP-008` A call whose address is a precompile's MUST run that precompile, and MUST be priced by it for gas detention ([Gas Detention](gas-detention.md)), whatever code the state holds at the address, an EIP-7702 delegation indicator included.

### Retired ids

None.

## Constants

| Constant                       | Value   | Description                                                 |
| ------------------------------ | ------- | ----------------------------------------------------------- |
| `KZG_POINT_EVALUATION_GAS`     | 100,000 | Fixed price of KZG point evaluation (`0x0A`)                |
| `P256VERIFY_GAS`               | 6,900   | Price of `P256VERIFY` (`0x100`)                             |
| `MODEXP_MIN_GAS`               | 500     | ModExp's minimum price under EIP-7883                       |
| `MODEXP_MAX_INPUT_SIZE`        | 1,024   | EIP-7823's bound on each of ModExp's lengths, in bytes      |
| `BN254_PAIRING_MAX_INPUT_SIZE` | 57,600  | Input limit of the BN254 pairing (`0x08`), in bytes         |
| `BLS12_G1_MSM_MAX_INPUT_SIZE`  | 288,960 | Input limit of the BLS12-381 G1 MSM (`0x0C`), in bytes      |
| `BLS12_G2_MSM_MAX_INPUT_SIZE`  | 278,784 | Input limit of the BLS12-381 G2 MSM (`0x0E`), in bytes      |
| `BLS12_PAIRING_MAX_INPUT_SIZE` | 156,672 | Input limit of the BLS12-381 pairing (`0x0F`), in bytes     |

## Rationale

**Why Karst's set?**
Satin builds on Optimism Karst ([Base Layer](../base-layer.md)), whose precompile set carries Osaka's `P256VERIFY` price and Optimism's tighter input limits; MegaETH changes only the KZG price.

**Why 100,000 for KZG point evaluation?**
Verifying a KZG proof takes far longer on a sequencer than 50,000 gas of opcodes; MegaETH has priced it at 100,000 since MiniRex, and the gas check before any verification keeps a call that cannot pay from doing the work.

**Why charge ModExp's formula price before the bound?**
That is go-ethereum's order, and the one the evm2 engine adopted: the call is charged what its lengths price, and only then refused for exceeding EIP-7823's bound.
A price read before the call runs is then the price the call is charged, so gas detention decides an over-bound input by what it costs, not by a price it never pays.

**Why dispatch by the called address?**
A precompile address cannot hold a signed EIP-7702 delegation in practice, since no key controls it, but a state given to a node can hold one; dispatching and pricing by the address keeps the call a precompile call on every node whatever that state holds.

## Security Considerations

- If a node priced KZG point evaluation at 50,000, a block could hold twice the verification work its gas suggests.
- If an over-limit input were checked after a gas check, a call forwarded little gas would fail out of gas on one node and on its size on another, with different gas consumed.
- If a node checked ModExp's bound before charging its formula price, gas detention would decide an over-bound call by a different price than the one charged, and the call would run on one node and stop on another.
- If a node dispatched a precompile address holding a delegation to its delegate, the same call would run a precompile on one node and contract code on another.

## Spec History

- [Satin](../../upgrades/satin.md) — Moved the Rex6 Isthmus set of [Precompiles](../../evm/precompiles.md) to Karst's: `P256VERIFY` at 6,900 and smaller OP input limits; kept KZG at 100,000 and ModExp on the Osaka schedule, charging the formula price before EIP-7823's bound.
