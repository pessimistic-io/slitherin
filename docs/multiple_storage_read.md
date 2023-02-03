# Multiple Storage Read

## Configuration
* Check: `multiple-storage-read`
* Severity: `Low`
* Confidence: `High`

## Description
The detector storage values which are read several times in the same function. 

## Exploit Scenario
[Exploit](../tests/multiple_storage_read_test.sol) 

## Related attack
N/A

## Recommendation
Assign storage value to a local variable when reading it multiple times in order to reduce gas costs.