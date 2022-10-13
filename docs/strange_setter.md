# Strange Setter

## Configuration
* Check: `strange-setter`
* Severity: `High`
* Confidence: `Medium`

## Description
Sees if contract contains a setter, that does not change contract storage variables.
Setter functions MUST change values of storage variables.
Setter functions which do not modify storage variables may lead to contract misfunctions.

## Exploit Scenario
[Exploit](tests\strange_setter_test.sol)

## Recommendation
Make sure that setter functions modify states of storage variables.