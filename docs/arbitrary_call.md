# Arbitrary Call

## Configuration

- Check: `pess-arbitrary-call`
- Severity: `High`
- Confidence: `Low`

## Description

The detector iterates over all low-level calls, checks if the destination or calldata could be tainted(manipulated).

### Potential Improvement

Filter out role protected calls, divide detector to multiple detectors with different severity and confidence

## Vulnerable Scenario

[test scenarios](../tests/arbitrary_call_test.sol)

## Recommendation

Do not allow users to make arbitrary calls.
