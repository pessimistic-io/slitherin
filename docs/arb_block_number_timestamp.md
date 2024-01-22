# Arbitrum block.number/block.timestamp

## Configuration

- Check: `pess-arb-solidity-version`
- Severity: `Low`
- Confidence: `High`

## Description

`block.number` and `block.timestamp` behave different, than how they behave on Ethereum. For details: [arbitrum docs](https://docs.arbitrum.io/for-devs/concepts/differences-between-arbitrum-ethereum/block-numbers-and-time)

## Vulnerable Scenario

[test scenarios](../tests/arbitrum_block_number_timestamp_test.sol)

## Recommendation

Verify, that contract's logic does not break because of this difference
