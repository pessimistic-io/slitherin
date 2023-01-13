# Magic Number

## Configuration
* Check: `magic-number`
* Severity: `Informational`
* Confidence: `High`

## Description
The detector highlights values not assigned to a variable. Such expressions decrease the code quality of contracts. 

## Exploit Scenario
[Exploit](../tests/magic_number_test.sol) 

## Related attack
N/A

## Recommendation
Don't use values without assigning them to variables.