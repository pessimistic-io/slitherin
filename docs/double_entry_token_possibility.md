# Double Entry Token Possibility

## Configuration
* Check: `double-entry-token-alert`
* Severity: `High`
* Confidence: `Low` 

## Description
Double-entry token is a token that has two entry points for interactions - logic contract and proxy contract.
The detector sees if a contract interacts with double-entry tokens, as such interactions might lead to a contract misfunction.

## Exploit Scenario
The exploit scenario is in progress.

## Related presentation
https://docs.google.com/presentation/d/1jbOBBou-6eUBzm32X8cflTl4V6xvFd8jdaIZmi1A7kM/edit#slide=id.g142209ff0ae_0_0

## Recommendation
A contract must ensure that vulnerabilities related to double token address pointers are not present.
