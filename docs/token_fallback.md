# Token Fallback

## Configuration
* Check: `pess-token-fallback`
* Severity: `High`
* Confidence: `Low`

## Description
The detector sees if a token contract has a fallback function.

## Vulnerable Scenario
[test scenario](../tests/token_fallback_test.sol)

## Recommendation
Be careful when implementing fallback function in token contracts.