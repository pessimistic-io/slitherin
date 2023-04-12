# Timelock Controller

## Configuration
* Check: `pess-timelock-controller`
* Severity: `High`
* Confidence: `Low`

## Description
The detector sees if a contract contains an openzeppelin timelock-contoller implementation.

## Vulnerable Scenario
The deploy address can govern the contract bypassing timelock-controller limitations.
[test scenario](../tests/timelock_controller_test.sol)

## Recommendation
Remove Proposer and Executor roles from the deployer address after deploy.