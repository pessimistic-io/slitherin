# Unprotected Initialize

## Configuration
* Check: `pess-unprotected-initialize`
* Severity: `High`
* Confidence: `Low`

## Description
The detector sees if a contract contains an initialize function without modifier protection or access control inside the function.

## Vulnerable Scenario
[test scenario](../tests/unprotected_initialize_test.sol)

## Recommendation
Add access control and make sure that initialize functions are protected. 