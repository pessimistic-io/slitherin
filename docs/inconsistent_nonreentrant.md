# Inconsistent Nonreentrant

## Configuration
* Check: `inconsistent-nonreentrant`
* Severity: `Medium`
* Confidence: `High`

## Description
The detector sees if a contract non-view functions do not have `nonReentrant` modifier while other functions have it.
If at least one contract non-view function has a `nonReentrant` modifier, it MUST be present on all non-view methods.

## Exploit Scenario
[Exploit](../tests/inconsistent_nonreentrant_test.sol)

## Recommendation
Ensure that `nonReentrant` modifier usage is consistent.