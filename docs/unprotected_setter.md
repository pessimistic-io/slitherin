# Unprotected Setter

## Configuration
* Check: `pess-unprotected-setter`
* Severity: `High`
* Confidence: `Medium`

## Description
The detector sees if a contract contains a setter that changes the contract parameters without modifier protection or access control inside the function.

## Vulnerable Scenario
[test scenario](../tests/unprotected_setter_test.sol)

## Recommendation
Add access control and make sure that setter functions are protected. 