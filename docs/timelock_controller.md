# Timelock Controller

## Configuration
* Check: `pess-timelock-controller`
* Severity: `High`
* Confidence: `Low`

## Description
The detector sees if a contract contains an openzeppelin timelock-contoller implementation.

## Exploit Scenario
The deploy address can govern the contract bypassing timelock-controller limitations.

## Recomendation
Remove Proposer and Executor roles from the deployer address after deploy. 