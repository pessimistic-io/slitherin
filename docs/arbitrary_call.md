# Arbitrary Call

## Configuration

- - Check: `pess-arbitrary-call`
  - Severity: `High`
  - Confidence: `High`

* - Check: `pess-arbitrary-call-with-stored-erc20-approves`
  - Severity: `High`
  - Confidence: `High`

- - Check: `pess-arbitrary-call-destination-tainted`
  - Severity: `Medium`
  - Confidence: `Medium`

* - Check: `pess-arbitrary-call-calldata-tainted`
  - Severity: `Medium`
  - Confidence: `Medium`

## Description

The detector iterates over all low-level calls, checks if the destination or calldata could be tainted(manipulated).
This detector consists of multiple detectors, which will run with this detector.

### Potential Improvement

Filter out proxy results

## Vulnerable Scenario

[test scenarios](../tests/arbitrary_call_test.sol)

## Recommendation

Do not allow users to make arbitrary calls.
