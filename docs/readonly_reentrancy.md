# Readonly Reentrancy

## Configuration

- Check: `readonly-reentrancy`
- Severity: `High`
- Confidence: `Medium`

## Description

Highlights the use of getter functions that returns a value that theoretically could be manipulated during the execution.

## Exploit Scenario

[Exploit](../tests/readonly_reentrancy.sol)

## Related attack

N/A

## Recommendation

Be careful while using this getter function.
