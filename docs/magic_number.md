# Magic Number

## Configuration
* Check: `magic-number`
* Severity: `Low`
* Confidence: `High`

## Description
Highlights values which are not assigned to a variable. Such expressions decrease code quality of contracts. 

## Exploit Scenario
[Exploit](tests\magic_number_test.sol) 

## Related attack
N/A

## Recommendation
Don't use values without assigning them to variables.