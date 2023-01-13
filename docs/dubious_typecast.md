# Dubious Typecast

## Configuration
* Check: `dubious-typecast`
* Severity: `Low`
* Confidence: `Low` 

## Description
Highlights unstandard typecasts.

## Exploit Scenario
Strangely formed constants can disrupt project integration.

[see test](../tests/dubious_typecast_test.sol)

## Related presentation
Makes contract logic more complex, which leads to error probability increment.

## Recommendation
Use clean variables without typecasts.