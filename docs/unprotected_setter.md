# Unprotected Setter

## Configuration
* Check: `pess-unprotected-setter`
* Severity: `High`
* Confidence: `Medium`

## Description
The detector sees if a contract contains a setter that changes the contract parameters without modifier protection or access control inside the function.

## Vulnerable Scenario
The exploit scenario is in progress.

## Recommendation
Add access control and make sure that setter functions are protected. 