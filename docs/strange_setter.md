# Strange Setter

## Configuration
* Check: `pess-strange-setter`
* Severity: `High`
* Confidence: `Medium`

## Description
The detector sees if a contract contains a setter (also constructor) that does not change contract storage variables or does not perform external calls using provided arguments.
Setter functions MUST change the values of storage variables or perform external calls using provided parameters.
Setter functions that do not use provided variables may lead to contract misfunctions.

### Potential Improvement
Detect shadowing before storage update/external call

## Vulnerable Scenario
[test scenario](../tests/strange_setter_test.sol)

## Recommendation
Make sure that setter functions modify the states of storage variables or performs external call using provided arguments.