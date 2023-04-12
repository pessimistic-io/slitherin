# Magic Number

## Configuration
* Check: `pess-magic-number`
* Severity: `Informational`
* Confidence: `High`

## Description
The detector highlights values not assigned to a variable. Such expressions decrease the code quality of contracts. 

## Vulnerable Scenario
[test scenario](../tests/magic_number_test.sol) 

## Recommendation
Don't use values without assigning them to variables.