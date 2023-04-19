# Readonly Reentrancy

## Configuration
* Check: `pess-readonly-reentrancy`
* Severity: `High`
* Confidence: `Low`

## Description
Highlights the use of getter functions that return a value that theoretically could be manipulated during the execution.

## Vulnerable Scenario
[test scenario](../tests/readonly_reentrancy_test.sol)

## Recommendation
Ensure that getter function values aren't crucial and can't be maliciously used in other contract parts during external calls before being updated.

**Also check out:**

- [Our article about Reentrancy attacks & defense methods.](https://blog.pessimistic.io/reentrancy-attacks-on-smart-contracts-distilled-7fed3b04f4b6)
- [A Historical Collection of Reentrancy Attacks](https://github.com/pcaversaccio/reentrancy-attacks)
- [Web3/Crypto Hacks DB](https://telegra.ph/Web3Crypto-Hacks-DB-04-19)
- [Our Blog](https://blog.pessimistic.io/)

