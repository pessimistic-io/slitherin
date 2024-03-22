# Arbitrum prevRandao/difficulty

## Configuration
* Check: `pess-arb-prevrandao-difficulty`
* Severity: `Medium`
* Confidence: `High`

## Description
The detector sees if an Arbitrum contract contains usages of prevRandao/difficulty block context variables or Yul funciton.

## Vulnerable Scenario
[test scenarios](../tests/arbitrum_prevrandao_difficulty_test.sol)

## Recommendation
Consider removing usage of prevRandao/difficulty inside Arbitrum contracts as they will constantly return `1` in Arbitrum.
