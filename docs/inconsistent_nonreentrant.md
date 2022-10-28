# Inconsistent Nonreentrant

## Configuration
* Check: `inconsistent-nonreentrant`
* Severity: `Medium`
* Confidence: `Medium`

## Description
Sees if contract non-view functions do not have `nonReentrant` modifier while other functions have it.
If contract has `nonReentrant` modifier it MUST be present on all non-view methods.

## Exploit Scenario
[Exploit](../tests/inconsistent_nonreentrant_test.sol)

## Recommendation
Make sure that `nonReentrant` modifier usage is consistent.