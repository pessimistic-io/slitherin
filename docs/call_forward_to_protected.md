# Call Forward To Protected

## Configuration
* Check: `call-forward-to-protected`
* Severity: `Medium`
* Confidence: `Low` 

## Description
Sees if contract function has low level calls to a custom address.

## Exploit Scenario
Attacker makes a call on behalf of another contract and interacts with functions through access control.

## Recommendation
Do not let calls to project contracts or do not give rights to a contract which can perform calls