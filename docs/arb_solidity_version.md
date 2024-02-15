# Arbitrum solidity version

## Configuration

- Check: `pess-arb-solidity-version`
- Severity: `High`
- Confidence: `Low`

## Description

Checks that sol version >= 0.8.20 is not used inside an Arbitrum contract. Solidity in these versions will utilize PUSH0 opcode, which is not supported on Arbitrum.

## Vulnerable Scenario

[test scenarios](../tests/arbitrum_prevrandao_solidity_version_test.sol)

## Recommendation

Either, use versions `0.8.19`` and below, or EVM versions below shanghai
