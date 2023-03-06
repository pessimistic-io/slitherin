# Readonly Reentrancy

## Configuration

- Check: `pess-readonly-reentrancy`
- Severity: `High`
- Confidence: `low`

## Description

Highlights the use of getter functions that return a value that theoretically could be manipulated during the execution.

## Exploit Scenario

[Exploit](../tests/readonly_reentrancy.sol)

## Related attack

N/A

## Recommendation

Ensure that getter function values aren't crucial and can't be maliciously used in other contract parts during external calls before being updated.
