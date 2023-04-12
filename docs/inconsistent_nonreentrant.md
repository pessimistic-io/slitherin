# Inconsistent Nonreentrant

## Configuration
* Check: `pess-inconsistent-nonreentrant`
* Severity: `Medium`
* Confidence: `Medium`

## Description
The detector sees if a contract non-view functions do not have `nonReentrant` modifier while other functions have it.
If at least one contract non-view function has a `nonReentrant` modifier, it MUST be present on all non-view methods.

## Vulnerable Scenario
[test scenario](../tests/inconsistent_nonreentrant_test.sol)

## Recommendation
Ensure that `nonReentrant` modifier usage is consistent.