# Public vs External

## Configuration

- Check: `pess-public-vs-external`
- Severity: `Low`
- Confidence: `Medium`

## Description

Detects functions that have `public` modifiers and could be turned into `external` (not used in the contract)

### Potential Improvement

There could be FP's because of inheritance

## Vulnerable Scenario

[test scenarios](../tests/public_vs_external_test.sol)

## Recommendation

Mark `public` functions as `external` where it is possible to enhance control-flow readability.
