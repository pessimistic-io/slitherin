# AAVE Flashloan callback detector

## Configuration

- Check: `pess-aave-flashloan-callback`
- Severity: `High`
- Confidence: `High`

## Description

It is important to validate `initiator` and `msg.sender` in `executeOperation` callback

## Vulnerable Scenario

[test scenarios](../tests/AaveFlashloanCallback.sol)

## Recommendation

Validate `initiator` and `msg.sender`
