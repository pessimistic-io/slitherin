# Dubious Typecast

## Configuration
* Check: `pess-dubious-typecast`
* Severity: `Low`
* Confidence: `Low` 

## Description
Highlights unstandard typecasts.

### Potential Improvement
Reduce the number of FP removing the highlight of OK typecasts.

## Vulnerable Scenario
[test scenario](../tests/dubious_typecast_test.sol)

## Recommendation
Makes contract logic more complex, which leads to an error probability increment. Use clean variables without typecasts.