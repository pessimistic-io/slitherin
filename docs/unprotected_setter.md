# Unprotected Setter

## Configuration
* Check: `unprotected-setter`
* Severity: `High`
* Confidence: `Medium`

## Description
Sees if contract contains a setter, that changes contract paramater without modifier protection or access control inside the function.
Setter functions are more likely to be protected by some role.

## Exploit Scenario
Exploit scenario is in progress.

## Recomendation
Add access-control and make sure that setter functions are protected. 