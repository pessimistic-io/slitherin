# Before Token Transfer

## Configuration

- Check: `pess-before-token-transfer`
- Severity: `Low`
- Confidence: `High`

## Description

The detector iterates over all low-level calls, checks if the destination or calldata could be tainted(manipulated).

### Potential Improvement

Find functions without virtual modifier and a call of a parent function without super.

## Vulnerable Scenario

[test scenarios](../tests/arbitrary_call_test.sol)

## Recommendation

Do not allow users to make arbitrary calls.
