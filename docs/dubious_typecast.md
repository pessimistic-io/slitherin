# Dubious Typecast

## Configuration

- Check: `pess-dubious-typecast`
- Severity: `Medium`
- Confidence: `High`

## Description

Highlights nonstandard typecasts. E.g: `uint256(uint8(K))`

## Vulnerable Scenario

[test scenario](../tests/dubious_typecast_test.sol)

## Recommendation

Verify that the typecast doesn't break the code.
