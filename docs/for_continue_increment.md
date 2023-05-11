# For Continue Increment

## Configuration
* Check: `for-continue-increment`
* Severity: `Medium`
* Confidence: `Low`

## Description
It's common practice to use unchecked {++i;} to save gas in for loops. However in this situation a continue statement before the index increase might lead to an infinite loop.

## Vulnerable Scenario
[test scenario](../tests/for_continue_increment.sol)

## Recommendation
- Perform the index increase before the continue statement
- Remove the gas saving unchecked increase
- Redesign the function