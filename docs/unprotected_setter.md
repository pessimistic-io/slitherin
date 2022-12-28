# Unprotected Setter

## Configuration
* Check: `unprotected-setter`
* Severity: `High`
* Confidence: `Medium`

## Description
The detector sees if a contract contains a setter that changes the contract parameter without modifier protection or access control inside the function.

## Exploit Scenario
The exploit scenario is in progress.

## Recomendation
Add access control and make sure that setter functions are protected. 