# Potential arithmetic overflow

## Configuration
* Check: `pess-potential-arithmetic-overflow`
* Severity: `Medium`
* Confidence: `Medium`

## Description
The detector sees if there are assignments/returns that calculate some arithmetic expressions and if some intermediate calculations
contain a type that is lower than the expected result. Such behavior may lead to unexpected overflow/underflow, e.g., trying to assign the multiplication of two `uint48` variables to `uint256` would look like `uint48 * uint48` and it may overflow (however, the final type would fit such multiplication).

### Potential Improvement
- Handle return statements that return tuples of arithmetic expressions;
- Handle signed integer underflow for subtraction operation e.g. `int256 = int64 - int64` should produce error (`int64` should be cast to `int256`).
- Improve the output of the detector (unroll complex expressions in something readable, not just `...`)

## Vulnerable Scenario
[test scenario](../tests/potential_arith_overflow.sol)

## Recommendation
Use explicit type casting in sub expressions when the assigment to a larger type is performed.