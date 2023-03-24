# Before Token Transfer

## Configuration
* Check: `pess-before-token-transfer`
* Severity: `Low`
* Confidence: `Medium`

## Description
The detector sees if a contract contains a beforeTokenTransfer function without virtual modifier and calls parent function without super.

## Exploit Scenario
The exploit scenario is in progress.

## Recomendation
Function beforeTokenTransfer must be virtual if has override and must call its parent function using super.