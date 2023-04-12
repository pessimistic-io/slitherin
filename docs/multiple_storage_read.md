# Multiple Storage Read

## Configuration
* Check: `pess-multiple-storage-read`
* Severity: `Optimization`
* Confidence: `High`

## Description
The detector highlights storage values which are read several times in the same function. 

## Vulnerable Scenario
[test scenario](../tests/multiple_storage_read_test.sol) 

## Recommendation
Assign storage value to a local variable when reading it multiple times in order to reduce gas costs.
