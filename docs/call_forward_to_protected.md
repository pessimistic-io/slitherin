# Call Forward To Protected

## Configuration
* Check: `pess-call-forward-to-protected`
* Severity: `Medium`
* Confidence: `Low` 

## Description
**The detector is obsolete since Slitherin 0.7.1.**
Sees if a contract function has low level calls to a custom address.

## Vulnerable Scenario
Attacker makes a call on behalf of another contract and interacts with functions through access control.
[test scenario](../tests/call_forward_to_protected_test.sol)

## Recommendation
Don't let low level calls to project contracts or don't give rights to a contract which can perform low level calls.