# Unprotected Initialize

## Configuration
* Check: `pess-unprotected-initialize`
* Severity: `High`
* Confidence: `Low`

## Description
The detector sees if a contract contains an initialize function without modifier protection or access control inside the function.

## Exploit Scenario
The exploit scenario is in progress.

## Recomendation
Add access control and make sure that initialize functions are protected. 