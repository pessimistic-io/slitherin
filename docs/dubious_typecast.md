# Dubious Typecast

## Configuration

- Check: `pess-dubious-typecast`
- Severity: `Medium`
- Confidence: `High`

## Description

Highlights explicit typecasts, where the result value can differ from the original one. E.g., `uint8(uint256(1e18))`, `uint256(int256(-1))`.

## Vulnerable Scenario

[test scenario](../tests/dubious_typecast_test.sol)

## Recommendation

Verify that the typecast doesn't break the code.
