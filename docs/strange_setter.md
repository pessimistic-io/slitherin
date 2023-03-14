# Strange Setter

## Configuration
* Check: `pess-strange-setter`
* Severity: `High`
* Confidence: `Medium`

## Description
The detector sees if a contract contains a setter (also constructor) that does not change contract storage variables.
Setter functions MUST change the values of storage variables.
Setter functions that do not modify storage variables may lead to contract misfunctions.

## Exploit Scenario
[Exploit](../tests/strange_setter_test.sol)

## Recommendation
Make sure that setter functions modify the states of storage variables.