# Before Token Transfer

## Configuration
* Check: `pess-before-token-transfer`
* Severity: `Low`
* Confidence: `High`

## Description
The detector sees if a contract contains a beforeTokenTransfer function.

### Potential Improvement
Find functions without virtual modifier and a call of a parent function without super.

## Vulnerable Scenario
[test scenarios](../tests/before_token_transfer_test.sol)

## Recommendation
Function beforeTokenTransfer must be virtual if has override and must call its parent function using super.
